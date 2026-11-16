# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


import pytest
from pydantic_core import PydanticSerializationError

from creator_studio_doc_format.core import (
    RGBA,
    BorderStyleType,
    Color,
    Fill,
    KeyxDocument,
    Override,
    Paragraph,
    Presentation,
    Slide,
    TextStroke,
)
from creator_studio_doc_format.validation import validate_document
from creator_studio_doc_format.validation._field_types import validate_field_types


def _doc_with_slide() -> KeyxDocument:
    return KeyxDocument(payload=Presentation(slides=[Slide(identifier="s1")]))


def _white() -> Color:
    return Color(rgba=RGBA(red=1.0, green=1.0, blue=1.0, alpha=1.0))


def test_wrong_model_appended_to_a_typed_list():
    doc = _doc_with_slide()
    doc.payload.slides.append(Paragraph())  # ty: ignore
    with pytest.raises(ValueError, match=r"`Presentation\.slides` holds a value"):
        validate_document(doc)


def test_wrong_model_in_a_scalar_position_field():
    doc = _doc_with_slide()
    doc.payload.slides[0].__dict__["note"] = Fill(color=_white())
    with pytest.raises(ValueError, match=r"`Slide\.note` holds a value"):
        validate_document(doc)


def test_non_model_spliced_into_a_typed_list():
    doc = _doc_with_slide()
    doc.payload.slides[0] = 42  # ty: ignore
    with pytest.raises(ValueError, match=r"`Presentation\.slides` holds a value"):
        validate_document(doc)


def test_scalar_corrupted_past_setattr():
    doc = _doc_with_slide()
    doc.payload.slides[0].__dict__["identifier"] = 12345
    with pytest.raises(ValueError, match=r"`Slide\.identifier` holds a value"):
        validate_document(doc)


def test_deleted_field_is_named_rather_than_emitted_as_null():
    doc = _doc_with_slide()
    del doc.payload.slides
    with pytest.raises(
        ValueError, match=r"`Presentation\.slides` was deleted or never set"
    ):
        validate_document(doc)


def test_required_field_model_construct_never_supplied():
    with pytest.raises(
        ValueError, match=r"`Presentation\.slides` was deleted or never set"
    ):
        validate_field_types(Presentation.model_construct())


@pytest.mark.parametrize(
    "override",
    [
        Override.not_set(),
        Override.cleared(),
        Override.value(TextStroke(none=True)),
    ],
    ids=["not_set", "cleared", "value"],
)
def test_every_override_state_is_accepted(override):
    validate_field_types(BorderStyleType.model_construct(stroke=override))


def test_override_carrying_a_wrongly_typed_value():
    model = BorderStyleType.model_construct(stroke=Override.value("not-a-stroke"))
    with pytest.raises(ValueError, match=r"`BorderStyleType\.stroke` holds a value"):
        validate_field_types(model)


@pytest.mark.parametrize(
    "bare",
    ["bare", TextStroke(none=True)],
    ids=["ill_typed", "well_typed"],
)
def test_bare_value_where_an_override_is_declared(bare):
    model = BorderStyleType.model_construct(stroke=bare)
    with pytest.raises(
        ValueError, match=r"`BorderStyleType\.stroke` [^`]+ isn't an `Override`"
    ):
        validate_field_types(model)


def test_bare_override_is_caught_where_the_serializer_would_have_caught_it():
    model = BorderStyleType().model_copy(update={"width": 3.0})
    with pytest.raises(PydanticSerializationError):
        model.model_dump(mode="json")
    with pytest.raises(
        ValueError, match=r"`BorderStyleType\.width` [^`]+ isn't an `Override`"
    ):
        validate_field_types(model)


def test_emptied_list_violating_min_length():
    doc = _doc_with_slide()
    doc.payload.slides.clear()
    with pytest.raises(ValueError, match=r"`Presentation\.slides` holds a value"):
        validate_field_types(doc.payload)


def test_forward_compatible_extra_keys_are_not_flagged():
    doc = _doc_with_slide()
    doc.payload.slides[0].__pydantic_extra__["future_field"] = {"a": 1}  # ty: ignore
    validate_document(doc)


def test_a_clean_document_passes():
    validate_document(_doc_with_slide())
