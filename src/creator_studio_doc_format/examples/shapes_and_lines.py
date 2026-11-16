# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0

"""Build a presentation with shapes, a connection line, and shared decoration.

`Shape` and `ConnectionLine` are the canvas objects you build by hand, unlike
`Image`, `Movie`, `Table`, and `Chart`, which wrap external content or
structured data.

A `BezierPath` carries only the outline, so position, size, rotation, and flip all come
from the owner's `Geometry`. To reuse a path at another size or angle, change the
`Geometry` and leave the path as is.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from creator_studio_doc_format.core import (
    RGBA,
    AlignmentType,
    Anchor,
    BezierPath,
    CanvasObject,
    CharacterProperties,
    Color,
    ConnectionLine,
    DropShadow,
    End,
    Fill,
    Geometry,
    KeynoteTheme,
    KeyxDocument,
    Label,
    LineEnd,
    LineType,
    Magnet,
    ParagraphProperties,
    Position,
    Presentation,
    Preset,
    Rect,
    Reflection,
    Shadow,
    Shape,
    Size,
    Slide,
    SlideBackground,
    SlideObject,
    Stroke,
    Text,
)
from creator_studio_doc_format.core import Line as StrokeLine

# Keeps `pathlib.Path` usable.
from creator_studio_doc_format.core import Path as ShapePath
from creator_studio_doc_format.validation import validate_document

_RGBA_ACCENT = RGBA(red=0.58, green=0.47, blue=0.96)
_RGBA_BG = RGBA(red=0.06, green=0.05, blue=0.12)
_RGBA_TEXT = RGBA(red=1.0, green=1.0, blue=1.0)


# Slide 1: canonical shape outlines (unit box, x right, y down).
#
# Ovals and rounded corners use elliptical arcs, written
# `A rx,ry x-rot large-arc sweep x,y`. `"Polygon"` and `"Star"` come from a vertex
# formula.
_RECTANGLE = "M 0,0 H 1 V 1 H 0 Z"
_ROUNDED_RECTANGLE = (
    "M 0.15,0 H 0.85 A 0.15,0.15 0 0 1 1,0.15 V 0.85 "
    "A 0.15,0.15 0 0 1 0.85,1 H 0.15 A 0.15,0.15 0 0 1 0,0.85 "
    "V 0.15 A 0.15,0.15 0 0 1 0.15,0 Z"
)
_OVAL = "M 0,0.5 A 0.5,0.5 0 1 1 1,0.5 A 0.5,0.5 0 1 1 0,0.5 Z"


def _polygon_points(
    sides: int, *, start_deg: float = -90.0
) -> list[tuple[float, float]]:
    """Returns a regular ``sides``-gon's vertices, inscribed in the unit box."""
    r = 0.5
    step = 2 * math.pi / sides
    start = math.radians(start_deg)
    return [
        (
            round(0.5 + r * math.cos(start + step * k), 3),
            round(0.5 + r * math.sin(start + step * k), 3),
        )
        for k in range(sides)
    ]


def _star_points(
    points: int, *, inner_ratio: float = 0.4, start_deg: float = -90.0
) -> list[tuple[float, float]]:
    """Returns a ``points``-pointed star's vertices, with outer radius 0.5.

    The inner radius is ``0.5*inner_ratio``.
    """
    outer, inner = 0.5, 0.5 * inner_ratio
    step = math.pi / points  # Half a step, because vertices alternate outer and inner.
    start = math.radians(start_deg)
    verts: list[tuple[float, float]] = []
    for k in range(points * 2):
        r = outer if k % 2 == 0 else inner
        verts.append(
            (
                round(0.5 + r * math.cos(start + step * k), 3),
                round(0.5 + r * math.sin(start + step * k), 3),
            )
        )
    return verts


def _poly_path(points: list[tuple[float, float]]) -> str:
    """Returns a closed polyline ``d`` string through ``points``."""
    head, *tail = points
    return f"M {head[0]},{head[1]} " + " ".join(f"L {x},{y}" for x, y in tail) + " Z"


_HEXAGON_PATH = _poly_path(_polygon_points(6))
_STAR_PATH = _poly_path(_star_points(5))
SHAPES: list[tuple[str, str]] = [
    ("Rectangle", _RECTANGLE),
    ("Rounded Rectangle", _ROUNDED_RECTANGLE),
    ("Oval", _OVAL),
    ("Polygon", _HEXAGON_PATH),
    ("Star", _STAR_PATH),
]

_UNIT_SPACE = Rect(position=Position(x=0, y=0), size=Size(width=1, height=1))


def _label(name: str, *, size: float = 32) -> Label:
    """Returns the centered off-white label used beneath each shape."""
    return Label(
        text=Text(string=name),
        paragraph_properties=ParagraphProperties(
            alignment=AlignmentType.CENTER,
            character_properties=CharacterProperties(
                font_size=size,
                character_fill=Fill(color=Color(preset_identifier="color_text")),
            ),
        ),
    )


