# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


from __future__ import annotations

from typing import Any

import pytest

from creator_studio_doc_format.authoring import (
    LayoutPlaceholderSummary,
    set_slide_placeholder_image,
    set_slide_placeholder_text,
    slide_from_layout,
    summarize_slide_layouts,
)
from creator_studio_doc_format.core import (
    Anchor,
    CanvasObject,
    Cell,
    CellReference,
    Chart,
    ColumnChart,
    ColumnHeader,
    ConnectionLine,
    Constituent,
    End,
    Formula,
    Geometry,
    Group,
    IdBasedFormula,
    Image,
    IndirectResource,
    InstantAlphaPath,
    KeynoteTheme,
    Mask,
    Paragraph,
    PlaceholderDefinition,
    PlaceholderInfo,
    Position,
    Resource,
    Row,
    Shape,
    Size,
    Slide,
    SlideLayout,
    SlideObject,
    SourceKind,
    Table,
    TaggedUnionModel,
    Text,
    Textbox,
    TextRun,
)
from creator_studio_doc_format.core import (
    SlideObjectPlaceholderInfoPlaceholderDefinitionKind as PlaceholderKind,
)


def _paragraph_runs(paragraphs: list[Paragraph]) -> list[str | None]:
    return [
        c.run.string
        for paragraph in paragraphs
        for c in (paragraph.contents or [])
        if c.run
    ]


def _resource(filename: str) -> Resource:
    return Resource(indirect=IndirectResource(filename=filename))


def _media_slide(image: Image) -> Slide:
    return Slide(
        contents=[
            SlideObject(
                object=CanvasObject(image=image),
                source_kind=SourceKind.PLACEHOLDER,
                placeholder_info=PlaceholderInfo(tagged="Media"),
            )
        ]
    )


def _text_object(
    string: str,
    *,
    source_kind: SourceKind | None,
    kind: PlaceholderKind | None = None,
    tag: str | None = None,
    is_visible: bool = True,
) -> SlideObject:
    info = None
    if kind is not None:
        defined = PlaceholderDefinition(kind=kind, is_visible=is_visible)
        info = PlaceholderInfo(defined=defined)
    elif tag is not None:
        info = PlaceholderInfo(tagged=tag)
    paragraph = Paragraph(contents=[Constituent(run=TextRun(string=string))])
    textbox = Textbox(text=Text(paragraphs=[paragraph]))
    return SlideObject(
        object=CanvasObject(textbox=textbox),
        source_kind=source_kind,
        placeholder_info=info,
    )


def _image_object(
    filename: str,
    *,
    source_kind: SourceKind | None,
    tag: str | None = None,
) -> SlideObject:
    info = PlaceholderInfo(tagged=tag) if tag is not None else None
    image = Image(
        resource=Resource(indirect=IndirectResource(filename=filename)),
        is_placeholder=True,
    )
    return SlideObject(
        object=CanvasObject(image=image),
        source_kind=source_kind,
        placeholder_info=info,
    )


@pytest.fixture
def theme() -> KeynoteTheme:
    layout = [
        _text_object("Decoration", source_kind=SourceKind.LAYOUT),
        _text_object(
            "Title Text", source_kind=SourceKind.PLACEHOLDER, kind=PlaceholderKind.TITLE
        ),
        _text_object("Caption", source_kind=SourceKind.PLACEHOLDER, tag="Caption"),
        _text_object(
            "Body", source_kind=None, kind=PlaceholderKind.BODY, is_visible=False
        ),
    ]
    return KeynoteTheme(
        name="Test",
        slide_layouts=[SlideLayout(name="Title", contents=layout)],
    )


def test_set_slide_placeholder_text_writes_and_returns_paragraphs(
    theme: KeynoteTheme,
) -> None:
    assert theme.slide_layouts is not None
    slide = Slide(contents=theme.slide_layouts[0].contents)
    title = set_slide_placeholder_text(slide, "TITLE", "Hi")
    assert _paragraph_runs(title) == ["Hi"]
    caption = set_slide_placeholder_text(slide, "Caption", ["a", "b"])
    assert _paragraph_runs(caption) == ["a", "b"]
    with pytest.raises(
        KeyError, match="No placeholder 'Nonexistent'. Available: .*'TITLE'"
    ):
        set_slide_placeholder_text(slide, "Nonexistent", None)


def test_set_slide_placeholder_text_returns_the_live_paragraphs() -> None:
    from creator_studio_doc_format.authoring._slide_layouts import (
        _first_text,
        _live_placeholders,
    )

    obj = _text_object("Prompt", source_kind=SourceKind.PLACEHOLDER, tag="TITLE")
    slide = Slide(contents=[obj])
    paragraphs = set_slide_placeholder_text(slide, "TITLE", ["a", "b", "c"])
    paragraphs[1].list_level = 1

    stored = _first_text(_live_placeholders(slide)[0])
    assert stored is not None and stored.paragraphs is not None
    assert stored.paragraphs[1] is paragraphs[1]
    assert stored.paragraphs[1].list_level == 1


