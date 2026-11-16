# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


from __future__ import annotations

import copy
import math
import uuid
from dataclasses import dataclass
from typing import Any, Literal

from creator_studio_doc_format._slide_layout_refs import resolve_slide_layout
from creator_studio_doc_format.core import (
    Anchor,
    CanvasObject,
    CellReference,
    CharacterProperties,
    Constituent,
    Geometry,
    Image,
    KeynoteTheme,
    Label,
    Mask,
    Paragraph,
    Position,
    Reference,
    Resource,
    Size,
    Slide,
    SlideObject,
    SourceKind,
    TaggedUnionModel,
    Text,
    TextRun,
)
from creator_studio_doc_format.core import (
    SlideObjectPlaceholderInfoPlaceholderDefinitionKind as PlaceholderKind,
)
from creator_studio_doc_format.navigation import iterate_models

_CLEARED_KINDS = frozenset({PlaceholderKind.TITLE, PlaceholderKind.BODY})


def _set_only_case(enum: TaggedUnionModel, case: str, value: Any) -> None:
    for case_name, _added, _valueless in type(enum).__wire_cases__:
        setattr(enum, case_name, value if case_name == case else None)


def _styled_line(
    template: Paragraph, line: str, style: CharacterProperties | None
) -> Paragraph:
    return copy.deepcopy(
        Paragraph(
            style=template.style,
            list_style=template.list_style,
            list_level=template.list_level,
            writing_direction=template.writing_direction,
            contents=[Constituent(run=TextRun(string=line, style=style))],
        )
    )


def _run_style(paragraph: Paragraph) -> CharacterProperties | None:
    return next(
        (
            c.run.style
            for c in paragraph.contents or []
            if c.run is not None and c.run.style is not None
        ),
        None,
    )


def _write_text(
    text: Text,
    lines: list[str],
    levels: list[int] | None = None,
) -> list[Paragraph]:
    if not text.paragraphs:
        _set_only_case(text, "string", "\n".join(lines))
        return []
    if not lines:
        cleared = text.paragraphs[0]
        cleared.contents = None
        paragraphs = [cleared]
    else:
        template = text.paragraphs[0]
        style = _run_style(template)
        paragraphs = []
        for line, level in zip(lines, levels or [None] * len(lines), strict=True):
            paragraph = _styled_line(template, line, style)
            if level is not None:
                paragraph.list_level = level or None
            paragraphs.append(paragraph)
        paragraphs[0].list_start = text.paragraphs[0].list_start
    _set_only_case(text, "paragraphs", paragraphs)
    return paragraphs


def _live_placeholders(slide: Slide) -> list[SlideObject]:
    out: list[SlideObject] = []
    for item in iterate_models(slide):
        model = item.model
        if (
            isinstance(model, SlideObject)
            and model.source_kind == SourceKind.PLACEHOLDER
        ):
            out.append(model)
    return out


def _placeholder_name(obj: SlideObject) -> str | None:
    info = obj.placeholder_info
    if info is None:
        return None
    if info.defined is not None:
        return info.defined.kind.name
    return info.tagged


def _first_text(obj: SlideObject) -> Text | None:
    first: Text | None = None
    for item in iterate_models(obj):
        if not isinstance(item.model, Text):
            continue
        if first is None:
            first = item.model
        if not (item.ancestors and isinstance(item.ancestors[-1], Label)):
            return item.model
    return first


def _placeholder_prompt(obj: SlideObject) -> str | None:
    if not _accepts(obj, "text"):
        return None
    if obj.instructional_text:
        return obj.instructional_text
    text = _first_text(obj)
    if text is None:
        return None
    for paragraph in text.paragraphs or []:
        for c in paragraph.contents or []:
            if c.run is not None and c.run.string is not None:
                return c.run.string
    return text.string


def _placeholder_tag(obj: SlideObject) -> str | None:
    info = obj.placeholder_info
    return info.tagged if info is not None else None


_MEDIA_CASES = frozenset({"audio", "image", "movie"})


def _accepts(obj: SlideObject, want: Literal["text", "image"]) -> bool:
    case = obj.object.union_primary_name()
    return case == "image" if want == "image" else case not in _MEDIA_CASES


