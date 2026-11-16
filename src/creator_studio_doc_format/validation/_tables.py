# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING

from creator_studio_doc_format.core import (
    Cell,
    CellFormat,
    ColumnHeader,
    FormatType,
    RowColumnIdRange,
    Table,
    TransformationInfo,
)

if TYPE_CHECKING:
    from creator_studio_doc_format.navigation import IteratedModel

    from ._model_tree import _IterationState


class TableValidator:
    def visit(self, state: "_IterationState", iterated: "IteratedModel") -> None:
        model = iterated.model
        if isinstance(model, Table) and not _is_base_table(iterated):
            _validate_table(model, iterated.path)

    def finalize(self, state: "_IterationState") -> None:
        return


def _is_base_table(iterated: "IteratedModel") -> bool:
    return any(
        isinstance(ancestor, TransformationInfo) for ancestor in iterated.ancestors
    )


def _validate_table(table: Table, path: str) -> None:
    _collect_unique(
        table.column_headers,
        lambda c: c.column_identifier,
        "column_headers",
        "ColumnHeader.column_identifier",
        path,
    )
    _collect_unique(
        table.content,
        lambda r: r.row_identifier,
        "content",
        "Row.row_identifier",
        path,
    )
    custom_format_ids = _collect_unique(
        table.custom_formats,
        lambda f: f.identifier,
        "custom_formats",
        "CustomFormat.identifier",
        path,
    )
    cond_style_set_ids = _collect_unique(
        table.conditional_style_sets,
        lambda s: s.identifier,
        "conditional_style_sets",
        "ConditionalStyleSet.identifier",
        path,
    )

    row_indices = _validate_sparse_indices(
        table.content,
        lambda r: r.row_index,
        table.number_of_rows,
        noun="row",
        field="row_index",
        list_field="content",
        path=path,
    )

    for ri, row in enumerate(table.content or []):
        _validate_sparse_indices(
            row.cells,
            lambda c: c.column_index,
            table.number_of_columns,
            noun="cell",
            field="column_index",
            list_field="cells",
            path=f"{path}.content[{ri}]",
        )
        for ci, cell in enumerate(row.cells or []):
            cell_path = f"{path}.content[{ri}].cells[{ci}]"
            _validate_cell(
                cell,
                custom_format_ids=custom_format_ids,
                cond_style_set_ids=cond_style_set_ids,
                cell_path=cell_path,
            )

    if table.merges:
        column_order = _column_positions(table.column_headers)
        row_order = {
            row.row_identifier: index
            for row, index in zip(table.content or [], row_indices, strict=True)
            if row.row_identifier is not None
        }
        for mi, merge in enumerate(table.merges):
            merge_range = merge.row_column_id_range
            if merge_range is not None:
                _validate_merged_range(
                    merge_range, row_order, column_order, f"{path}.merges[{mi}]"
                )


def _validate_cell(
    cell: Cell,
    *,
    custom_format_ids: set[str],
    cond_style_set_ids: set[str],
    cell_path: str,
) -> None:
    csid = cell.conditional_style_set_identifier
    if csid is not None and csid not in cond_style_set_ids:
        raise LookupError(
            f"`Cell.conditional_style_set_identifier` {csid!r} matches no "
            f"`ConditionalStyleSet` (at {cell_path}.conditional_style_set_identifier)"
        )
    if cell.cell_format is not None:
        _validate_custom_format_id(
            cell.cell_format, custom_format_ids, f"{cell_path}.cell_format"
        )


def _validate_sparse_indices[T](
    items: Sequence[T] | None,
    get_index: Callable[[T], int | None],
    bound: int,
    *,
    noun: str,
    field: str,
    list_field: str,
    path: str,
) -> list[int]:
    resolved: list[int] = []
    previous = -1
    for i, item in enumerate(items or []):
        raw = get_index(item)
        index = previous + 1 if raw is None else raw
        item_path = f"{path}.{list_field}[{i}].{field}"
        if not 0 <= index < bound:
            raise ValueError(
                f"`{noun.capitalize()}.{field}` {index} is out of range "
                f"[0, {bound}) (at {item_path})"
            )
        if index <= previous:
            raise ValueError(
                f"`{noun.capitalize()}.{field}` {index} isn't greater than the "
                f"previous {noun}'s index {previous} (at {item_path}). "
                f"List {noun}s in strictly ascending order of index."
            )
        previous = index
        resolved.append(index)
    return resolved


def _collect_unique[T](
    items: Sequence[T] | None,
    get_id: Callable[[T], str | None],
    list_field: str,
    id_name: str,
    table_path: str,
) -> set[str]:
    seen: dict[str, int] = {}
    for i, item in enumerate(items or []):
        value = get_id(item)
        if value is None:
            continue
        if value in seen:
            raise ValueError(
                f"`{id_name}` {value!r} is a duplicate within the table "
                f"(at {table_path}.{list_field}[{i}]). The first is at "
                f"{table_path}.{list_field}[{seen[value]}]."
            )
        seen[value] = i
    return set(seen)


def _validate_custom_format_id(
    cell_format: CellFormat, custom_format_ids: set[str], path: str
) -> None:
    if (
        cell_format.format_type == FormatType.CUSTOM
        and cell_format.custom_format_identifier is not None
        and cell_format.custom_format_identifier not in custom_format_ids
    ):
        raise LookupError(
            f"`CellFormat.custom_format_identifier` "
            f"{cell_format.custom_format_identifier!r} matches no `CustomFormat` "
            f"(at {path}.custom_format_identifier)"
        )


def _column_positions(headers: Sequence[ColumnHeader] | None) -> dict[str, int]:
    return {
        h.column_identifier: i
        for i, h in enumerate(headers or [])
        if h.column_identifier is not None
    }


def _validate_merged_range(
    merge_range: RowColumnIdRange,
    row_order: dict[str, int],
    column_order: dict[str, int],
    path: str,
) -> None:
    for field_name, rid in (
        ("top_left_row_identifier", merge_range.top_left_row_identifier),
        ("bottom_right_row_identifier", merge_range.bottom_right_row_identifier),
    ):
        if rid not in row_order:
            raise LookupError(
                f"`RowColumnIdRange.{field_name}` {rid!r} matches no "
                f"`Row.row_identifier` (at {path}.row_column_id_range.{field_name})"
            )
    for field_name, cid in (
        ("top_left_column_identifier", merge_range.top_left_column_identifier),
        ("bottom_right_column_identifier", merge_range.bottom_right_column_identifier),
    ):
        if cid not in column_order:
            raise LookupError(
                f"`RowColumnIdRange.{field_name}` {cid!r} matches no "
                f"`ColumnHeader.column_identifier` "
                f"(at {path}.row_column_id_range.{field_name})"
            )
    if (
        row_order[merge_range.top_left_row_identifier]
        > row_order[merge_range.bottom_right_row_identifier]
        or column_order[merge_range.top_left_column_identifier]
        > column_order[merge_range.bottom_right_column_identifier]
    ):
        raise ValueError(
            f"`RowColumnIdRange` top-left corner "
            f"({merge_range.top_left_row_identifier!r}, "
            f"{merge_range.top_left_column_identifier!r}) sits after its "
            f"bottom-right corner ({merge_range.bottom_right_row_identifier!r}, "
            f"{merge_range.bottom_right_column_identifier!r}) (at "
            f"{path}.row_column_id_range)"
        )
