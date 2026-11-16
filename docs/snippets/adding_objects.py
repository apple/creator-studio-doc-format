# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0

# [union]
from creator_studio_doc_format.core import RGBA, Color, Fill, Stroke

# `Fill.color` holds a `Color`, which is itself a union.
red = Fill(color=Color(rgba=RGBA(red=0.8, green=0.1, blue=0.1, alpha=1)))
no_border = Stroke(empty=True)  # A case with no payload takes `True`.
# [/union]

# [text]
from creator_studio_doc_format.core import (
    CanvasObject,
    CharacterProperties,
    Constituent,
    Paragraph,
    Slide,
    SlideObject,
    Text,
    Textbox,
    TextRun,
)

plain = Text(string="Stargazing Tips")
styled = Text(
    text_runs=[
        TextRun(string="Full moon", style=CharacterProperties(bold=True))
    ]
)
lines = Text(
    paragraphs=[
        Paragraph(contents=[Constituent(run=TextRun(string="First line"))]),
        Paragraph(contents=[Constituent(run=TextRun(string="Second line"))]),
    ]
)

# A content object goes on a slide inside a `SlideObject` and a `CanvasObject`.
slide = Slide(
    contents=[SlideObject(object=CanvasObject(textbox=Textbox(text=plain)))]
)
# [/text]

# [shape]
from creator_studio_doc_format.core import (
    BezierPath,
    Geometry,
    Path,
    Position,
    Rect,
    Shape,
    Size,
)

UNIT_BOX = Rect(position=Position(x=0, y=0), size=Size(width=1, height=1))
OVAL = "M 0,0.5 A 0.5,0.5 0 1 1 1,0.5 A 0.5,0.5 0 1 1 0,0.5 Z"

shape = Shape(
    identifier="oval",
    geometry=Geometry(
        position=Position(x=1000, y=200), size=Size(width=180, height=180)
    ),
    path=Path(bezier=BezierPath(path=OVAL, space=UNIT_BOX)),
)
# [/shape]

# [image]
import pathlib

from creator_studio_doc_format.core import (
    Image,
    IndirectResource,
    KeyxDocument,
    Resource,
)

doc = KeyxDocument.open("presentation.keyx")
png_bytes = pathlib.Path("cover.png").read_bytes()

name = doc.resources.unique_filename("cover.png")
doc.resources[name] = png_bytes
image = Image(
    resource=Resource(
        indirect=IndirectResource(identifier=name, filename="cover.png")
    ),
    geometry=Geometry(
        position=Position(x=160, y=120), size=Size(width=600, height=396)
    ),
)
# [/image]

# [table]
from creator_studio_doc_format.core import (
    Cell,
    ColumnHeader,
    Row,
    Table,
    UnformattedValue,
)


def revenue_cell(millions: int) -> Cell:
    return Cell(
        value=str(millions),
        unformatted_value=UnformattedValue(number=millions),
    )


table = Table(
    geometry=Geometry(
        position=Position(x=160, y=260), size=Size(width=800, height=160)
    ),
    number_of_rows=2,
    number_of_columns=2,
    column_headers=[
        ColumnHeader(column_identifier="product"),
        ColumnHeader(column_identifier="revenue"),
    ],
    content=[
        Row(
            row_identifier="coffee",
            cells=[Cell(value="Coffee"), revenue_cell(41)],
        ),
        Row(
            row_identifier="tea",
            cells=[Cell(value="Tea"), revenue_cell(12)],
        ),
    ],
)
# [/table]

# [chart]
from creator_studio_doc_format.core import (
    Chart,
    ChartData,
    ChartDataRow,
    ChartDataSource,
    ChartDataValue,
    ColumnChart,
    PlotDirection,
)

revenue = ChartData(
    chart_data_source=ChartDataSource.CHART_DATA_GRID,
    plot_direction=PlotDirection.ROWS_AS_SERIES,
    row_labels=["Coffee", "Tea"],
    column_labels=["Q1", "Q2", "Q3"],
    rows=[
        ChartDataRow(
            values=[ChartDataValue(number=n) for n in (42.1, 48.3, 51.0)]
        ),
        ChartDataRow(
            values=[ChartDataValue(number=n) for n in (38.5, 41.0, 44.2)]
        ),
    ],
)
chart = Chart(
    column=ColumnChart(
        data=revenue,
        geometry=Geometry(
            position=Position(x=160, y=200), size=Size(width=1200, height=700)
        ),
    )
)
# [/chart]


# [connection-line]
from creator_studio_doc_format.core import Anchor, ConnectionLine, End, LineEnd

arrow = ConnectionLine(
    tail=End(end_point=Position(x=450, y=290)),
    head=End(
        end_point=Position(x=1090, y=290),
        anchor=Anchor(object_id="oval"),
        line_end=LineEnd.FILLED_ARROW,
    ),
)
# [/connection-line]

# [preset]
from creator_studio_doc_format.core import Preset

doc = KeyxDocument.open("presentation.keyx")
doc.presets.extend(
    [
        Preset("body", {"font_name": "Helvetica Neue", "font_size": 24}),
        # The title inherits `font_name` from the body.
        Preset(
            "title", {"font_size": 48, "bold": True}, parent_identifier="body"
        ),
    ]
)

# A model adopts a preset through `preset_identifier`.
heading = TextRun(
    string="Baking Sourdough",
    style=CharacterProperties(preset_identifier="title"),
)
step = TextRun(
    string="Feed the starter",
    style=CharacterProperties(preset_identifier="body"),
)
# [/preset]
