# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


from pathlib import Path
from typing import Any

import pytest

from creator_studio_doc_format.core import (
    CanvasObject,
    IndirectResource,
    KeyxDocument,
    Movie,
    Package,
    PlaybackOptions,
    Presentation,
    Preset,
    Resource,
    Slide,
    SlideObject,
)
from creator_studio_doc_format.core.package import (
    PresetRegistry,
    _iter_indirect_identifiers,
)
from creator_studio_doc_format.validation import validate_document

from .builders import doc_with_indirect_image, slide_size


def test_validate_indirect_resource_missing_raises() -> None:
    doc = doc_with_indirect_image("missing.png")
    with pytest.raises(LookupError, match=r"missing\.png"):
        validate_document(doc)


def test_validate_indirect_resource_present_passes() -> None:
    doc = doc_with_indirect_image("present.png")
    doc.resources["present.png"] = b"\x89PNG\r\n\x1a\n"
    validate_document(doc)


def test_validate_looks_up_identifier_over_filename() -> None:
    doc = doc_with_indirect_image("shown.png", identifier="stored.png")
    doc.resources["shown.png"] = b"\x89PNG\r\n\x1a\n"
    with pytest.raises(LookupError, match=r"stored\.png"):
        validate_document(doc)

    doc.resources["stored.png"] = b"\x89PNG\r\n\x1a\n"
    validate_document(doc)


def test_validate_names_the_lookup_field_of_a_missing_resource() -> None:
    doc = doc_with_indirect_image("Photo.png", identifier="a1b2.png")
    with pytest.raises(
        LookupError, match=r"`IndirectResource\.identifier` 'a1b2\.png' matches no"
    ):
        validate_document(doc)


@pytest.mark.parametrize("filename", ["", "   "])
def test_validate_blank_filename_is_malformed_even_with_identifier(
    filename: str,
) -> None:
    doc = doc_with_indirect_image(filename, identifier="a1b2.png")
    doc.resources["a1b2.png"] = b"\x89PNG\r\n\x1a\n"
    with pytest.raises(
        ValueError, match=r"`IndirectResource\.filename` .* is empty or blank"
    ):
        validate_document(doc)


def test_validate_padded_filename_allowed_when_identifier_set() -> None:
    doc = doc_with_indirect_image("photo.png ", identifier="a1b2.png")
    doc.resources["a1b2.png"] = b"\x89PNG\r\n\x1a\n"
    validate_document(doc)


def test_validate_padded_identifier_resolves_when_stored() -> None:
    doc = doc_with_indirect_image("Photo.png", identifier=" a1b2.png")
    doc.resources[" a1b2.png"] = b"\x89PNG\r\n\x1a\n"
    validate_document(doc)


def test_validate_blank_identifier_diagnoses_reference_not_resource() -> None:
    doc = doc_with_indirect_image("Photo.png", identifier=" ")
    with pytest.raises(
        ValueError, match=r"`IndirectResource\.identifier` .* is empty or blank"
    ):
        validate_document(doc)


def test_validate_empty_filename_diagnoses_reference_not_resource() -> None:
    doc = doc_with_indirect_image("")
    with pytest.raises(
        ValueError, match=r"`IndirectResource\.filename` .* is empty or blank"
    ):
        validate_document(doc)


def test_validate_whitespace_filename_diagnoses_reference_not_resource() -> None:
    doc = doc_with_indirect_image("   ")
    with pytest.raises(
        ValueError, match=r"`IndirectResource\.filename` .* is empty or blank"
    ):
        validate_document(doc)


def test_validate_padded_filename_resolves_by_exact_name() -> None:
    doc = doc_with_indirect_image("  img.png  ")
    doc.resources["img.png"] = b"\x89PNG\r\n\x1a\n"
    with pytest.raises(LookupError, match=r"'  img\.png  '"):
        validate_document(doc)
    doc.resources["  img.png  "] = b"\x89PNG\r\n\x1a\n"
    validate_document(doc)


def test_validate_accepts_a_unique_ascii_skeleton_match() -> None:
    doc = doc_with_indirect_image("ÕåÖþ£ƒ")
    doc.resources["写真"] = b"\x89PNG\r\n\x1a\n"
    validate_document(doc)
    doc.resources["画像"] = b"\x89PNG\r\n\x1a\n"
    with pytest.raises(LookupError, match="ÕåÖþ£ƒ"):
        validate_document(doc)


