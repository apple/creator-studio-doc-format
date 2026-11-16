# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0

"""The JSON codec every generated model inherits.

A field spec is (``wire_key``, ``version_added`` as ``(major, minor)``, ``kind``). The
kind decides when the field is on the wire:

- ``"req"``: required, with no default. Always on the wire.
- ``"def"``: has a default. On the wire only when explicitly set, so a default instance
  omits it.
- ``"opt"``: optional, with no default. On the wire when not ``None``, and can raise the
  version.
- ``"ovr"``: an ``Override`` with no default. ``.not_set`` omits the key, ``.cleared``
  writes null, and ``.value`` writes the value. Like ``"opt"``, it can raise the version
  when present.
- ``"ovrdef"``: an ``Override`` with a default. An absent key decodes to
  ``.value(default)``. Like ``"def"``, it's on the wire only when it's explicitly set.

An omittable field counts toward the version when it holds a value or a clear. A
``None`` doesn't count, even where it's written.

An edit drops the version a value was decoded at instead of keeping it as a floor. A
newer key often takes precedence over an older one that stays as the fallback for older
readers, so keeping the floor can let unknown data override the edit.
"""

from __future__ import annotations

import logging
import os
import re
import sys
import warnings
from collections.abc import Callable, Iterable
from enum import Enum
from functools import total_ordering
from typing import (
    Any,
    ClassVar,
    Generic,
    TypeVar,
    cast,
    get_args,
)

import pydantic
from pydantic import (
    BaseModel,
    ConfigDict,
    GetCoreSchemaHandler,
    ModelWrapValidatorHandler,
    PrivateAttr,
    ValidationInfo,
    model_serializer,
    model_validator,
)
from pydantic_core import core_schema

from ._errors import DocumentVersionError
from ._preset import (
    _CLEAR,
    _FILLED_KEY,
    _NO_FILL,
    _cached_preset_adapter,
    _fill_from_preset,
    _preset_gate_context,
    _preset_supply,
    _PresetFilled,
    _resolved_preset_props,
)

logger = logging.getLogger(__name__)

_M = TypeVar("_M", bound="ObjectModel")
_E = TypeVar("_E", bound="TaggedUnionModel")


_VERSION_STR_RE = re.compile(r"^(\d+)(?:\.(\d+))?$", re.ASCII)


@total_ordering
class Version:
    """A version number in major.minor form, as the file writes it.

    The value is either an object's ``version`` or the manifest's ``package_version``.
    ``parse`` accepts a ``"major.minor"`` or ``"major"`` string, a ``{"major": ...,
    "minor": ...}`` mapping, where ``minor`` is optional, or a ``Version``. A missing
    minor reads as 0, and ``parse`` ignores leading zeros.

    Args:
        major: The major version, which a reader must implement to read the value.
        minor: The minor version, which a reader can be older than.
    """

    __slots__ = ("major", "minor")

    def __init__(self, major: int, minor: int = 0) -> None:
        self.major = major
        self.minor = minor

    @classmethod
    def parse(cls, value: Any) -> Version | None:
        """Returns the version that a value spells.

        Args:
            value: A version in one of the forms the class accepts.

        Returns:
            Version | None: The version, or ``None`` if ``value`` isn't in an accepted
            form.
        """
        if value is None or isinstance(value, bool):
            return None
        if isinstance(value, Version):
            return value
        if isinstance(value, dict):
            major = value.get("major")
            if not isinstance(major, int) or isinstance(major, bool) or major < 0:
                return None
            minor = value.get("minor", 0)
            if minor is None:
                minor = 0
            if not isinstance(minor, int) or isinstance(minor, bool) or minor < 0:
                return None
            return cls(major, minor)
        if isinstance(value, str):
            m = _VERSION_STR_RE.fullmatch(value)
            if m is None:
                return None
            return cls(int(m.group(1)), int(m.group(2)) if m.group(2) else 0)
        return None

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return (self.major, self.minor) == (other.major, other.minor)

    def __lt__(self, other: Version) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return (self.major, self.minor) < (other.major, other.minor)

    def __hash__(self) -> int:
        return hash((self.major, self.minor))


FieldSpec = tuple[str, tuple[int, int], str]

_BASE_KINDS = ("req", "def")


def _object_version(
    field_specs: Iterable[FieldSpec], present_optional: set[str]
) -> tuple[int, int]:
    base = (1, 0)
    for _wk, added, kind in field_specs:
        if kind in _BASE_KINDS and added > base:
            base = added
    ver = base
    for wk, added, kind in field_specs:
        if (
            kind not in _BASE_KINDS
            and wk in present_optional
            and added > base
            and added > ver
        ):
            ver = added
    return ver


def _schema_version(version: str) -> tuple[int, int]:
    if (v := Version.parse(version)) is None:
        raise ValueError(f"unparsable schema version {version!r}")
    return (v.major, v.minor)


class _Same:
    __slots__ = ("model",)

    def __init__(self, model: BaseModel) -> None:
        self.model = model

    def __eq__(self, other: object) -> bool:
        return isinstance(other, _Same) and other.model is self.model

    __hash__ = None  # type: ignore[assignment]


