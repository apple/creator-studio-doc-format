# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0

"""Build a presentation with a mixed chart, a pie chart, and a scatter chart.

The 26 cases of `Chart` fall into three axis arrangements. Switching between cases
in one arrangement changes one token. Switching arrangements changes the axis fields:

  - Bar, column, line, and area charts are cartesian. They use `category_axis` and
    `value_axis`, plus an optional `value_axis_secondary`.
  - Scatter and bubble charts use `value_axis_x` and `value_axis_y`, with no category
    axis.
  - Pie and donut charts are circular, with no axes at all.

The example builds one canonical chart per arrangement. `MixedChart` is cartesian, with
mixed series types on one frame. `PieChart` is circular, and `ScatterChart` has two
value axes.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from creator_studio_doc_format.core import (
    RGBA,
    CanvasObject,
    CharacterProperties,
    Chart,
    ChartCategoryAxis,
    ChartData,
    ChartDataRow,
    ChartDataSource,
    ChartDataValue,
    ChartLegend,
    ChartSeries,
    ChartValueAxis,
    Color,
    Fill,
    Geometry,
    KeyxDocument,
    Label,
    Line,
    MixedChart,
    MixedSeriesType,
    ParagraphProperties,
    PieChart,
    PlotDirection,
    Position,
    Presentation,
    Preset,
    ScatterChart,
    SeriesSymbolType,
    Shape,
    Size,
    Slide,
    SlideObject,
    Stroke,
    Text,
)
from creator_studio_doc_format.validation import validate_document

_RGBA_BRAND_BLUE = RGBA(red=0.12, green=0.45, blue=0.82)
_RGBA_BRAND_ORANGE = RGBA(red=0.94, green=0.55, blue=0.20)
_RGBA_BRAND_TEAL = RGBA(red=0.20, green=0.65, blue=0.62)

# Series reference these fills through presets, so editing a preset recolors every
# series that uses it.
BRAND_BLUE = Fill(preset_identifier="fill_brand_blue")
BRAND_ORANGE = Fill(preset_identifier="fill_brand_orange")
BRAND_TEAL = Fill(preset_identifier="fill_brand_teal")

QUARTERS = ["Q1 2026", "Q2 2026"]


def _rows(values: list[list[float]]) -> list[ChartDataRow]:
    """Wraps a 2D array of numbers in ``ChartDataRow`` and ``ChartDataValue`` models."""
    return [
        ChartDataRow(values=[ChartDataValue(number=v) for v in row]) for row in values
    ]


# One geometry for all three chart slides.
# A chart's `Geometry` is its plot area. The axis labels, axis titles, chart title, and
# legend draw outside it, so a frame near a slide edge pushes them off the slide.
# With 32 to 40 pt axis text, leave about 150 pt on the left, 120 pt below, 135 pt
# above, and 20 to 30 pt on the right. Scale those margins with the text size.
CHART_FRAME = Geometry(
    position=Position(x=200, y=220),
    size=Size(width=1520, height=620),
)


def _text_style(font_size: float) -> ParagraphProperties:
    return ParagraphProperties(
        character_properties=CharacterProperties(font_size=font_size)
    )


# Text sizes that stay legible on a 1920 x 1080 slide.
TITLE_STYLE = _text_style(48)
SECONDARY_TEXT_STYLE = _text_style(40)  # Captions and axis titles.
AXIS_LABEL_STYLE = _text_style(32)
SMALL_TEXT_STYLE = _text_style(32)  # The legend and value labels.


def _mixed_chart() -> SlideObject:
    """Builds a cartesian chart with two column series and a line series."""
    data = ChartData(
        chart_data_source=ChartDataSource.CHART_DATA_GRID,
        column_labels=QUARTERS,
        row_labels=["Bakery", "Café", "Catering"],
        rows=_rows(
            [
                [42.1, 48.3],
                [38.5, 41.0],
                [12.4, 15.9],
            ]
        ),
    )
    bakery = ChartSeries(
        mixed_series_type=MixedSeriesType.COLUMN,
        fill=BRAND_BLUE,
    )
    cafe = ChartSeries(
        mixed_series_type=MixedSeriesType.COLUMN,
        fill=BRAND_ORANGE,
    )
    catering = ChartSeries(
        mixed_series_type=MixedSeriesType.LINE,
        fill=BRAND_TEAL,
        symbol_type=SeriesSymbolType.CIRCLE,
        symbol_size=8,
    )
    chart = MixedChart(
        title=Label(
            text=Text(string="Quarterly revenue by product ($M)"),
            paragraph_properties=TITLE_STYLE,
        ),
        caption=Label(
            text=Text(
                string="FY2026 outlook: the bakery leads, and catering is gaining momentum."
            ),
            paragraph_properties=SECONDARY_TEXT_STYLE,
        ),
        data=data,
        series=[bakery, cafe, catering],
        category_axis=ChartCategoryAxis(
            title="Quarter",
            show_title=True,
            title_text_style=SECONDARY_TEXT_STYLE,
            label_text_style=AXIS_LABEL_STYLE,
        ),
        value_axis=ChartValueAxis(
            title="Revenue ($M)",
            show_title=True,
            title_text_style=SECONDARY_TEXT_STYLE,
            label_text_style=AXIS_LABEL_STYLE,
        ),
        legend=ChartLegend(label_text_style=SMALL_TEXT_STYLE),
        geometry=CHART_FRAME,
    )
    return SlideObject(object=CanvasObject(chart=Chart(mixed=chart)))


def _pie_chart() -> SlideObject:
    """Builds a pie chart, which has no axes.

    With ``plot_direction=COLUMNS_AS_SERIES``, each column is a wedge and
    ``series[i].fill`` colors wedge ``i``. The data is one row, and its values line
    up with ``column_labels`` and ``series``.
    """
    wedges = [
        ("Bakery", 34.2, BRAND_BLUE),
        ("Café", 28.1, BRAND_ORANGE),
        ("Catering", 22.7, BRAND_TEAL),
    ]
    data = ChartData(
        chart_data_source=ChartDataSource.CHART_DATA_GRID,
        plot_direction=PlotDirection.COLUMNS_AS_SERIES,
        column_labels=[name for name, _, _ in wedges],
        row_labels=["Market share"],
        rows=[ChartDataRow(values=[ChartDataValue(number=v) for _, v, _ in wedges])],
    )
    series = [
        ChartSeries(
            fill=fill,
            value_label_text_style=SMALL_TEXT_STYLE,
        )
        for _, _, fill in wedges
    ]
    chart = PieChart(
        title=Label(
            text=Text(string="Category market share (Q4)"),
            paragraph_properties=TITLE_STYLE,
        ),
        caption=Label(
            text=Text(
                string="The bakery remains dominant, and catering is narrowing the gap."
            ),
            paragraph_properties=SECONDARY_TEXT_STYLE,
        ),
        data=data,
        series=series,
        legend=ChartLegend(label_text_style=SMALL_TEXT_STYLE),
        geometry=CHART_FRAME,
    )
    return SlideObject(object=CanvasObject(chart=Chart(pie=chart)))


def _scatter_chart() -> SlideObject:
    """Builds a scatter chart, which has an x and a y value axis and no category axis.

    With ``plot_direction=COLUMNS_AS_SERIES`` and ``shared_xvalues=True``, each row
    is one data point. Column 0 holds the shared X, and columns 1..K hold Y for
    each of the K series. Bubble charts use the same layout, with each series taking
    a size column after its Y column. A bubble's size comes from that value, not
    ``symbol_size``.
    """
    points = [
        (8.0, 18.5),
        (21.0, 30.1),
        (33.0, 44.3),
    ]
    data = ChartData(
        chart_data_source=ChartDataSource.CHART_DATA_GRID,
        plot_direction=PlotDirection.COLUMNS_AS_SERIES,
        shared_xvalues=True,
        column_labels=["Ad spend", "Revenue"],
        rows=[
            ChartDataRow(values=[ChartDataValue(number=x), ChartDataValue(number=y)])
            for x, y in points
        ],
    )
    campaign = ChartSeries(
        fill=BRAND_TEAL,
        symbol_type=SeriesSymbolType.CIRCLE,
        symbol_size=12,
    )
    chart = ScatterChart(
        title=Label(
            text=Text(string="Revenue versus ad spend"),
            paragraph_properties=TITLE_STYLE,
        ),
        caption=Label(
            text=Text(string="Positive correlation across recent campaigns."),
            paragraph_properties=SECONDARY_TEXT_STYLE,
        ),
        data=data,
        series=[campaign],
        value_axis_x=ChartValueAxis(
            title="Ad spend ($M)",
            show_title=True,
            title_text_style=SECONDARY_TEXT_STYLE,
            label_text_style=AXIS_LABEL_STYLE,
        ),
        value_axis_y=ChartValueAxis(
            title="Revenue ($M)",
            show_title=True,
            title_text_style=SECONDARY_TEXT_STYLE,
            label_text_style=AXIS_LABEL_STYLE,
        ),
        legend=ChartLegend(label_text_style=SMALL_TEXT_STYLE),
        geometry=CHART_FRAME,
    )
    return SlideObject(object=CanvasObject(chart=Chart(scatter=chart)))


def _border(frame: Geometry) -> SlideObject:
    """Builds a rectangular frame with no fill.

    Chart classes don't expose a border field, so a ``Shape`` with a thin line at the
    same geometry acts as one.
    """
    border = Shape(
        geometry=frame,
        stroke=Stroke(
            line=Line(
                color=Color(rgba=RGBA(red=0.75, green=0.75, blue=0.78)), width=1.5
            )
        ),
    )
    return SlideObject(object=CanvasObject(shape=border))


def _presets() -> list[Preset]:
    return [
        Preset(
            identifier=fill.preset_identifier,
            properties={"color": {"rgba": rgba.model_dump(mode="json")}},
        )
        for fill, rgba in [
            (BRAND_BLUE, _RGBA_BRAND_BLUE),
            (BRAND_ORANGE, _RGBA_BRAND_ORANGE),
            (BRAND_TEAL, _RGBA_BRAND_TEAL),
        ]
    ]


def _slides() -> list[Slide]:
    return [
        Slide(contents=[_mixed_chart()]),
        Slide(contents=[_border(CHART_FRAME), _pie_chart()]),
        Slide(contents=[_scatter_chart()]),
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.partition("\n")[0])
    parser.add_argument("output", type=Path, nargs="?", default=Path("tmp/charts.keyx"))
    args = parser.parse_args()

    doc = KeyxDocument(
        payload=Presentation(
            slide_size=Size(width=1920, height=1080),
            slides=_slides(),
        ),
        presets=_presets(),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(args.output, pre_save_hooks=[validate_document])
    print(f"wrote {args.output} ({args.output.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
