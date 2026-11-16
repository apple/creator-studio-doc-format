# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0

# [create]
from creator_studio_doc_format.core import (
    CanvasObject,
    CharacterProperties,
    Geometry,
    KeynoteTheme,
    KeyxDocument,
    LayoutProperties,
    ParagraphProperties,
    Position,
    Presentation,
    Size,
    Slide,
    SlideObject,
    Stroke,
    Text,
    Textbox,
)

title = Textbox(
    geometry=Geometry(
        position=Position(x=160, y=440), size=Size(width=1600, height=200)
    ),
    stroke=Stroke(empty=True),
    layout_properties=LayoutProperties(vertical_alignment="center"),
    paragraph_properties=ParagraphProperties(
        alignment="center",
        character_properties=CharacterProperties(font_size=96),
    ),
    text=Text(string="Hello, Keynote"),
)
slide = Slide(contents=[SlideObject(object=CanvasObject(textbox=title))])

doc = KeyxDocument(
    Presentation(
        # Without a theme, Keynote uses White in the system locale. The name is
        # localized, so pair it with a locale.
        theme=KeynoteTheme(name="White", locale="en_US"),
        # Without a slide size, Keynote has to supply one, such as the theme's,
        # or reject the document.
        slide_size=Size(width=1920, height=1080),
        slides=[slide],
    )
)

doc.save("hello.keyx")
# [/create]

# [edit]
from creator_studio_doc_format.validation import validate_document

doc = KeyxDocument.open("hello.keyx")
first = doc.presentation.slides[0]  # Read.
first.note = Text(string="Welcome everyone, then move on.")  # Assign.

doc.presentation.slides.append(Slide())  # Construct.
del first.contents[0]  # Delete.

doc.save("edited.keyx", pre_save_hooks=[validate_document])
# [/edit]
