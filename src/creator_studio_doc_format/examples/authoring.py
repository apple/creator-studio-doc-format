# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0

"""Build a themed presentation with `creator_studio_doc_format.authoring`.

The theme already gives everything a meaningful name: slide layouts, placeholders,
placeholder prompts, and styles. The example reads those names back through
`summarize_slide_layouts` and directly from `stylesheet.paragraph_styles`, and
addresses content by name instead of by index.

The following lines inspect the theme in `fixtures/Tidal_en.keyx`:

>>> doc = KeyxDocument.open(FIXTURES / "Tidal_en.keyx")
>>> next(iter(summarize_slide_layouts(doc.presentation.theme)))
'Title'
>>> pairs = [
...     (s.name, s.properties.preset_identifier)
...     for s in doc.presentation.stylesheet.paragraph_styles
...     if s.properties.preset_identifier
... ]
>>> pairs[0]  # A (style name, preset identifier) pair.
('Title Small', 'text-1-paragraphstyle-Title Alt')
>>> dict(pairs)["Title Small"]  # The preset identifier can differ from the style name.
'text-1-paragraphstyle-Title Alt'
>>> reg = PresetRegistry(doc.presets)
>>> body = "text-2-paragraphstyle-Body"  # Query by identifier.
>>> reg.resolved_properties(body)["space_after"]
24
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from creator_studio_doc_format.authoring import (
    set_slide_placeholder_image,
    set_slide_placeholder_text,
    slide_from_layout,
    summarize_slide_layouts,
)
from creator_studio_doc_format.core import (
    RGBA,
    CanvasObject,
    CharacterProperties,
    Color,
    Constituent,
    Fill,
    Geometry,
    IndirectResource,
    Insets,
    KeyxDocument,
    LayoutProperties,
    Paragraph,
    ParagraphProperties,
    ParagraphStyle,
    Position,
    Preset,
    PresetRegistry,
    Resource,
    ShapeStyle,
    Size,
    SlideObject,
    Stroke,
    Text,
    Textbox,
    TextRun,
    VerticalAlignmentType,
)
from creator_studio_doc_format.validation import validate_document

logger = logging.getLogger(__name__)

FIXTURES = Path(__file__).parent / "fixtures"

# The theme has no preset for this color, so it is set inline.
_ACCENT = RGBA(red=0.929, green=0.353, blue=0.157)

# Vertical extent of the pillar text columns, in points.
_TEXT_TOP = 570.0
_BODY_BOTTOM = 980.0


def _preset_identifiers(
    styles: list[ParagraphStyle] | list[ShapeStyle] | None,
) -> dict[str, str]:
    """Maps each style name to its ``preset_identifier``, for styles that have one."""
    return {
        s.name: s.properties.preset_identifier
        for s in styles or []
        if s.name and s.properties.preset_identifier
    }


def _heading_gap(presets: list[Preset], paragraph_styles: dict[str, str]) -> float:
    """Returns the larger resolved ``space_after`` of ``"Subtitle"`` and ``"Body"``.

    The registry warns about a missing preset instead of raising, so this function
    raises on ``reg.warnings`` rather than letting the gap fall back to ``0.0``.
    """
    reg = PresetRegistry(presets)
    # A preset that clears `space_after` leaves an explicit `None`, which a `.get`
    # default doesn't replace. `or 0.0` covers that case.
    gap = max(
        reg.resolved_properties(paragraph_styles["Subtitle"]).get("space_after") or 0.0,
        reg.resolved_properties(paragraph_styles["Body"]).get("space_after") or 0.0,
    )
    if reg.warnings:
        raise LookupError(f"Unresolved preset reference: {', '.join(reg.warnings)}")
    return gap


def _column(
    x: float,
    heading: str,
    lines: list[str],
    paragraph_styles: dict[str, str],
    textbox_preset_id: str,
    *,
    heading_gap: float,
    accent: bool = False,
) -> SlideObject:
    """Builds a freeform column, styled entirely from the document's presets."""
    run_style = (
        CharacterProperties(character_fill=Fill(color=Color(rgba=_ACCENT)))
        if accent
        else None
    )
    # The heading gets a wide gap below it, and the items get tight spacing. The presets
    # give `"Subtitle"` the smaller `space_after`, so the caller passes the larger.
    heading_paragraph = Paragraph(
        style=ParagraphProperties(
            preset_identifier=paragraph_styles["Subtitle"], space_after=heading_gap
        ),
        contents=[Constituent(run=TextRun(string=heading, style=run_style))],
    )
    body = [
        Paragraph(
            style=ParagraphProperties(
                preset_identifier=paragraph_styles["Body"], space_after=6
            ),
            contents=[Constituent(run=TextRun(string=line))],
        )
        for line in lines
    ]
    return SlideObject(
        object=CanvasObject(
            textbox=Textbox(
                preset_identifier=textbox_preset_id,
                stroke=Stroke(empty=True),
                # Top alignment keeps the gap above the heading the same at any
                # line count.
                layout_properties=LayoutProperties(
                    vertical_alignment=VerticalAlignmentType.TOP,
                    padding=Insets(top=0, bottom=0, left=24, right=24),
                ),
                geometry=Geometry(
                    position=Position(x=x, y=_TEXT_TOP),
                    size=Size(width=500, height=_BODY_BOTTOM - _TEXT_TOP),
                ),
                text=Text(paragraphs=[heading_paragraph, *body]),
            )
        )
    )


