# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


import pytest

from creator_studio_doc_format.core import (
    CanvasObject,
    KeynoteTheme,
    KeyxDocument,
    PlaceholderDefinition,
    PlaceholderInfo,
    Presentation,
    Shape,
    Slide,
    SlideLayout,
    SlideObject,
)
from creator_studio_doc_format.core import (
    SlideObjectPlaceholderInfoPlaceholderDefinitionKind as PlaceholderKind,
)
from creator_studio_doc_format.validation import validate_document

from .builders import slide_size


def defined_placeholder(
    kind: PlaceholderKind, *, is_visible: bool = True
) -> SlideObject:
    return SlideObject(
        object=CanvasObject(shape=Shape()),
        placeholder_info=PlaceholderInfo(
            defined=PlaceholderDefinition(kind=kind, is_visible=is_visible)
        ),
    )


def tagged_placeholder(tag: str) -> SlideObject:
    return SlideObject(
        object=CanvasObject(shape=Shape()), placeholder_info=PlaceholderInfo(tagged=tag)
    )


def _doc(*slides: Slide, layouts: list[SlideLayout] | None = None) -> KeyxDocument:
    theme = KeynoteTheme(slide_layouts=layouts) if layouts is not None else None
    return KeyxDocument(
        Presentation(
            slide_size=slide_size(), slides=list(slides) or [Slide()], theme=theme
        ),
        presets=[],
    )


def test_validate_detects_duplicate_defined_kind_on_slide() -> None:
    with pytest.raises(
        ValueError, match=r"`PlaceholderDefinition\.kind` 'title' is a duplicate"
    ):
        validate_document(
            _doc(
                Slide(
                    contents=[
                        defined_placeholder(PlaceholderKind.TITLE),
                        defined_placeholder(PlaceholderKind.TITLE),
                    ]
                )
            )
        )


def test_validate_detects_duplicate_defined_kind_on_slide_layout() -> None:
    layout = SlideLayout(
        name="Title",
        contents=[
            defined_placeholder(PlaceholderKind.BODY),
            defined_placeholder(PlaceholderKind.BODY),
        ],
    )
    with pytest.raises(
        ValueError, match=r"`PlaceholderDefinition\.kind` 'body' is a duplicate"
    ):
        validate_document(_doc(layouts=[layout]))


def test_validate_detects_duplicate_defined_kind_across_visibility() -> None:
    with pytest.raises(
        ValueError, match=r"`PlaceholderDefinition\.kind` 'title' is a duplicate"
    ):
        validate_document(
            _doc(
                Slide(
                    contents=[
                        defined_placeholder(PlaceholderKind.TITLE, is_visible=False),
                        defined_placeholder(PlaceholderKind.TITLE),
                    ]
                )
            )
        )


def test_validate_allows_one_placeholder_of_each_defined_kind() -> None:
    doc = _doc(
        Slide(contents=[defined_placeholder(kind) for kind in PlaceholderKind]),
    )
    validate_document(doc)


def test_validate_allows_the_same_defined_kind_on_different_slides() -> None:
    doc = _doc(
        Slide(contents=[defined_placeholder(PlaceholderKind.TITLE)]),
        Slide(contents=[defined_placeholder(PlaceholderKind.TITLE)]),
    )
    validate_document(doc)


def test_validate_allows_duplicate_tagged_placeholders() -> None:
    doc = _doc(
        Slide(contents=[tagged_placeholder("Media"), tagged_placeholder("Media")])
    )
    validate_document(doc)


def test_validate_allows_a_tag_alongside_a_defined_kind() -> None:
    doc = _doc(
        Slide(
            contents=[
                defined_placeholder(PlaceholderKind.TITLE),
                tagged_placeholder("Title"),
            ]
        )
    )
    validate_document(doc)


def test_validate_slide_layout_resolves_by_identifier() -> None:
    doc = _doc(
        Slide(layout="layout-1"),
        layouts=[SlideLayout(identifier="layout-1", name="Title & Subtitle")],
    )
    validate_document(doc)


