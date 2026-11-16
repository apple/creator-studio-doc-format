# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


from typing import TYPE_CHECKING

from creator_studio_doc_format.core import Chart, TwoAxisChart

from ._cases import unwrap_primary_case

if TYPE_CHECKING:
    from creator_studio_doc_format.navigation import IteratedModel

    from ._model_tree import _IterationState


class ChartValidator:
    def visit(self, state: "_IterationState", iterated: "IteratedModel") -> None:
        if isinstance(iterated.model, Chart):
            _validate_chart(iterated.model, iterated.path)

    def finalize(self, state: "_IterationState") -> None:
        return


def _validate_chart(chart: Chart, path: str) -> None:
    case_name, model = unwrap_primary_case(chart)
    if not isinstance(model, TwoAxisChart):
        return
    for i, series in enumerate(model.series or []):
        selection = series.y_axis_selection
        if selection is not None and selection not in (0, 1):
            raise ValueError(
                f"`ChartSeries.y_axis_selection` {selection!r} isn't 0 or 1 "
                f"(at {path}.{case_name}.series[{i}].y_axis_selection)"
            )