def test_set_slide_placeholder_image_swaps_named_placeholder() -> None:
    deco = _image_object("deco.png", source_kind=SourceKind.LAYOUT, tag="Deco")
    media = _image_object("sample.jpg", source_kind=SourceKind.PLACEHOLDER, tag="Media")
    slide = Slide(contents=[deco, media])
    set_slide_placeholder_image(slide, "Media", _resource("p.png"))
    assert media.object is not None
    img = media.object.image
    assert img is not None and img.resource.indirect is not None
    assert img.resource.indirect.filename == "p.png"
    assert img.was_media_replaced is True

    with pytest.raises(KeyError):
        set_slide_placeholder_image(slide, "Deco", _resource("p.png"))


def test_set_slide_placeholder_image_on_text_placeholder_raises(
    theme: KeynoteTheme,
) -> None:
    assert theme.slide_layouts is not None
    slide = Slide(contents=theme.slide_layouts[0].contents)
    with pytest.raises(TypeError):
        set_slide_placeholder_image(slide, "TITLE", _resource("p.png"))


def test_set_captioned_media_is_image_not_text() -> None:
    from creator_studio_doc_format.core import Label

    caption_paragraph = Paragraph(
        contents=[Constituent(run=TextRun(string="A caption"))]
    )
    caption = Label(text=Text(paragraphs=[caption_paragraph]))
    image = Image(
        resource=Resource(indirect=IndirectResource(filename="photo.jpg")),
        caption=caption,
    )
    obj = SlideObject(
        object=CanvasObject(image=image),
        source_kind=SourceKind.PLACEHOLDER,
        placeholder_info=PlaceholderInfo(tagged="Media"),
    )
    slide = Slide(contents=[obj])
    with pytest.raises(TypeError):
        set_slide_placeholder_text(slide, "Media", "x")
    set_slide_placeholder_image(slide, "Media", _resource("new.png"))
    assert image.resource.indirect is not None
    assert image.resource.indirect.filename == "new.png"


def test_set_slide_placeholder_text_prefers_body_over_caption_and_title() -> None:
    from creator_studio_doc_format.core import Label, Shape

    def label(s: str) -> Label:
        paragraph = Paragraph(contents=[Constituent(run=TextRun(string=s))])
        return Label(text=Text(paragraphs=[paragraph]))

    body_paragraph = Paragraph(
        contents=[Constituent(run=TextRun(string="Body Sample"))]
    )
    shape = Shape(
        title=label("Title Sample"),
        caption=label("Caption Sample"),
        text=Text(paragraphs=[body_paragraph]),
    )
    obj = SlideObject(
        object=CanvasObject(shape=shape),
        source_kind=SourceKind.PLACEHOLDER,
        placeholder_info=PlaceholderInfo(
            defined=PlaceholderDefinition(kind=PlaceholderKind.BODY)
        ),
    )
    slide = Slide(contents=[obj])

    assert _paragraph_runs(set_slide_placeholder_text(slide, "BODY", "New")) == ["New"]
    assert shape.title is not None and shape.title.text is not None
    assert shape.title.text.paragraphs is not None
    assert _paragraph_runs(shape.title.text.paragraphs) == ["Title Sample"]
    assert shape.caption is not None and shape.caption.text is not None
    assert shape.caption.text.paragraphs is not None
    assert _paragraph_runs(shape.caption.text.paragraphs) == ["Caption Sample"]


def test_set_slide_placeholder_text_ignores_a_stale_primary_case() -> None:
    paragraph = Paragraph(contents=[Constituent(run=TextRun(string="Fill me"))])
    canvas = CanvasObject.union_of(
        "image",
        image=Image(resource=Resource(indirect=IndirectResource(filename="photo.jpg"))),
        textbox=Textbox(text=Text(paragraphs=[paragraph])),
    )
    canvas.image = None
    obj = SlideObject(
        object=canvas,
        source_kind=SourceKind.PLACEHOLDER,
        placeholder_info=PlaceholderInfo(tagged="Shared"),
    )
    slide = Slide(contents=[obj])
    assert canvas.union_primary_name() == "textbox"
    assert set_slide_placeholder_text(slide, "Shared", "Fill me")


def test_set_resolves_by_kind_when_name_is_shared() -> None:
    for contents in (
        [
            _image_object(
                "photo.jpg", source_kind=SourceKind.PLACEHOLDER, tag="Shared"
            ),
            _text_object("Fill me", source_kind=SourceKind.PLACEHOLDER, tag="Shared"),
        ],
        [
            _text_object("Fill me", source_kind=SourceKind.PLACEHOLDER, tag="Shared"),
            _image_object(
                "photo.jpg", source_kind=SourceKind.PLACEHOLDER, tag="Shared"
            ),
        ],
    ):
        slide = Slide(contents=contents)
        assert _paragraph_runs(
            set_slide_placeholder_text(slide, "Shared", "Fill me")
        ) == ["Fill me"]
        image = set_slide_placeholder_image(slide, "Shared", _resource("p.png"))
        assert image.resource.indirect is not None
        assert image.resource.indirect.filename == "p.png"


