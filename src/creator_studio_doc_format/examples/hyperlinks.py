# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0

"""Build a presentation with a hyperlink of each target kind.

A hyperlink is a `Paragraph.Constituent` case, alongside `run` and `inline_object`.
`Hyperlink` is a union over four targets (`url`, `slide_jump`, `file`, and `program`),
so each `Hyperlink` sets exactly one field.

`SlideTarget` names a slide by identifier or by one of five position cases. A position
case doesn't depend on the identifiers in the document, so it's the dependable choice
when authoring. `by_identifier` is meaningful only against the identifiers of the
document that holds the link.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from creator_studio_doc_format.core import (
    RGBA,
    CanvasObject,
    CharacterProperties,
    Constituent,
    Fill,
    Geometry,
    Hyperlink,
    HyperlinkField,
    KeyxDocument,
    Paragraph,
    Position,
    Presentation,
    Preset,
    Size,
    Slide,
    SlideBackground,
    SlideObject,
    SlideTarget,
    Stroke,
    Text,
    Textbox,
    TextRun,
    UnderlineType,
)
from creator_studio_doc_format.validation import validate_document

_RGBA_WHITE = RGBA(red=1.0, green=1.0, blue=1.0)
_RGBA_INK = RGBA(red=0.1, green=0.1, blue=0.12)
_RGBA_LINK = RGBA(red=0.10, green=0.35, blue=0.85)
_WHITE_BG = Fill(preset_identifier="fill_slide_bg")
# `Textbox.stroke` defaults to a visible black line. An empty stroke draws no border.
_NO_BORDER = Stroke(empty=True)

_BODY_STYLE = CharacterProperties(
    font_size=40, character_fill=Fill(preset_identifier="fill_ink")
)
# Every hyperlink shares this style, whatever its target.
_LINK_STYLE = CharacterProperties(
    font_size=40,
    underline=UnderlineType.SINGLE,
    character_fill=Fill(preset_identifier="fill_link"),
)

_PRESETS = [
    Preset(
        identifier=name,
        properties={"color": {"rgba": rgba.model_dump(mode="json")}},
    )
    for name, rgba in [
        ("fill_slide_bg", _RGBA_WHITE),
        ("fill_ink", _RGBA_INK),
        ("fill_link", _RGBA_LINK),
    ]
]

_ID_COVER = "slide-cover"
_ID_APPENDIX = "slide-appendix"


def _plain(text: str) -> Constituent:
    return Constituent(run=TextRun(string=text, style=_BODY_STYLE))


def _linked(display: str, target: Hyperlink) -> Constituent:
    """Wraps ``display`` in a ``HyperlinkField`` that points at ``target``."""
    return Constituent(
        hyperlink=HyperlinkField(
            target=target,
            run=TextRun(string=display, style=_LINK_STYLE),
        )
    )


def _cover_slide() -> Slide:
    """Builds the cover slide, with one textbox that shows every ``Hyperlink`` case."""
    p1 = Paragraph(
        contents=[
            _plain("Visit "),
            _linked("example.com", Hyperlink(url="https://www.example.com")),
            _plain(", jump to the "),
            _linked(
                "appendix",
                Hyperlink(slide_jump=SlideTarget(by_identifier=_ID_APPENDIX)),
            ),
            _plain(", open the "),
            _linked("notes", Hyperlink(file="file:///tmp/notes.txt")),
            _plain(", or "),
            _linked("exit", Hyperlink(program="exit_slideshow")),
            _plain("."),
        ]
    )

    p2 = Paragraph(
        contents=[
            _plain("Navigate: "),
            _linked("next slide", Hyperlink(slide_jump=SlideTarget(next=True))),
            _plain("."),
        ]
    )

    textbox = SlideObject(
        object=CanvasObject(
            textbox=Textbox(
                stroke=_NO_BORDER,
                geometry=Geometry(
                    position=Position(x=160, y=380),
                    size=Size(width=1600, height=320),
                ),
                text=Text(paragraphs=[p1, p2]),
            )
        )
    )
    return Slide(
        identifier=_ID_COVER,
        contents=[textbox],
        background=SlideBackground(standard=_WHITE_BG),
    )


def _appendix_slide() -> Slide:
    """Builds the target slide for the ``by_identifier`` jump on the cover."""
    paragraph = Paragraph(
        contents=[
            _plain("Appendix: jump target for "),
            _linked(
                "the cover link",
                Hyperlink(slide_jump=SlideTarget(by_identifier=_ID_COVER)),
            ),
            _plain("."),
        ]
    )
    textbox = SlideObject(
        object=CanvasObject(
            textbox=Textbox(
                stroke=_NO_BORDER,
                geometry=Geometry(
                    position=Position(x=160, y=480),
                    size=Size(width=1600, height=120),
                ),
                text=Text(paragraphs=[paragraph]),
            )
        )
    )
    return Slide(
        identifier=_ID_APPENDIX,
        contents=[textbox],
        background=SlideBackground(standard=_WHITE_BG),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.partition("\n")[0])
    parser.add_argument(
        "output", type=Path, nargs="?", default=Path("tmp/hyperlinks.keyx")
    )
    args = parser.parse_args()

    doc = KeyxDocument(
        payload=Presentation(
            slide_size=Size(width=1920, height=1080),
            slides=[_cover_slide(), _appendix_slide()],
        ),
        presets=_PRESETS,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(args.output, pre_save_hooks=[validate_document])
    print(f"wrote {args.output} ({args.output.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
