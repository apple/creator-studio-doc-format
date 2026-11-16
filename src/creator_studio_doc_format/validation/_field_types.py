# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


from typing import TYPE_CHECKING

from pydantic import BaseModel, ValidationError

from creator_studio_doc_format.core import Override
from creator_studio_doc_format.navigation import iterate_models

from ._paths import extend_path
from ._resolve import _REVALIDATE_HINT

if TYPE_CHECKING:
    from creator_studio_doc_format.navigation import IteratedModel

_PREVIEW_LEN = 60


def validate_field_types(payload: BaseModel) -> None:
    for iterated in iterate_models(payload):
        model = iterated.model
        cls = type(model)
        if gone := cls.model_fields.keys() - model.__dict__.keys():
            name = min(gone)
            raise ValueError(
                f"`{cls.__name__}.{name}` was deleted or never set by `model_construct` "
                f"(at {extend_path(iterated.path, name)})"
            )
        _validate_override_fields(cls, iterated)
        try:
            cls.model_validate(dict(model.__dict__))
        except ValidationError as exc:
            raise _rejected_error(cls, iterated, exc) from exc


def _validate_override_fields(cls: type[BaseModel], iterated: "IteratedModel") -> None:
    for wire_key, _added, kind in getattr(cls, "__wire_fields__", ()):
        if kind in ("ovr", "ovrdef") and not isinstance(
            value := iterated.model.__dict__[wire_key], Override
        ):
            raise ValueError(
                f"`{cls.__name__}.{wire_key}` {_preview(value)} isn't an `Override` "
                f"(at {extend_path(iterated.path, wire_key)}). Wrap it with "
                f"`Override.value(...)`, or use `Override.cleared()` or "
                f"`Override.not_set()`."
            )


def _rejected_error(
    cls: type[BaseModel], iterated: "IteratedModel", exc: ValidationError
) -> ValueError:
    loc = exc.errors()[0]["loc"]
    field = str(loc[0]) if loc else ""
    if field in cls.model_fields:
        head = f"`{cls.__name__}.{field}` holds a value its field declaration rejects"
        where = extend_path(iterated.path, field)
    else:
        head = f"`{cls.__name__}` holds values its declaration rejects"
        where = iterated.path or "<root>"
    return ValueError(
        f"{head} (at {where}). {_REVALIDATE_HINT} Validation errors:\n{_render(exc)}"
    )


def _preview(value: object) -> str:
    got = repr(value)
    if len(got) > _PREVIEW_LEN:
        got = f"{got[:_PREVIEW_LEN]}… ({len(got)} characters)"
    return got


def _render(exc: ValidationError) -> str:
    lines = []
    for err in exc.errors():
        where = ".".join(str(x) for x in err["loc"])
        got = _preview(err.get("input"))
        lines.append(f"  at {where or '<value>'}: {err['msg']} (got {got})")
    return "\n".join(lines)
