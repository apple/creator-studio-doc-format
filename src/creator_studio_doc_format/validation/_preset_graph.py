# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


import graphlib
from collections.abc import Iterable, Sequence
from typing import Any

from creator_studio_doc_format.core import Preset


def validate_preset_graph(presets: Sequence[Preset]) -> None:
    _detect_cycle(_build_preset_edges(presets))


def _build_preset_edges(presets: Sequence[Preset]) -> dict[str, set[str]]:
    edges: dict[str, set[str]] = {}
    parents: dict[str, str] = {}
    dupes: set[str] = set()
    for i, p in enumerate(presets):
        if not p.identifier:
            raise ValueError(
                f"`Preset.identifier` is empty (at presets[{i}]). "
                f"Every `Preset` needs a nonempty `identifier`."
            )
        if p.identifier in edges:
            dupes.add(p.identifier)
            continue
        neighbors: set[str] = set()
        if p.parent_identifier:
            neighbors.add(p.parent_identifier)
            parents[p.identifier] = p.parent_identifier
        neighbors.update(_collect_nested_preset_refs(p.properties))
        edges[p.identifier] = neighbors
    if dupes:
        raise ValueError(
            f"`Preset.identifier` values {sorted(dupes)} are duplicates "
            f"(at presets). Each `Preset.identifier` must be unique."
        )
    for child, parent in sorted(parents.items()):
        if parent not in edges:
            raise LookupError(
                f"`Preset.parent_identifier` {parent!r} matches no preset "
                f"(at preset {child!r})"
            )
    return edges


def _detect_cycle(edges: dict[str, set[str]]) -> None:
    sorter: graphlib.TopologicalSorter[str] = graphlib.TopologicalSorter()
    for node, neighbors in edges.items():
        sorter.add(node, *(n for n in neighbors if n in edges))
    try:
        sorter.prepare()
    except graphlib.CycleError as e:
        cycle = " -> ".join(reversed(e.args[1]))
        raise ValueError(f"Presets form a cycle: {cycle} (at presets)") from None


def _collect_nested_preset_refs(
    properties: dict[str, Any],
) -> Iterable[str]:
    _seen: set[int] = {id(properties)}
    for v in properties.values():
        yield from _walk_for_refs(v, _seen)


def _walk_for_refs(value: Any, _seen: set[int]) -> Iterable[str]:
    if isinstance(value, dict):
        if id(value) in _seen:
            return
        _seen.add(id(value))
        ref = value.get("preset_identifier")
        if isinstance(ref, str) and ref:
            yield ref
        for v in value.values():
            yield from _walk_for_refs(v, _seen)
    elif isinstance(value, list):
        if id(value) in _seen:
            return
        _seen.add(id(value))
        for v in value:
            yield from _walk_for_refs(v, _seen)
