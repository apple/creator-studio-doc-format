# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Protocol

from pydantic import BaseModel

from creator_studio_doc_format.navigation import IteratedModel, iterate_models

from ._canvas_objects import CanvasObjectValidator
from ._charts import ChartValidator
from ._slides import SlideValidator
from ._string_formats import StringFormatValidator
from ._tables import TableValidator

if TYPE_CHECKING:
    from ._slides import _PendingLayoutRef, _PendingSlideTarget


@dataclass
class _IterationState:
    slide_ids: dict[str, str] = field(default_factory=dict)
    slide_layout_ids: dict[str, str] = field(default_factory=dict)
    canvas_object_ids: dict[str, str] = field(default_factory=dict)
    slide_layout_names: dict[str, str] = field(default_factory=dict)
    pending_slide_targets: list["_PendingSlideTarget"] = field(default_factory=list)
    pending_layout_refs: list["_PendingLayoutRef"] = field(default_factory=list)


class ModelTreeValidator(Protocol):
    def visit(self, state: _IterationState, iterated: IteratedModel) -> None: ...

    def finalize(self, state: _IterationState) -> None: ...


_VALIDATORS: tuple[ModelTreeValidator, ...] = (
    SlideValidator(),
    CanvasObjectValidator(),
    TableValidator(),
    ChartValidator(),
    StringFormatValidator(),
)


def validate_model_tree(payload: BaseModel) -> None:
    state = _IterationState()
    for iterated in iterate_models(payload):
        for validator in _VALIDATORS:
            validator.visit(state, iterated)
    for validator in _VALIDATORS:
        validator.finalize(state)