def test_summarize_slide_layouts_lists_layouts_and_names(theme: KeynoteTheme) -> None:
    assert summarize_slide_layouts(theme) == {
        "Title": [
            LayoutPlaceholderSummary(
                name="TITLE",
                object_case="textbox",
                prompt="Title Text",
                tag=None,
            ),
            LayoutPlaceholderSummary(
                name="Caption",
                object_case="textbox",
                prompt="Caption",
                tag="Caption",
            ),
        ]
    }


def test_summarize_slide_layouts_summary_carries_object_case_prompt_and_tag() -> None:
    layout = [
        _text_object(
            "Type a quote here.", source_kind=SourceKind.PLACEHOLDER, tag="Text"
        ),
        _image_object("sample.jpg", source_kind=SourceKind.PLACEHOLDER, tag="Media"),
    ]
    theme = KeynoteTheme(
        name="T", slide_layouts=[SlideLayout(name="Quote", contents=layout)]
    )
    assert summarize_slide_layouts(theme) == {
        "Quote": [
            LayoutPlaceholderSummary(
                name="Text",
                object_case="textbox",
                prompt="Type a quote here.",
                tag="Text",
            ),
            LayoutPlaceholderSummary(
                name="Media", object_case="image", prompt=None, tag="Media"
            ),
        ]
    }


def test_empty_theme_has_no_layouts() -> None:
    empty = KeynoteTheme(name="Empty")
    assert summarize_slide_layouts(empty) == {}


def test_slide_from_layout_copies_placeholders_and_clears(theme: KeynoteTheme) -> None:
    slide = slide_from_layout(theme, "Title")

    assert slide.layout == "Title"
    for name in ("TITLE", "Caption"):
        assert _paragraph_runs(set_slide_placeholder_text(slide, name, None)) in (
            [],
            [None],
        )


def test_slide_from_layout_empties_hidden_title_and_body_definitions() -> None:
    layout = [
        _text_object(
            "Body Level One",
            source_kind=None,
            kind=PlaceholderKind.BODY,
            is_visible=False,
        ),
    ]
    theme = KeynoteTheme(
        name="T", slide_layouts=[SlideLayout(name="L", contents=layout)]
    )

    from creator_studio_doc_format.authoring._slide_layouts import _first_text

    slide = slide_from_layout(theme, "L")
    assert slide.contents is not None
    text = _first_text(slide.contents[0])
    assert text is not None and text.paragraphs is not None
    assert len(text.paragraphs) == 1
    assert not text.paragraphs[0].contents


def test_slide_from_layout_resets_was_media_replaced() -> None:
    obj = _image_object("sample.jpg", source_kind=SourceKind.PLACEHOLDER, tag="Media")
    assert obj.object is not None and obj.object.image is not None
    obj.object.image.was_media_replaced = True
    theme = KeynoteTheme(
        name="T", slide_layouts=[SlideLayout(name="L", contents=[obj])]
    )

    made_contents = slide_from_layout(theme, "L").contents
    assert made_contents is not None
    made = made_contents[0]
    assert made.object is not None and made.object.image is not None
    assert made.object.image.was_media_replaced is False

    unset = _image_object("s.jpg", source_kind=SourceKind.PLACEHOLDER, tag="Media")
    theme2 = KeynoteTheme(
        name="T", slide_layouts=[SlideLayout(name="L", contents=[unset])]
    )
    got_contents = slide_from_layout(theme2, "L").contents
    assert got_contents is not None
    got = got_contents[0]
    assert got.object is not None and got.object.image is not None
    assert "was_media_replaced" not in got.object.image.model_dump(mode="json")


def test_slide_from_layout_keeps_layout_object_was_media_replaced_when_layering() -> (
    None
):
    deco = _image_object("deco.png", source_kind=SourceKind.LAYOUT, tag="Deco")
    assert deco.object is not None and deco.object.image is not None
    deco.object.image.was_media_replaced = True
    theme = KeynoteTheme(
        name="T",
        slide_layouts=[
            SlideLayout(name="L", contents=[deco], slide_objects_layer_with_layout=True)
        ],
    )

    made_contents = slide_from_layout(theme, "L").contents
    assert made_contents is not None
    made = made_contents[0]
    assert made.object is not None and made.object.image is not None
    assert made.object.image.was_media_replaced is True


