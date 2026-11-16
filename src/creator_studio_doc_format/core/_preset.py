# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import copy
from collections.abc import Iterable
from enum import Enum
from types import UnionType
from typing import TYPE_CHECKING, Any, Union, cast, get_args, get_origin

from pydantic import BaseModel, ConfigDict, TypeAdapter, ValidationError

from ._errors import DocumentError, DocumentVersionError

if TYPE_CHECKING:
    from ._wire import ObjectModel, TaggedUnionModel


class Preset:
    """A preset, as one entry in the presets file stores it.

    ``PresetRegistry`` resolves inheritance along ``parent_identifier``.

    Args:
        identifier: The name that an adopting object's ``preset_identifier`` refers to.
        properties: The properties that adopting objects inherit, as raw JSON.
        display_name: The name that Keynote shows.
        parent_identifier: The identifier of the preset this one inherits from.
    """

    __slots__ = ("display_name", "identifier", "parent_identifier", "properties")

    def __init__(
        self,
        identifier: str,
        properties: dict[str, Any],
        *,
        display_name: str | None = None,
        parent_identifier: str | None = None,
    ) -> None:
        self.identifier = identifier
        self.display_name = display_name
        self.parent_identifier = parent_identifier
        self.properties = properties

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Preset:
        """Creates a preset from a decoded entry of the presets file.

        Args:
            data: One decoded entry of the ``presets.json`` array.

        Returns:
            Preset: The preset, with its properties as raw JSON.

        Raises:
            KeyError: ``data`` has no ``identifier`` or no ``properties``.
        """  # noqa: DOC502 -- the `KeyError` comes from indexing `data`
        return cls(
            data["identifier"],
            data["properties"],
            display_name=data.get("display_name"),
            parent_identifier=data.get("parent_identifier"),
        )

    def to_dict(self) -> dict[str, Any]:
        """Returns the preset in the form that the presets file stores.

        Returns:
            dict[str, Any]: The entry, without any optional key that holds ``None``.
        """
        out: dict[str, Any] = {"identifier": self.identifier}
        if self.display_name is not None:
            out["display_name"] = self.display_name
        if self.parent_identifier is not None:
            out["parent_identifier"] = self.parent_identifier
        out["properties"] = self.properties
        return out


class PresetRegistry:
    """A resolver of preset inheritance for decoding and encoding.

    The registry walks the ``parent_identifier`` chain and merges each child's
    properties over its parent's. A cycle raises ``ValueError``. A missing preset or
    parent adds an entry to ``warnings`` and contributes no properties. A model takes
    the registry as its ``context["wire_presets"]`` resolver.

    Args:
        presets: The presets to resolve against. A later preset replaces an earlier one
            with the same identifier.

    >>> from creator_studio_doc_format.core import (
    ...     CellProperties,
    ...     Preset,
    ...     PresetRegistry,
    ... )
    >>> registry = PresetRegistry(
    ...     [
    ...         Preset("base", {"text_wrap": True, "vertical_alignment": "top"}),
    ...         Preset(
    ...             "wrapped",
    ...             {"vertical_alignment": "middle"},
    ...             parent_identifier="base",
    ...         ),
    ...     ]
    ... )
    >>> registry.resolved_properties("wrapped")
    {'text_wrap': True, 'vertical_alignment': 'middle'}

    When the JSON omits a field, decoding takes its value from the preset. Encoding with
    the same registry leaves out a value that still matches the preset, so the value
    stays linked to it. A value that differs is written:

    >>> context = {"wire_presets": registry}
    >>> cell = CellProperties.model_validate(
    ...     {"preset_identifier": "wrapped"}, context=context
    ... )
    >>> cell.text_wrap
    True
    >>> "text_wrap" in cell.model_dump(mode="json", context=context)
    False
    >>> cell.text_wrap = False
    >>> cell.model_dump(mode="json", context=context)["text_wrap"]
    False
    """

    __slots__ = ("_by_id", "_cache", "_cycle", "_gate_memo", "warnings")

    def __init__(self, presets: list[Preset]) -> None:
        self._by_id: dict[str, Preset] = {p.identifier: p for p in presets}
        self.warnings: list[str] = []
        self._cache: dict[str, dict[str, Any]] = {}
        self._gate_memo: dict[Any, Any] = {}
        self._cycle: str | None = None

    def resolved_properties(self, identifier: str) -> dict[str, Any]:
        """Returns the properties of a preset, merged over its ancestors' properties.

        Every call for an identifier returns the same dictionary, so don't mutate it.

        Args:
            identifier: The identifier of the preset to resolve.

        Returns:
            dict[str, Any]: The merged properties, or an empty dictionary when the
            preset is missing.

        Raises:
            ValueError: the ``parent_identifier`` chain has a cycle.
        """  # noqa: DOC502 -- raised by `_resolve`
        cached = self._cache.get(identifier)
        if cached is not None:
            return cached
        resolved = self._resolve(identifier, set())
        self._cache[identifier] = resolved
        return resolved

    def _resolve(self, identifier: str, visited: set[str]) -> dict[str, Any]:
        if identifier in visited:
            self._cycle = identifier
            raise ValueError(
                f"circular preset `parent_identifier` chain at {identifier!r}"
            )
        preset = self._by_id.get(identifier)
        if preset is None:
            self.warnings.append(f"missing preset {identifier!r}")
            return {}
        parent: dict[str, Any] = {}
        if preset.parent_identifier is not None:
            parent = self._resolve(preset.parent_identifier, visited | {identifier})
        return {**parent, **preset.properties}