def _shape(
    d: str,
    position: Position,
    size: Size,
    *,
    label: str | None = None,
    identifier: str | None = None,
    fill: str = "color_accent",
    shadow: Shadow | None = None,
    reflection: Reflection | None = None,
    title_on_top: bool = False,
) -> Shape:
    """Builds a filled shape from a path in a unit box, placed by ``Geometry`` alone."""
    return Shape(
        identifier=identifier,
        preset_identifier="shape_base",
        geometry=Geometry(position=position, size=size),
        path=ShapePath(bezier=BezierPath(path=d, space=_UNIT_SPACE)),
        fill=Fill(color=Color(preset_identifier=fill)),
        shadow=shadow,
        reflection=reflection,
        title=_label(label) if label else None,
        title_is_positioned_on_top=title_on_top,
    )


def _presets() -> list[Preset]:
    # `"empty"` draws no outline. The connection line sets its own visible stroke.
    return [
        Preset(identifier="shape_base", properties={"stroke": "empty"}),
        Preset(
            identifier="color_accent",
            properties={"rgba": _RGBA_ACCENT.model_dump(mode="json")},
        ),
        Preset(
            identifier="color_text",
            properties={"rgba": _RGBA_TEXT.model_dump(mode="json")},
        ),
        Preset(
            identifier="fill_slide_bg",
            properties={"color": {"rgba": _RGBA_BG.model_dump(mode="json")}},
        ),
    ]


def _basic_shapes_slide() -> Slide:
    """Builds a row of the shapes, placing each by its slot's ``Geometry``."""
    margin_x = 80.0
    slot_width = (1920 - 2 * margin_x) / len(SHAPES)
    box = 170.0  # Rendered shape size, in points.

    slide_objects: list[SlideObject] = []
    for i, (name, d) in enumerate(SHAPES):
        cx = margin_x + i * slot_width + slot_width / 2
        position = Position(x=cx - box / 2, y=540 - box / 2)
        shape = _shape(d, position, Size(width=box, height=box), label=name)
        slide_objects.append(SlideObject(object=CanvasObject(shape=shape)))

    return Slide(
        background=SlideBackground(standard=Fill(preset_identifier="fill_slide_bg")),
        contents=slide_objects,
    )


def _connection_line_slide() -> Slide:
    """Builds an anchored connection line with an arrowhead, plus shared decoration."""
    box_a = _shape(
        _ROUNDED_RECTANGLE,
        Position(x=280, y=200),
        Size(width=340, height=180),
        label="From",
        identifier="box_a",
    )
    box_b = _shape(
        _ROUNDED_RECTANGLE,
        Position(x=1000, y=200),
        Size(width=340, height=180),
        label="To",
        identifier="box_b",
        fill="color_text",
    )
    connection_line = ConnectionLine(
        line_type=LineType(straight=True),
        tail=End(
            end_point=Position(x=620, y=290),  # `box_a` east edge midpoint.
            anchor=Anchor(object_id="box_a", magnet=Magnet(east=True)),
        ),
        head=End(
            end_point=Position(x=1000, y=290),  # `box_b` west edge midpoint.
            anchor=Anchor(object_id="box_b", magnet=Magnet(west=True)),
            line_end=LineEnd.FILLED_ARROW,
        ),
        stroke=Stroke(
            line=StrokeLine(color=Color(preset_identifier="color_text"), width=3)
        ),
    )

    with_shadow = _shape(
        _STAR_PATH,
        Position(x=340, y=560),
        Size(width=200, height=200),
        label="dropShadow",
        shadow=Shadow(dropShadow=DropShadow(offset=8, radius=10, opacity=0.6)),
    )
    with_reflection = _shape(
        _OVAL,
        Position(x=870, y=560),
        Size(width=200, height=200),
        label="reflection",
        reflection=Reflection(opacity=0.4),
        # The reflection extends below the shape, so the label goes above it.
        title_on_top=True,
    )

    return Slide(
        background=SlideBackground(standard=Fill(preset_identifier="fill_slide_bg")),
        contents=[
            SlideObject(object=CanvasObject(shape=box_a)),
            SlideObject(object=CanvasObject(shape=box_b)),
            SlideObject(object=CanvasObject(connectionLine=connection_line)),
            SlideObject(object=CanvasObject(shape=with_shadow)),
            SlideObject(object=CanvasObject(shape=with_reflection)),
        ],
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.partition("\n")[0])
    parser.add_argument(
        "output", type=Path, nargs="?", default=Path("tmp/shapes_and_lines.keyx")
    )
    args = parser.parse_args()

    doc = KeyxDocument(
        payload=Presentation(
            theme=KeynoteTheme(name="White", locale="en_US"),
            slide_size=Size(width=1920, height=1080),
            slides=[_basic_shapes_slide(), _connection_line_slide()],
        ),
        presets=_presets(),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(args.output, pre_save_hooks=[validate_document])
    print(f"wrote {args.output} ({args.output.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