def _resolve_placeholder(
    slide: Slide, name: str, *, want: Literal["text", "image"]
) -> SlideObject:
    live = _live_placeholders(slide)
    matches = [o for o in live if _placeholder_name(o) == name]
    if not matches:
        available = dict.fromkeys(n for o in live if (n := _placeholder_name(o)))
        raise KeyError(
            f"No placeholder {name!r}. Available: {', '.join(map(repr, available))}"
        )
    typed = next((o for o in matches if _accepts(o, want)), None)
    if typed is None:
        raise TypeError(f"Placeholder {name!r} isn't a {want} placeholder")
    return typed


def set_slide_placeholder_text(
    slide: Slide,
    placeholder_name: str,
    lines: str | list[str] | None,
    *,
    list_levels: list[int] | None = None,
) -> list[Paragraph]:
    """Writes lines into a text placeholder and returns the paragraphs it wrote.

    Every line takes the placeholder's own paragraph and text style at every level. Some
    built-in themes style each level of the sample text differently, so a nested line
    needs that level's style. Set it on the returned paragraph.

    Args:
        slide: The slide to write into.
        placeholder_name: The text placeholder's name, as
            :func:`summarize_slide_layouts` reports it.
        lines: One paragraph's text, or a list with one text per paragraph. ``None``
            or ``[]`` clears the placeholder, and ``""`` writes an empty run.
        list_levels: Each line's list level, from 0 for the top level through 8, with
            one entry per line. A placeholder with text that is a plain string ignores
            it.

    Returns:
        list[Paragraph]: The paragraphs written into the placeholder. They're live, so
        changing one changes the slide. A placeholder with text that is a plain string
        has no paragraphs, so the result is ``[]`` and the function joins the lines
        with newlines.

    Raises:
        KeyError: No placeholder named ``placeholder_name`` exists on ``slide``.
        TypeError: ``placeholder_name`` names an image, movie, or audio placeholder, or
            a text placeholder that has no
            :class:`~creator_studio_doc_format.core.models.Text`.
        ValueError: ``list_levels`` has a different length than ``lines``, or a level
            outside 0 through 8.
    """  # noqa: DOC503 (`KeyError` is raised by `_resolve_placeholder`, not here)
    match lines:
        case None:
            lines = []
        case str():
            lines = [lines]
    if list_levels is not None and len(list_levels) != len(lines):
        raise ValueError(
            f"`list_levels` has {len(list_levels)} entries for {len(lines)} lines"
        )
    if list_levels is not None and any(not 0 <= lv <= 8 for lv in list_levels):
        raise ValueError(f"`list_levels` must be 0 through 8, not {list_levels}")
    obj = _resolve_placeholder(slide, placeholder_name, want="text")
    text = _first_text(obj)
    if text is None:
        raise TypeError(f"Placeholder {placeholder_name!r} has no text")
    return _write_text(text, lines, list_levels)


def set_slide_placeholder_image(
    slide: Slide,
    placeholder_name: str,
    resource: Resource,
    *,
    size: Size | None = None,
) -> Image:
    """Points an image placeholder at a resource and returns the image.

    Important:
        The function doesn't store the image's bytes. An indirect ``resource`` needs
        them in ``doc.resources``, and by default the document's ``save`` raises
        ``ValueError`` without them.

    Args:
        slide: The slide to write into.
        placeholder_name: The image placeholder's name, as
            :func:`summarize_slide_layouts` reports it.
        resource: The image's resource.
        size: The width and height of the image ``resource`` holds. The function then
            fills the placeholder's mask with the image and centers it there, as with
            Replace Image in Keynote. Only the aspect ratio matters. ``None`` keeps the
            placeholder's geometry, and the image stretches to it.

    Returns:
        Image: The placeholder's image, now pointing at ``resource``. It is live, so
        changing its ``geometry`` adjusts the crop.

    Raises:
        KeyError: No placeholder named ``placeholder_name`` exists on ``slide``.
        TypeError: ``placeholder_name`` names a text, movie, or audio placeholder.
        ValueError: ``size`` has a width or height that isn't positive.
    """  # noqa: DOC503 (`KeyError` is raised by `_resolve_placeholder`, not here)
    if size is not None and not (size.width > 0 and size.height > 0):
        raise ValueError(f"`size` must be positive, not {size}")
    obj = _resolve_placeholder(slide, placeholder_name, want="image")
    image = obj.object.image if obj.object is not None else None
    if image is None:
        raise TypeError(f"Placeholder {placeholder_name!r} has no image")
    image.resource = copy.deepcopy(resource)
    if size is not None:
        _fill_mask(image, size)
    image.instant_alpha_path = None
    image.description = None
    image.was_media_replaced = True
    return image