_MAX_PRESET_GATE_DEPTH = 4

_NO_FILL = object()
_CLEAR = object()
_MEMO_MISS = object()
_FILLED_KEY = "\x00wire_filled"


class _PresetFilled:
    __slots__ = ("keys",)

    def __init__(self, keys: frozenset[str] = frozenset()) -> None:
        self.keys = keys

    def __eq__(self, other: object) -> bool:
        return isinstance(other, _PresetFilled)

    def __hash__(self) -> int:
        return 0


def _annotation_is_enum(annotation: Any) -> bool:
    candidates = get_args(annotation) or (annotation,)
    return any(isinstance(c, type) and issubclass(c, Enum) for c in candidates)


def _union_members(annotation: Any) -> tuple[Any, ...]:
    if get_origin(annotation) in (Union, UnionType):
        return get_args(annotation)
    return (annotation,)


def _nested_type_ids(annotation: Any) -> set[str]:
    ids: set[str] = set()
    for m in _union_members(annotation):
        if isinstance(m, type) and (tid := getattr(m, "__wire_type_id__", "")):
            ids.add(tid)
        elif get_origin(m) is list and (args := get_args(m)):
            ids |= _nested_type_ids(args[0])
    return ids


def _declares_foreign_type(candidate: Any, annotation: Any) -> bool:
    if isinstance(candidate, list):
        elements = [
            args[0]
            for m in _union_members(annotation)
            if get_origin(m) is list and (args := get_args(m))
        ]
        return bool(elements) and all(
            any(_declares_foreign_type(e, el) for e in candidate) for el in elements
        )
    if not isinstance(candidate, dict) or not (tid := candidate.get("type_identifier")):
        return False
    allowed = _nested_type_ids(annotation)
    return bool(allowed) and tid not in allowed


def _resolved_preset_props(
    model: ObjectModel | TaggedUnionModel, info: Any
) -> tuple[Any, dict[str, Any]] | None:
    pid = model.preset_identifier
    if not pid:
        return None
    ctx = getattr(info, "context", None)
    if (registry := ctx.get("wire_presets") if ctx else None) is None:
        raise ValueError(
            f"{type(model).__name__}: adopts preset {pid!r}, so encoding needs the presets. "
            "Save through Package.save, or pass context={'wire_presets': registry}."
        )
    return registry, cast("dict[str, Any]", registry.resolved_properties(pid))