def test_slide_from_layout_carries_hidden_definitions_except_object() -> None:
    layout = [
        _text_object(
            "Title", source_kind=SourceKind.PLACEHOLDER, kind=PlaceholderKind.TITLE
        ),
        _text_object(
            "Body", source_kind=None, kind=PlaceholderKind.BODY, is_visible=False
        ),
        _text_object(
            "Slide number",
            source_kind=None,
            kind=PlaceholderKind.SLIDE_NUMBER,
            is_visible=False,
        ),
        _text_object(
            "Object", source_kind=None, kind=PlaceholderKind.OBJECT, is_visible=False
        ),
    ]
    theme = KeynoteTheme(
        name="T", slide_layouts=[SlideLayout(name="L", contents=layout)]
    )

    slide = slide_from_layout(theme, "L")

    from creator_studio_doc_format.authoring._slide_layouts import _placeholder_name

    assert slide.contents is not None
    assert [(_placeholder_name(o), o.source_kind) for o in slide.contents] == [
        ("TITLE", SourceKind.PLACEHOLDER),
        ("BODY", None),
        ("SLIDE_NUMBER", None),
    ]


def test_slide_from_layout_drops_instructional_text() -> None:
    obj = _text_object("Prompt", source_kind=SourceKind.PLACEHOLDER, tag="Text")
    obj.instructional_text = "Presentation Title"
    theme = KeynoteTheme(
        name="T", slide_layouts=[SlideLayout(name="L", contents=[obj])]
    )

    slide = slide_from_layout(theme, "L")

    assert slide.contents is not None
    assert slide.contents[0].instructional_text is None
    assert obj.instructional_text == "Presentation Title"


def test_slide_from_layout_clears_only_title_and_body_prompts() -> None:
    from creator_studio_doc_format.authoring._slide_layouts import (
        _first_text,
        _live_placeholders,
    )
    from creator_studio_doc_format.core import (
        RGBA,
        CharacterProperties,
        Color,
        Fill,
        Override,
    )

    accent = CharacterProperties(
        character_fill=Override.value(
            Fill(color=Color(rgba=RGBA(red=0.0, green=0.0, blue=1.0)))
        )
    )
    nav = Paragraph(
        contents=[
            Constituent(run=TextRun(string="Why Us", style=accent)),
            Constituent(run=TextRun(string="\tGoals")),
        ]
    )
    tagged = SlideObject(
        object=CanvasObject(textbox=Textbox(text=Text(paragraphs=[nav]))),
        source_kind=SourceKind.PLACEHOLDER,
        placeholder_info=PlaceholderInfo(tagged="Text-4"),
    )
    layout = [
        _text_object(
            "Title Text", source_kind=SourceKind.PLACEHOLDER, kind=PlaceholderKind.TITLE
        ),
        _text_object(
            "Body Level One",
            source_kind=SourceKind.PLACEHOLDER,
            kind=PlaceholderKind.BODY,
        ),
        tagged,
    ]
    theme = KeynoteTheme(
        name="T", slide_layouts=[SlideLayout(name="L", contents=layout)]
    )

    slide = slide_from_layout(theme, "L")

    assert _paragraph_runs(set_slide_placeholder_text(slide, "TITLE", None)) in (
        [],
        [None],
    )
    assert _paragraph_runs(set_slide_placeholder_text(slide, "BODY", None)) in (
        [],
        [None],
    )
    kept = _live_placeholders(slide)[2]
    text = _first_text(kept)
    assert text is not None and text.paragraphs is not None
    contents = text.paragraphs[0].contents
    assert contents is not None
    assert [c.run.string for c in contents if c.run] == ["Why Us", "\tGoals"]
    assert contents[0].run is not None and contents[0].run.style == accent
    assert contents[1].run is not None and contents[1].run.style is None


def test_slide_from_layout_keeps_layout_objects_only_when_layering() -> None:
    deco = _text_object("Decoration", source_kind=SourceKind.LAYOUT)
    title = _text_object(
        "Title", source_kind=SourceKind.PLACEHOLDER, kind=PlaceholderKind.TITLE
    )

    def kinds(*, layers: bool) -> list[SourceKind | None]:
        theme = KeynoteTheme(
            name="T",
            slide_layouts=[
                SlideLayout(
                    name="L",
                    contents=[deco, title],
                    slide_objects_layer_with_layout=layers,
                )
            ],
        )
        contents = slide_from_layout(theme, "L").contents
        assert contents is not None
        return [o.source_kind for o in contents]

    assert kinds(layers=False) == [SourceKind.PLACEHOLDER]
    assert kinds(layers=True) == [SourceKind.LAYOUT, SourceKind.PLACEHOLDER]


def test_slide_from_layout_unknown_layout_raises(theme: KeynoteTheme) -> None:
    with pytest.raises(KeyError, match="No layout 'Nonexistent'. Available: '"):
        slide_from_layout(theme, "Nonexistent")