def _fill_mask(image: Image, size: Size) -> None:
    if image.mask is None:
        if image.geometry is None:
            return
        image.mask = Mask(geometry=image.geometry.model_copy(deep=True))
    if (frame := image.mask.geometry) is None:
        return
    scale = max(frame.size.width / size.width, frame.size.height / size.height)
    fitted = Size(width=size.width * scale, height=size.height * scale)
    if image.geometry is None:
        image.geometry = Geometry(position=Position(x=0, y=0), size=fitted)
    frame_w, frame_h = _bounds(frame.size, frame.angle)
    image_w, image_h = _bounds(fitted, image.geometry.angle)
    image.geometry.size = fitted
    image.geometry.position = Position(
        x=frame.position.x + (frame_w - image_w) / 2,
        y=frame.position.y + (frame_h - image_h) / 2,
    )


def _bounds(size: Size, angle: float) -> tuple[float, float]:
    cos, sin = abs(math.cos(math.radians(angle))), abs(math.sin(math.radians(angle)))
    return size.width * cos + size.height * sin, size.width * sin + size.height * cos


@dataclass(frozen=True)
class LayoutPlaceholderSummary:
    """A read-only summary of a placeholder in a slide layout.

    One summary stands for every placeholder that shares its name and setter. You don't
    create a summary directly. :func:`summarize_slide_layouts` returns them.
    """

    name: str
    """The placeholder's name within its layout, which a setter takes. A custom
    placeholder's name is its tag. Any other placeholder's name is its kind's member
    name, such as ``"TITLE"``."""

    object_case: str
    """The case the placeholder's canvas object holds. A text placeholder holds a case
    such as ``"shape"`` or ``"textbox"``, and an image placeholder holds ``"image"``."""

    prompt: str | None
    """The prompt or sample text Keynote shows in the placeholder. It's ``None`` when
    there's none, as for an image, movie, or audio placeholder."""

    tag: str | None
    """The label the theme's designer gives a custom placeholder. It's ``None`` for a
    predefined one such as ``"TITLE"``."""


def _setter_for(obj: SlideObject) -> str:
    if _accepts(obj, "image"):
        return "image"
    if _accepts(obj, "text"):
        return "text"
    return obj.object.union_primary_name() or "?"


def summarize_slide_layouts(
    theme: KeynoteTheme,
) -> dict[str, list[LayoutPlaceholderSummary]]:
    """Returns the placeholders of each slide layout.

    Args:
        theme: The theme that holds the slide layouts.

    Returns:
        dict[str, list[LayoutPlaceholderSummary]]: Each layout's placeholders, keyed by
        layout name, or ``{}`` when ``theme.slide_layouts`` is absent.
    """
    summaries: dict[str, list[LayoutPlaceholderSummary]] = {}
    for layout in theme.slide_layouts or []:
        if (
            layout.name is None
            or resolve_slide_layout(theme.slide_layouts or [], layout.name)
            is not layout
        ):
            continue
        placeholders: list[LayoutPlaceholderSummary] = []
        seen: set[tuple[str, str]] = set()
        for obj in _live_placeholders(Slide(contents=layout.contents)):
            name = _placeholder_name(obj)
            if name is None:
                continue
            setter = _setter_for(obj)
            if (name, setter) in seen:
                continue
            seen.add((name, setter))
            placeholders.append(
                LayoutPlaceholderSummary(
                    name=name,
                    object_case=obj.object.union_primary_name() or "?",
                    prompt=_placeholder_prompt(obj),
                    tag=_placeholder_tag(obj),
                )
            )
        summaries[layout.name] = placeholders
    return summaries


