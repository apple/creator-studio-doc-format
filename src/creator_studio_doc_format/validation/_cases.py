# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


from pydantic import BaseModel

from creator_studio_doc_format.core import ObjectModel, TaggedUnionModel


def unwrap_primary_case(model: BaseModel) -> tuple[str, ObjectModel]:
    name = ""
    while isinstance(model, TaggedUnionModel):
        name, model = _resolve_case(model)
    if not isinstance(model, ObjectModel):
        raise TypeError(f"`{type(model).__name__}` is not an object model")
    return name, model


def _resolve_case(model: TaggedUnionModel) -> tuple[str, BaseModel]:
    for name, value in model.union_cases():
        if isinstance(value, BaseModel):
            return name, value
    raise ValueError(f"`{type(model).__name__}` has no case present")