def test_slide_from_layout_resolves_layouts_like_keynote() -> None:
    def layout(name: str, prompt: str, identifier: str | None = None) -> SlideLayout:
        obj = _text_object(prompt, source_kind=SourceKind.PLACEHOLDER, tag="Note")
        return SlideLayout(name=name, identifier=identifier, contents=[obj])

    theme = KeynoteTheme(
        name="T",
        slide_layouts=[
            layout("Title", "first"),
            layout("title", "second"),
            layout("Other", "by id", identifier="Plain"),
            layout("Plain", "by name"),
        ],
    )

    def prompt(layout_name: str) -> str | None:
        return summarize_slide_layouts(theme)[layout_name][0].prompt

    assert list(summarize_slide_layouts(theme)) == ["Title", "Other"]
    assert prompt("Title") == "first"

    def built(layout_name: str) -> list[str | None]:
        contents = slide_from_layout(theme, layout_name).contents
        assert contents is not None
        return _paragraph_runs(_first_text_of(contents[0]).paragraphs or [])

    assert built("title") == ["first"]
    assert built("Plain") == ["by id"]


def test_set_slide_placeholder_text_writes_lines_and_clears() -> None:
    obj = _text_object("Prompt", source_kind=SourceKind.PLACEHOLDER, tag="Body")
    slide = Slide(contents=[obj])

    assert _paragraph_runs(
        set_slide_placeholder_text(slide, "Body", ["One", "Two"])
    ) == [
        "One",
        "Two",
    ]

    cleared = set_slide_placeholder_text(slide, "Body", None)
    assert len(cleared) == 1
    assert not cleared[0].contents


def test_set_slide_placeholder_text_takes_a_str_as_one_paragraph() -> None:
    obj = _text_object("Prompt", source_kind=SourceKind.PLACEHOLDER, tag="Body")
    slide = Slide(contents=[obj])

    assert _paragraph_runs(set_slide_placeholder_text(slide, "Body", "a\nb")) == [
        "a\nb"
    ]
    assert _paragraph_runs(set_slide_placeholder_text(slide, "Body", "")) == [""]


def test_set_slide_placeholder_text_clears_on_an_empty_list() -> None:
    obj = _text_object("Prompt", source_kind=SourceKind.PLACEHOLDER, tag="Body")
    slide = Slide(contents=[obj])
    cleared = set_slide_placeholder_text(slide, "Body", [])
    assert cleared == set_slide_placeholder_text(slide, "Body", None)
    assert len(cleared) == 1
    assert not cleared[0].contents


def test_slide_from_layout_then_set_preserves_run_style() -> None:
    from creator_studio_doc_format.core import (
        RGBA,
        CharacterProperties,
        Color,
        Fill,
        Override,
    )

    style = CharacterProperties(
        character_fill=Override.value(
            Fill(color=Color(rgba=RGBA(red=1.0, green=0.0, blue=0.0)))
        )
    )
    run = TextRun(string="Prompt", style=style)
    textbox = Textbox(
        text=Text(paragraphs=[Paragraph(contents=[Constituent(run=run)])])
    )
    obj = SlideObject(
        object=CanvasObject(textbox=textbox),
        source_kind=SourceKind.PLACEHOLDER,
        placeholder_info=PlaceholderInfo(tagged="Title"),
    )
    theme = KeynoteTheme(
        name="T", slide_layouts=[SlideLayout(name="L", contents=[obj])]
    )

    slide = slide_from_layout(theme, "L")
    paragraphs = set_slide_placeholder_text(slide, "Title", "Hello")
    assert _paragraph_runs(paragraphs) == ["Hello"]
    contents = paragraphs[0].contents
    assert contents is not None and contents[0].run is not None
    filled_style = contents[0].run.style
    assert filled_style is not None
    assert filled_style == style


def test_set_slide_placeholder_text_on_textless_placeholder_raises() -> None:
    from creator_studio_doc_format.core import Shape

    obj = SlideObject(
        object=CanvasObject(shape=Shape()),
        source_kind=SourceKind.PLACEHOLDER,
        placeholder_info=PlaceholderInfo(tagged="Empty"),
    )
    slide = Slide(contents=[obj])
    with pytest.raises(TypeError):
        set_slide_placeholder_text(slide, "Empty", "x")


def test_summarize_slide_layouts_captioned_image_has_no_prompt() -> None:
    from creator_studio_doc_format.core import Label

    caption = Label(
        text=Text(
            paragraphs=[Paragraph(contents=[Constituent(run=TextRun(string="Cap"))])]
        )
    )
    image = Image(
        resource=Resource(indirect=IndirectResource(filename="p.jpg")),
        caption=caption,
        is_placeholder=True,
    )
    obj = SlideObject(
        object=CanvasObject(image=image),
        source_kind=SourceKind.PLACEHOLDER,
        placeholder_info=PlaceholderInfo(tagged="Media"),
    )
    theme = KeynoteTheme(
        name="T", slide_layouts=[SlideLayout(name="L", contents=[obj])]
    )
    assert summarize_slide_layouts(theme) == {
        "L": [
            LayoutPlaceholderSummary(
                name="Media", object_case="image", prompt=None, tag="Media"
            )
        ]
    }


