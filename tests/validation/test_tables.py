# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


import pytest

from creator_studio_doc_format.core import (
    Cell,
    CellFormat,
    CellRange,
    CellReference,
    ColumnHeader,
    ConditionalStyleSet,
    CustomFormat,
    Formula,
    IdBasedFormula,
    Predicate,
    Row,
    RowColumnIdRange,
    Table,
    TableConditionalStyleSetRule,
    TransformationInfo,
)
from creator_studio_doc_format.validation import validate_document

from .builders import doc_with_tables


def _rule() -> TableConditionalStyleSetRule:
    return TableConditionalStyleSetRule(
        predicate=Predicate(predicate_type="duplicates")
    )


def _merged_table(merge: CellRange) -> Table:
    return Table(
        number_of_columns=2,
        number_of_rows=2,
        column_headers=[
            ColumnHeader(column_identifier="c1"),
            ColumnHeader(column_identifier="c2"),
        ],
        content=[Row(row_identifier="r1"), Row(row_identifier="r2")],
        merges=[merge],
    )


def _table_with_reference(ref: CellReference) -> Table:
    formula = Formula(id_based=IdBasedFormula(expression="={ref0}", references=[ref]))
    return Table(
        number_of_columns=2,
        number_of_rows=2,
        column_headers=[
            ColumnHeader(column_identifier="c1"),
            ColumnHeader(column_identifier="c2"),
        ],
        content=[
            Row(row_identifier="r1", cells=[Cell(value="a", formula=formula)]),
            Row(row_identifier="r2"),
        ],
    )


def test_validate_detects_duplicate_column_identifier() -> None:
    doc = doc_with_tables(
        Table(
            number_of_columns=2,
            number_of_rows=1,
            column_headers=[
                ColumnHeader(column_identifier="dup"),
                ColumnHeader(column_identifier="dup"),
            ],
            content=[Row(cells=[Cell(value="a"), Cell(value="b")])],
        )
    )
    with pytest.raises(
        ValueError, match=r"`ColumnHeader.column_identifier` .* is a duplicate"
    ):
        validate_document(doc)


def test_validate_detects_duplicate_row_identifier() -> None:
    doc = doc_with_tables(
        Table(
            number_of_columns=1,
            number_of_rows=2,
            content=[Row(row_identifier="dup"), Row(row_identifier="dup")],
        )
    )
    with pytest.raises(ValueError, match=r"`Row.row_identifier` .* is a duplicate"):
        validate_document(doc)


def test_validate_detects_duplicate_custom_format_identifier() -> None:
    doc = doc_with_tables(
        Table(
            number_of_columns=1,
            number_of_rows=1,
            content=[Row(cells=[Cell(value="a")])],
            custom_formats=[
                CustomFormat(identifier="dup", format_string="#"),
                CustomFormat(identifier="dup", format_string="0"),
            ],
        )
    )
    with pytest.raises(
        ValueError, match=r"`CustomFormat.identifier` .* is a duplicate"
    ):
        validate_document(doc)


def test_validate_detects_duplicate_conditional_style_set_identifier() -> None:
    doc = doc_with_tables(
        Table(
            number_of_columns=1,
            number_of_rows=1,
            content=[Row(cells=[Cell(value="a")])],
            conditional_style_sets=[
                ConditionalStyleSet(identifier="dup", rules=[_rule()]),
                ConditionalStyleSet(identifier="dup", rules=[_rule()]),
            ],
        )
    )
    with pytest.raises(
        ValueError, match=r"`ConditionalStyleSet.identifier` .* is a duplicate"
    ):
        validate_document(doc)


def test_validate_allows_none_identifiers_and_distinct_identifiers() -> None:
    doc = doc_with_tables(
        Table(
            number_of_columns=2,
            number_of_rows=2,
            column_headers=[
                ColumnHeader(column_identifier="a"),
                ColumnHeader(column_identifier=None),
            ],
            content=[Row(row_identifier=None), Row(row_identifier="r1")],
        )
    )
    validate_document(doc)


