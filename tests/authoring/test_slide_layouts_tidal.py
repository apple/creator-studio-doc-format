# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


from __future__ import annotations

import uuid
from pathlib import Path

import pytest

from creator_studio_doc_format.authoring import (
    set_slide_placeholder_image,
    slide_from_layout,
)
from creator_studio_doc_format.authoring._slide_layouts import (
    _first_text,
    _placeholder_name,
)
from creator_studio_doc_format.core import (
    IndirectResource,
    KeynoteTheme,
    KeyxDocument,
    Resource,
    Slide,
    SlideLayout,
    SlideObject,
)
from creator_studio_doc_format.navigation import iterate_models
from creator_studio_doc_format.validation import validate_document

from .test_slide_layouts import _paragraph_runs

FIXTURE = (
    Path(__file__).parents[2]
    / "src/creator_studio_doc_format/examples/fixtures/Tidal_en.keyx"
)

LAYOUTS = [
    "Title",
    "Title & Bullets",
    "Hidden Definitions",
    "Layered Decoration",
    "Title, Bullets & Photo",
    "Photo - Horizontal",
    "Captioned Image",
    "Quote",
    "Instructional Prompts",
    "Mixed Content Types",
    "Shared Tag Duplicate",
    "Layered Group Decoration",
    "Title, Bullets & Live Video",
    "Layered Photo Decoration",
    "Nested Lists",
    "Blank",
]


@pytest.fixture(scope="module")
def doc() -> KeyxDocument:
    return KeyxDocument.open(FIXTURE)


@pytest.fixture(scope="module")
def theme(doc: KeyxDocument) -> KeynoteTheme:
    assert doc.presentation.theme is not None
    return doc.presentation.theme


@pytest.fixture(scope="module")
def real_slides(doc: KeyxDocument, theme: KeynoteTheme) -> dict[str, Slide]:
    names = {l.identifier: l.name for l in theme.slide_layouts or [] if l.identifier}
    slides = {
        names.get(s.layout, s.layout): s
        for s in doc.presentation.slides or []
        if s.layout
    }
    missing = [name for name in LAYOUTS if name not in slides]
    assert not missing, (
        f"`Tidal_en.keyx` has no slide for the layouts {missing}. Add one slide per "
        "layout in Keynote and export the file again."
    )
    laid_out = [s for s in doc.presentation.slides or [] if s.layout]
    assert len(slides) == len(laid_out), (
        "`Tidal_en.keyx` has more than one slide for some layout. Delete the extra "
        "slides so each test compares against one slide per layout."
    )
    return slides


def _objects(slide: Slide | SlideLayout) -> list[SlideObject]:
    return [
        item.model
        for item in iterate_models(slide)
        if isinstance(item.model, SlideObject)
    ]


def _identifier(obj: SlideObject) -> str | None:
    if obj.object is None or (case := obj.object.union_primary_name()) is None:
        return None
    return getattr(getattr(obj.object, case, None), "identifier", None)


def _is_uuid(value: str) -> bool:
    try:
        return str(uuid.UUID(value)) == value.lower()
    except ValueError:
        return False


def test_fixture_slides_carry_keynote_generated_identifiers(
    theme: KeynoteTheme, real_slides: dict[str, Slide]
) -> None:
    layout_identifiers = {
        identifier
        for layout in theme.slide_layouts or []
        for obj in _objects(layout)
        if (identifier := _identifier(obj))
    }
    for name, slide in real_slides.items():
        assert slide.identifier and _is_uuid(slide.identifier), (
            f"The slide for layout {name!r} has identifier {slide.identifier!r}, "
            "which isn't a UUID. Keynote writes a UUID there, so check whether "
            "someone edited the fixture by hand."
        )
        for obj in _objects(slide):
            if (placeholder := _placeholder_name(obj)) is None:
                continue
            identifier = _identifier(obj)
            assert (
                identifier
                and _is_uuid(identifier)
                and identifier not in layout_identifiers
            ), (
                f"Placeholder {placeholder!r} on the slide for layout {name!r} has "
                f"identifier {identifier!r}. Each placeholder on a slide needs its own "
                "UUID, distinct from the layout's."
            )


def _signature(obj: SlideObject) -> tuple[str | None, str | None, str | None]:
    source_kind = obj.source_kind.name if obj.source_kind else None
    kind = obj.object.union_primary_name() if obj.object is not None else None
    return (source_kind, kind, _placeholder_name(obj))


@pytest.mark.parametrize("layout", LAYOUTS)
def test_slide_from_layout_matches_keynotes_object_set(
    theme: KeynoteTheme, real_slides: dict[str, Slide], layout: str
) -> None:
    real, made = real_slides[layout], slide_from_layout(theme, layout)
    assert [_signature(o) for o in _objects(made)] == [
        _signature(o) for o in _objects(real)
    ]


def test_title_clearing_drops_the_run_like_keynote(
    theme: KeynoteTheme, real_slides: dict[str, Slide]
) -> None:
    real, made = (
        real_slides["Title & Bullets"],
        slide_from_layout(theme, "Title & Bullets"),
    )
    real_title = next(o for o in _objects(real) if _placeholder_name(o) == "TITLE")
    made_title = next(o for o in _objects(made) if _placeholder_name(o) == "TITLE")
    real_text, made_text = _first_text(real_title), _first_text(made_title)
    assert real_text is not None and made_text is not None
    assert real_text.paragraphs is not None and made_text.paragraphs is not None
    assert real_text.paragraphs[0].contents is None
    assert made_text.paragraphs[0].contents is None


