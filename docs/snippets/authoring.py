# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0

# [summarize]
from creator_studio_doc_format.authoring import summarize_slide_layouts
from creator_studio_doc_format.core import KeyxDocument

doc = KeyxDocument.open("themed.keyx")
theme = doc.presentation.theme

for layout, placeholders in summarize_slide_layouts(theme).items():
    print(layout, [p.name for p in placeholders])
# [/summarize]

# [slide-from-layout]
from creator_studio_doc_format.authoring import slide_from_layout

slide = slide_from_layout(theme, "Title & Bullets")
# [/slide-from-layout]

# [set-slide-placeholder-text]
from creator_studio_doc_format.authoring import set_slide_placeholder_text

set_slide_placeholder_text(slide, "TITLE", "Baking Sourdough")
set_slide_placeholder_text(
    slide,
    "BODY",
    ["Feed the starter", "Twice a day"],
    # Sets each line's list level. Every level keeps the placeholder's
    # paragraph style.
    list_levels=[0, 1],
)
# Passing None clears the tagged placeholder's sample text.
set_slide_placeholder_text(slide, "Presentation Name", None)
# [/set-slide-placeholder-text]

# [set-slide-placeholder-image]
from pathlib import Path

from creator_studio_doc_format.authoring import set_slide_placeholder_image
from creator_studio_doc_format.core import IndirectResource, Resource, Size

photo = slide_from_layout(theme, "Title, Bullets & Photo")
filename = doc.resources.unique_filename("cover.png")
doc.resources[filename] = Path("cover.png").read_bytes()
set_slide_placeholder_image(
    photo,
    "Media",
    Resource(indirect=IndirectResource(filename=filename)),
    # The width and height of cover.png, so the image fills the
    # placeholder's mask without stretching.
    size=Size(width=1200, height=792),
)
# [/set-slide-placeholder-image]

# [together]
from creator_studio_doc_format.validation import validate_document

sections = [
    ("Baking Sourdough", ["Feed the starter", "Shape the loaf"]),
    ("Baking Day", ["Preheat the oven"]),
]

doc = KeyxDocument.open("themed.keyx")
theme = doc.presentation.theme

slides = []
for title, bullets in sections:
    slide = slide_from_layout(theme, "Title & Bullets")
    set_slide_placeholder_text(slide, "TITLE", title)
    set_slide_placeholder_text(slide, "BODY", bullets)
    set_slide_placeholder_text(slide, "Presentation Name", None)
    slides.append(slide)

# Replacing the slides in place keeps the theme, its presets, and everything
# else in the document.
doc.presentation.slides = slides
doc.save("presentation.keyx", pre_save_hooks=[validate_document])
# [/together]

# [presets]
from creator_studio_doc_format.core import PresetRegistry

styles = {
    style.name: style.properties.preset_identifier
    for style in doc.presentation.stylesheet.paragraph_styles
    if style.properties.preset_identifier
}
registry = PresetRegistry(doc.presets)
font = registry.resolved_properties(styles["Body"])["character_properties"]
print(font["font_name"], font["font_size"])
# [/presets]
