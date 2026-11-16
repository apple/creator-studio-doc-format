# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0

from typing import cast

from pydantic import BaseModel

from creator_studio_doc_format.core import (
    RGBA,
    Color,
    Flavor,
    Gradient,
    Linear,
    Override,
    Stop,
)
from creator_studio_doc_format.navigation import IteratedModel, iterate_models


def test_root_is_first_and_has_empty_path_and_ancestors():
    root = RGBA()
    visits = list(iterate_models(root))
    assert len(visits) >= 1
    first = visits[0]
    assert isinstance(first, IteratedModel)
    assert first.model is root
    assert first.path == ""
    assert first.ancestors == ()
    assert first.index_path == ()


def test_path_shape_for_nested_list_and_single_model_descents():
    color = Color(rgba=RGBA(red=0.5, green=0.5, blue=0.5))
    stop = Stop(color=color, fraction=0.0)
    gradient = Gradient(stops=[stop], flavor=Flavor(linear=Linear(angle=0)))

    paths = {
        visit.model.__class__.__name__: visit.path for visit in iterate_models(gradient)
    }

    assert paths["Gradient"] == ""
    assert paths["Stop"] == "stops[0]"
    assert paths["Color"] == "stops[0].color"
    assert paths["RGBA"] == "stops[0].color.rgba"


def test_ancestors_at_depth_returns_outermost_to_innermost_chain():
    color = Color(rgba=RGBA())
    stop = Stop(color=color, fraction=0.0)
    gradient = Gradient(stops=[stop], flavor=Flavor(linear=Linear(angle=0)))

    rgba_visit = next(v for v in iterate_models(gradient) if isinstance(v.model, RGBA))
    ancestors = rgba_visit.ancestors

    assert [type(a).__name__ for a in ancestors] == ["Gradient", "Stop", "Color"]
    assert ancestors[0] is gradient
    assert ancestors[1] is stop
    assert ancestors[2] is color


def test_index_path_encodes_only_list_indices_not_field_names():
    color = Color(rgba=RGBA())
    stops = [
        Stop(color=color, fraction=0.0),
        Stop(color=Color(rgba=RGBA()), fraction=0.5),
        Stop(color=Color(rgba=RGBA()), fraction=1.0),
    ]
    gradient = Gradient(stops=stops, flavor=Flavor(linear=Linear(angle=0)))

    rgba_index_paths = sorted(
        v.index_path for v in iterate_models(gradient) if isinstance(v.model, RGBA)
    )
    assert rgba_index_paths == [(0,), (1,), (2,)]


def test_dict_of_basemodel_field_is_iterated():
    class Child(BaseModel):
        n: int

    class Parent(BaseModel):
        children: dict[str, Child]

    parent = Parent(children={"a": Child(n=1), "b": Child(n=2)})

    child_visits = [v for v in iterate_models(parent) if isinstance(v.model, Child)]
    ns = sorted(cast(Child, v.model).n for v in child_visits)
    assert ns == [1, 2]

    paths = sorted(v.path for v in child_visits)
    assert paths == ["children['a']", "children['b']"]

    assert all(v.index_path == () for v in child_visits)


def test_cycle_is_cut_silently_and_iterator_terminates():
    class Cyclic(BaseModel):
        model_config = {"arbitrary_types_allowed": True}
        child: object = None

    a = Cyclic()
    b = Cyclic()
    object.__setattr__(a, "child", b)
    object.__setattr__(b, "child", a)

    visits = list(iterate_models(a))

    assert visits[0].model is a
    assert any(v.model is b for v in visits)
    a_visits = [v for v in visits if v.model is a]
    assert len(a_visits) == 1


def test_sibling_shared_subtree_yields_distinct_visits():
    shared = RGBA(red=0.1)
    color_a = Color(rgba=shared)
    color_b = Color(rgba=shared)
    stops = [Stop(color=color_a, fraction=0.0), Stop(color=color_b, fraction=1.0)]
    gradient = Gradient(stops=stops, flavor=Flavor(linear=Linear(angle=0)))

    rgba_visits = [v for v in iterate_models(gradient) if isinstance(v.model, RGBA)]

    assert len(rgba_visits) == 2
    paths = sorted(v.path for v in rgba_visits)
    assert paths == ["stops[0].color.rgba", "stops[1].color.rgba"]


def test_override_value_is_descended_and_not_set_is_skipped():
    class Leaf(BaseModel):
        n: int

    class Holder(BaseModel):
        set_field: Override[Leaf] = Override.value(Leaf(n=1))
        unset_field: Override[Leaf] = Override.not_set()
        cleared_field: Override[Leaf] = Override.cleared()

    root = Holder()
    visits = list(iterate_models(root))

    leaves = [v for v in visits if isinstance(v.model, Leaf)]
    assert len(leaves) == 1
    assert cast(Leaf, leaves[0].model).n == 1
    assert leaves[0].path == "set_field"