def main() -> None:
    """Builds the example presentation from a themed one and saves it."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    parser = argparse.ArgumentParser(description=__doc__.partition("\n")[0])
    parser.add_argument(
        "input",
        type=Path,
        nargs="?",
        default=FIXTURES / "Tidal_en.keyx",
        help="a .keyx exported from Keynote. Defaults to fixtures/Tidal_en.keyx.",
    )
    parser.add_argument(
        "output", type=Path, nargs="?", default=Path("tmp/authoring.keyx")
    )
    args = parser.parse_args()

    doc = KeyxDocument.open(args.input)
    pres = doc.presentation
    theme = pres.theme
    if theme is not None and theme.slide_layouts is not None:
        for name, placeholders in summarize_slide_layouts(theme).items():
            summary_lines = [name] + [
                f"    {p.name}:{p.object_case} {p.prompt!r}" for p in placeholders
            ]
            logger.info("%s", "\n".join(summary_lines))

        # Text placeholders differ by name and prompt. On the `"Quote"` layout,
        # `"Text"` is the quotation and `"Text-1"` is the attribution.
        slide_specs = [
            (
                "Photo - Horizontal",
                {
                    "TITLE": ["Our Community Garden"],
                    "BODY": ["Growing food together, one bed at a time"],
                },
            ),
            (
                "Title, Bullets & Photo",
                {"TITLE": ["Season Plan"]},
            ),
            (
                "Quote",
                {
                    "Text": [
                        "A garden grows one seed at a time, and so does a community."
                    ],
                    "Text-1": ["Community Garden Volunteer"],
                },
            ),
        ]
        built = []
        for layout, texts in slide_specs:
            slide = slide_from_layout(theme, layout)
            for name, lines in texts.items():
                set_slide_placeholder_text(slide, name, lines)
            built.append(slide)

        season_plan = next(s for s in built if s.layout == "Title, Bullets & Photo")
        set_slide_placeholder_text(
            season_plan,
            "BODY",
            ["Spring", "Build raised beds", "Sow seeds", "Summer", "Harvest and share"],
            list_levels=[0, 1, 1, 0, 1],
        )

        # Give the "Season Plan" slide's `"Media"` placeholder a new image. The new
        # resource replaces the theme's sample photo.
        filename = doc.resources.unique_filename("season_plan.png")
        doc.resources[filename] = (FIXTURES / "photo_placeholder.png").read_bytes()
        set_slide_placeholder_image(
            season_plan,
            "Media",
            Resource(indirect=IndirectResource(filename=filename)),
            size=Size(width=1200, height=792),  # The PNG's width and height.
        )

        # Content outside the placeholders uses the theme's styles. `stylesheet` is
        # optional, so these dictionaries can be empty.
        stylesheet = pres.stylesheet
        paragraph_styles = _preset_identifiers(
            stylesheet.paragraph_styles if stylesheet else None
        )
        for name, identifier in paragraph_styles.items():
            logger.info("%s -> %s", name, identifier)
        textbox_preset_id = next(
            iter(
                _preset_identifiers(
                    stylesheet.textbox_styles if stylesheet else None
                ).values()
            ),
            "",  # A theme with no textbox style gets a bare `Textbox` with no preset.
        )
        heading_gap = _heading_gap(doc.presets, paragraph_styles)
        logger.info("resolved heading gap: %spt", heading_gap)

        hybrid = slide_from_layout(theme, "Title & Bullets")
        set_slide_placeholder_text(hybrid, "TITLE", "Three pillars")
        # Clear the footer's sample text, which `slide_from_layout` keeps.
        set_slide_placeholder_text(hybrid, "Presentation Name", None)
        # Each pillar holds x, heading, body lines, and whether it's the accent column.
        pillars = [
            (140, "Plan", ["Map the beds", "Pick the crops"], False),
            (710, "Plant", ["Water daily", "Pull weeds"], False),
            (1280, "Harvest", ["Pick when ripe", "Share the surplus"], True),
        ]
        # `contents` is `None` on a layout with no canvas objects.
        if hybrid.contents is None:
            hybrid.contents = []
        for x, heading, lines, accent in pillars:
            hybrid.contents.append(
                _column(
                    x,
                    heading,
                    lines,
                    paragraph_styles,
                    textbox_preset_id,
                    heading_gap=heading_gap,
                    accent=accent,
                )
            )
        quote_index = next(i for i, s in enumerate(built) if s.layout == "Quote")
        built.insert(quote_index, hybrid)

        # Assigning the list replaces the slide that the exported file starts with.
        pres.slides = built

    args.output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(args.output, pre_save_hooks=[validate_document])
    logger.info("Wrote %s", args.output)


if __name__ == "__main__":
    main()
