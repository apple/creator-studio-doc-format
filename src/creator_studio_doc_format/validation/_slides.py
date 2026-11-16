# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


from dataclasses import dataclass
from typing import TYPE_CHECKING

from creator_studio_doc_format._slide_layout_refs import layout_name_key
from creator_studio_doc_format.core import Slide, SlideLayout, SlideObject, SlideTarget

from ._identifiers import claim_unique

if TYPE_CHECKING:
    from creator_studio_doc_format.navigation import IteratedModel

    from ._model_tree import _IterationState


class SlideValidator:
    def visit(self, state: "_IterationState", iterated: "IteratedModel") -> None:
        model = iterated.model
        match model:
            case Slide():
                _register_slide(state, model, iterated.path)
                _defer_layout_ref(state, model, iterated.path)
                _validate_placeholder_kinds(model.contents, iterated.path)
            case SlideLayout():
                _register_slide_layout(state, model, iterated.path)
                _validate_placeholder_kinds(model.contents, iterated.path)
            case SlideTarget():
                _defer_slide_target(state, model, iterated.path)

    def finalize(self, state: "_IterationState") -> None:
        _resolve_slide_targets(state)
        _resolve_layout_refs(state)


@dataclass
class _PendingSlideTarget:
    path: str
    slide_id: str


@dataclass
class _PendingLayoutRef:
    path: str
    layout: str


def _register_slide(state: "_IterationState", slide: Slide, path: str) -> None:
    if (identifier := slide.identifier) is None:
        return
    claim_unique(state.slide_ids, identifier, path, "Slide.identifier")


def _register_slide_layout(
    state: "_IterationState", slide_layout: SlideLayout, path: str
) -> None:
    state.slide_layout_names.setdefault(
        layout_name_key(slide_layout.name), slide_layout.name
    )
    if (identifier := slide_layout.identifier) is None:
        return
    claim_unique(
        state.slide_layout_ids,
        identifier,
        path,
        "SlideLayout.identifier",
    )


def _validate_placeholder_kinds(contents: list[SlideObject] | None, path: str) -> None:
    if contents is None:
        return
    seen_kinds: dict[str, str] = {}
    for index, obj in enumerate(contents):
        if (info := obj.placeholder_info) is None or info.defined is None:
            continue
        claim_unique(
            seen_kinds,
            info.defined.kind.value,
            f"{path}.contents[{index}].placeholder_info.defined.kind",
            "PlaceholderDefinition.kind",
        )


def _defer_slide_target(
    state: "_IterationState", target: SlideTarget, path: str
) -> None:
    if (slide_id := target.by_identifier) is not None:
        state.pending_slide_targets.append(_PendingSlideTarget(path, slide_id))


def _defer_layout_ref(state: "_IterationState", slide: Slide, path: str) -> None:
    if (layout := slide.layout) is not None:
        state.pending_layout_refs.append(_PendingLayoutRef(path, layout))


def _resolve_slide_targets(state: "_IterationState") -> None:
    for pending in state.pending_slide_targets:
        if pending.slide_id not in state.slide_ids:
            raise LookupError(
                f"`SlideTarget.by_identifier` {pending.slide_id!r} matches no "
                f"`Slide.identifier` (at {pending.path}.by_identifier)"
            )


def _ascii_skeleton(key: str) -> str:
    return "".join(c for c in key if c.isascii())


def _resolve_layout_refs(state: "_IterationState") -> None:
    if not state.slide_layout_names:
        return
    non_ascii_skeletons = {
        _ascii_skeleton(key) for key in state.slide_layout_names if not key.isascii()
    }
    for pending in state.pending_layout_refs:
        if (
            pending.layout in state.slide_layout_ids
            or (key := layout_name_key(pending.layout)) in state.slide_layout_names
            or (
                not pending.layout.isascii()
                and _ascii_skeleton(key) in non_ascii_skeletons
            )
        ):
            continue
        raise LookupError(
            f"`Slide.layout` {pending.layout!r} matches no `SlideLayout` "
            f"(at {pending.path}.layout). The theme's slide layout names are "
            f"{sorted(state.slide_layout_names.values())}."
        )
