# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


import pytest

from creator_studio_doc_format.core import Chart
from creator_studio_doc_format.validation import (
    DocumentVersionWarning,
    validate_document,
)
from creator_studio_doc_format.validation._version_drift import validate_version_drift

from .builders import doc_with_chart


def test_unknown_primary_case_warns() -> None:
    doc = doc_with_chart(
        Chart.model_validate(
            {"column": {}, "super_axis": {}, "primary_case": "super_axis"}
        )
    )
    with pytest.warns(
        DocumentVersionWarning,
        match="super_axis",
    ):
        validate_document(doc)


def test_unknown_sibling_with_known_primary_does_not_warn() -> None:
    doc = doc_with_chart(Chart.model_validate({"column": {}, "super_axis": {}}))
    validate_document(doc)


def test_clean_same_version_doc_passes() -> None:
    doc = doc_with_chart(Chart.model_validate({"column": {}}))
    validate_document(doc)


def test_no_primary_not_flagged() -> None:
    validate_version_drift(Chart.model_construct())
