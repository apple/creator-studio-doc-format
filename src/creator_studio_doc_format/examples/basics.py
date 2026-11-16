# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0

"""Build a presentation of one slide with presets, text, shapes, and an image."""

from __future__ import annotations

import argparse
from pathlib import Path

from creator_studio_doc_format.core import (
    RGBA,
    AlignmentType,
    BezierPath,
    CanvasObject,
    CharacterProperties,
    Color,
    Constituent,
    Fill,
    Flavor,
    Geometry,
    Gradient,
    Group,
    Image,
    IndirectResource,
    KeynoteTheme,
    KeyxDocument,
    Label,
    Linear,
    Paragraph,
    ParagraphProperties,
    Position,
    Presentation,
    Preset,
    Rect,
    Resource,
    Shape,
    Size,
    Slide,
    SlideBackground,
    SlideObject,
    Stop,
    Text,
    Textbox,
    TextRun,
)

# Keeps `pathlib.Path` usable.
from creator_studio_doc_format.core import Path as ShapePath
from creator_studio_doc_format.validation import validate_document

# Sample files come with the examples so they run with no setup.
FIXTURES = Path(__file__).parent / "fixtures"


# `_RGBA_MOSS` and `_RGBA_OFF_WHITE` feed the presets below. The slide references those
# presets through `Fill(preset_identifier=…)`, so each color has one definition.
# `_RGBA_DARK` is used directly, for the slide's background and the hero overlay.
_RGBA_MOSS = RGBA(red=0.412, green=0.510, blue=0.106)
_RGBA_DARK = RGBA(red=0.05, green=0.06, blue=0.10)
_RGBA_OFF_WHITE = RGBA(red=0.96, green=0.94, blue=0.90)


def _presets() -> list[Preset]:
    """Returns character, paragraph, and textbox presets, with a ``base_text`` chain."""
    off_white_json = _RGBA_OFF_WHITE.model_dump(mode="json")
    return [
        Preset(
            identifier="fill_moss",
            properties={"color": {"rgba": _RGBA_MOSS.model_dump(mode="json")}},
        ),
        Preset(
            identifier="fill_off_white",
            properties={"color": {"rgba": off_white_json}},
        ),
        Preset(
            identifier="base_text",
            # `tracking` is a fraction of the em, not points, so `1.0` adds a full em
            # between letters.
            properties={"font_name": "Helvetica Neue", "tracking": 0.0},
        ),
        Preset(
            identifier="title_text",
            parent_identifier="base_text",
            properties={
                "font_name": "Avenir Next Condensed",
                "font_size": 120,
                "bold": True,
                "character_fill": {"color": {"rgba": off_white_json}},
            },
        ),
        Preset(
            identifier="subtitle_text",
            parent_identifier="base_text",
            properties={
                "font_name": "Helvetica Neue Light",
                "font_size": 32,
                "character_fill": {"color": {"rgba": off_white_json}},
            },
        ),
        Preset(
            identifier="para_left",
            properties={
                "alignment": "left",
                "line_spacing": {"value": 1.0, "kind": "relative"},
            },
        ),
        Preset(
            identifier="para_right",
            properties={
                "alignment": "right",
                "line_spacing": {"value": 1.0, "kind": "relative"},
            },
        ),
        # One preset gives every textbox the same border, shadow, and text layout.
        # Each textbox adopts it through `preset_identifier`.
        Preset(
            identifier="textbox_base",
            properties={
                "stroke": "empty",
                "shadow": "none",
                "layout_properties": {
                    "shrink_to_fit": True,
                    "padding": {"top": 0, "bottom": 0, "left": 0, "right": 0},
                    # Use `"center"`, not `"middle"`.
                    "vertical_alignment": "center",
                },
            },
        ),
        # `Shape.stroke` defaults to a visible `Line`, so this preset sets `"empty"`
        # to draw shapes without an outline.
        Preset(
            identifier="shape_base",
            properties={"stroke": "empty"},
        ),
    ]


