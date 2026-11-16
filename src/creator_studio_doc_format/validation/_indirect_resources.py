# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


from typing import Any

from creator_studio_doc_format.core import IndirectResource, Package, PayloadT
from creator_studio_doc_format.navigation import iterate_models

from ._string_formats import _reject_empty


def validate_indirect_resources(doc: Package[PayloadT], resolved: Any) -> None:
    for iterated in iterate_models(resolved):
        if not isinstance(model := iterated.model, IndirectResource):
            continue
        field, name = (
            ("filename", model.filename)
            if model.identifier is None
            else ("identifier", model.identifier)
        )
        if not name.strip():
            raise ValueError(
                f"`IndirectResource.{field}` {name!r} is empty or blank "
                f"(at {iterated.path}.{field})"
            )
        if field == "identifier":
            _reject_empty(
                model.filename, iterated.path, "filename", cls="IndirectResource"
            )
        if doc.resources._resolve_key(name) is None:
            raise LookupError(
                f"`IndirectResource.{field}` {name!r} matches no stored resource "
                f"(at {iterated.path}.{field})"
            )
