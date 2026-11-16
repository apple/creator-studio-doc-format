# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0

"""Build a presentation with a financial table: cell formats, formulas, and merges.

Styling is minimal, so the file stays focused on how the computation works.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from creator_studio_doc_format.core import (
    RGBA,
    AlignmentType,
    CanvasObject,
    Cell,
    CellFormat,
    CellProperties,
    CellRange,
    CellReference,
    CharacterProperties,
    ColumnHeader,
    CurrencyFormat,
    Fill,
    Formula,
    Geometry,
    IdBasedFormula,
    KeyxDocument,
    Label,
    NumberFormat,
    OverallProperties,
    ParagraphProperties,
    Position,
    Presentation,
    Preset,
    Row,
    RowColumnIdRange,
    Size,
    Slide,
    SlideObject,
    Table,
    Text,
    UnformattedValue,
    VisualProperties,
)
from creator_studio_doc_format.validation import validate_document

_RGBA_ALT_ROW = RGBA(red=0.95, green=0.95, blue=0.97)

_CURRENCY_FORMAT = CellFormat(
    format_type="currency",
    currency_format=CurrencyFormat(
        decimal_places=2, use_thousands_separator=True, currency_code="USD"
    ),
)
_PERCENT_FORMAT = CellFormat(
    format_type="percentage",
    number_format=NumberFormat(decimal_places=1),
)


def _valued(display: str, number: float, cell_format: CellFormat) -> Cell:
    """Returns a cell that pairs a formatted display string with its numeric source.

    The cell's ``CellFormat`` drives rendering, so the source is a raw number.
    Currency passes the amount, such as ``120_000.0``, and percentage passes the
    fraction, such as ``0.30`` for 30 percent.
    """
    return Cell(
        value=display,
        unformatted_value=UnformattedValue(number=number),
        cell_format=cell_format,
    )


def _slide_1_formats_formulas_merges() -> Slide:
    """Builds a slide with cell formats, a formula by identifier, and a merged
    banner.
    """
    visual = VisualProperties(
        overall_properties=OverallProperties(behaves_like_spreadsheet=True),
        footer_row_cell_properties=CellProperties(
            fill=Fill(preset_identifier="fill_alt_row")
        ),
    )

    column_headers = [
        # Column widths take precedence over `geometry.size.width`, so they sum to the
        # table width.
        ColumnHeader(
            column_identifier="c_category", title="Category", column_width=640
        ),
        ColumnHeader(column_identifier="c_spend", title="Spend", column_width=480),
        ColumnHeader(column_identifier="c_pct", title="% of Budget", column_width=480),
    ]

    content = [
        Row(
            row_identifier="r_hdr",
            row_height=60,
            cells=[Cell(value=c.title or "") for c in column_headers],
        ),
        Row(
            row_identifier="r_ads",
            row_height=68,
            cells=[
                Cell(value="Ads"),
                _valued("$120,000.00", 120_000.0, _CURRENCY_FORMAT),
                _valued("30.0%", 0.30, _PERCENT_FORMAT),
            ],
        ),
        Row(
            row_identifier="r_events",
            row_height=68,
            cells=[
                Cell(value="Events"),
                _valued("$60,000.00", 60_000.0, _CURRENCY_FORMAT),
                _valued("15.0%", 0.15, _PERCENT_FORMAT),
            ],
        ),
        # The banner row. The merge below spans its first two columns, with the content
        # in the top-left cell and the other merged cells blank.
        Row(
            row_identifier="r_sub",
            row_height=56,
            cells=[
                Cell(
                    value="Marketing subtotal (see footer)",
                    cell_properties=CellProperties(
                        fill=Fill(preset_identifier="fill_alt_row")
                    ),
                    # Replaces the table's text style rather than merging with it,
                    # so it restates the size. The cell can still render smaller
                    # than the rest of the table. A column's `text_properties`,
                    # as in `tables.py`, keeps the size.
                    text_properties=ParagraphProperties(
                        alignment=AlignmentType.CENTER,
                        character_properties=CharacterProperties(font_size=32),
                    ),
                ),
                Cell(value=""),
                Cell(value=""),
            ],
        ),
        # Footer: `SUM` by identifier over the `"c_spend"` column of the two body rows.
        Row(
            row_identifier="r_total",
            row_height=68,
            cells=[
                Cell(value="TOTAL"),
                Cell(
                    value="$180,000.00",
                    unformatted_value=UnformattedValue(number=180_000.0),
                    cell_format=_CURRENCY_FORMAT,
                    # References resolve against `row_identifier` and
                    # `column_identifier`.
                    formula=Formula(
                        id_based=IdBasedFormula(
                            expression="=SUM({ref0})",
                            references=[
                                CellReference(
                                    placeholder="{ref0}",
                                    display_notation="B2:B3",
                                    start_row_identifier="r_ads",
                                    start_column_identifier="c_spend",
                                    end_row_identifier="r_events",
                                    end_column_identifier="c_spend",
                                )
                            ],
                        )
                    ),
                ),
                Cell(value=""),
            ],
        ),
    ]

    # `CellRange` uses the identifiers from `content` and `column_headers`.
    merges = [
        CellRange(
            row_column_id_range=RowColumnIdRange(
                top_left_row_identifier="r_sub",
                top_left_column_identifier="c_category",
                bottom_right_row_identifier="r_sub",
                bottom_right_column_identifier="c_spend",
            )
        )
    ]

    table = Table(
        geometry=Geometry(
            position=Position(x=160, y=200), size=Size(width=1600, height=400)
        ),
        number_of_columns=3,
        number_of_rows=5,
        number_of_header_rows=1,
        number_of_footer_rows=1,
        title=Label(text=Text(string="Q4 Marketing Budget")),
        visual_properties=visual,
        column_headers=column_headers,
        content=content,
        merges=merges,
    )
    return Slide(contents=[SlideObject(object=CanvasObject(table=table))])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.partition("\n")[0])
    parser.add_argument(
        "output", type=Path, nargs="?", default=Path("tmp/spreadsheets.keyx")
    )
    args = parser.parse_args()

    doc = KeyxDocument(
        payload=Presentation(
            slide_size=Size(width=1920, height=1080),
            slides=[_slide_1_formats_formulas_merges()],
        ),
        presets=[
            Preset(
                identifier="fill_alt_row",
                properties={"color": {"rgba": _RGBA_ALT_ROW.model_dump(mode="json")}},
            )
        ],
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(args.output, pre_save_hooks=[validate_document])
    print(f"wrote {args.output} ({args.output.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
