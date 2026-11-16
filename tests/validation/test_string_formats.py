# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


import base64
from collections.abc import Callable

import pytest

from creator_studio_doc_format.core import (
    Base64EncodedResource,
    BezierPath,
    CanvasObject,
    Constituent,
    CurrencyFormat,
    CustomFormat,
    CustomFormatType,
    Hyperlink,
    HyperlinkField,
    Image,
    IndirectResource,
    InstantAlphaPath,
    KeynoteTheme,
    KeyxDocument,
    NumberFormatData,
    Paragraph,
    Path,
    Presentation,
    Resource,
    Shape,
    Slide,
    SlideObject,
    Table,
    Text,
    TextRun,
)
from creator_studio_doc_format.validation import validate_document

from .builders import slide_size


def _doc_with_canvas(canvas_obj: CanvasObject) -> KeyxDocument:
    return KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[Slide(contents=[SlideObject(object=canvas_obj)])],
        ),
        presets=[],
    )


def _doc_with_theme(theme: KeynoteTheme) -> KeyxDocument:
    return KeyxDocument(
        Presentation(slide_size=slide_size(), slides=[Slide()], theme=theme),
        presets=[],
    )


def _doc_with_note(note: Text) -> KeyxDocument:
    return KeyxDocument(
        Presentation(slide_size=slide_size(), slides=[Slide(note=note)]),
        presets=[],
    )


def _expect_validation(doc: KeyxDocument, expected: str | None) -> None:
    if expected is None:
        validate_document(doc)
    else:
        with pytest.raises(ValueError, match=expected):
            validate_document(doc)


def _doc_with_bezier_path(path: str) -> KeyxDocument:
    return _doc_with_canvas(
        CanvasObject(shape=Shape(path=Path(bezier=BezierPath(path=path))))
    )


def _doc_with_instant_alpha_path(path: str) -> KeyxDocument:
    image = Image(
        resource=Resource(indirect=IndirectResource(filename="x.png")),
        instant_alpha_path=InstantAlphaPath(path=path),
    )
    doc = _doc_with_canvas(CanvasObject(image=image))
    doc.resources["x.png"] = b"\x89PNG\r\n\x1a\n"
    return doc


@pytest.mark.parametrize(
    ("make_doc", "expected"),
    [
        (lambda: _doc_with_bezier_path("M 0 0 L 10 10 Z"), None),
        (
            lambda: _doc_with_bezier_path("not a path"),
            r"'not a path' isn't SVG path data",
        ),
        (lambda: _doc_with_bezier_path(""), r"is empty or blank"),
        (lambda: _doc_with_bezier_path("1,2,3"), r"'1,2,3' isn't SVG path data"),
        (lambda: _doc_with_instant_alpha_path("!!!"), r"'\!\!\!' isn't SVG path data"),
    ],
    ids=[
        "bezier-valid",
        "bezier-malformed",
        "bezier-empty",
        "bezier-no-command-letter",
        "alpha-malformed",
    ],
)
def test_svg_path_format(
    make_doc: Callable[[], KeyxDocument], expected: str | None
) -> None:
    _expect_validation(make_doc(), expected)


def _doc_with_currency_via_cell(code: str) -> KeyxDocument:
    table = Table(
        number_of_columns=1,
        number_of_rows=1,
        content=[
            {
                "cells": [
                    {
                        "value": "1",
                        "cell_format": {
                            "format_type": "currency",
                            "currency_format": CurrencyFormat(currency_code=code),
                        },
                    }
                ]
            }
        ],  # ty: ignore
    )
    return _doc_with_canvas(CanvasObject(table=table))


def _doc_with_currency_via_custom_format(code: str) -> KeyxDocument:
    table = Table(
        number_of_columns=1,
        number_of_rows=1,
        custom_formats=[
            CustomFormat(
                identifier="cf1",
                format_string="#,##0",
                format_type=CustomFormatType.NUMBER,
                number_format_data=NumberFormatData(currency_code=code),
            )
        ],
    )
    return _doc_with_canvas(CanvasObject(table=table))


@pytest.mark.parametrize(
    ("make_doc", "expected"),
    [
        (lambda: _doc_with_currency_via_cell("USD"), None),
        (
            lambda: _doc_with_currency_via_cell("usd"),
            r"currency_code` 'usd' isn't three uppercase letters",
        ),
        (
            lambda: _doc_with_currency_via_custom_format("Us$"),
            r"currency_code` 'Us\$' isn't three uppercase letters",
        ),
    ],
    ids=[
        "currency-format-valid",
        "currency-format-lowercase",
        "number-format-data-symbol",
    ],
)
def test_iso4217_format(
    make_doc: Callable[[], KeyxDocument], expected: str | None
) -> None:
    _expect_validation(make_doc(), expected)


