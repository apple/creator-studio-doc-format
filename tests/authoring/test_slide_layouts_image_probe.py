# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


from __future__ import annotations

import struct
from pathlib import Path

import pytest

from creator_studio_doc_format.authoring import (
    set_slide_placeholder_image,
    slide_from_layout,
)
from creator_studio_doc_format.core import (
    Geometry,
    Image,
    KeyxDocument,
    Size,
    Slide,
)

FIXTURES = Path(__file__).parents[1] / "fixtures"
EXPORTS = ["image_probe_replaced_wide.keyx", "image_probe_replaced_tall.keyx"]


def _docs() -> dict[str, KeyxDocument]:
    return {name: KeyxDocument.open(FIXTURES / name) for name in EXPORTS}


_DOCS = _docs()


def _media(slide: Slide) -> Image:
    return next(
        o.object.image
        for o in slide.contents or []
        if o.object is not None and o.object.image is not None
    )


def _pixel_size(png: bytes) -> Size:
    width, height = struct.unpack(">II", png[16:24])
    return Size(width=width, height=height)


def _assert_geometry(got: Geometry | None, want: Geometry | None) -> None:
    assert got is not None and want is not None
    assert got.position.x == pytest.approx(want.position.x)
    assert got.position.y == pytest.approx(want.position.y)
    assert got.size.width == pytest.approx(want.size.width)
    assert got.size.height == pytest.approx(want.size.height)
    assert got.angle == pytest.approx(want.angle)
    assert got.flip_horizontally == want.flip_horizontally


@pytest.mark.parametrize(
    ("export", "index"),
    [
        pytest.param(name, i, id=f"{name}-{i}")
        for name, doc in _DOCS.items()
        for i in range(len(doc.presentation.slides))
    ],
)
def test_replaced_image_matches_keynote(export: str, index: int) -> None:
    doc = _DOCS[export]
    theme = doc.presentation.theme
    assert theme is not None
    saved = doc.presentation.slides[index]
    assert saved.layout is not None
    want = _media(saved)
    filename = want.resource.indirect.filename if want.resource.indirect else None
    assert filename is not None

    got = set_slide_placeholder_image(
        slide_from_layout(theme, saved.layout),
        "Media",
        want.resource,
        size=_pixel_size(doc.resources[filename]),
    )

    _assert_geometry(got.geometry, want.geometry)
    assert got.mask is not None and want.mask is not None
    _assert_geometry(got.mask.geometry, want.mask.geometry)
    assert got.instant_alpha_path == want.instant_alpha_path
    assert got.description == want.description
    assert got.was_media_replaced == want.was_media_replaced
