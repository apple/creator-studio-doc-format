# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


from creator_studio_doc_format.core import (
    CanvasObject,
    Chart,
    Constituent,
    Hyperlink,
    HyperlinkField,
    Image,
    IndirectResource,
    KeynoteTheme,
    KeyxDocument,
    Paragraph,
    Presentation,
    Preset,
    Resource,
    Size,
    Slide,
    SlideLayout,
    SlideObject,
    SlideTarget,
    Table,
    Text,
    TextRun,
)


def slide_size() -> Size:
    return Size(width=1024, height=768)


def empty_doc() -> KeyxDocument:
    return KeyxDocument(
        Presentation(slide_size=slide_size(), slides=[Slide()]),
        presets=[],
    )


def doc_with_indirect_image(
    filename: str,
    identifier: str | None = None,
    *,
    preset_identifier: str = "",
    presets: list[Preset] | None = None,
) -> KeyxDocument:
    indirect = IndirectResource(
        identifier=identifier, filename=filename, preset_identifier=preset_identifier
    )
    image = Image(resource=Resource(indirect=indirect))
    return KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[Slide(contents=[SlideObject(object=CanvasObject(image=image))])],
        ),
        presets=presets or [],
    )


def doc_with_slide_layout(slide_layout: SlideLayout) -> KeyxDocument:
    return KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[Slide()],
            theme=KeynoteTheme(slide_layouts=[slide_layout]),
        ),
        presets=[],
    )


def doc_with_tables(*tables: Table) -> KeyxDocument:
    return KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[
                Slide(
                    contents=[SlideObject(object=CanvasObject(table=t)) for t in tables]
                )
            ],
        ),
        presets=[],
    )


def doc_with_chart(chart: Chart) -> KeyxDocument:
    return KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[Slide(contents=[SlideObject(object=CanvasObject(chart=chart))])],
        ),
        presets=[],
    )


def slide_with_hyperlink(target: SlideTarget) -> Slide:
    return Slide(
        note=Text(
            paragraphs=[
                Paragraph(
                    contents=[
                        Constituent(
                            hyperlink=HyperlinkField(
                                target=Hyperlink(slide_jump=target),
                                run=TextRun(string="jump"),
                            )
                        )
                    ]
                )
            ]
        )
    )