def test_validate_slide_layout_resolves_by_name() -> None:
    doc = _doc(
        Slide(layout="Title & Subtitle"),
        layouts=[SlideLayout(identifier="layout-1", name="Title & Subtitle")],
    )
    validate_document(doc)


def test_validate_slide_layout_resolves_by_name_case_insensitively() -> None:
    doc = _doc(
        Slide(layout="title & subtitle"),
        layouts=[SlideLayout(name="Title & Subtitle")],
    )
    validate_document(doc)


@pytest.mark.parametrize(
    ("layout", "name"),
    [
        pytest.param("ıstanbul", "ISTANBUL", id="turkish-dotless-i"),
        pytest.param("İSTANBUL", "istanbul", id="turkish-dotted-capital-i"),
        pytest.param("café", "cafe\u0301", id="nfc-vs-nfd"),
        pytest.param("İ\u0301", "í", id="turkish-dotted-capital-i-with-mark"),
        pytest.param("ı\u0307", "i", id="dotless-i-with-dot"),
        pytest.param("İ\u0323", "I\u0323", id="dot-reordered-behind-lower-mark"),
        pytest.param("ﬁle", "FILE", id="ligature"),
        pytest.param("Ｔｉｔｌｅ", "Title", id="fullwidth"),
        pytest.param("Title²", "Title2", id="superscript"),
        pytest.param("aa", "Å", id="danish-aa"),
        pytest.param("タイトル", "見出し", id="non-ascii-both-sides"),
        pytest.param("タイトレ", "タイトル", id="non-ascii-typo-uncaught"),
    ],
)
def test_validate_slide_layout_accepts_names_some_locale_resolves(
    layout: str, name: str
) -> None:
    doc = _doc(Slide(layout=layout), layouts=[SlideLayout(name=name)])
    validate_document(doc)


@pytest.mark.parametrize(
    ("layout", "name"),
    [
        pytest.param("Tilte", "Title", id="ascii-typo"),
        pytest.param("Tilte", "見出し", id="ascii-reference-non-ascii-name"),
        pytest.param("見出し", "Title", id="non-ascii-reference-ascii-name"),
    ],
)
def test_validate_slide_layout_rejects_names_no_locale_resolves(
    layout: str, name: str
) -> None:
    doc = _doc(Slide(layout=layout), layouts=[SlideLayout(name=name)])
    with pytest.raises(LookupError, match=layout):
        validate_document(doc)


@pytest.mark.parametrize(
    "layout",
    [
        pytest.param("Títle", id="non-ascii-typo-of-ascii-name"),
        pytest.param("Title\u200b", id="invisible-suffix"),
    ],
)
def test_validate_slide_layout_rejects_against_unrelated_non_ascii_name(
    layout: str,
) -> None:
    doc = _doc(
        Slide(layout=layout),
        layouts=[SlideLayout(name="Title"), SlideLayout(name="見出し")],
    )
    with pytest.raises(LookupError, match="matches no `SlideLayout`"):
        validate_document(doc)


def test_validate_slide_layout_missing_raises() -> None:
    doc = _doc(
        Slide(layout="No Such Layout"),
        layouts=[SlideLayout(name="Title & Subtitle")],
    )
    with pytest.raises(LookupError, match="No Such Layout"):
        validate_document(doc)


def test_validate_slide_layout_absent_is_allowed() -> None:
    doc = _doc(Slide(), layouts=[SlideLayout(name="Title & Subtitle")])
    validate_document(doc)


@pytest.mark.parametrize("theme", [None, KeynoteTheme(name="Gradient")])
def test_validate_slide_layout_unvalidated_without_custom_layouts(
    theme: KeynoteTheme | None,
) -> None:
    doc = KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[Slide(layout="Title & Subtitle")],
            theme=theme,
        ),
        presets=[],
    )
    validate_document(doc)


def test_validate_slide_layout_resolves_against_any_layout_not_just_the_first() -> None:
    doc = _doc(
        Slide(layout="Bullets"),
        layouts=[SlideLayout(name="Title"), SlideLayout(name="Bullets")],
    )
    validate_document(doc)
