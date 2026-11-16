# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


import pytest

from creator_studio_doc_format.core import (
    RGBA,
    CanvasObject,
    Color,
    ConnectionLine,
    End,
    Fill,
    KeyxDocument,
    LineEnd,
    Override,
    Position,
    Presentation,
    Preset,
    Shape,
    Slide,
    SlideBackground,
    SlideObject,
)
from creator_studio_doc_format.validation import validate_document
from creator_studio_doc_format.validation._resolve import _resolve_properties

from .builders import empty_doc, slide_size


def test_validate_minimal_passes() -> None:
    validate_document(empty_doc())


def test_validate_detects_preset_cycle() -> None:
    presets = [
        Preset("a", {}, parent_identifier="b"),
        Preset("b", {}, parent_identifier="a"),
    ]
    doc = KeyxDocument(
        Presentation(slide_size=slide_size(), slides=[Slide()]),
        presets=presets,
    )
    with pytest.raises(ValueError, match="Presets form a cycle"):
        validate_document(doc)


def test_validate_detects_preset_cycle_an_object_adopts() -> None:
    shape = Shape(preset_identifier="a")
    doc = KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[Slide(contents=[SlideObject(object=CanvasObject(shape=shape))])],
        ),
        presets=[
            Preset("a", {}, parent_identifier="b"),
            Preset("b", {}, parent_identifier="a"),
        ],
    )
    with pytest.raises(ValueError, match="Presets form a cycle"):
        validate_document(doc)


def test_validate_detects_preset_duplicate_identifiers() -> None:
    presets = [Preset("dup", {}), Preset("dup", {})]
    doc = KeyxDocument(
        Presentation(slide_size=slide_size(), slides=[Slide()]),
        presets=presets,
    )
    with pytest.raises(
        ValueError, match=r"`Preset\.identifier` values .* are duplicates"
    ):
        validate_document(doc)


def test_validate_rejects_empty_preset_identifier() -> None:
    doc = KeyxDocument(
        Presentation(slide_size=slide_size(), slides=[Slide()]),
        presets=[Preset("", {})],
    )
    with pytest.raises(ValueError, match=r"`Preset\.identifier` is empty"):
        validate_document(doc)


def test_validate_allows_empty_string_parent_identifier() -> None:
    doc = KeyxDocument(
        Presentation(slide_size=slide_size(), slides=[Slide()]),
        presets=[Preset("a", {}, parent_identifier="")],
    )
    validate_document(doc)


def test_validate_detects_cycle_through_a_property_reference() -> None:
    presets = [
        Preset("a", {}, parent_identifier="b"),
        Preset("b", properties={"fill": {"preset_identifier": "a"}}),
    ]
    doc = KeyxDocument(
        Presentation(slide_size=slide_size(), slides=[Slide()]),
        presets=presets,
    )
    with pytest.raises(ValueError, match="Presets form a cycle"):
        validate_document(doc)


def test_validate_accepts_dag_of_presets() -> None:
    presets = [
        Preset("root", {}),
        Preset("child_a", {}, parent_identifier="root"),
        Preset("child_b", {}, parent_identifier="root"),
    ]
    doc = KeyxDocument(
        Presentation(slide_size=slide_size(), slides=[Slide()]),
        presets=presets,
    )
    validate_document(doc)


def test_validate_strict_resolution_raises_on_missing_preset() -> None:
    shape = Shape(preset_identifier="not-there")
    doc = KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[Slide(contents=[SlideObject(object=CanvasObject(shape=shape))])],
        ),
        presets=[],
    )
    with pytest.raises(LookupError, match="not-there"):
        validate_document(doc)


def test_validate_strict_resolution_passes_with_registered_preset() -> None:
    slide = Slide(
        background=Override.value(
            SlideBackground(
                standard=Fill(color=Color(rgba=RGBA(preset_identifier="mid-red")))
            )
        )
    )
    doc = KeyxDocument(
        Presentation(slide_size=slide_size(), slides=[slide]),
        presets=[Preset("mid-red", properties={"red": 0.5})],
    )
    validate_document(doc)

    resolved = _resolve_properties(doc, doc._to_main_json())
    background = resolved.slides[0].background.get()
    assert background is not None
    fill = background.standard
    assert fill is not None and fill.color is not None and fill.color.rgba is not None
    assert fill.color.rgba.red == 0.5


def test_validate_accepts_unknown_preset_property_key() -> None:
    shape = Shape(preset_identifier="unknown-key")
    doc = KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[Slide(contents=[SlideObject(object=CanvasObject(shape=shape))])],
        ),
        presets=[Preset("unknown-key", properties={"not_a_shape_field": 1})],
    )
    validate_document(doc)


