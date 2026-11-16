# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


import pytest

from creator_studio_doc_format.core import Preset, PresetRegistry
from creator_studio_doc_format.validation._preset_graph import validate_preset_graph


def test_multi_level_chain_deepest_child_wins() -> None:
    reg = PresetRegistry(
        [
            Preset("gp", {"a": 1, "b": 1, "c": 1}),
            Preset("p", {"b": 2, "c": 2}, parent_identifier="gp"),
            Preset("c", {"c": 3}, parent_identifier="p"),
        ],
    )
    assert reg.resolved_properties("c") == {"a": 1, "b": 2, "c": 3}


def test_resolved_properties_returns_raw_values() -> None:
    props = {"preset_identifier": "self_ref", "opacity": None, "keep": 1}
    reg = PresetRegistry([Preset("a", props)])
    assert reg.resolved_properties("a") == {
        "preset_identifier": "self_ref",
        "opacity": None,
        "keep": 1,
    }


def test_child_none_overrides_parent_value() -> None:
    reg = PresetRegistry(
        [
            Preset("parent", {"space_after": 10}),
            Preset("child", {"space_after": None}, parent_identifier="parent"),
        ],
    )
    assert reg.resolved_properties("child") == {"space_after": None}


def test_dag_two_children_one_parent_resolves() -> None:
    reg = PresetRegistry(
        [
            Preset("parent", {"a": 1}),
            Preset("c1", {"b": 2}, parent_identifier="parent"),
            Preset("c2", {"c": 3}, parent_identifier="parent"),
        ],
    )
    assert reg.resolved_properties("c1") == {"a": 1, "b": 2}
    assert reg.resolved_properties("c2") == {"a": 1, "c": 3}


def test_resolved_properties_is_cached() -> None:
    reg = PresetRegistry(
        [
            Preset("parent", {"a": 1}),
            Preset("child", {"b": 2}, parent_identifier="parent"),
        ],
    )
    first = reg.resolved_properties("child")
    second = reg.resolved_properties("child")
    assert first == second == {"a": 1, "b": 2}
    assert first is second


def test_missing_parent_names_the_child_preset() -> None:
    with pytest.raises(LookupError, match=r"matches no preset \(at preset 'child'\)"):
        validate_preset_graph([Preset("child", {}, parent_identifier="missing")])


def test_parent_cycle_raises() -> None:
    with pytest.raises(ValueError, match="Presets form a cycle"):
        validate_preset_graph(
            [
                Preset("a", {}, parent_identifier="b"),
                Preset("b", {}, parent_identifier="a"),
            ]
        )


def test_cross_edge_cycle_raises() -> None:
    with pytest.raises(ValueError, match="Presets form a cycle"):
        validate_preset_graph(
            [
                Preset("a", {}, parent_identifier="b"),
                Preset("b", {"fill": {"preset_identifier": "a"}}),
            ]
        )


def test_duplicate_identifier_raises() -> None:
    with pytest.raises(
        ValueError, match=r"`Preset\.identifier` values .* are duplicates"
    ):
        validate_preset_graph(
            [
                Preset("a", {"x": 1}),
                Preset("a", {"y": 2}),
            ]
        )


def test_empty_identifier_raises() -> None:
    with pytest.raises(ValueError, match="`Preset.identifier` is empty"):
        validate_preset_graph([Preset("", {})])


def test_top_level_preset_identifier_key_is_not_a_graph_edge() -> None:
    presets = [
        Preset("a", {}, parent_identifier="b"),
        Preset("b", {"preset_identifier": "a"}),
    ]
    validate_preset_graph(presets)
    reg = PresetRegistry(presets)
    assert reg.resolved_properties("a") == {"preset_identifier": "a"}