def _edit_shape(value: Any) -> Any:
    match value:
        case BaseModel():
            return _Same(value)
        case Override():
            return (Override, value.state, _edit_shape(value._value))
        case list() | tuple():
            return (type(value), [_edit_shape(v) for v in value])
        case dict():
            return {k: _edit_shape(v) for k, v in value.items()}
    return value


def _own_shape(model: BaseModel) -> Any:
    return (
        _edit_shape(model.__dict__),
        _edit_shape(model.__pydantic_extra__ or {}),
        frozenset(model.__pydantic_fields_set__),
    )


_B = TypeVar("_B", bound=BaseModel)


def _deepcopy_with_memo(model: _B, memo: dict[int, Any] | None) -> _B:
    return BaseModel.__deepcopy__(model, {} if memo is None else memo)


class _WireFloor:
    __slots__ = ("decoded", "version")

    def __init__(
        self, version: tuple[int, int] | None = None, model: BaseModel | None = None
    ) -> None:
        self.version = version
        self.decoded = None if model is None else _own_shape(model)

    @classmethod
    def at(
        cls, stamp: tuple[int, int] | None, schema: tuple[int, int], model: BaseModel
    ) -> _WireFloor:
        if stamp is None or stamp <= schema:
            return cls()
        return cls(stamp, model) if model.__pydantic_extra__ else cls()

    def __eq__(self, other: object) -> bool:
        return isinstance(other, _WireFloor)

    def __hash__(self) -> int:
        return 0

    def holds(self, model: BaseModel) -> bool:
        if self.version is None or not model.__pydantic_extra__:
            return False
        if _same_value(_own_shape(model), self.decoded):
            return True
        warnings.warn(
            f"{type(model).__name__}: edited after decoding at {self.version[0]}."
            f"{self.version[1]}. Its unknown keys {sorted(model.__pydantic_extra__)} are kept, but "
            f"a newer reader ignores any that are newer than the version written.",
            UserWarning,
            stacklevel=_caller_stacklevel(),
        )
        return False


_INTERNAL_DIRS = tuple(
    os.path.dirname(f) + os.sep for f in (__file__, pydantic.__file__)
)


def _caller_stacklevel() -> int:
    frame, level = sys._getframe(1), 1
    while frame.f_back is not None and frame.f_code.co_filename.startswith(
        _INTERNAL_DIRS
    ):
        frame, level = frame.f_back, level + 1
    return level


def wire(
    type_id: str, *, version: str, fields: list[FieldSpec]
) -> Callable[[type[_M]], type[_M]]:

    def wrap(cls: type[_M]) -> type[_M]:
        cls.__wire_type_id__ = type_id
        cls.__wire_version__ = version
        cls.__wire_version_tuple__ = _schema_version(version)
        cls.__wire_fields__ = tuple(fields)
        return cls

    return wrap


_OT = TypeVar("_OT")


class _OverrideState(Enum):
    NOT_SET = "not_set"
    CLEARED = "cleared"
    VALUE = "value"


def _ser_override(ov: Override[Any], info: Any) -> Any:
    if not isinstance(ov, Override):
        raise TypeError(
            f"override field expected Override, got a bare {type(ov).__name__}"
        )
    if not ov.is_value:
        return None
    v = ov._value
    if isinstance(v, BaseModel):
        return v.model_dump(mode="json", context=info.context)
    if isinstance(v, Enum):
        return v.value
    return v