def _slide() -> Slide:
    """Builds one slide that uses every feature this example covers."""
    background = Fill(color=Color(rgba=_RGBA_DARK))

    # `Group.children` takes `CanvasObject` directly, with no `SlideObject` wrapper.
    hero_image = CanvasObject(
        image=Image(
            geometry=Geometry(
                position=Position(x=0, y=-567),
                size=Size(width=1920, height=1267),
            ),
            resource=Resource(indirect=IndirectResource(filename="hero.png")),
        )
    )
    hero_overlay = CanvasObject(
        shape=Shape(
            preset_identifier="shape_base",
            geometry=Geometry(
                position=Position(x=0, y=350),
                size=Size(width=1920, height=350),
            ),
            fill=Fill(
                gradient=Gradient(
                    stops=[
                        Stop(
                            color=Color(
                                rgba=_RGBA_DARK.model_copy(update={"alpha": 0})
                            ),
                            fraction=0.0,
                        ),
                        Stop(color=Color(rgba=_RGBA_DARK), fraction=0.75),
                        Stop(color=Color(rgba=_RGBA_DARK), fraction=1.0),
                    ],
                    flavor=Flavor(linear=Linear(angle=270)),
                )
            ),
        )
    )
    hero_stack = SlideObject(
        object=CanvasObject(
            group=Group(
                title=Label(
                    text=Text(string="Hero"),
                    paragraph_properties=ParagraphProperties(
                        alignment=AlignmentType.CENTER,
                        character_properties=CharacterProperties(
                            font_size=14,
                            character_fill=Fill(preset_identifier="fill_off_white"),
                        ),
                    ),
                ),
                caption=Label(
                    text=Text(string="Caption hidden on the slide"),
                    is_visible=False,
                ),
                children=[hero_image, hero_overlay],
            )
        )
    )

    divider = SlideObject(
        object=CanvasObject(
            shape=Shape(
                preset_identifier="shape_base",
                geometry=Geometry(
                    position=Position(x=130, y=900),
                    size=Size(width=20, height=20),
                ),
                path=ShapePath(
                    bezier=BezierPath(
                        path="M 0.5,0 L 1,0.5 L 0.5,1 L 0,0.5 Z",
                        space=Rect(
                            position=Position(x=0, y=0),
                            size=Size(width=1, height=1),
                        ),
                    )
                ),
                fill=Fill(preset_identifier="fill_moss"),
            )
        )
    )

    title_run = TextRun(
        string="Kyoto",
        style=CharacterProperties(preset_identifier="title_text"),
    )
    subtitle_run = TextRun(
        string="Where tradition ",
        style=CharacterProperties(preset_identifier="subtitle_text"),
    )
    subtitle_accent_run = TextRun(
        string="meets quiet beauty.",
        style=CharacterProperties(
            preset_identifier="subtitle_text",
            italic=True,
            character_fill=Fill(preset_identifier="fill_moss"),
        ),
    )
    # Both lines share the `"para_left"` alignment, so the textbox sets it once as
    # its default instead of repeating it on each `Paragraph.style`. A paragraph
    # needs its own `style` only when it differs from that default.
    title_paragraph = Paragraph(contents=[Constituent(run=title_run)])
    subtitle_paragraph = Paragraph(
        contents=[Constituent(run=subtitle_run), Constituent(run=subtitle_accent_run)],
    )
    title_box = SlideObject(
        object=CanvasObject(
            textbox=Textbox(
                preset_identifier="textbox_base",
                geometry=Geometry(
                    position=Position(x=130, y=640),
                    size=Size(width=1700, height=240),
                ),
                paragraph_properties=ParagraphProperties(preset_identifier="para_left"),
                # `Text.paragraphs` carries the line break between title and subtitle.
                text=Text(paragraphs=[title_paragraph, subtitle_paragraph]),
            )
        )
    )

    # `text_runs` skips the `Paragraph`/`Constituent` wrapping that `paragraphs`
    # requires, which suits a single run with no list or paragraph break.
    footer_run = TextRun(
        string="EST. 794  ·  THE ANCIENT CAPITAL",
        style=CharacterProperties(
            font_size=18,
            character_fill=Fill(preset_identifier="fill_off_white"),
        ),
    )
    footer = SlideObject(
        object=CanvasObject(
            textbox=Textbox(
                preset_identifier="textbox_base",
                geometry=Geometry(
                    position=Position(x=130, y=970),
                    size=Size(width=1660, height=40),
                ),
                paragraph_properties=ParagraphProperties(
                    preset_identifier="para_right"
                ),
                text=Text(text_runs=[footer_run]),
            )
        )
    )

    return Slide(
        background=SlideBackground(standard=background),
        contents=[hero_stack, divider, title_box, footer],
        # Presenter notes are a plain `Text` on the slide, not a canvas object.
        note=Text(string="Open on the photo, then land the 'quiet beauty' line."),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.partition("\n")[0])
    parser.add_argument("output", type=Path, nargs="?", default=Path("tmp/basics.keyx"))
    args = parser.parse_args()

    doc = KeyxDocument(
        payload=Presentation(
            theme=KeynoteTheme(name="White", locale="en_US"),
            slide_size=Size(width=1920, height=1080),
            slides=[_slide()],
        ),
        presets=_presets(),
        resources={"hero.png": (FIXTURES / "photo_placeholder.png").read_bytes()},
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(args.output, pre_save_hooks=[validate_document])
    print(f"wrote {args.output} ({args.output.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
