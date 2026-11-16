# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0

"""Create slides from a theme's layouts, and fill in their text and image placeholders.

Each placeholder has a name that identifies it within a slide layout. A text
placeholder takes text, an image placeholder takes an image, and a movie or audio
placeholder has no setter.
"""

from __future__ import annotations

from ._slide_layouts import (
    LayoutPlaceholderSummary,
    set_slide_placeholder_image,
    set_slide_placeholder_text,
    slide_from_layout,
    summarize_slide_layouts,
)

__all__ = [
    "LayoutPlaceholderSummary",
    "set_slide_placeholder_image",
    "set_slide_placeholder_text",
    "slide_from_layout",
    "summarize_slide_layouts",
]