def test_summarize_slide_layouts_collapses_same_named_same_kind_placeholders() -> None:
    layout = [
        _text_object("First", source_kind=SourceKind.PLACEHOLDER, tag="Text"),
        _text_object("Second", source_kind=SourceKind.PLACEHOLDER, tag="Text"),
        _image_object("a.jpg", source_kind=SourceKind.PLACEHOLDER, tag="Both"),
        _text_object("Body", source_kind=SourceKind.PLACEHOLDER, tag="Both"),
    ]
    theme = KeynoteTheme(
        name="T", slide_layouts=[SlideLayout(name="L", contents=layout)]
    )
    assert summarize_slide_layouts(theme) == {
        "L": [
            LayoutPlaceholderSummary(
                name="Text", object_case="textbox", prompt="First", tag="Text"
            ),
            LayoutPlaceholderSummary(
                name="Both", object_case="image", prompt=None, tag="Both"
            ),
            LayoutPlaceholderSummary(
                name="Both", object_case="textbox", prompt="Body", tag="Both"
            ),
        ]
    }


def test_set_slide_placeholder_text_does_not_alias_run_style_across_lines() -> None:
    from creator_studio_doc_format.core import CharacterProperties

    run = TextRun(string="P", style=CharacterProperties())
    textbox = Textbox(
        text=Text(paragraphs=[Paragraph(contents=[Constituent(run=run)])])
    )
    obj = SlideObject(
        object=CanvasObject(textbox=textbox),
        source_kind=SourceKind.PLACEHOLDER,
        placeholder_info=PlaceholderInfo(tagged="Body"),
    )
    slide = Slide(contents=[obj])

    paragraphs = set_slide_placeholder_text(slide, "Body", ["One", "Two"])
    c0, c1 = paragraphs[0].contents, paragraphs[1].contents
    assert c0 is not None and c1 is not None
    r0, r1 = c0[0].run, c1[0].run
    assert r0 is not None and r1 is not None
    assert r0.style is not r1.style
    assert r0.style == r1.style


def test_set_slide_placeholder_image_swaps_resource_and_flags() -> None:
    image = Image(
        resource=Resource(
            indirect=IndirectResource(
                filename="theme_sample.jpg",
                identifier="stale-id",
            )
        )
    )
    resource = _resource("myphoto.png")

    returned = set_slide_placeholder_image(_media_slide(image), "Media", resource)

    assert returned is image
    assert image.resource == resource
    assert image.was_media_replaced is True


def test_set_slide_placeholder_image_copies_resource() -> None:
    resource = Resource(
        indirect=IndirectResource(filename="sample.jpg", identifier="data-key")
    )

    def media() -> Slide:
        return _media_slide(Image(resource=_resource("old.png")))

    a = set_slide_placeholder_image(media(), "Media", resource)
    b = set_slide_placeholder_image(media(), "Media", resource)

    assert a.resource is not resource
    assert a.resource is not b.resource
    assert a.resource.indirect is not None
    assert a.resource.indirect.identifier == "data-key"


def _masked_image() -> Image:
    return Image(
        resource=Resource(indirect=IndirectResource(filename="theme.jpg")),
        geometry=Geometry(
            position=Position(x=-3, y=-96), size=Size(width=1926, height=1271)
        ),
        mask=Mask(
            geometry=Geometry(
                position=Position(x=0, y=0), size=Size(width=1920, height=1080)
            )
        ),
    )


def test_set_slide_placeholder_image_without_size_keeps_geometry() -> None:
    image = _masked_image()
    set_slide_placeholder_image(_media_slide(image), "Media", _resource("new.png"))

    assert image.geometry is not None
    assert image.geometry.position.x == -3
    assert image.geometry.position.y == -96
    assert image.geometry.size.width == 1926
    assert image.geometry.size.height == 1271


@pytest.mark.parametrize(
    "size",
    [Size(width=0, height=792), Size(width=1200, height=-792)],
)
def test_set_slide_placeholder_image_rejects_non_positive_size(
    size: Size,
) -> None:
    image = _masked_image()
    before = image.model_copy(deep=True)

    with pytest.raises(ValueError, match="`size`"):
        set_slide_placeholder_image(
            _media_slide(image), "Media", _resource("new.png"), size=size
        )

    assert image == before


def test_set_slide_placeholder_image_drops_instant_alpha() -> None:
    image = Image(
        resource=_resource("theme.png"),
        instant_alpha_path=InstantAlphaPath(path="M 0,0 L 1,0 L 1,1 Z"),
    )

    set_slide_placeholder_image(_media_slide(image), "Media", _resource("new.png"))

    assert image.instant_alpha_path is None


