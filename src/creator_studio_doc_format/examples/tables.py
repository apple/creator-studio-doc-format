# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0

"""Build a presentation with styled tables."""

from __future__ import annotations

import argparse
from pathlib import Path

from creator_studio_doc_format.core import (
    RGBA,
    AlignmentType,
    BodyStrokeProperties,
    CanvasObject,
    Cell,
    CellProperties,
    CharacterProperties,
    Color,
    ColumnHeader,
    Fill,
    Geometry,
    HeaderFooterStrokeProperties,
    Insets,
    KeyxDocument,
    Label,
    Line,
    OverallProperties,
    ParagraphProperties,
    Position,
    Presentation,
    Preset,
    Row,
    Size,
    Slide,
    SlideBackground,
    SlideObject,
    Stroke,
    Table,
    Text,
    VerticalAlignmentType,
    VisualProperties,
)
from creator_studio_doc_format.validation import validate_document

_RGBA_GRID = RGBA(red=0.82, green=0.83, blue=0.86)
_RGBA_HEADER_BG = RGBA(red=0.94, green=0.94, blue=0.96)
_RGBA_BORDER = RGBA(red=0.75, green=0.76, blue=0.80)
_RGBA_POSITIVE = RGBA(red=0.80, green=0.92, blue=0.82)
_RGBA_NEGATIVE = RGBA(red=0.98, green=0.85, blue=0.85)
_RGBA_ALT_ROW = RGBA(red=0.95, green=0.95, blue=0.97)
_RGBA_WHITE = RGBA(red=1.0, green=1.0, blue=1.0)

# Each stroke's width and color live in its preset, built from these definitions.
_STROKES = {
    "stroke_grid": Stroke(line=Line(color=Color(rgba=_RGBA_GRID), width=0.5)),
    "stroke_border": Stroke(line=Line(color=Color(rgba=_RGBA_BORDER), width=1.0)),
    "stroke_separator": Stroke(line=Line(color=Color(rgba=_RGBA_BORDER), width=1.5)),
}
_STROKE_GRID = Stroke(preset_identifier="stroke_grid")
_STROKE_BORDER = Stroke(preset_identifier="stroke_border")
_STROKE_SEPARATOR = Stroke(preset_identifier="stroke_separator")


def _presets() -> list[Preset]:
    """Returns the strokes and fills the slides reference by identifier."""
    return [
        *(
            Preset(
                identifier=name,
                # A preset holds only the properties of a `Stroke`, so the dump leaves
                # out `type_identifier` and `version`.
                properties=stroke.model_dump(
                    mode="json", exclude={"type_identifier", "version"}
                ),
            )
            for name, stroke in _STROKES.items()
        ),
        *(
            Preset(
                identifier=name,
                properties={"color": {"rgba": rgba.model_dump(mode="json")}},
            )
            for name, rgba in [
                ("fill_header_bg", _RGBA_HEADER_BG),
                ("fill_alt_row", _RGBA_ALT_ROW),
                ("fill_positive", _RGBA_POSITIVE),
                ("fill_negative", _RGBA_NEGATIVE),
                ("fill_slide_bg", _RGBA_WHITE),
            ]
        ),
    ]


_CELL_HEADER = CellProperties(
    fill=Fill(preset_identifier="fill_header_bg"),
    vertical_alignment=VerticalAlignmentType.CENTER,
    padding=Insets(top=8, bottom=8, left=12, right=12),
)
_CELL_BODY = CellProperties(
    vertical_alignment=VerticalAlignmentType.CENTER,
    padding=Insets(top=8, bottom=8, left=12, right=12),
)
_TEXT_HEADER = ParagraphProperties(
    alignment=AlignmentType.CENTER,
    character_properties=CharacterProperties(font_size=32, bold=True),
)
_TEXT_BODY = ParagraphProperties(
    character_properties=CharacterProperties(font_size=32),
)
_TEXT_BODY_CENTER = ParagraphProperties(
    alignment=AlignmentType.CENTER,
    character_properties=CharacterProperties(font_size=32),
)


def _slide_1_basics() -> Slide:
    """Builds a slide with a header row, alternating rows, and a ``Label`` title."""
    visual = VisualProperties(
        overall_properties=OverallProperties(
            has_alternating_rows=True,
            alternating_rows_fill=Fill(preset_identifier="fill_alt_row"),
        ),
        body_stroke_properties=BodyStrokeProperties(
            horizontal_stroke=_STROKE_GRID,
            vertical_stroke=_STROKE_GRID,
            horizontal_border_stroke=_STROKE_BORDER,
            vertical_border_stroke=_STROKE_BORDER,
        ),
        header_row_cell_properties=_CELL_HEADER,
        header_row_text_properties=_TEXT_HEADER,
        header_row_stroke_properties=HeaderFooterStrokeProperties(
            separator_stroke=_STROKE_SEPARATOR,
            separator_visible=True,
        ),
        body_cell_properties=_CELL_BODY,
        body_text_properties=_TEXT_BODY,
    )

    column_headers = [
        ColumnHeader(column_identifier="c_feature", title="Feature", column_width=400),
        ColumnHeader(column_identifier="c_owner", title="Owner", column_width=320),
        # The column sets the alignment because a cell's own `text_properties`
        # renders at a smaller size than the table's, even when it restates the
        # size.
        ColumnHeader(
            column_identifier="c_status",
            title="Status",
            column_width=280,
            text_properties=_TEXT_BODY_CENTER,
        ),
        ColumnHeader(column_identifier="c_notes", title="Notes", column_width=600),
    ]

    def _status_cell(text: str, fill_preset: str) -> Cell:
        return Cell(
            value=text,
            cell_properties=CellProperties(fill=Fill(preset_identifier=fill_preset)),
        )

    content = [
        Row(
            row_identifier="r_hdr",
            row_height=72,
            cells=[
                Cell(value="Feature"),
                Cell(value="Owner"),
                Cell(value="Status"),
                Cell(value="Notes"),
            ],
        ),
        Row(
            row_identifier="r1",
            row_height=84,
            cells=[
                Cell(value="Feature A"),
                Cell(value="Alex"),
                _status_cell("Done", "fill_positive"),
                Cell(value="Released last quarter"),
            ],
        ),
        Row(
            row_identifier="r2",
            row_height=84,
            cells=[
                Cell(value="Feature B"),
                Cell(value="Sam"),
                _status_cell("Blocked", "fill_negative"),
                Cell(value="Waiting on review"),
            ],
        ),
    ]

    table = Table(
        geometry=Geometry(
            position=Position(x=160, y=260), size=Size(width=1600, height=240)
        ),
        number_of_columns=4,
        number_of_rows=3,
        number_of_header_rows=1,
        title=Label(text=Text(string="Q4 Feature Rollout")),
        visual_properties=visual,
        column_headers=column_headers,
        content=content,
    )
    return Slide(
        contents=[SlideObject(object=CanvasObject(table=table))],
        background=SlideBackground(standard=Fill(preset_identifier="fill_slide_bg")),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.partition("\n")[0])
    parser.add_argument("output", type=Path, nargs="?", default=Path("tmp/tables.keyx"))
    args = parser.parse_args()

    doc = KeyxDocument(
        payload=Presentation(
            slide_size=Size(width=1920, height=1080),
            slides=[
                _slide_1_basics(),
            ],
        ),
        presets=_presets(),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(args.output, pre_save_hooks=[validate_document])
    print(f"wrote {args.output} ({args.output.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
