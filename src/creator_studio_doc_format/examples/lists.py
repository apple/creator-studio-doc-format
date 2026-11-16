# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0

"""Build a presentation with bulleted, numbered, and image bullet lists, and a rule.

Text and textbox styling here is deliberately minimal, with plain inline
`CharacterProperties` and `ParagraphProperties`, so the file stays focused on list
styles.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from creator_studio_doc_format.core import (
    RGBA,
    BorderStyleType,
    CanvasObject,
    CharacterProperties,
    Color,
    Constituent,
    Fill,
    Format,
    Geometry,
    IndirectResource,
    KeyxDocument,
    Line,
    ListImageLabel,
    ListLabelType,
    ListLevelType,
    ListNumberLabel,
    ListProperties,
    ListStringLabel,
    NumberFormatType,
    NumberFormatTypeKind,
    Paragraph,
    ParagraphProperties,
    Position,
    Presentation,
    Preset,
    Resource,
    Size,
    Slide,
    SlideBackground,
    SlideObject,
    Stroke,
    Text,
    Textbox,
    TextRun,
    TextStroke,
)
from creator_studio_doc_format.validation import validate_document

# `fixtures/bullet.png` is a small opaque PNG so the image bullet is visible.
FIXTURES = Path(__file__).parent / "fixtures"

_RGBA_OFF_WHITE = RGBA(red=0.96, green=0.94, blue=0.90)
_RGBA_ORANGE = RGBA(red=0.929, green=0.353, blue=0.157)

_TITLE_STYLE = CharacterProperties(font_size=96, bold=True)
_HEADING_STYLE = CharacterProperties(font_size=32, bold=True)
_BODY_STYLE = CharacterProperties(font_size=40)

# `Textbox.stroke` defaults to a visible black line. An empty stroke draws no border.
_NO_BORDER = Stroke(empty=True)


def _list_style(levels: list[ListLevelType]) -> ListProperties:
    return ListProperties(levels=levels)


BULLET_LEVELS = [
    ListLevelType(
        label_indent=0,
        text_indent=1.5,
        label=ListLabelType(string=ListStringLabel(string="•")),
    ),
    ListLevelType(
        label_indent=32,
        text_indent=3.0,
        label=ListLabelType(string=ListStringLabel(string="▸")),
    ),
]

NUMBERED_LEVELS = [
    ListLevelType(
        label_indent=0,
        text_indent=1.5,
        label=ListLabelType(
            number=ListNumberLabel(
                number_format=NumberFormatType(
                    kind=NumberFormatTypeKind.NUMERIC,
                    format=Format.DECIMAL,
                ),
            )
        ),
    ),
]

# The image bullet's resource must be in `doc.resources` under its
# `IndirectResource.identifier`, or under its `filename` when the identifier is unset.
# `scale=0.5` is half the image's pixel size. A leading space on each paragraph below
# separates it from the bullet.
IMAGE_LEVELS = [
    ListLevelType(
        label_indent=0,
        text_indent=1.8,
        label=ListLabelType(
            image=ListImageLabel(
                resource=Resource(indirect=IndirectResource(filename="bullet.png")),
                scale=0.5,
            )
        ),
    ),
]


def _slide() -> Slide:
    """Builds one slide with a title, three section headings, and three body blocks."""

    def _textbox(
        style: CharacterProperties, x: float, y: float, w: float, h: float, *, text: str
    ) -> SlideObject:
        return SlideObject(
            object=CanvasObject(
                textbox=Textbox(
                    stroke=_NO_BORDER,
                    geometry=Geometry(
                        position=Position(x=x, y=y), size=Size(width=w, height=h)
                    ),
                    text=Text(text_runs=[TextRun(string=text, style=style)]),
                )
            )
        )

    def _paragraph(
        list_style: ListProperties | None,
        text: str,
        *,
        list_start: int | None = None,
        list_level: int | None = None,
    ) -> Paragraph:
        # A paragraph doesn't inherit `list_style`, so every paragraph sets it. Omit
        # `list_level` for level 0. Numbering doesn't continue on its own, so every
        # numbered item that isn't "1" sets `list_start`.
        return Paragraph(
            list_style=list_style,
            list_start=list_start,
            list_level=list_level,
            contents=[Constituent(run=TextRun(string=text, style=_BODY_STYLE))],
        )

    title = _textbox(_TITLE_STYLE, 130, 60, 1660, 130, text="Advanced text")
    heading_a = _textbox(_HEADING_STYLE, 130, 220, 850, 50, text="LISTS")
    heading_b = _textbox(_HEADING_STYLE, 1020, 220, 770, 50, text="IMAGE BULLETS")
    heading_c = _textbox(_HEADING_STYLE, 1020, 620, 770, 50, text="PARAGRAPH RULE")

    numbered = _list_style(NUMBERED_LEVELS)
    bullet = _list_style(BULLET_LEVELS)
    block_a = SlideObject(
        object=CanvasObject(
            textbox=Textbox(
                stroke=_NO_BORDER,
                geometry=Geometry(
                    position=Position(x=130, y=280), size=Size(width=850, height=700)
                ),
                text=Text(
                    paragraphs=[
                        _paragraph(numbered, " list_start=1 → shows 1", list_start=1),
                        _paragraph(
                            numbered,
                            " no list_start → also shows 1, because numbering doesn't continue",
                        ),
                        _paragraph(
                            numbered,
                            " list_start=2 → shows 2 only when set explicitly",
                            list_start=2,
                        ),
                        _paragraph(
                            bullet, "Bullet at level 0, with list_level omitted"
                        ),
                        _paragraph(
                            bullet, "Nested bullet at list_level=1", list_level=1
                        ),
                        _paragraph(
                            bullet, "Back to level 0, with list_level omitted again"
                        ),
                        _paragraph(None, "Plain paragraph with no list_style at all"),
                    ]
                ),
            )
        )
    )

    image_bullet = _list_style(IMAGE_LEVELS)
    block_b = SlideObject(
        object=CanvasObject(
            textbox=Textbox(
                stroke=_NO_BORDER,
                geometry=Geometry(
                    position=Position(x=1020, y=280), size=Size(width=770, height=300)
                ),
                text=Text(
                    paragraphs=[
                        _paragraph(
                            image_bullet,
                            " Image bullet with its resource in doc.resources",
                            list_start=1,
                        ),
                        _paragraph(
                            image_bullet,
                            " Second image bullet at the same level, with the same resource",
                        ),
                    ]
                ),
            )
        )
    )

    rule_border = BorderStyleType(
        stroke=TextStroke(
            stroke=Stroke(
                line=Line(
                    width=2.0,
                    color=Color(preset_identifier="color_accent"),
                )
            )
        ),
        width=2.0,
        before=True,
    )
    block_c = SlideObject(
        object=CanvasObject(
            textbox=Textbox(
                stroke=_NO_BORDER,
                geometry=Geometry(
                    position=Position(x=1020, y=680), size=Size(width=770, height=300)
                ),
                text=Text(
                    paragraphs=[
                        Paragraph(
                            style=ParagraphProperties(borders=rule_border),
                            contents=[
                                Constituent(
                                    run=TextRun(
                                        string="Paragraph with a rule above (before=True)",
                                        style=_BODY_STYLE,
                                    )
                                )
                            ],
                        ),
                    ]
                ),
            )
        )
    )

    return Slide(
        contents=[title, heading_a, heading_b, heading_c, block_a, block_b, block_c],
        background=SlideBackground(standard=Fill(preset_identifier="fill_slide_bg")),
    )


def _presets() -> list[Preset]:
    return [
        Preset(
            identifier="color_accent",
            properties={"rgba": _RGBA_ORANGE.model_dump(mode="json")},
        ),
        Preset(
            identifier="fill_slide_bg",
            properties={"color": {"rgba": _RGBA_OFF_WHITE.model_dump(mode="json")}},
        ),
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.partition("\n")[0])
    parser.add_argument("output", type=Path, nargs="?", default=Path("tmp/lists.keyx"))
    args = parser.parse_args()

    doc = KeyxDocument(
        payload=Presentation(
            slide_size=Size(width=1920, height=1080),
            slides=[_slide()],
        ),
        presets=_presets(),
        resources={"bullet.png": (FIXTURES / "bullet.png").read_bytes()},
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(args.output, pre_save_hooks=[validate_document])
    print(f"wrote {args.output} ({args.output.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