class Override(Generic[_OT]):
    """A property value that tells an omitted property, a null, and a value apart.

    - ``Override.not_set()``: omitted from the JSON, so the property can inherit a
      value.
    - ``Override.cleared()``: an explicit null, which blocks inheritance and clears the
      value.
    - ``Override.value(x)``: the value ``x``.

    A field uses ``Override`` because ``T | None`` can't tell an omitted property from a
    null one. The JSON keeps the two apart. Assigning a bare value to an ``Override``
    field wraps it. ``None`` becomes ``.cleared()``, and any other value becomes
    ``.value(x)``.

    >>> from creator_studio_doc_format.core import CellProperties
    >>> CellProperties.model_validate({"fill": None}).fill.is_cleared
    True
    """

    __slots__ = ("_value", "state")

    def __init__(self, state: _OverrideState, value: Any = None) -> None:
        self.state = state
        self._value = value

    @classmethod
    def not_set(cls) -> Override[_OT]:
        """Returns an override for an omitted property.

        Returns:
            Override[_OT]: An override that leaves the property free to inherit a value.
        """
        return cls(_OverrideState.NOT_SET)

    @classmethod
    def cleared(cls) -> Override[_OT]:
        """Returns an override for an explicit null.

        Returns:
            Override[_OT]: An override that blocks inheritance and clears the value.
        """
        return cls(_OverrideState.CLEARED)

    @classmethod
    def value(cls, value: _OT) -> Override[_OT]:
        """Returns an override that holds a value.

        Args:
            value: The property's value.

        Returns:
            Override[_OT]: An override that holds ``value``.
        """
        return cls(_OverrideState.VALUE, value)

    @property
    def is_not_set(self) -> bool:
        """A Boolean value that indicates whether the property is omitted."""
        return self.state is _OverrideState.NOT_SET

    @property
    def is_cleared(self) -> bool:
        """A Boolean value that indicates whether the property is an explicit null."""
        return self.state is _OverrideState.CLEARED

    @property
    def is_value(self) -> bool:
        """A Boolean value that indicates whether the property has a value."""
        return self.state is _OverrideState.VALUE

    def get(self) -> _OT | None:
        """Returns the property's value.

        Returns:
            _OT | None: The value, or ``None`` if the property is omitted or cleared.
        """
        return (
            cast("_OT | None", self._value)
            if self.state is _OverrideState.VALUE
            else None
        )

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Override)
            and self.state is other.state
            and self._value == other._value
        )

    def __repr__(self) -> str:
        if self.state is _OverrideState.VALUE:
            return f"Override.value({self._value!r})"
        return f"Override.{self.state.value}()"

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Any, handler: GetCoreSchemaHandler
    ) -> Any:
        args = get_args(source)
        inner = handler.generate_schema(args[0]) if args else core_schema.any_schema()
        if isinstance(inner, dict) and inner.get("type") == "enum":
            inner = {**inner, "strict": False}

        def _validate(v: Any, validate_inner: Any) -> Override[Any]:
            if not isinstance(v, Override):
                return (
                    Override.cleared()
                    if v is None
                    else Override.value(validate_inner(v))
                )
            if v.is_value:
                return Override.value(validate_inner(v._value))
            return v

        return core_schema.no_info_wrap_validator_function(
            _validate,
            inner,
            serialization=core_schema.plain_serializer_function_ser_schema(
                _ser_override, info_arg=True
            ),
        )


_NOT_SET = object()


def _gate_wire_version(
    cls: type[ObjectModel | TaggedUnionModel],
    out: dict[str, Any],
    specs: Iterable[tuple[str, tuple[int, int], Any]],
    dropped: str,
) -> tuple[set[str], tuple[int, int] | None]:
    if (wire_v := out.get("version")) is None:
        return set(), None
    if (wire := Version.parse(wire_v)) is None:
        raise ValueError(f"{cls.__name__}: unparsable version {wire_v!r}")
    schema = cls.__wire_version_tuple__
    if wire.major > schema[0]:
        raise DocumentVersionError(
            f"{cls.__name__}: input declares version {wire} but this library "
            f"implements {schema[0]}.x. Update this library to a newer version to "
            "read it.",
        )
    stamp = (wire.major, wire.minor)
    too_new = {name for name, added, _x in specs if added > stamp}
    for name in too_new & out.keys():
        logger.warning(
            "%s.%s: the key is newer than the version %s, so it decodes as %s.",
            cls.__name__,
            name,
            wire,
            dropped,
        )
        del out[name]
    return too_new, stamp


def _adopted_preset(out: dict[str, Any]) -> Any:
    if "preset_identifier" in out and out["preset_identifier"] is None:
        del out["preset_identifier"]
    return out.get("preset_identifier")


def _decode_adoption(
    pid: Any, info: ValidationInfo
) -> tuple[Any, dict[str, Any], bool, dict[str, Any]] | None:
    ctx = info.context
    registry = ctx.get("wire_presets") if ctx else None
    if registry is None or not isinstance(pid, str) or not pid:
        return None
    strict, gate_ctx = _preset_gate_context(ctx)
    return registry, registry.resolved_properties(pid), strict, gate_ctx


def _same_value(a: Any, b: Any) -> bool:
    match a, b:
        case (bool(), _) | (_, bool()):
            return type(a) is type(b) and a == b
        case int() | float(), int() | float():
            return type(a) is type(b) and a == b
        case BaseModel(), BaseModel():
            return (
                type(a) is type(b)
                and _same_value(a.__dict__, b.__dict__)
                and _same_value(a.__pydantic_extra__ or {}, b.__pydantic_extra__ or {})
                and (
                    a._read_primary() == b._read_primary()
                    if isinstance(a, TaggedUnionModel)
                    and isinstance(b, TaggedUnionModel)
                    else a.__pydantic_private__ == b.__pydantic_private__
                )
            )
        case Override(), Override():
            return a.state is b.state and _same_value(a._value, b._value)
        case dict(), dict():
            return a.keys() == b.keys() and all(_same_value(a[k], b[k]) for k in a)
        case list() | tuple(), list() | tuple():
            return len(a) == len(b) and all(
                _same_value(x, y) for x, y in zip(a, b, strict=False)
            )
    return type(a) is type(b) and a == b


def _same_as_preset(
    value: Any, fill: Any, preset_json: Any, own_json: Any = _NOT_SET
) -> bool:
    return _same_value(value, fill) and (
        own_json is _NOT_SET or same_json(own_json, preset_json)
    )


