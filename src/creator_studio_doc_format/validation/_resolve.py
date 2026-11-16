# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


from typing import Any

from pydantic import ValidationError

from creator_studio_doc_format.core import Package, PayloadT, Preset, PresetRegistry


# A preset cycle recurses without end, so call this only after
# `validate_preset_graph(doc.presets)` passes.
def _resolve_properties(doc: Package[PayloadT], main_json: dict[str, Any]) -> PayloadT:
    reg = PresetRegistry(doc.presets)
    payload_cls = type(doc.payload)
    try:
        resolved = payload_cls.model_validate(
            main_json, context={"wire_presets": reg, "wire_presets_strict": True}
        )
    except ValidationError as e:
        _raise_if_unresolved(reg)
        raise _attributed_error(e, payload_cls, main_json, doc.presets) from e
    _raise_if_unresolved(reg)
    return resolved


def _raise_if_unresolved(reg: PresetRegistry) -> None:
    if reg.warnings:
        missing = ", ".join(
            sorted({w.removeprefix("missing preset ") for w in reg.warnings})
        )
        raise LookupError(f"`preset_identifier` matches no preset: {missing}")


def _attributed_error(
    e: ValidationError,
    payload_cls: type[PayloadT],
    main_json: dict[str, Any],
    presets: list[Preset],
) -> ValueError:
    try:
        payload_cls.model_validate(
            main_json, context={"wire_presets": PresetRegistry(presets)}
        )
    except ValidationError as lenient:
        return _payload_defect_error(lenient, bool(presets))
    return _inherited_value_error(e)


def _render_locs(e: ValidationError) -> str:
    return "\n".join(
        f"  at {'.'.join(str(x) for x in err['loc'])}: {err['msg']}"
        for err in e.errors()
    )


_REVALIDATE_HINT = (
    "In-place mutation, `model_construct`, or `model_copy(update=...)` likely set "
    "the value, and all three skip validation. Reassign the field to "
    "revalidate it."
)


def _payload_defect_error(e: ValidationError, has_presets: bool) -> ValueError:
    if has_presets:
        return ValueError(
            "The document doesn't validate against its own JSON. Fix any invalid "
            "preset property. Otherwise, an edit bypassed validation. "
            + _REVALIDATE_HINT
            + " Validation errors:\n"
            + _render_locs(e)
        )
    return ValueError(
        "An edit bypassed validation, so the document doesn't validate against "
        "its own JSON. " + _REVALIDATE_HINT + " Validation errors:\n" + _render_locs(e)
    )


def _inherited_value_error(e: ValidationError) -> ValueError:
    return ValueError(
        "An inherited preset value is invalid. Fix the preset properties. "
        "Validation errors:\n" + _render_locs(e)
    )