def test_image_flags_and_crop_match_keynote(
    theme: KeynoteTheme, real_slides: dict[str, Slide]
) -> None:
    real = real_slides["Title, Bullets & Photo"]
    made = slide_from_layout(theme, "Title, Bullets & Photo")
    real_media = next(o for o in _objects(real) if _placeholder_name(o) == "Media")
    made_media = next(o for o in _objects(made) if _placeholder_name(o) == "Media")
    assert real_media.object is not None and made_media.object is not None
    real_img, made_img = real_media.object.image, made_media.object.image
    assert real_img is not None and made_img is not None
    assert made_img.was_media_replaced == real_img.was_media_replaced is False
    assert made_img.is_placeholder == real_img.is_placeholder is True
    assert made_img.geometry == real_img.geometry
    assert made_img.mask == real_img.mask


def test_caption_survives_like_keynote(
    theme: KeynoteTheme, real_slides: dict[str, Slide]
) -> None:
    real = real_slides["Captioned Image"]
    made = slide_from_layout(theme, "Captioned Image")
    real_media = next(o for o in _objects(real) if _placeholder_name(o) == "Media")
    made_media = next(o for o in _objects(made) if _placeholder_name(o) == "Media")
    assert real_media.object is not None and made_media.object is not None
    real_img, made_img = real_media.object.image, made_media.object.image
    assert real_img is not None and made_img is not None
    real_caption, made_caption = real_img.caption, made_img.caption
    assert real_caption is not None and made_caption is not None
    assert real_caption.text is not None and made_caption.text is not None
    real_runs = _paragraph_runs(real_caption.text.paragraphs or [])
    made_runs = _paragraph_runs(made_caption.text.paragraphs or [])
    assert made_runs == real_runs == ["Photo caption sample"]


def test_live_video_placeholder_takes_an_image_like_an_image_placeholder(
    theme: KeynoteTheme, real_slides: dict[str, Slide]
) -> None:
    layout = "Title, Bullets & Live Video"
    real = real_slides[layout]
    made = slide_from_layout(theme, layout)

    def live_video(slide: Slide) -> SlideObject:
        return next(o for o in _objects(slide) if _placeholder_name(o) == "Live Video")

    real_obj, made_obj = live_video(real), live_video(made)
    assert real_obj.object is not None and made_obj.object is not None
    assert real_obj.object.image is not None and made_obj.object.image is not None
    assert made_obj.object.image.resource == real_obj.object.image.resource

    image = set_slide_placeholder_image(
        made, "Live Video", Resource(indirect=IndirectResource(filename="frame.png"))
    )
    assert image.was_media_replaced is True


def test_nested_list_text_keeps_its_list_style_and_levels_like_keynote(
    theme: KeynoteTheme, real_slides: dict[str, Slide]
) -> None:
    layout = "Nested Lists"
    real = real_slides[layout]
    made = slide_from_layout(theme, layout)

    def levels(slide: Slide, tag: str) -> list[tuple[str | None, int | None]]:
        obj = next(o for o in _objects(slide) if _placeholder_name(o) == tag)
        text = _first_text(obj)
        assert text is not None
        return [
            (p.list_style.preset_identifier if p.list_style else None, p.list_level)
            for p in text.paragraphs or []
        ]

    outline = "text-5-liststyle-Outline"
    assert levels(made, "Text") == levels(real, "Text")
    assert levels(made, "Text") == [(outline, level) for level in (None, 1, 2, 3, 4, 5)]
    assert levels(made, "Text-1") == levels(real, "Text-1")
    assert {style for style, _ in levels(made, "Text-1")} == {"text-1-liststyle-Bullet"}


def test_layered_slide_copies_the_layout_image_like_keynote(
    theme: KeynoteTheme, real_slides: dict[str, Slide]
) -> None:
    layout = "Layered Photo Decoration"
    real = real_slides[layout]
    made = slide_from_layout(theme, layout)
    real_objs, made_objs = _objects(real), _objects(made)
    assert [o.source_kind for o in made_objs] == [o.source_kind for o in real_objs]
    real_img = next(o for o in real_objs if o.object and o.object.image)
    made_img = next(o for o in made_objs if o.object and o.object.image)
    assert real_img.object is not None and made_img.object is not None
    assert real_img.object.image is not None and made_img.object.image is not None
    assert made_img.object.image.resource == real_img.object.image.resource
    assert (
        made_img.object.image.was_media_replaced
        == real_img.object.image.was_media_replaced
    )


@pytest.mark.parametrize("layout", LAYOUTS)
def test_slides_from_one_layout_can_share_a_document(layout: str) -> None:
    doc = KeyxDocument.open(FIXTURE)
    assert doc.presentation.theme is not None and doc.presentation.slides is not None
    doc.presentation.slides += [
        slide_from_layout(doc.presentation.theme, layout) for _ in range(2)
    ]
    validate_document(doc)
