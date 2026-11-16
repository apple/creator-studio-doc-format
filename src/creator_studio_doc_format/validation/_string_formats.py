# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


import re
import urllib.parse
from typing import TYPE_CHECKING

from pydantic import BaseModel

from creator_studio_doc_format.core import (
    Base64EncodedResource,
    BezierPath,
    CurrencyFormat,
    Hyperlink,
    InstantAlphaPath,
    KeynoteTheme,
    NumberFormatData,
)

from ._paths import extend_path

if TYPE_CHECKING:
    from creator_studio_doc_format.navigation import IteratedModel

    from ._model_tree import _IterationState

_SVG_PATH_RE = re.compile(
    r"^(?=.*[MmLlHhVvCcSsQqTtAaZz])[\sMmLlHhVvCcSsQqTtAaZz0-9.,\-+eE]+$"
)

_ISO4217_RE = re.compile(r"^[A-Z]{3}$")

_BCP47_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_\-@=.;]*$")

_BASE64_RE = re.compile(r"^[A-Za-z0-9+/]+={0,2}$")

_BASE64_PREVIEW_LEN = 40


STRING_FORMAT_FIELDS: dict[type[BaseModel], tuple[str, ...]] = {
    BezierPath: ("path",),
    InstantAlphaPath: ("path",),
    CurrencyFormat: ("currency_code",),
    NumberFormatData: ("currency_code",),
    KeynoteTheme: ("locale",),
    Hyperlink: ("url", "file"),
    Base64EncodedResource: ("string", "filename"),
}


class StringFormatValidator:
    def visit(self, state: "_IterationState", iterated: "IteratedModel") -> None:
        model = iterated.model
        if isinstance(model, (BezierPath, InstantAlphaPath)):
            _reject_bad_svg_path(model.path, iterated.path, type(model).__name__)
        elif isinstance(model, CurrencyFormat):
            _reject_bad_iso4217(model.currency_code, iterated.path, "CurrencyFormat")
        elif isinstance(model, NumberFormatData):
            if model.currency_code is not None:
                _reject_bad_iso4217(
                    model.currency_code, iterated.path, "NumberFormatData"
                )
        elif isinstance(model, KeynoteTheme):
            if model.locale is not None:
                _reject_bad_bcp47(model.locale, iterated.path)
        elif isinstance(model, Hyperlink):
            if model.url is not None:
                _reject_bad_url(model.url, iterated.path)
            if model.file is not None:
                _reject_empty(model.file, iterated.path, "file", cls="Hyperlink")
        elif isinstance(model, Base64EncodedResource):
            _reject_bad_base64(model.string, iterated.path)
            _reject_empty(
                model.filename, iterated.path, "filename", cls="Base64EncodedResource"
            )

    def finalize(self, state: "_IterationState") -> None:
        return


def _reject_bad_svg_path(value: str, model_path: str, cls: str) -> None:
    where = extend_path(model_path, "path")
    if not value or not value.strip():
        raise ValueError(f"`{cls}.path` {value!r} is empty or blank (at {where})")
    if not _SVG_PATH_RE.fullmatch(value):
        raise ValueError(
            f"`{cls}.path` {value!r} isn't SVG path data (at {where}). Use the syntax "
            f"of an SVG `<path>` element's `d` attribute."
        )


def _reject_bad_iso4217(value: str, model_path: str, cls: str) -> None:
    if not _ISO4217_RE.fullmatch(value):
        raise ValueError(
            f"`{cls}.currency_code` {value!r} isn't three uppercase letters "
            f"(at {extend_path(model_path, 'currency_code')}). Use a code such as "
            f"'USD' or 'EUR'."
        )


def _reject_bad_bcp47(value: str, model_path: str) -> None:
    if not value or not _BCP47_RE.fullmatch(value):
        raise ValueError(
            f"`KeynoteTheme.locale` {value!r} isn't a locale identifier "
            f"(at {extend_path(model_path, 'locale')}). Use a value such as 'en_US'."
        )


def _reject_bad_url(value: str, model_path: str) -> None:
    where = extend_path(model_path, "url")
    if not value or not value.strip():
        raise ValueError(f"`Hyperlink.url` {value!r} is empty or blank (at {where})")
    try:
        parsed = urllib.parse.urlparse(value)
    except ValueError as exc:
        raise ValueError(
            f"`Hyperlink.url` {value!r} isn't a URL (at {where}). {exc}."
        ) from exc
    if parsed.scheme == "file":
        raise ValueError(
            f"`Hyperlink.url` {value!r} has a 'file:' scheme (at {where}). "
            f"Use `Hyperlink.file` instead."
        )


def _reject_empty(value: str, model_path: str, field: str, *, cls: str) -> None:
    if not value or not value.strip():
        raise ValueError(
            f"`{cls}.{field}` {value!r} is empty or blank "
            f"(at {extend_path(model_path, field)})"
        )


def _reject_bad_base64(value: str, model_path: str) -> None:
    where = extend_path(model_path, "string")
    if not (stripped := "".join(value.split())):
        raise ValueError(
            f"`Base64EncodedResource.string` {value!r} is empty or blank (at {where})"
        )
    if len(stripped) % 4 != 0 or not _BASE64_RE.fullmatch(stripped):
        preview = (
            value
            if len(value) <= _BASE64_PREVIEW_LEN
            else f"{value[:_BASE64_PREVIEW_LEN]}… ({len(value)} characters)"
        )
        raise ValueError(
            f"`Base64EncodedResource.string` {preview!r} isn't valid Base64 "
            f"(at {where}). Use letters, digits, '+' and '/', padded with '=' to a "
            f"multiple of 4 characters."
        )