def _leveled_theme(*, identifier: str | None = None) -> KeynoteTheme:
    from creator_studio_doc_format.core import ParagraphProperties

    def sample(level: int | None, preset: str) -> Paragraph:
        return Paragraph(
            list_level=level,
            style=ParagraphProperties(preset_identifier=preset),
            contents=[Constituent(run=TextRun(string=f"Body Level {level}"))],
        )

    body = _text_object(
        "", source_kind=SourceKind.PLACEHOLDER, kind=PlaceholderKind.BODY
    )
    text = _first_text_of(body)
    text.paragraphs = [sample(None, "Subtitle"), sample(1, "Deep"), sample(2, "Deeper")]
    layout = SlideLayout(name="Photo", identifier=identifier, contents=[body])
    return KeynoteTheme(name="T", slide_layouts=[layout])


def _first_text_of(obj: SlideObject) -> Text:
    from creator_studio_doc_format.authoring._slide_layouts import _first_text

    text = _first_text(obj)
    assert text is not None
    return text


def _presets(paragraphs: list[Paragraph]) -> list[str | None]:
    return [p.style.preset_identifier if p.style else None for p in paragraphs]


def test_list_levels_clone_the_slide_paragraph_not_the_layout_sample() -> None:
    theme = _leveled_theme()
    slide = slide_from_layout(theme, "Photo")
    paragraphs = set_slide_placeholder_text(
        slide, "BODY", ["a", "b"], list_levels=[0, 1]
    )

    assert [p.list_level for p in paragraphs] == [None, 1]
    assert _presets(paragraphs) == ["Subtitle", "Subtitle"]


def test_list_levels_ignore_the_slide_existing_levels() -> None:
    from creator_studio_doc_format.core import ParagraphProperties

    body = _text_object(
        "", source_kind=SourceKind.PLACEHOLDER, kind=PlaceholderKind.BODY
    )
    _first_text_of(body).paragraphs = [
        Paragraph(style=ParagraphProperties(preset_identifier="First")),
        Paragraph(list_level=2, style=ParagraphProperties(preset_identifier="Old")),
    ]
    paragraphs = set_slide_placeholder_text(
        Slide(contents=[body]), "BODY", ["x", "y"], list_levels=[0, 2]
    )

    assert _presets(paragraphs) == ["First", "First"]
    assert [p.list_level for p in paragraphs] == [None, 2]


def test_lines_do_not_repeat_the_template_list_start_or_break() -> None:
    from creator_studio_doc_format.core import BreakType

    theme = _leveled_theme()
    assert theme.slide_layouts is not None
    layout_contents = theme.slide_layouts[0].contents
    assert layout_contents is not None
    samples = _first_text_of(layout_contents[0]).paragraphs
    assert samples is not None
    samples[0].list_start = 1
    samples[0].break_type = BreakType.COLUMN
    slide = slide_from_layout(theme, "Photo")
    paragraphs = set_slide_placeholder_text(
        slide, "BODY", ["a", "b", "c"], list_levels=[0, 0, 0]
    )

    assert [p.list_start for p in paragraphs] == [1, None, None]
    assert [p.break_type for p in paragraphs] == [None, None, None]
    assert _presets(paragraphs) == ["Subtitle", "Subtitle", "Subtitle"]


def test_lines_keep_the_template_writing_direction() -> None:
    from creator_studio_doc_format.core import WritingDirectionType

    obj = _text_object("Prompt", source_kind=SourceKind.PLACEHOLDER, tag="Body")
    template = _first_text_of(obj).paragraphs
    assert template is not None
    template[0].writing_direction = WritingDirectionType.RIGHT_TO_LEFT
    paragraphs = set_slide_placeholder_text(Slide(contents=[obj]), "Body", ["a", "b"])

    assert [p.writing_direction for p in paragraphs] == [
        WritingDirectionType.RIGHT_TO_LEFT,
        WritingDirectionType.RIGHT_TO_LEFT,
    ]


def test_list_levels_must_match_lines() -> None:
    slide = slide_from_layout(_leveled_theme(), "Photo")
    with pytest.raises(ValueError, match="list_levels"):
        set_slide_placeholder_text(slide, "BODY", ["a", "b"], list_levels=[0])
    with pytest.raises(ValueError, match="list_levels"):
        set_slide_placeholder_text(slide, "BODY", "a", list_levels=[0, 1])
    for level in (-1, 9):
        with pytest.raises(ValueError, match="list_levels"):
            set_slide_placeholder_text(slide, "BODY", ["a"], list_levels=[level])


def test_unsupported_object_is_an_ordinary_image_placeholder() -> None:
    unsupported = _image_object(
        "unsupported-object.pdf", source_kind=SourceKind.PLACEHOLDER, tag="Live Video"
    )
    assert unsupported.object is not None and unsupported.object.image is not None
    unsupported.object.image.is_placeholder = False
    theme = KeynoteTheme(
        name="T", slide_layouts=[SlideLayout(name="L", contents=[unsupported])]
    )
    assert [(p.name, p.object_case) for p in summarize_slide_layouts(theme)["L"]] == [
        ("Live Video", "image")
    ]

    image = set_slide_placeholder_image(
        Slide(contents=[unsupported]), "Live Video", _resource("new.png")
    )
    assert image.resource == _resource("new.png")
    assert image.is_placeholder is False
    assert image.was_media_replaced is True