def test_validate_cell_conditional_style_set_identifier_resolves() -> None:
    doc = doc_with_tables(
        Table(
            number_of_columns=1,
            number_of_rows=1,
            content=[
                Row(cells=[Cell(value="a", conditional_style_set_identifier="cs1")])
            ],
            conditional_style_sets=[
                ConditionalStyleSet(identifier="cs1", rules=[_rule()])
            ],
        )
    )
    validate_document(doc)


def test_validate_cell_conditional_style_set_identifier_dangling_raises() -> None:
    doc = doc_with_tables(
        Table(
            number_of_columns=1,
            number_of_rows=1,
            content=[
                Row(cells=[Cell(value="a", conditional_style_set_identifier="ghost")])
            ],
            conditional_style_sets=[
                ConditionalStyleSet(identifier="cs1", rules=[_rule()])
            ],
        )
    )
    with pytest.raises(LookupError, match="ghost"):
        validate_document(doc)


def test_validate_custom_format_identifier_dangling_raises() -> None:
    doc = doc_with_tables(
        Table(
            number_of_columns=1,
            number_of_rows=1,
            content=[
                Row(
                    cells=[
                        Cell(
                            value="42",
                            cell_format=CellFormat(
                                format_type="custom",
                                custom_format_identifier="format-that-never-was",
                            ),
                        )
                    ]
                )
            ],
            custom_formats=None,
        )
    )
    with pytest.raises(LookupError, match="format-that-never-was"):
        validate_document(doc)


def test_validate_custom_format_identifier_resolves() -> None:
    doc = doc_with_tables(
        Table(
            number_of_columns=1,
            number_of_rows=1,
            content=[
                Row(
                    cells=[
                        Cell(
                            value="42",
                            cell_format=CellFormat(
                                format_type="custom", custom_format_identifier="fmt1"
                            ),
                        )
                    ]
                )
            ],
            custom_formats=[CustomFormat(identifier="fmt1", format_string="#")],
        )
    )
    validate_document(doc)


def test_validate_custom_format_identifier_on_non_custom_format_is_not_checked() -> (
    None
):
    doc = doc_with_tables(
        Table(
            number_of_columns=1,
            number_of_rows=1,
            content=[
                Row(
                    cells=[
                        Cell(
                            value="42",
                            cell_format=CellFormat(
                                format_type="number", custom_format_identifier="dropped"
                            ),
                        )
                    ]
                )
            ],
            custom_formats=None,
        )
    )
    validate_document(doc)


def test_validate_merged_range_resolves() -> None:
    merge = CellRange(
        row_column_id_range=RowColumnIdRange(
            top_left_row_identifier="r1",
            top_left_column_identifier="c1",
            bottom_right_row_identifier="r2",
            bottom_right_column_identifier="c2",
        )
    )
    validate_document(doc_with_tables(_merged_table(merge)))


def test_validate_merged_range_dangling_row_identifier_raises() -> None:
    merge = CellRange(
        row_column_id_range=RowColumnIdRange(
            top_left_row_identifier="r1",
            top_left_column_identifier="c1",
            bottom_right_row_identifier="ghost-row",
            bottom_right_column_identifier="c2",
        )
    )
    with pytest.raises(LookupError, match="ghost-row"):
        validate_document(doc_with_tables(_merged_table(merge)))


def test_validate_merged_range_dangling_column_identifier_raises() -> None:
    merge = CellRange(
        row_column_id_range=RowColumnIdRange(
            top_left_row_identifier="r1",
            top_left_column_identifier="ghost-col",
            bottom_right_row_identifier="r2",
            bottom_right_column_identifier="c2",
        )
    )
    with pytest.raises(LookupError, match="ghost-col"):
        validate_document(doc_with_tables(_merged_table(merge)))


