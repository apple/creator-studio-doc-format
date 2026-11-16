# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


from creator_studio_doc_format.core import Chart, ColumnChart, TwoAxisChart
from creator_studio_doc_format.validation._cases import unwrap_primary_case


def test_unwrap_primary_case_lone_case() -> None:
    name, model = unwrap_primary_case(Chart(column=ColumnChart()))
    assert name == "column"
    assert isinstance(model, ColumnChart)


def test_unwrap_primary_case_prefers_primary_over_declaration_order() -> None:
    chart = Chart.union_of("two_axis", column=ColumnChart(), two_axis=TwoAxisChart())
    name, model = unwrap_primary_case(chart)
    assert name == "two_axis"
    assert isinstance(model, TwoAxisChart)