def _payload(obj: SlideObject) -> Any:
    case = obj.object.union_primary()
    assert case is not None
    payload = case[1]
    while isinstance(payload, TaggedUnionModel):
        inner = payload.union_primary()
        assert inner is not None
        payload = inner[1]
    return payload


def test_slide_from_layout_renews_identifiers_and_remaps_connection_anchors() -> None:
    line = ConnectionLine(
        tail=End(end_point=Position(x=0, y=0), anchor=Anchor(object_id="a")),
        head=End(end_point=Position(x=1, y=0), anchor=Anchor(object_id="b")),
    )
    layout = SlideLayout(
        name="L",
        contents=[
            SlideObject(object=CanvasObject(shape=Shape(identifier="a"))),
            SlideObject(
                object=CanvasObject(chart=Chart(column=ColumnChart(identifier="b")))
            ),
            SlideObject(object=CanvasObject(connectionLine=line)),
        ],
    )

    slide = slide_from_layout(KeynoteTheme(slide_layouts=[layout]), "L")

    assert slide.contents is not None
    a, b, joined = (_payload(o) for o in slide.contents)
    assert {a.identifier, b.identifier}.isdisjoint({"a", "b"})
    assert a.identifier != b.identifier
    assert joined.tail.anchor.object_id == a.identifier
    assert joined.head.anchor.object_id == b.identifier
    assert layout.contents is not None
    assert _payload(layout.contents[0]).identifier == "a"


def test_slide_from_layout_renews_group_children_and_remaps_their_anchors() -> None:
    line = ConnectionLine(
        tail=End(end_point=Position(x=0, y=0), anchor=Anchor(object_id="a")),
        head=End(end_point=Position(x=1, y=0), anchor=Anchor(object_id="b")),
    )
    group = Group(
        identifier="g",
        children=[
            CanvasObject(shape=Shape(identifier="a")),
            CanvasObject(shape=Shape(identifier="b")),
            CanvasObject(connectionLine=line),
        ],
    )
    layout = SlideLayout(
        name="L", contents=[SlideObject(object=CanvasObject(group=group))]
    )

    slide = slide_from_layout(KeynoteTheme(slide_layouts=[layout]), "L")

    assert slide.contents is not None
    renewed = _payload(slide.contents[0])
    a, b, joined = (c.union_primary()[1] for c in renewed.children)
    assert {renewed.identifier, a.identifier, b.identifier}.isdisjoint({"g", "a", "b"})
    assert joined.tail.anchor.object_id == a.identifier
    assert joined.head.anchor.object_id == b.identifier


def test_slide_from_layout_remaps_cross_table_formula_references() -> None:
    ref = CellReference(
        placeholder="{ref0}",
        start_row_identifier="r",
        start_column_identifier="c",
        table_identifier="source",
    )
    source = Table(
        identifier="source",
        number_of_columns=1,
        number_of_rows=1,
        column_headers=[ColumnHeader(column_identifier="c")],
        content=[Row(row_identifier="r", cells=[Cell(value="1")])],
    )
    target = Table(
        identifier="target",
        number_of_columns=1,
        number_of_rows=1,
        content=[
            Row(
                cells=[
                    Cell(
                        value="1",
                        formula=Formula(
                            id_based=IdBasedFormula(
                                expression="={ref0}", references=[ref]
                            )
                        ),
                    )
                ]
            )
        ],
    )
    layout = SlideLayout(
        name="L",
        contents=[
            SlideObject(object=CanvasObject(table=source)),
            SlideObject(object=CanvasObject(table=target)),
        ],
    )

    slide = slide_from_layout(KeynoteTheme(slide_layouts=[layout]), "L")

    assert slide.contents is not None
    renewed_source, renewed_target = (_payload(o) for o in slide.contents)
    assert renewed_source.identifier != "source"
    renewed_ref = renewed_target.content[0].cells[0].formula.id_based.references[0]
    assert renewed_ref.table_identifier == renewed_source.identifier


def test_slide_from_layout_keeps_the_identifier_of_a_layout_sourced_object() -> None:
    layout = SlideLayout(
        name="L",
        slide_objects_layer_with_layout=True,
        contents=[
            SlideObject(
                object=CanvasObject(shape=Shape(identifier="deco")),
                source_kind=SourceKind.LAYOUT,
            )
        ],
    )

    slide = slide_from_layout(KeynoteTheme(slide_layouts=[layout]), "L")

    assert slide.contents is not None
    assert _payload(slide.contents[0]).identifier == "deco"