def test_validate_merged_range_rejects_swapped_row_order() -> None:
    merge = CellRange(
        row_column_id_range=RowColumnIdRange(
            top_left_row_identifier="r2",
            top_left_column_identifier="c1",
            bottom_right_row_identifier="r1",
            bottom_right_column_identifier="c2",
        )
    )
    with pytest.raises(ValueError, match="sits after its bottom-right corner"):
        validate_document(doc_with_tables(_merged_table(merge)))


def test_validate_merged_range_rejects_swapped_column_order() -> None:
    merge = CellRange(
        row_column_id_range=RowColumnIdRange(
            top_left_row_identifier="r1",
            top_left_column_identifier="c2",
            bottom_right_row_identifier="r2",
            bottom_right_column_identifier="c1",
        )
    )
    with pytest.raises(ValueError, match="sits after its bottom-right corner"):
        validate_document(doc_with_tables(_merged_table(merge)))


def test_validate_base_table_is_not_validated() -> None:
    base = Table(
        number_of_columns=2,
        number_of_rows=1,
        column_headers=[
            ColumnHeader(column_identifier="dup"),
            ColumnHeader(column_identifier="dup"),
        ],
        content=[Row(row_identifier="br1")],
    )
    top = Table(
        number_of_columns=1,
        number_of_rows=1,
        content=[Row(row_identifier="tr1")],
        transformation=TransformationInfo(base_table=base),
    )
    validate_document(doc_with_tables(top))


def test_validate_rejects_out_of_range_row_index() -> None:
    doc = doc_with_tables(
        Table(
            number_of_columns=1,
            number_of_rows=2,
            content=[Row(row_index=5, row_identifier="r1")],
        )
    )
    with pytest.raises(ValueError, match="row_index` 5 is out of range"):
        validate_document(doc)


def test_validate_rejects_reversed_row_index() -> None:
    doc = doc_with_tables(
        Table(
            number_of_columns=1,
            number_of_rows=3,
            content=[
                Row(row_index=2, row_identifier="r1"),
                Row(row_index=1, row_identifier="r2"),
            ],
        )
    )
    with pytest.raises(ValueError, match="strictly ascending"):
        validate_document(doc)


def test_validate_rejects_duplicate_row_index() -> None:
    doc = doc_with_tables(
        Table(
            number_of_columns=1,
            number_of_rows=3,
            content=[
                Row(row_index=1, row_identifier="r1"),
                Row(row_index=1, row_identifier="r2"),
            ],
        )
    )
    with pytest.raises(ValueError, match="strictly ascending"):
        validate_document(doc)


def test_validate_allows_sparse_ascending_row_index() -> None:
    doc = doc_with_tables(
        Table(
            number_of_columns=1,
            number_of_rows=10,
            content=[
                Row(row_index=0, row_identifier="r1"),
                Row(row_index=5, row_identifier="r2"),
            ],
        )
    )
    validate_document(doc)


def test_validate_rejects_out_of_range_column_index() -> None:
    doc = doc_with_tables(
        Table(
            number_of_columns=2,
            number_of_rows=1,
            content=[Row(cells=[Cell(value="a", column_index=5)])],
        )
    )
    with pytest.raises(ValueError, match="column_index` 5 is out of range"):
        validate_document(doc)


def test_validate_rejects_reversed_column_index() -> None:
    doc = doc_with_tables(
        Table(
            number_of_columns=3,
            number_of_rows=1,
            content=[
                Row(
                    cells=[
                        Cell(value="a", column_index=2),
                        Cell(value="b", column_index=1),
                    ]
                )
            ],
        )
    )
    with pytest.raises(ValueError, match="strictly ascending"):
        validate_document(doc)


def test_validate_allows_sparse_ascending_column_index() -> None:
    doc = doc_with_tables(
        Table(
            number_of_columns=10,
            number_of_rows=1,
            content=[
                Row(
                    cells=[
                        Cell(value="a", column_index=0),
                        Cell(value="b", column_index=4),
                    ]
                )
            ],
        )
    )
    validate_document(doc)
