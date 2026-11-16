# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0

"""Check in-place edits, presets, and references across a document before you save it.

:func:`validate_document` raises on an invalid value in a
:class:`~creator_studio_doc_format.core.Package`, naming its path, before the document
is saved.
"""

__all__ = ["DocumentVersionWarning", "validate_document"]

import json
from typing import Any

from creator_studio_doc_format.core import Package, PayloadT

from ._field_types import validate_field_types
from ._indirect_resources import validate_indirect_resources
from ._model_tree import validate_model_tree
from ._preset_graph import validate_preset_graph
from ._resolve import _resolve_properties
from ._version_drift import DocumentVersionWarning, validate_version_drift


def validate_document(
    doc: Package[PayloadT], main_json: dict[str, Any] | None = None
) -> None:
    """Checks a document and raises on the first value that breaks the format's rules.

    Unlike a model's own validation, this also checks values changed in place, values
    inherited from a preset, resource references, and references across the document.

    Args:
        doc: The document to validate.
        main_json: The JSON that ``save`` passes to a ``pre_save_hooks`` entry. When
            omitted, the function computes it from ``doc``.

    Warns:
        DocumentVersionWarning: The document holds a union case this version of the
            library doesn't implement, so it reads the case's fallback instead.

    Raises:
        LookupError: A preset, identifier, or reference doesn't resolve.
        ValueError: A resolved value violates an invariant, or the serializer can't
            encode the document when the function produces its own JSON.
        DocumentVersionError: When the function produces its own JSON, a union's only
            case comes from a preset value too new for this version of the library to
            read.
        RuntimeError: The function changed ``main_json``. This indicates a defect in
            ``validate_document``.
    """  # noqa: DOC502,DOC503 (LookupError/ValueError/DocumentVersionError come from the checks and the dump)
    validate_version_drift(doc.payload)
    validate_field_types(doc.payload)
    # Runs before the dump so that a preset cycle is reported here, not as a
    # serializer error.
    validate_preset_graph(doc.presets)
    main = doc._to_main_json() if main_json is None else main_json
    before = json.dumps(main) if main_json is not None else None
    resolved = _resolve_properties(doc, main)
    validate_indirect_resources(doc, resolved)
    validate_model_tree(resolved)
    if before is not None and json.dumps(main) != before:
        raise RuntimeError(
            "`main_json` changed during `validate_document`. This is a defect in "
            "`validate_document`."
        )