def _doc_with_preset_supplied_poster(filename: str) -> KeyxDocument:
    movie = Movie(
        resource=Resource(indirect=IndirectResource(filename="real.mp4")),
        playback_options=PlaybackOptions(),
        preset_identifier="poster",
    )
    doc = KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[Slide(contents=[SlideObject(object=CanvasObject(movie=movie))])],
        ),
        presets=[
            Preset(
                "poster",
                properties={
                    "poster_image": {
                        "indirect": {
                            "type_identifier": "indirect-resource",
                            "version": "1.0",
                            "filename": filename,
                        }
                    }
                },
            )
        ],
    )
    doc.resources["real.mp4"] = b"\x00\x00\x00\x18ftyp"
    return doc


def test_validate_catches_dangling_resource_reached_only_via_preset() -> None:
    doc = _doc_with_preset_supplied_poster("ghost.png")

    serialized_references = {
        name
        for _field, name in _iter_indirect_identifiers(
            doc._to_main_json(), PresetRegistry(doc.presets)
        )
    }
    assert serialized_references == {"real.mp4"}
    assert all(doc.resources.can_resolve(f) for f in serialized_references)

    with pytest.raises(LookupError, match=r"ghost\.png"):
        validate_document(doc)


def test_validate_passes_when_preset_supplied_resource_is_present() -> None:
    doc = _doc_with_preset_supplied_poster("poster.png")
    doc.resources["poster.png"] = b"\x89PNG\r\n\x1a\n"
    validate_document(doc)


def _doc_with_identifier_from_preset(stored: str) -> KeyxDocument:
    doc = doc_with_indirect_image(
        "Photo.png",
        identifier="a1b2.png",
        preset_identifier="img",
        presets=[Preset("img", properties={"identifier": "a1b2.png"})],
    )
    doc.resources[stored] = b"\x89PNG\r\n\x1a\n"
    return doc


def test_save_resolves_by_identifier_not_filename(tmp_path: Path) -> None:
    doc = doc_with_indirect_image("Photo.png", identifier="a1b2.png")
    doc.resources["Photo.png"] = b"\x89PNG\r\n\x1a\n"
    with pytest.raises(ValueError, match=r"'a1b2\.png' \(looked up by identifier\)"):
        doc.save(tmp_path / "bad.keyx")
    doc.resources["a1b2.png"] = b"\x89PNG\r\n\x1a\n"
    doc.save(tmp_path / "ok.keyx")


def test_save_resolves_preset_omitted_identifier(tmp_path: Path) -> None:
    _doc_with_identifier_from_preset("a1b2.png").save(tmp_path / "ok.keyx")
    with pytest.raises(ValueError, match=r"a1b2\.png"):
        _doc_with_identifier_from_preset("Photo.png").save(tmp_path / "bad.keyx")


def test_save_resolves_against_presets_as_hooks_leave_them(tmp_path: Path) -> None:
    doc = _doc_with_identifier_from_preset("a1b2.png")

    def repoint(d: Package[Presentation], _main: dict[str, Any]) -> None:
        d.presets = [Preset("img", properties={"identifier": "other.png"})]

    with pytest.raises(ValueError, match=r"other\.png"):
        doc.save(tmp_path / "bad.keyx", pre_save_hooks=[repoint])


def test_save_skips_wrong_typed_preset_identifier(tmp_path: Path) -> None:
    doc = doc_with_indirect_image(
        "missing.png",
        preset_identifier="img",
        presets=[Preset("img", properties={"identifier": 123})],
    )
    with pytest.raises(ValueError, match=r"indirect\.identifier"):
        validate_document(doc)
    with pytest.raises(ValueError, match=r"'missing\.png' \(looked up by filename\)"):
        doc.save(tmp_path / "bad.keyx")


def test_save_reports_a_missing_name_once(tmp_path: Path) -> None:
    doc = doc_with_indirect_image("Photo.png", identifier="x.png")
    doc.payload.slides.append(doc_with_indirect_image("x.png").payload.slides[0])
    with pytest.raises(
        ValueError, match=r"Data/: 'x\.png' \(looked up by filename and identifier\)$"
    ):
        doc.save(tmp_path / "bad.keyx")
