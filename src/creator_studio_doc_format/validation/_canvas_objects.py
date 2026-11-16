# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


from collections.abc import Sequence
from typing import TYPE_CHECKING

from creator_studio_doc_format.core import (
    CanvasObject,
    ConnectionLine,
    Constituent,
    Group,
    ObjectModel,
    Slide,
    SlideLayout,
    SlideObject,
    SourceKind,
)

from ._cases import unwrap_primary_case
from ._identifiers import claim_unique
from ._paths import extend_path

if TYPE_CHECKING:
    from creator_studio_doc_format.navigation import IteratedModel

    from ._model_tree import _IterationState


class CanvasObjectValidator:
    def visit(self, state: "_IterationState", iterated: "IteratedModel") -> None:
        model = iterated.model
        from_layout = any(
            isinstance(a, SlideObject) and a.source_kind == SourceKind.LAYOUT
            for a in iterated.ancestors
        )
        match model:
            case Slide() | SlideLayout():
                _validate_canvas_object_container(
                    state, iterated.path, model.contents or [], "contents", from_layout
                )
            case Group():
                _validate_canvas_object_container(
                    state, iterated.path, model.children, "children", from_layout
                )
            case Constituent() if (inline := model.inline_object) is not None:
                if not from_layout:
                    _, resolved = unwrap_primary_case(inline)
                    _claim_document_wide(
                        state, resolved, extend_path(iterated.path, "inline_object")
                    )

    def finalize(self, state: "_IterationState") -> None:
        return


def _validate_canvas_object_container(
    state: "_IterationState",
    path: str,
    items: Sequence[SlideObject | CanvasObject],
    field_name: str,
    from_layout: bool,
) -> None:
    local_id_paths: dict[str, str] = {}
    connection_lines: list[tuple[str, ConnectionLine]] = []
    for i, item in enumerate(items):
        if isinstance(item, SlideObject):
            canvas_object: CanvasObject = item.object
            suffix = f"{field_name}[{i}].object"
        else:
            canvas_object = item
            suffix = f"{field_name}[{i}]"
        item_path = extend_path(path, suffix)
        _, resolved = unwrap_primary_case(canvas_object)
        _register_canvas_object(resolved, item_path, local_id_paths)
        if not from_layout and not (
            isinstance(item, SlideObject) and item.source_kind == SourceKind.LAYOUT
        ):
            _claim_document_wide(state, resolved, item_path)
        if isinstance(resolved, ConnectionLine):
            connection_lines.append((item_path, resolved))
    for line_path, line in connection_lines:
        _validate_connection_line_ends(line_path, line, local_id_paths)


def _validate_connection_line_ends(
    path: str, line: ConnectionLine, local_id_paths: dict[str, str]
) -> None:
    for end_name, end in (("tail", line.tail), ("head", line.head)):
        if end.end_point is None:
            raise ValueError(
                f"`ConnectionLine.End.end_point` is missing "
                f"(at {path}.{end_name}.end_point)"
            )
        if (anchor := end.anchor) is None:
            continue
        if anchor.object_id not in local_id_paths:
            raise LookupError(
                f"`ConnectionLine.End.Anchor.object_id` {anchor.object_id!r} "
                f"matches no sibling of the line "
                f"(at {path}.{end_name}.anchor.object_id)"
            )


def _register_canvas_object(
    model: ObjectModel,
    path: str,
    local_id_paths: dict[str, str],
) -> None:
    if (identifier := getattr(model, "identifier")) is not None:  # noqa: B009
        claim_unique(
            local_id_paths, identifier, path, f"{type(model).__name__}.identifier"
        )


def _claim_document_wide(
    state: "_IterationState", model: ObjectModel, path: str
) -> None:
    if (identifier := getattr(model, "identifier", None)) is not None:
        claim_unique(
            state.canvas_object_ids,
            identifier,
            path,
            f"{type(model).__name__}.identifier",
        )
