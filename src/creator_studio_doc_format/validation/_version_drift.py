# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


import warnings

from pydantic import BaseModel

import creator_studio_doc_format
from creator_studio_doc_format.core import TaggedUnionModel
from creator_studio_doc_format.navigation import iterate_models


class DocumentVersionWarning(UserWarning):
    """A warning about a union case this version of the library doesn't implement.

    A newer version of the app can write a value as several cases at once. The new
    case is the primary, and an older case is a fallback for readers that predate it.
    This version of the library doesn't implement the primary, so ``union_primary`` and
    ``union_cases`` return the fallback, which can be a different kind of value. A save
    still writes the primary back.

    ``validate_document`` issues the warning. Catch it to detect that a document was
    read through a fallback. The message names the primary and the fallback. By default,
    the ``warnings`` module shows a warning once per call site, so checking many
    documents from one line needs the ``"always"`` action.
    """


def validate_version_drift(payload: BaseModel) -> None:
    for iterated in iterate_models(payload):
        model = iterated.model
        if not isinstance(model, TaggedUnionModel):
            continue
        primary = model._primary
        if primary is None:
            continue
        known_cases = {item for item, _added, _valueless in type(model).__wire_cases__}
        if primary in known_cases:
            continue
        fallback = model.union_primary_name()
        reads = "no case" if fallback is None else repr(fallback)
        warnings.warn(
            f"`{type(model).__name__}` primary case {primary!r} isn't implemented "
            f"in this version of the library "
            f"({creator_studio_doc_format.__version__}), so "
            f"`union_primary` reads {reads} instead "
            f"(at {iterated.path or '<root>'}). Upgrade "
            f"`creator_studio_doc_format` to read and validate it.",
            DocumentVersionWarning,
            stacklevel=3,
        )