class ObjectModel(BaseModel):
    """The base for the model of every object that isn't a tagged union.

    Besides the fields, the JSON carries an envelope that keeps documents compatible
    across versions, backward and forward. ``model_dump`` writes its ``type_identifier``
    and ``version`` itself, so neither is a field. Dumping a whole document isn't
    recommended, because it's large as JSON, but a small model like this one is fine:

    >>> from creator_studio_doc_format.core import Size
    >>> dumped = Size(width=100.0, height=50.0).model_dump(mode="json")
    >>> dumped["type_identifier"], dumped["version"]
    ('com.apple.apps.content-language.size', '1.0')

    An assignment such as ``m.field = x`` validates as strictly as construction does. A
    change in place, such as ``m.items.append(bad)`` or ``m.mapping[k] = bad``, skips
    validation. Reassign the whole field to revalidate it.

    The model handles the envelope and preset inheritance itself, so ``model_dump`` and
    ``model_dump_json`` raise ``ValueError`` for the options that filter fields, such as
    ``exclude_unset`` and ``exclude_none``.
    """

    # `allow_inf_nan=False` because Pydantic would otherwise write NaN and Infinity as
    # null.
    model_config = ConfigDict(
        strict=True, extra="allow", allow_inf_nan=False, validate_assignment=True
    )

    preset_identifier: str = ""
    _wire_filled: _PresetFilled = PrivateAttr(default_factory=_PresetFilled)
    _wire_floor: _WireFloor = PrivateAttr(default_factory=_WireFloor)

    __wire_type_id__: ClassVar[str] = ""
    __wire_version__: ClassVar[str] = "1.0"
    __wire_version_tuple__: ClassVar[tuple[int, int]] = (1, 0)
    __wire_fields__: ClassVar[tuple[FieldSpec, ...]] = ()

    def __deepcopy__(self: _M, memo: dict[int, Any] | None = None) -> _M:
        return _deepcopy_with_memo(self, memo)

    @classmethod
    def _preset_annotation(cls, wire_key: str, kind: str) -> Any:
        annotation = cls.model_fields[wire_key].annotation
        if kind in ("ovr", "ovrdef"):
            inner = get_args(annotation)
            annotation = inner[0] if inner else Any
        return annotation

    @classmethod
    def _field_preset_supply(
        cls,
        *,
        registry: Any,
        pid: str,
        props: dict[str, Any],
        wk: str,
        kind: str,
        gate_ctx: dict[str, Any],
        strict: bool,
    ) -> Any:
        if wk not in props:
            return _NO_FILL
        return _preset_supply(
            registry=registry,
            owner=cls,
            pid=pid,
            props=props,
            key=wk,
            annotation=cls._preset_annotation(wk, kind),
            gate_ctx=gate_ctx,
            strict=strict,
            clears=kind in ("ovr", "ovrdef"),
            required=kind == "req",
        )

    @model_validator(mode="before")
    @classmethod
    def _wire_before(cls, data: Any, info: ValidationInfo) -> Any:
        # `info` must not have a default. Pydantic 2.13.x treats a defaulted third
        # parameter as absent and never injects `ValidationInfo`. `info.context` is then
        # always `None`, and the preset fill silently does nothing.
        if not isinstance(data, dict):
            return data
        out = dict(data)
        too_new, _stamp = _gate_wire_version(
            cls, out, cls.__wire_fields__, "its default"
        )
        for wk, _added, kind in cls.__wire_fields__:
            if kind == "def" and wk in out and out[wk] is None:
                out[wk] = cls.model_fields[wk].get_default(call_default_factory=True)
        pid = _adopted_preset(out)
        if (adoption := _decode_adoption(pid, info)) is not None:
            registry, props, strict, gate_ctx = adoption
            supplies = [
                (
                    wk,
                    cls._field_preset_supply(
                        registry=registry,
                        pid=pid,
                        props=props,
                        wk=wk,
                        kind=kind,
                        gate_ctx=gate_ctx,
                        strict=strict,
                    ),
                )
                for wk, _added, kind in cls.__wire_fields__
                if wk not in too_new and wk not in out
            ]
            if filled := _fill_from_preset(out, props, supplies):
                out[_FILLED_KEY] = filled
        for wk, _added, kind in cls.__wire_fields__:
            if kind in ("ovr", "ovrdef") and wk in out:
                raw_ov = out[wk]
                if isinstance(raw_ov, Override):
                    continue
                out[wk] = (
                    Override.cleared() if raw_ov is None else Override.value(raw_ov)
                )
        out.pop("type_identifier", None)
        out.pop("version", None)
        return out

    @model_validator(mode="wrap")
    @classmethod
    def _wire_inherited(
        cls, data: Any, handler: ModelWrapValidatorHandler[ObjectModel]
    ) -> ObjectModel:
        model = handler(data)
        if isinstance(data, dict) and data.get("preset_identifier"):
            model.__pydantic_fields_set__.difference_update(
                wk for wk, _a, _kind in cls.__wire_fields__ if wk not in data
            )
            if (
                filled := (model.__pydantic_extra__ or {}).pop(_FILLED_KEY, None)
            ) is not None:
                model._wire_filled = _PresetFilled(filled)
        if (
            isinstance(data, dict)
            and (wire_v := Version.parse(data.get("version"))) is not None
        ):
            model._wire_floor = _WireFloor.at(
                (wire_v.major, wire_v.minor), cls.__wire_version_tuple__, model
            )
        return model

    @model_serializer(mode="wrap")
    def _wire_after(self, handler: Any, info: Any) -> dict[str, Any]:
        if (
            info.exclude_unset
            or info.exclude_defaults
            or info.exclude_none
            or info.include is not None
            or info.exclude is not None
        ):
            raise ValueError(
                "Models own their JSON shape, so the field-filtering dump options `exclude_unset`, "
                "`exclude_defaults`, `exclude_none`, `include`, and `exclude` would corrupt it. "
                'Use `model_dump(mode="json")` or `model_dump_json()` with no field filters.'
            )
        raw = handler(self)
        cls = type(self)
        authored = {wk for wk, _a, _k in cls.__wire_fields__}
        out: dict[str, Any] = {}
        present: set[str] = set()
        registry, props = _resolved_preset_props(self, info) or (None, None)
        gate_ctx = _preset_gate_context(info.context)[1] if props is not None else {}

        def _preset_value(wk: str, kind: str) -> Any:
            if props is None:
                return _NO_FILL
            try:
                return cls._field_preset_supply(
                    registry=registry,
                    pid=self.preset_identifier,
                    props=props,
                    wk=wk,
                    kind=kind,
                    gate_ctx=gate_ctx,
                    strict=False,
                )
            except DocumentVersionError:
                return _NO_FILL

        def _as_decoded(wk: str, kind: str, value: Any) -> Any:
            adapter = _cached_preset_adapter(
                (cls, wk), cls._preset_annotation(wk, kind)
            )
            return adapter.validate_python(value, context=gate_ctx)

        def _default(wk: str, kind: str) -> Any:
            default = cls.model_fields[wk].get_default(call_default_factory=True)
            return _as_decoded(
                wk, kind, default.get() if isinstance(default, Override) else default
            )

        def _preset_supplies(wk: str, kind: str, fill: Any) -> bool:
            if fill is _NO_FILL:
                return False
            if kind != "ovrdef" or fill is _CLEAR:
                return True
            return not _same_value(fill, _default(wk, kind))

        def _untouched(wk: str, kind: str, value: Any, fill: Any) -> bool:
            if wk in self._wire_filled.keys:
                return (
                    fill is not _NO_FILL
                    and fill is not _CLEAR
                    and _same_value(value, fill)
                )
            return _same_value(_as_decoded(wk, kind, value), _default(wk, kind))

        def _factor_out(wk: str, fill: Any, value: Any) -> bool:
            if props is None or fill is _NO_FILL or fill is _CLEAR:
                return False
            own = raw.get(wk) if wk in self.model_fields_set else _NOT_SET
            return _same_as_preset(value, fill, props[wk], own)

        nulls: dict[str, tuple[int, int]] = {}
        for wk, added, kind in cls.__wire_fields__:
            if kind == "req":
                if not _factor_out(
                    wk, _preset_value(wk, kind), getattr(self, wk, None)
                ):
                    out[wk] = raw.get(wk)
            elif kind == "def":
                fill = _preset_value(wk, kind)
                if wk in self.model_fields_set:
                    if not _factor_out(wk, fill, getattr(self, wk, None)):
                        out[wk] = raw.get(wk)
                elif hasattr(self, wk) and not _untouched(
                    wk, kind, getattr(self, wk), fill
                ):
                    out[wk] = raw.get(wk)
            elif kind in ("ovr", "ovrdef"):
                ov = getattr(self, wk)
                fill = _preset_value(wk, kind)
                if (
                    kind == "ovrdef"
                    and wk not in self.model_fields_set
                    and (
                        ov.is_not_set
                        or (ov.is_value and _untouched(wk, kind, ov.get(), fill))
                    )
                ):
                    if ov.is_value and not _same_value(
                        _as_decoded(wk, kind, ov.get()), _default(wk, kind)
                    ):
                        present.add(wk)
                    continue
                if ov.is_cleared:
                    if wk in self.model_fields_set or fill is not _CLEAR:
                        out[wk] = None
                    present.add(wk)
                elif ov.is_value:
                    present.add(wk)
                    holds_default = kind == "ovrdef" and _same_value(
                        _as_decoded(wk, kind, ov.get()), _default(wk, kind)
                    )
                    if holds_default or not _factor_out(wk, fill, ov.get()):
                        out[wk] = raw.get(wk)
            else:
                fill = _preset_value(wk, kind)
                if (v := getattr(self, wk)) is not None:
                    present.add(wk)
                    if not _factor_out(wk, fill, v):
                        out[wk] = raw.get(wk)
                elif wk in self.model_fields_set and _preset_supplies(wk, kind, fill):
                    out[wk] = None
                    nulls[wk] = added
        out["type_identifier"] = cls.__wire_type_id__
        ver = _object_version(cls.__wire_fields__, present)
        if self._wire_floor.holds(self):
            ver = max(ver, cast(tuple[int, int], self._wire_floor.version))
        out["version"] = f"{ver[0]}.{ver[1]}"
        for wk, added in nulls.items():
            if added > ver:
                del out[wk]
        if self.preset_identifier:
            out["preset_identifier"] = raw.get("preset_identifier")
        base_keys = {"preset_identifier"}
        for k, v in raw.items():
            if k not in authored and k not in base_keys and k not in out:
                out[k] = v
        return out


