# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0

"""Iterate depth-first over a tree of models.

A child model can sit in a plain field, a list, a dictionary, an
:class:`~creator_studio_doc_format.core.Override` wrapper, or a
:class:`~creator_studio_doc_format.core.TaggedUnionModel` union case, so walking the
tree by hand takes care.
"""

__all__ = ["IteratedModel", "iterate_models"]

from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel

if TYPE_CHECKING:
    from .core import Override


@dataclass(frozen=True, eq=False)
class IteratedModel:
    """One model the iteration yields, with lazy access to its position in the tree.

    Each read of ``ancestors``, ``index_path``, or ``path`` costs O(depth). Caching the
    value can speed up a hot loop.

    An ``IteratedModel`` compares and hashes by identity, so it can go in a set. A
    model yielded twice gives two ``IteratedModel`` instances, and they compare unequal.

    You don't create an ``IteratedModel`` directly. :func:`iterate_models` yields them.
    """

    model: BaseModel
    """The model at this position in the tree."""

    _parent: "IteratedModel | None" = field(default=None, repr=False)
    _list_index: int | None = field(default=None, repr=False)
    _field_name: str | None = field(default=None, repr=False)
    _dict_key: object | None = field(default=None, repr=False)

    @property
    def ancestors(self) -> tuple[BaseModel, ...]:
        """The enclosing models, outermost first. It's ``()`` for the root."""
        out: list[BaseModel] = []
        cur = self._parent
        while cur is not None:
            out.append(cur.model)
            cur = cur._parent
        return tuple(reversed(out))

    @property
    def index_path(self) -> tuple[int, ...]:
        """The list indices along the path from the root, without field names.

        For example, iterating a slide gives ``(2, 3)`` for
        ``contents[2].object.group.children[3]``, and ``()`` for the root. Read
        ``ancestors`` or ``path`` when field names matter.
        """
        out: list[int] = []
        cur: IteratedModel | None = self
        while cur is not None:
            if cur._list_index is not None:
                out.append(cur._list_index)
            cur = cur._parent
        return tuple(reversed(out))

    @property
    def path(self) -> str:
        """The dotted path from the root. It's ``""`` for the root.

        For example, iterating a slide gives ``contents[0].object.shape.text``. A
        dictionary key goes through ``repr``, so ``field['a']`` and ``field[3]`` stay
        distinct.
        """
        segments: list[str] = []
        cur: IteratedModel | None = self
        while cur is not None and cur._field_name is not None:
            seg = cur._field_name
            if cur._list_index is not None:
                seg = f"{seg}[{cur._list_index}]"
            elif cur._dict_key is not None:
                seg = f"{seg}[{cur._dict_key!r}]"
            segments.append(seg)
            cur = cur._parent
        return ".".join(reversed(segments))


def iterate_models(root: BaseModel) -> Iterator[IteratedModel]:
    """Yields a model, then every model reachable from it, in depth-first pre-order.

    The iteration descends model fields, ``list[BaseModel]``, and
    ``dict[_, BaseModel]``, including a model held in an
    :class:`~creator_studio_doc_format.core.Override`. An ``Override`` that is unset or
    cleared holds no model and is skipped.

    Args:
        root: The model to start from.

    Yields:
        IteratedModel: Each model, a parent before its descendants. A model under two
        parents appears once for each.
    """
    yield from _iterate(
        root,
        parent=None,
        field_name=None,
        list_index=None,
        dict_key=None,
        path_ids=set(),
    )


def _iterate(
    model: BaseModel,
    *,
    parent: IteratedModel | None,
    field_name: str | None,
    list_index: int | None,
    dict_key: object | None,
    path_ids: set[int],
) -> Iterator[IteratedModel]:
    if id(model) in path_ids:
        return
    here = IteratedModel(model, parent, list_index, field_name, dict_key)
    yield here
    path_ids.add(id(model))
    try:
        for name in type(model).model_fields:
            value = getattr(model, name, None)
            if hasattr(value, "is_value") and hasattr(value, "get"):
                ov: Override[Any] = value
                if not ov.is_value:
                    continue
                value = ov.get()
            if isinstance(value, BaseModel):
                yield from _iterate(
                    value,
                    parent=here,
                    field_name=name,
                    list_index=None,
                    dict_key=None,
                    path_ids=path_ids,
                )
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, BaseModel):
                        yield from _iterate(
                            item,
                            parent=here,
                            field_name=name,
                            list_index=i,
                            dict_key=None,
                            path_ids=path_ids,
                        )
            elif isinstance(value, dict):
                for k, item in value.items():
                    if isinstance(item, BaseModel):
                        yield from _iterate(
                            item,
                            parent=here,
                            field_name=name,
                            list_index=None,
                            dict_key=k,
                            path_ids=path_ids,
                        )
    finally:
        path_ids.discard(id(model))