def _preset_gate_context(ctx: dict[str, Any] | None) -> tuple[bool, dict[str, Any]]:
    strict = bool(ctx.get("wire_presets_strict", False)) if ctx else False
    depth = (ctx.get("_wire_gate_depth", 0) if ctx else 0) + 1
    gate_ctx: dict[str, Any] = {**(ctx or {}), "_wire_gate_depth": depth}
    if depth >= _MAX_PRESET_GATE_DEPTH:
        gate_ctx["wire_presets_strict"] = True
    return strict, gate_ctx


def _preset_gate(
    adapter: TypeAdapter[Any],
    candidate: Any,
    gate_ctx: dict[str, Any],
    *,
    required: bool,
) -> Any:
    try:
        return adapter.validate_python(candidate, context=gate_ctx)
    except DocumentVersionError:
        # A skip on a required field would report `Field required` and hide the upgrade
        # message.
        if required:
            raise
        return _NO_FILL
    except (ValidationError, DocumentError):
        return _NO_FILL


def _cached_preset_adapter(
    cache_key: tuple[type, str], annotation: Any
) -> TypeAdapter[Any]:
    owner, wire_key = cache_key
    if (cache := owner.__dict__.get("__wire_preset_adapters__")) is None:
        cache = {}
        owner.__wire_preset_adapters__ = cache  # type: ignore[attr-defined]
    adapter = cache.get(wire_key)
    if adapter is None:
        if isinstance(annotation, type) and issubclass(annotation, BaseModel):
            adapter = TypeAdapter(annotation)
        else:
            strict = not _annotation_is_enum(annotation)
            adapter = TypeAdapter(
                annotation, config=ConfigDict(strict=strict, allow_inf_nan=False)
            )
        cache[wire_key] = adapter
    return adapter


def _preset_fill(
    *,
    owner: type,
    key: str,
    annotation: Any,
    candidate: Any,
    gate_ctx: dict[str, Any],
    strict: bool,
    required: bool,
) -> Any:
    if _declares_foreign_type(candidate, annotation):
        return _NO_FILL
    if strict:
        return candidate
    adapter = _cached_preset_adapter((owner, key), annotation)
    return _preset_gate(adapter, candidate, gate_ctx, required=required)


def _preset_supply(
    *,
    registry: Any,
    owner: type,
    pid: str,
    props: dict[str, Any],
    key: str,
    annotation: Any,
    gate_ctx: dict[str, Any],
    strict: bool,
    clears: bool,
    required: bool,
) -> Any:
    if (candidate := props.get(key)) is None:
        return _CLEAR if clears and key in props else _NO_FILL
    nested_strict = bool(gate_ctx.get("wire_presets_strict", False))
    memo_key = (owner, key, pid, gate_ctx["_wire_gate_depth"], strict, nested_strict)
    memo = getattr(registry, "_gate_memo", None)

    def fill_now() -> Any:
        return _preset_fill(
            owner=owner,
            key=key,
            annotation=annotation,
            candidate=candidate,
            gate_ctx=gate_ctx,
            strict=strict,
            required=required,
        )

    if memo is None:
        return fill_now()
    if (fill := memo.get(memo_key, _MEMO_MISS)) is _MEMO_MISS:
        try:
            fill = memo[memo_key] = fill_now()
        except DocumentVersionError as e:
            memo[memo_key] = copy.copy(e)
            raise
    if isinstance(fill, DocumentVersionError):
        raise copy.copy(fill)
    return fill


def _fill_from_preset(
    out: dict[str, Any], props: dict[str, Any], supplies: Iterable[tuple[str, Any]]
) -> frozenset[str]:
    filled: set[str] = set()
    for key, fill in supplies:
        if fill is _CLEAR:
            out[key] = None
        elif fill is not _NO_FILL:
            out[key] = props[key]
            filled.add(key)
    return frozenset(filled)
