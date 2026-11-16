# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


import pytest

from creator_studio_doc_format.core import (
    Chart,
    ChartSeries,
    ColumnChart,
    MixedChart,
    TwoAxisChart,
)
from creator_studio_doc_format.validation import validate_document

from .builders import doc_with_chart


def _two_axis(*series: ChartSeries) -> Chart:
    return Chart(two_axis=TwoAxisChart(series=list(series)))


def _column(*series: ChartSeries) -> Chart:
    return Chart(column=ColumnChart(series=list(series)))


def _mixed(*series: ChartSeries) -> Chart:
    return Chart(mixed=MixedChart(series=list(series)))


def test_validate_detects_y_axis_selection_out_of_range() -> None:
    doc = doc_with_chart(
        _two_axis(
            ChartSeries(series_index=0, y_axis_selection=0),
            ChartSeries(series_index=1, y_axis_selection=999),
        )
    )
    with pytest.raises(ValueError, match="isn't 0 or 1"):
        validate_document(doc)


def test_two_axis_selection_0_and_1_ok() -> None:
    doc = doc_with_chart(
        _two_axis(
            ChartSeries(series_index=0, y_axis_selection=0),
            ChartSeries(series_index=1, y_axis_selection=1),
        )
    )
    validate_document(doc)


def test_two_axis_selection_none_ok() -> None:
    doc = doc_with_chart(_two_axis(ChartSeries(series_index=0)))
    validate_document(doc)


def test_two_axis_selection_negative_out_of_range() -> None:
    doc = doc_with_chart(_two_axis(ChartSeries(series_index=0, y_axis_selection=-1)))
    with pytest.raises(ValueError, match="isn't 0 or 1"):
        validate_document(doc)


def test_non_two_axis_selection_is_not_checked() -> None:
    doc = doc_with_chart(_column(ChartSeries(series_index=0, y_axis_selection=999)))
    validate_document(doc)


def test_mixed_chart_y_axis_selection_is_not_checked() -> None:
    doc = doc_with_chart(_mixed(ChartSeries(series_index=0, y_axis_selection=999)))
    validate_document(doc)
