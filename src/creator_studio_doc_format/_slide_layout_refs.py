# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


import unicodedata
from collections.abc import Iterable

from creator_studio_doc_format.core import SlideLayout


def resolve_slide_layout(
    layouts: Iterable[SlideLayout], ref: str
) -> SlideLayout | None:
    layouts = list(layouts)
    if (
        match := next((ts for ts in layouts if ts.identifier == ref), None)
    ) is not None:
        return match
    key = layout_name_key(ref)
    return next((ts for ts in layouts if layout_name_key(ts.name) == key), None)


def layout_name_key(name: str) -> str:
    folded = unicodedata.normalize(
        "NFKD", unicodedata.normalize("NFKD", name).casefold()
    ).replace("ı", "i")
    chars: list[str] = []
    base = ""
    for c in folded:
        if not unicodedata.combining(c):
            base = c
        elif c == "\u0307" and base == "i":
            continue
        chars.append(c)
    return unicodedata.normalize("NFKC", "".join(chars)).replace("å", "aa")