def test_validate_ignores_projected_preset_property_key() -> None:
    end = End(end_point=Position(x=0.0, y=0.0), line_end=LineEnd.NONE)
    connection_line = ConnectionLine(tail=end, head=end, preset_identifier="proj")
    doc = KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[
                Slide(
                    contents=[
                        SlideObject(object=CanvasObject(connectionLine=connection_line))
                    ]
                )
            ],
        ),
        presets=[
            Preset(
                "proj",
                properties={
                    "paragraph_properties": {
                        "type_identifier": "paragraph-properties",
                        "version": "1.0",
                    }
                },
            )
        ],
    )
    validate_document(doc)


def test_validate_skips_none_inherited_value_on_known_field() -> None:
    shape = Shape(preset_identifier="null-head")
    doc = KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[Slide(contents=[SlideObject(object=CanvasObject(shape=shape))])],
        ),
        presets=[Preset("null-head", properties={"head": None})],
    )
    validate_document(doc)
    resolved = _resolve_properties(doc, doc._to_main_json())
    contents = resolved.slides[0].contents
    assert contents is not None
    shape = contents[0].object.shape
    assert shape is not None and shape.head == LineEnd.NONE


def test_validate_skips_none_inherited_value_on_unknown_field() -> None:
    shape = Shape(preset_identifier="null-unknown")
    doc = KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[Slide(contents=[SlideObject(object=CanvasObject(shape=shape))])],
        ),
        presets=[Preset("null-unknown", properties={"not_a_shape_field": None})],
    )
    validate_document(doc)


def test_validate_raises_on_type_incompatible_inherited_value() -> None:
    slide = Slide(
        background=Override.value(
            SlideBackground(
                standard=Fill(color=Color(rgba=RGBA(preset_identifier="bad-rgba")))
            )
        )
    )
    doc = KeyxDocument(
        Presentation(slide_size=slide_size(), slides=[slide]),
        presets=[Preset("bad-rgba", properties={"red": "not-a-number"})],
    )
    with pytest.raises(ValueError, match="inherited preset value is invalid"):
        validate_document(doc)


def test_validate_names_the_preset_cause_on_constraint_violating_inherited_value() -> (
    None
):
    slide = Slide(
        background=Override.value(
            SlideBackground(
                standard=Fill(color=Color(rgba=RGBA(preset_identifier="bad-rgba")))
            )
        )
    )
    doc = KeyxDocument(
        Presentation(slide_size=slide_size(), slides=[slide]),
        presets=[Preset("bad-rgba", properties={"red": 5.0})],
    )
    with pytest.raises(ValueError, match="Fix any invalid preset property"):
        validate_document(doc)


def test_validate_type_mismatch_attributes_deepest_subkey() -> None:
    slide = Slide(preset_identifier="bad-slide")
    doc = KeyxDocument(
        Presentation(slide_size=slide_size(), slides=[slide]),
        presets=[
            Preset(
                "bad-slide",
                properties={
                    "background": {
                        "standard": {"color": {"rgba": {"red": "not-a-number"}}}
                    }
                },
            )
        ],
    )
    with pytest.raises(
        ValueError,
        match=r"at slides\.0\.background\.standard\.color\.rgba\.red",
    ):
        validate_document(doc)


def test_validate_missing_parent_names_the_child_preset() -> None:
    shape = Shape(preset_identifier="child")
    doc = KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[Slide(contents=[SlideObject(object=CanvasObject(shape=shape))])],
        ),
        presets=[Preset("child", {}, parent_identifier="missing-parent")],
    )
    with pytest.raises(LookupError, match=r"matches no preset \(at preset 'child'\)"):
        validate_document(doc)


def test_validate_unresolved_preset_wins_over_downstream_inherited_value_error() -> (
    None
):
    slide = Slide(
        background=Override.value(
            SlideBackground(
                standard=Fill(color=Color(rgba=RGBA(preset_identifier="bad-rgba")))
            )
        ),
        contents=[
            SlideObject(object=CanvasObject(shape=Shape(preset_identifier="gone")))
        ],
    )
    doc = KeyxDocument(
        Presentation(slide_size=slide_size(), slides=[slide]),
        presets=[Preset("bad-rgba", properties={"red": "not-a-number"})],
    )
    with pytest.raises(LookupError, match="gone"):
        validate_document(doc)


def test_validate_top_level_preset_identifier_in_properties_is_not_a_graph_edge() -> (
    None
):
    presets = [
        Preset("a", {}, parent_identifier="b"),
        Preset("b", properties={"preset_identifier": "a"}),
    ]
    doc = KeyxDocument(
        Presentation(slide_size=slide_size(), slides=[Slide()]),
        presets=presets,
    )
    validate_document(doc)