def _instantiates(obj: SlideObject, *, layers: bool) -> bool:
    match obj.source_kind:
        case SourceKind.PLACEHOLDER:
            return True
        case SourceKind.LAYOUT:
            return layers
        case None:
            defined = obj.placeholder_info.defined if obj.placeholder_info else None
            return defined is None or defined.kind != PlaceholderKind.OBJECT
        case _:
            return False


def _renew_identifiers(objs: list[SlideObject]) -> None:
    renamed: dict[str, str] = {}
    anchors: list[Anchor] = []
    table_refs: list[CellReference | Reference] = []
    for item in (i for obj in objs for i in iterate_models(obj)):
        match item.model:
            case Anchor() as anchor:
                anchors.append(anchor)
                continue
            case CellReference() | Reference() as ref:
                table_refs.append(ref)
                continue
            case CanvasObject() as canvas_object:
                pass
            case _:
                continue
        if (primary := canvas_object.union_primary()) is None:
            continue
        payload = primary[1]
        while isinstance(payload, TaggedUnionModel):
            if (case := payload.union_primary()) is None:
                break
            payload = case[1]
        if (old := getattr(payload, "identifier", None)) is not None:
            renamed[old] = str(uuid.uuid4()).upper()
            setattr(payload, "identifier", renamed[old])  # noqa: B010
    for anchor in anchors:
        if anchor.object_id in renamed:
            anchor.object_id = renamed[anchor.object_id]
    for ref in table_refs:
        if ref.table_identifier in renamed:
            ref.table_identifier = renamed[ref.table_identifier]


def slide_from_layout(theme: KeynoteTheme, layout_name: str) -> Slide:
    """Returns a new slide made from a layout, as Keynote creates one.

    Args:
        theme: The theme to instantiate the layout from.
        layout_name: The layout's name, which is a key of the result of
            :func:`summarize_slide_layouts`.

    Returns:
        Slide: The new slide. Only its ``"TITLE"`` and ``"BODY"`` placeholders start
        empty. A custom placeholder keeps its sample text, and an image placeholder
        keeps its sample photo until a setter replaces it. Add the slide to
        ``presentation.slides`` to put it in a document.

    Raises:
        KeyError: ``layout_name`` matches no layout identifier or layout name in
            ``theme``.
    """
    layout = resolve_slide_layout(theme.slide_layouts or [], layout_name)
    if layout is None:
        available = [ts.name for ts in theme.slide_layouts or [] if ts.name]
        raise KeyError(
            f"No layout {layout_name!r}. Available: {', '.join(map(repr, available))}"
        )
    layers = layout.slide_objects_layer_with_layout
    contents: list[SlideObject] = []
    for obj in layout.contents or []:
        if not _instantiates(obj, layers=layers):
            continue
        copied = copy.deepcopy(obj)
        copied.instructional_text = None
        contents.append(copied)
    _renew_identifiers([o for o in contents if o.source_kind != SourceKind.LAYOUT])
    slide = Slide(layout=layout_name, contents=contents)
    for item in iterate_models(slide):
        model = item.model
        if isinstance(model, Image) and model.was_media_replaced:
            owner = next(
                (a for a in reversed(item.ancestors) if isinstance(a, SlideObject)),
                None,
            )
            if owner is not None and owner.source_kind == SourceKind.PLACEHOLDER:
                model.was_media_replaced = False
        if not isinstance(model, SlideObject):
            continue
        info = model.placeholder_info
        defined = None if info is None else info.defined
        if defined is None or defined.kind not in _CLEARED_KINDS:
            continue
        text = _first_text(model)
        if text is not None:
            _write_text(text, [])
    return slide


__all__ = [
    "LayoutPlaceholderSummary",
    "set_slide_placeholder_image",
    "set_slide_placeholder_text",
    "slide_from_layout",
    "summarize_slide_layouts",
]