CaseSpec = tuple[str, tuple[int, int], bool]


def wire_union(
    type_id: str, *, version: str, cases: list[CaseSpec]
) -> Callable[[type[_E]], type[_E]]:

    def wrap(cls: type[_E]) -> type[_E]:
        cls.__wire_type_id__ = type_id
        cls.__wire_version__ = version
        cls.__wire_version_tuple__ = _schema_version(version)
        cls.__wire_cases__ = tuple(cases)
        return cls

    return wrap


def _ser_payload(v: Any, ctx: Any = None) -> Any:
    if isinstance(v, BaseModel):
        return v.model_dump(mode="json", context=ctx)
    if isinstance(v, Enum):
        return v.value
    return v


def _newest_case(cases: Iterable[tuple[str, tuple[int, int]]]) -> str:
    return min(cases, key=lambda p: (-p[1][0], -p[1][1], p[0]))[0]


def _set_primary(inst: TaggedUnionModel, primary: str | None) -> None:
    priv = inst.__pydantic_private__
    if priv is None:
        priv = {
            k: a.get_default() for k, a in type(inst).__private_attributes__.items()
        }
        object.__setattr__(inst, "__pydantic_private__", priv)
    priv["_primary"] = primary


class TaggedUnionModel(BaseModel):
    """The base for every tagged union, a property that holds one of several cases.

    A subclass declares one optional attribute per case: the payload type, or
    ``Literal[True]`` for a case with no payload. A document can also hold a second
    case, such as a newer encoding beside an older one. The primary case is the one a
    reader acts on, and editing only the primary leaves the others stale.

    Read a value with a ``match`` on ``union_primary()`` that ends in ``assert_never``,
    so a case added later is a type error. An ``if … is not None`` chain would skip it
    instead.

    A union adopts a preset through ``preset_identifier``, as an object does. Without a
    designation, the preset can supply the primary, so pin it with ``union_of``.
    """

    model_config = ConfigDict(
        strict=True, extra="allow", allow_inf_nan=False, validate_assignment=True
    )

    _primary: str | None = PrivateAttr(default=None)
    _wire_floor: _WireFloor = PrivateAttr(default_factory=_WireFloor)

    preset_identifier: str = ""

    __wire_type_id__: ClassVar[str] = ""
    __wire_version__: ClassVar[str] = "1.0"
    __wire_version_tuple__: ClassVar[tuple[int, int]] = (1, 0)
    __wire_cases__: ClassVar[tuple[CaseSpec, ...]] = ()

    def __deepcopy__(self: _E, memo: dict[int, Any] | None = None) -> _E:
        return _deepcopy_with_memo(self, memo)

    @classmethod
    def union_of(cls: type[_E], primary: str, **cases: Any) -> _E:
        """Creates a value from its cases, with one designated as the primary case.

        Args:
            primary: The name of the case a reader acts on. ``cases`` must set it.
            **cases: The payload of each case, keyed by case name.

        Returns:
            _E: The value, with ``primary`` designated.

        Raises:
            ValueError: ``primary`` names no case of the class.
        """
        if primary not in {wn for wn, _a, _v in cls.__wire_cases__}:
            raise ValueError(f"{cls.__name__}: unknown primary case {primary!r}")
        inst = cls(**cases)
        _set_primary(inst, primary)
        return inst

    def _designated_primary(
        self, cases: Iterable[tuple[str, Any, Any]], unknown: Iterable[str]
    ) -> str | None:
        designated = self._primary
        if not isinstance(designated, str) or not designated:
            return None
        if designated in unknown or any(c[0] == designated for c in cases):
            return designated
        return None

    def _read_primary(self) -> tuple[str | None, str | None]:
        known = [(wn, None, None) for wn, _a, _v in type(self).__wire_cases__]
        shown = self.union_primary_name()
        name = self._designated_primary(known, self.__pydantic_extra__ or {})
        return shown, None if name == shown else name

    def __eq__(self, other: object) -> bool:
        if type(other) is not type(self) or not isinstance(other, TaggedUnionModel):
            return NotImplemented
        if (
            self.__dict__ != other.__dict__
            or self.__pydantic_extra__ != other.__pydantic_extra__
        ):
            return False
        return self._read_primary() == other._read_primary()

    def union_cases(self) -> tuple[tuple[str, Any], ...]:
        """Returns the cases that a value holds, primary first, then the others by name.

        The primary is the designated case, else the newest. The first entry is the
        ``primary_case`` that ``model_dump`` writes when all of these hold:

        - The primary is a case this build knows.
        - The value holds every case its preset supplies.
        - The value has a designation, or holds no unknown case.

        Cases this build doesn't know are left out, though a round trip still preserves
        them. The result is empty only for a value with no case set, which
        ``model_dump`` rejects unless the value adopts a preset.

        Returns:
            tuple[tuple[str, Any], ...]: A ``(case_name, payload)`` pair for each
            present case.
        """
        present = [
            (wn, value)
            for wn, _added, _vl in type(self).__wire_cases__
            if (value := getattr(self, wn, None)) is not None
        ]
        if not present:
            return ()
        names = [wn for wn, _payload in present]
        if self._primary in names:
            primary = self._primary
        else:
            added = {wn: a for wn, a, _vl in type(self).__wire_cases__}
            primary = _newest_case((wn, added[wn]) for wn in names)
        return tuple(sorted(present, key=lambda p: (p[0] != primary, p[0])))

    def union_primary(self) -> tuple[str, Any] | None:
        """Returns the case that a reader acts on, with its payload.

        Prefer it to ``union_primary_name`` plus ``getattr``: the payload comes back
        resolved, as ``True`` for a valueless case, and the pair destructures in a
        ``match``. The primary is the case the document designates, so pick another
        representation, such as plain text, from ``union_cases()``. The payload is the
        live model, not a copy.

        Returns:
            tuple[str, Any] | None: The ``(case_name, payload)`` pair, or ``None`` if no
            case is set.
        """
        items = self.union_cases()
        return items[0] if items else None

    def union_primary_name(self) -> str | None:
        """Returns the name of the case that a reader acts on.

        The name is also the attribute name, so it suits classifying a value without
        touching the payload.

        Returns:
            str | None: The case name, or ``None`` if no case is set.
        """
        item = self.union_primary()
        return item[0] if item is not None else None

    @classmethod
    def _case_preset_fills(
        cls,
        wns: Iterable[str],
        *,
        registry: Any,
        pid: str,
        props: dict[str, Any],
        gate_ctx: dict[str, Any],
        strict: bool,
    ) -> tuple[dict[str, Any], DocumentVersionError | None]:
        fills: dict[str, Any] = {}
        too_new: DocumentVersionError | None = None
        for wn in wns:
            if wn not in props:
                continue
            try:
                fill = _preset_supply(
                    registry=registry,
                    owner=cls,
                    pid=pid,
                    props=props,
                    key=wn,
                    annotation=cls.model_fields[wn].annotation,
                    gate_ctx=gate_ctx,
                    strict=strict,
                    clears=False,
                    required=True,
                )
            except DocumentVersionError as e:
                too_new = too_new or e
                continue
            if fill is not _NO_FILL:
                fills[wn] = fill
        return fills, too_new

    @model_validator(mode="wrap")
    @classmethod
    def _wire_decode_wrap(cls, data: Any, handler: Any, info: ValidationInfo) -> Any:
        # `info` must not have a default, for the reason given in
        # `ObjectModel._wire_before`.
        valueless = {wn for wn, _a, vl in cls.__wire_cases__ if vl}
        if isinstance(data, str):
            if data not in valueless:
                raise ValueError(f"{cls.__name__}: unknown bare case {data!r}")
            inst = handler({data: True})
            _set_primary(inst, data)
            return inst
        if isinstance(data, dict):
            out = dict(data)
            too_new_cases, stamp = _gate_wire_version(
                cls, out, cls.__wire_cases__, "absent"
            )
            primary = out.pop("primary_case", None)
            if isinstance(primary, str) and primary in too_new_cases:
                primary = None
            out.pop("type_identifier", None)
            out.pop("version", None)
            pid = _adopted_preset(out)
            filled: frozenset[str] = frozenset()
            too_new: DocumentVersionError | None = None
            if (adoption := _decode_adoption(pid, info)) is not None:
                registry, props, strict, gate_ctx = adoption
                fills, too_new = cls._case_preset_fills(
                    (
                        wn
                        for wn, _a, vl in cls.__wire_cases__
                        if not vl and wn not in out and wn not in too_new_cases
                    ),
                    registry=registry,
                    pid=pid,
                    props=props,
                    gate_ctx=gate_ctx,
                    strict=strict,
                )
                filled = _fill_from_preset(out, props, fills.items())
            for wn in valueless:
                if wn in out and out[wn] is None:
                    out[wn] = True
            inst = handler(out)
            inst.__pydantic_fields_set__.difference_update(filled)
            present = [
                (wn, added)
                for wn, added, _v in cls.__wire_cases__
                if getattr(inst, wn) is not None
            ]
            if not present:
                if too_new is not None:
                    raise too_new
                if not pid or adoption is not None or inst.__pydantic_extra__:
                    raise ValueError(f"{cls.__name__}: no case present")
            _set_primary(inst, primary)
            inst._wire_floor = _WireFloor.at(stamp, cls.__wire_version_tuple__, inst)
            return inst
        prior = (data._primary, data._wire_floor) if isinstance(data, cls) else None
        inst = handler(data)
        if prior is not None:
            _set_primary(inst, prior[0])
            inst._wire_floor = prior[1]
        return inst

    @model_serializer(mode="plain")
    def _wire_encode(self, info: Any) -> Any:
        cls = type(self)
        present = [
            (wn, added, vl)
            for wn, added, vl in cls.__wire_cases__
            if getattr(self, wn) is not None
        ]
        extra = dict(self.__pydantic_extra__ or {})
        unknown_cases = set(extra)
        if not present and not self.preset_identifier:
            raise ValueError(f"{cls.__name__}: can't encode with no case set")
        if (
            not extra
            and not self.preset_identifier
            and len(present) == 1
            and present[0][2]
        ):
            return present[0][0]
        ver = max((added for _wn, added, _vl in present), default=(1, 0))
        if floored := self._wire_floor.holds(self):
            ver = max(ver, cast(tuple[int, int], self._wire_floor.version))
        reload_cases = list(present)
        factored: set[str] = set()
        nulls: set[str] = set()
        payloads: dict[str, Any] = {}
        if (resolved := _resolved_preset_props(self, info)) is not None:
            registry, props = resolved
            gate_ctx = _preset_gate_context(info.context)[1]
            fills, too_new = cls._case_preset_fills(
                (
                    wn
                    for wn, added, vl in cls.__wire_cases__
                    if not vl and (not present or added <= ver)
                ),
                registry=registry,
                pid=self.preset_identifier,
                props=props,
                gate_ctx=gate_ctx,
                strict=False,
            )
            if not present:
                ver = max(
                    [ver, *(a for wn, a, _vl in cls.__wire_cases__ if wn in fills)]
                )
            for wn, added, vl in cls.__wire_cases__:
                if (fill := fills.get(wn, _NO_FILL)) is _NO_FILL:
                    continue
                if (v := getattr(self, wn)) is not None:
                    if wn in self.model_fields_set:
                        payloads[wn] = _ser_payload(v, info.context)
                    if _same_as_preset(v, fill, props[wn], payloads.get(wn, _NOT_SET)):
                        factored.add(wn)
                elif wn in self.model_fields_set:
                    nulls.add(wn)
                else:
                    reload_cases.append((wn, added, vl))
            if not reload_cases:
                if too_new is not None:
                    if info.context.get("_wire_version_error", too_new) is None:
                        info.context["_wire_version_error"] = too_new
                    raise too_new
                if nulls:
                    raise ValueError(
                        f"{cls.__name__}: can't encode with no case set: the value sets "
                        f"{', '.join(map(repr, sorted(nulls)))} to None over preset "
                        f"{self.preset_identifier!r}"
                    )
                raise ValueError(
                    f"{cls.__name__}: can't encode with no case set, and preset "
                    f"{self.preset_identifier!r} supplies none"
                )
        primary = designated = self._designated_primary(reload_cases, unknown_cases)
        if primary is None and reload_cases:
            primary = _newest_case((wn, added) for wn, added, _vl in reload_cases)
        first = (
            primary
            if not present or any(wn == primary for wn, _a, _vl in present)
            else _newest_case((wn, added) for wn, added, _vl in present)
        )
        ordered = sorted(present, key=lambda p: (p[0] != first, p[0]))
        out: dict[str, Any] = {}
        if primary in unknown_cases:
            out[primary] = extra[primary]
        for wn, _added, vl in ordered:
            if wn in factored:
                continue
            if vl:
                out[wn] = None
            elif wn in payloads:
                out[wn] = payloads[wn]
            else:
                out[wn] = _ser_payload(getattr(self, wn), info.context)
        for wn in sorted(nulls):
            out[wn] = None
        for k, v in extra.items():
            if k not in out:
                out[k] = v
        names_known = any(wn == self._primary for wn, _a, _vl in cls.__wire_cases__)
        if floored and designated is None and names_known:
            primary = self._primary
        if (
            primary is not None
            and len(reload_cases) + len(unknown_cases) > 1
            and (not floored or designated is not None or names_known)
        ):
            out["primary_case"] = primary
        out["type_identifier"] = cls.__wire_type_id__
        out["version"] = f"{ver[0]}.{ver[1]}"
        if self.preset_identifier:
            out["preset_identifier"] = self.preset_identifier
        return out


def same_json(a: Any, b: Any) -> bool:
    """Returns a Boolean value that indicates whether two parsed JSON values are equal.

    Two strings of JSON text compare only as strings, so parse the text first. Key order
    doesn't matter, but array order does. Numbers compare by value, so ``1`` equals
    ``1.0``. ``True`` and ``False`` never equal ``1`` and ``0``. A ``null`` differs from
    an absent key.

    Args:
        a: A parsed JSON value.
        b: A parsed JSON value.

    Returns:
        bool: ``True`` if ``a`` and ``b`` are the same JSON, or ``False`` if they
        aren't.
    """
    if isinstance(a, bool) or isinstance(b, bool):
        return type(a) is type(b) and a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a == b
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(same_json(a[k], b[k]) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(
            same_json(x, y) for x, y in zip(a, b, strict=False)
        )
    return type(a) is type(b) and a == b