@pytest.mark.parametrize(
    ("locale", "expected"),
    [
        ("en_US", None),
        ("en@calendar=buddhist;numbers=thai", None),
        ("en US!", r"`KeynoteTheme\.locale` 'en US!' isn't a locale identifier"),
        ("", r"`KeynoteTheme\.locale` '' isn't a locale identifier"),
        (".", r"`KeynoteTheme\.locale` '\.' isn't a locale identifier"),
        (";;;", r"`KeynoteTheme\.locale` ';;;' isn't a locale identifier"),
    ],
    ids=[
        "bcp47-simple",
        "icu-extension",
        "space-and-bang",
        "empty",
        "dot-only",
        "semicolons-only",
    ],
)
def test_locale_format(locale: str, expected: str | None) -> None:
    _expect_validation(_doc_with_theme(KeynoteTheme(locale=locale)), expected)


def _doc_with_hyperlink(link: Hyperlink) -> KeyxDocument:
    note = Text(
        paragraphs=[
            Paragraph(
                contents=[
                    Constituent(
                        hyperlink=HyperlinkField(
                            target=link, run=TextRun(string="click me")
                        )
                    )
                ]
            )
        ]
    )
    return _doc_with_note(note)


@pytest.mark.parametrize(
    ("link", "expected"),
    [
        (Hyperlink(url="https://example.com"), None),
        (Hyperlink(url="mailto:someone@example.com"), None),
        (Hyperlink(url="example.com"), None),
        (Hyperlink(url="#bookmark"), None),
        (Hyperlink(url="?sectionid=abc"), None),
        (Hyperlink(url="file:///tmp/x.pdf"), r"file:' scheme"),
        (Hyperlink(url=""), r"`Hyperlink\.url` '' is empty or blank"),
        (Hyperlink(file=""), r"`Hyperlink\.file` '' is empty or blank"),
        (Hyperlink(url="https:"), None),
        (
            Hyperlink(url="http://[malformed"),
            r"`Hyperlink\.url` 'http://\[malformed' isn't a URL",
        ),
    ],
    ids=[
        "https-valid",
        "mailto-valid",
        "scheme-less-relative-ok",
        "bookmark-ok",
        "sectionid-ok",
        "file-scheme-belongs-in-file-case",
        "empty-url",
        "empty-file",
        "scheme-only-ok",
        "urlparse-crash-wrapped",
    ],
)
def test_hyperlink_format(link: Hyperlink, expected: str | None) -> None:
    _expect_validation(_doc_with_hyperlink(link), expected)


def _doc_with_base64_image(b64: str) -> KeyxDocument:
    image = Image(
        resource=Resource(
            base64_encoded=Base64EncodedResource(string=b64, filename="i.png")
        )
    )
    return _doc_with_canvas(CanvasObject(image=image))


@pytest.mark.parametrize(
    ("b64", "expected"),
    [
        (base64.b64encode(b"\x89PNG\r\n\x1a\nHelloWorld").decode("ascii"), None),
        ("!!!not base64!!!", r"`Base64EncodedResource.string` .* isn't valid Base64"),
        ("", r"`Base64EncodedResource.string` '' is empty or blank"),
        ("QUJD", None),
        ("QUJDR", r"`Base64EncodedResource.string` 'QUJDR' isn't valid Base64"),
        (base64.encodebytes(b"\x89PNG\r\n\x1a\n" + b"x" * 200).decode("ascii"), None),
        ("   \n\t ", r"`Base64EncodedResource.string` .* is empty or blank"),
    ],
    ids=[
        "valid",
        "undecodable",
        "empty",
        "valid-len-4",
        "bad-length",
        "wrapped",
        "whitespace-only",
    ],
)
def test_base64_resource_format(b64: str, expected: str | None) -> None:
    _expect_validation(_doc_with_base64_image(b64), expected)


def test_base64_resource_filename_empty() -> None:
    image = Image(
        resource=Resource(
            base64_encoded=Base64EncodedResource(
                string=base64.b64encode(b"\x89PNG\r\n\x1a\n").decode("ascii"),
                filename="",
            )
        )
    )
    doc = _doc_with_canvas(CanvasObject(image=image))
    with pytest.raises(
        ValueError, match=r"`Base64EncodedResource\.filename` '' is empty or blank"
    ):
        validate_document(doc)


def test_validate_error_message_carries_iteration_path() -> None:
    with pytest.raises(ValueError, match=r"at slides\[0\]\.contents\[0\]"):
        validate_document(_doc_with_bezier_path("not-a-path"))
