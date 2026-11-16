# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0

"""Build a presentation with every `Image` decoration and a `Shape` with an `ImageFill`.

`Movie` and `Audio` aren't shown.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from creator_studio_doc_format.core import (
    RGBA,
    BezierPath,
    CanvasObject,
    Color,
    ContactShadow,
    CurvedShadow,
    DropShadow,
    Fill,
    Frame,
    Geometry,
    Image,
    ImageFill,
    IndirectResource,
    KeyxDocument,
    Mask,
    Name,
    Position,
    Presentation,
    Preset,
    Rect,
    Reflection,
    Resource,
    Shadow,
    Shape,
    Size,
    Slide,
    SlideBackground,
    SlideObject,
    Stroke,
    Technique,
)
from creator_studio_doc_format.core import (
    # Keeps `pathlib.Path` usable.
    Path as ShapePath,
)
from creator_studio_doc_format.validation import validate_document

FIXTURES = Path(__file__).parent / "fixtures"


_RGBA_BG = RGBA(red=0.90, green=0.94, blue=0.98)
_RGBA_INK = RGBA(red=0.07, green=0.12, blue=0.22)
_RGBA_ACCENT = RGBA(red=0.10, green=0.30, blue=0.60)


def _presets() -> list[Preset]:
    """Returns the slide's colors and background fill as presets, plus a ``Shape`` base.

    The slide references them through ``Color(preset_identifier=…)`` and
    ``Fill(preset_identifier=…)``, which suit a color that's shared or inherited.
    """
    return [
        Preset(
            identifier="color_ink",
            properties={"rgba": _RGBA_INK.model_dump(mode="json")},
        ),
        Preset(
            identifier="fill_slide_bg",
            properties={"color": {"rgba": _RGBA_BG.model_dump(mode="json")}},
        ),
        Preset(
            identifier="shape_base",
            properties={"stroke": "empty"},
        ),
    ]


def _slide() -> Slide:
    """Builds a slide with every decoration field on ``Image``, plus ``ImageFill``."""
    photo = Resource(indirect=IndirectResource(filename="photo.png"))

    # `Mask.geometry` uses slide coordinates, as the image's geometry does.
    # `Mask.path` is drawn in a unit square `space` that maps onto the mask's geometry.
    tile_a_geometry = Geometry(
        position=Position(x=240, y=90), size=Size(width=600, height=396), angle=-4
    )
    tile_a = SlideObject(
        object=CanvasObject(
            image=Image(
                geometry=tile_a_geometry,
                resource=photo,
                mask=Mask(
                    geometry=tile_a_geometry,
                    path=ShapePath(
                        bezier=BezierPath(
                            path=(
                                "M 0.05,0 L 0.95,0 "
                                "Q 1,0 1,0.15 L 1,0.85 "
                                "Q 1,1 0.95,1 L 0.05,1 "
                                "Q 0,1 0,0.85 L 0,0.15 "
                                "Q 0,0 0.05,0 Z"
                            ),
                            space=Rect(
                                position=Position(x=0, y=0),
                                size=Size(width=1, height=1),
                            ),
                        )
                    ),
                ),
                shadow=Shadow(
                    dropShadow=DropShadow(
                        angle=270,
                        opacity=0.5,
                        color=Color(preset_identifier="color_ink"),
                        offset=6,
                        radius=18,
                    )
                ),
            )
        )
    )

    tile_b = SlideObject(
        object=CanvasObject(
            image=Image(
                geometry=Geometry(
                    position=Position(x=1080, y=90),
                    size=Size(width=600, height=396),
                ),
                resource=photo,
                stroke=Stroke(
                    frame=Frame(name=Name.PORTFOLIO_INSET, scale_percent=100)
                ),
                reflection=Reflection(opacity=0.35, fade_acceleration=1.2),
            )
        )
    )

    tile_c = SlideObject(
        object=CanvasObject(
            image=Image(
                geometry=Geometry(
                    position=Position(x=240, y=590),
                    size=Size(width=600, height=396),
                ),
                resource=photo,
                shadow=Shadow(
                    contactShadow=ContactShadow(
                        angle=270,
                        opacity=0.6,
                        color=Color(preset_identifier="color_ink"),
                        offset=4,
                        radius=32,
                    )
                ),
                opacity=0.9,
            )
        )
    )

    tile_d = SlideObject(
        object=CanvasObject(
            shape=Shape(
                preset_identifier="shape_base",
                geometry=Geometry(
                    position=Position(x=1080, y=590),
                    size=Size(width=600, height=396),
                ),
                fill=Fill(
                    image=ImageFill(
                        resource=photo,
                        technique=Technique.SCALE_TO_FIT,
                        # The tint paints over the image, so an opaque tint would
                        # hide it.
                        tint_color=Color(
                            rgba=_RGBA_ACCENT.model_copy(update={"alpha": 0.4})
                        ),
                    )
                ),
                shadow=Shadow(
                    curvedShadow=CurvedShadow(
                        angle=270,
                        opacity=0.55,
                        color=Color(preset_identifier="color_ink"),
                        offset=8,
                        radius=24,
                        curve=0.6,
                    )
                ),
            )
        )
    )

    return Slide(
        background=SlideBackground(standard=Fill(preset_identifier="fill_slide_bg")),
        contents=[tile_a, tile_b, tile_c, tile_d],
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.partition("\n")[0])
    parser.add_argument(
        "output", type=Path, nargs="?", default=Path("tmp/image_decoration.keyx")
    )
    args = parser.parse_args()

    doc = KeyxDocument(
        payload=Presentation(
            slide_size=Size(width=1920, height=1080),
            slides=[_slide()],
        ),
        presets=_presets(),
        resources={"photo.png": (FIXTURES / "photo_placeholder.png").read_bytes()},
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(args.output, pre_save_hooks=[validate_document])
    print(f"wrote {args.output} ({args.output.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
