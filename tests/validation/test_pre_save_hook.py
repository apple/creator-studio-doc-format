# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


import copy
import json

import pytest

from creator_studio_doc_format.core import (
    CanvasObject,
    KeyxDocument,
    Presentation,
    Preset,
    Shape,
    Slide,
    SlideObject,
)
from creator_studio_doc_format.validation import validate_document

from .builders import doc_with_indirect_image, empty_doc, slide_size


def _valid_doc():
    doc = doc_with_indirect_image("present.png")
    doc.resources["present.png"] = b"\x89PNG\r\n\x1a\n"
    return doc


def test_hook_violation_aborts_the_save(tmp_path) -> None:
    out = tmp_path / "d.keyx"
    doc = doc_with_indirect_image("missing.png")
    with pytest.raises(LookupError, match=r"missing\.png"):
        doc.save(out, pre_save_hooks=[validate_document])
    assert not out.exists()


def test_hook_clean_doc_writes(tmp_path) -> None:
    out = tmp_path / "d.keyx"
    _valid_doc().save(out, pre_save_hooks=[validate_document])
    assert out.is_file()


def test_hook_serializes_the_payload_once(tmp_path, monkeypatch) -> None:
    calls: list[dict] = []
    original = Presentation.model_dump
    monkeypatch.setattr(
        Presentation,
        "model_dump",
        lambda self, **kw: (calls.append(kw), original(self, **kw))[1],
    )
    _valid_doc().save(tmp_path / "d.keyx", pre_save_hooks=[validate_document])
    assert len(calls) == 1


def _snapshot(doc):
    return (
        json.dumps(doc._to_main_json(), sort_keys=True),
        json.dumps([p.to_dict() for p in doc.presets], sort_keys=True),
        json.dumps(doc.manifest.to_dict(), sort_keys=True),
        sorted(doc.resources.keys()),
    )


def test_the_hook_does_not_mutate_the_document() -> None:
    doc = _valid_doc()
    before = _snapshot(doc)
    validate_document(doc)
    assert _snapshot(doc) == before


def test_the_hook_does_not_mutate_the_main_json_passed_in() -> None:
    doc = _valid_doc()
    main = doc._to_main_json()
    frozen = copy.deepcopy(main)
    validate_document(doc, main)
    assert main == frozen


def test_a_phase_that_mutates_main_json_is_caught(monkeypatch) -> None:
    import creator_studio_doc_format.validation as validation_mod

    real = validation_mod._resolve_properties

    def mutating(doc, main_json):
        main_json["injected"] = 1
        return real(doc, main_json)

    monkeypatch.setattr(validation_mod, "_resolve_properties", mutating)
    doc = _valid_doc()
    with pytest.raises(
        RuntimeError, match=r"`main_json` changed during `validate_document`"
    ):
        validate_document(doc, doc._to_main_json())


def test_the_self_check_is_skipped_when_main_json_is_not_passed_in() -> None:
    validate_document(_valid_doc())


def test_hook_reports_a_preset_cycle_an_object_adopts(
    tmp_path,
) -> None:
    out = tmp_path / "d.keyx"
    slide = Slide(
        contents=[SlideObject(object=CanvasObject(shape=Shape(preset_identifier="a")))]
    )
    doc = KeyxDocument(
        Presentation(slide_size=slide_size(), slides=[slide]),
        presets=[
            Preset("a", {}, parent_identifier="b"),
            Preset("b", {}, parent_identifier="a"),
        ],
    )
    with pytest.raises(ValueError, match="circular preset"):
        doc.save(out, pre_save_hooks=[validate_document])
    assert not out.exists()


@pytest.mark.filterwarnings("ignore:Pydantic serializer warnings")
def test_an_in_place_append_has_a_path_only_when_validated_directly(
    tmp_path,
) -> None:
    doc = empty_doc()
    doc.payload.slides.append("x")  # ty: ignore
    with pytest.raises(ValueError, match="at slides"):
        validate_document(doc)
    with pytest.raises(ValueError) as hooked:
        doc.save(tmp_path / "d.keyx", pre_save_hooks=[validate_document])
    assert "at slides" not in str(hooked.value)
