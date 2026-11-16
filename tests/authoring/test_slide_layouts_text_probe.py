# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


from __future__ import annotations

from pathlib import Path

import pytest

from creator_studio_doc_format.authoring import (
    set_slide_placeholder_text,
    slide_from_layout,
)
from creator_studio_doc_format.authoring._slide_layouts import (
    _first_text,
    _live_placeholders,
    _placeholder_name,
)
from creator_studio_doc_format.core import KeyxDocument, Paragraph, Slide, Text

FIXTURE = Path(__file__).parents[1] / "fixtures" / "text_probe_typed.keyx"
_DOC = KeyxDocument.open(FIXTURE)


def _text(slide: Slide, name: str) -> Text:
    obj = next(o for o in _live_placeholders(slide) if _placeholder_name(o) == name)
    text = _first_text(obj)
    assert text is not None
    return text


def _typed() -> list[tuple[int, str]]:
    return [
        (i, name)
        for i, slide in enumerate(_DOC.presentation.slides)
        for o in _live_placeholders(slide)
        if (name := _placeholder_name(o)) is not None and _first_text(o) is not None
    ]


def _line(paragraph: Paragraph) -> str:
    return "".join(c.run.string for c in paragraph.contents or [] if c.run is not None)


@pytest.mark.parametrize(
    ("index", "name"), [pytest.param(i, n, id=f"{i}-{n}") for i, n in _typed()]
)
def test_typed_text_matches_keynote(index: int, name: str) -> None:
    theme = _DOC.presentation.theme
    assert theme is not None
    saved = _DOC.presentation.slides[index]
    assert saved.layout is not None
    want = _text(saved, name).paragraphs or []
    lines = [_line(p) for p in want]
    levels = [p.list_level or 0 for p in want]
    made = slide_from_layout(theme, saved.layout)

    set_slide_placeholder_text(
        made,
        name,
        None if lines == [""] else lines,
        list_levels=None if lines == [""] else levels,
    )

    assert _text(made, name).paragraphs == want
