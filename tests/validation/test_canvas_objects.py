# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


import pytest

from creator_studio_doc_format.core import (
    Anchor,
    Audio,
    Base64EncodedResource,
    CanvasObject,
    Chart,
    ColumnChart,
    ConnectionLine,
    End,
    Group,
    KeynoteTheme,
    KeyxDocument,
    PlaybackOptions,
    Position,
    Presentation,
    Resource,
    Shape,
    Slide,
    SlideLayout,
    SlideObject,
    SlideTarget,
    SourceKind,
)
from creator_studio_doc_format.validation import validate_document
from creator_studio_doc_format.validation._canvas_objects import _register_canvas_object

from .builders import doc_with_slide_layout, slide_size, slide_with_hyperlink


def test_validate_detects_duplicate_canvas_object_identifier() -> None:
    doc = KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[
                Slide(
                    contents=[
                        SlideObject(object=CanvasObject(shape=Shape(identifier="dup"))),
                        SlideObject(object=CanvasObject(shape=Shape(identifier="dup"))),
                    ]
                ),
            ],
        ),
        presets=[],
    )
    with pytest.raises(ValueError, match=r"`Shape\.identifier` .* is a duplicate"):
        validate_document(doc)


def test_validate_detects_duplicate_canvas_object_identifier_across_containers() -> (
    None
):
    doc = KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[
                Slide(
                    contents=[
                        SlideObject(object=CanvasObject(shape=Shape(identifier="dup")))
                    ]
                ),
                Slide(
                    contents=[
                        SlideObject(object=CanvasObject(shape=Shape(identifier="dup")))
                    ]
                ),
            ],
        ),
        presets=[],
    )
    with pytest.raises(
        ValueError,
        match=r"`Shape\.identifier` 'dup' is a duplicate \(at .*slides\[1\]",
    ):
        validate_document(doc)


def test_validate_detects_duplicate_identifier_on_a_nested_union_payload() -> None:
    def chart() -> SlideObject:
        return SlideObject(
            object=CanvasObject(chart=Chart(column=ColumnChart(identifier="dup")))
        )

    doc = KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[Slide(contents=[chart()]), Slide(contents=[chart()])],
        ),
        presets=[],
    )
    with pytest.raises(
        ValueError,
        match=r"`ColumnChart\.identifier` 'dup' is a duplicate \(at .*slides\[1\]",
    ):
        validate_document(doc)


def test_validate_detects_duplicate_identifier_in_group_and_slide() -> None:
    doc = KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[
                Slide(
                    contents=[
                        SlideObject(object=CanvasObject(shape=Shape(identifier="dup"))),
                        SlideObject(
                            object=CanvasObject(
                                group=Group(
                                    children=[
                                        CanvasObject(shape=Shape(identifier="dup"))
                                    ]
                                )
                            )
                        ),
                    ]
                )
            ],
        ),
        presets=[],
    )
    with pytest.raises(ValueError, match=r"`Shape\.identifier` 'dup' is a duplicate"):
        validate_document(doc)


def test_validate_allows_layout_sourced_object_to_share_its_layout_identifier() -> None:
    doc = KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[
                Slide(
                    layout="L",
                    contents=[
                        SlideObject(
                            object=CanvasObject(shape=Shape(identifier="from-layout")),
                            source_kind=SourceKind.LAYOUT,
                        )
                    ],
                )
            ],
            theme=KeynoteTheme(
                slide_layouts=[
                    SlideLayout(
                        name="L",
                        contents=[
                            SlideObject(
                                object=CanvasObject(
                                    shape=Shape(identifier="from-layout")
                                )
                            )
                        ],
                    )
                ]
            ),
        ),
        presets=[],
    )
    validate_document(doc)


def test_validate_detects_placeholder_sourced_object_reusing_a_layout_identifier() -> (
    None
):
    doc = KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[
                Slide(
                    layout="L",
                    contents=[
                        SlideObject(
                            object=CanvasObject(shape=Shape(identifier="reused")),
                            source_kind=SourceKind.PLACEHOLDER,
                        )
                    ],
                )
            ],
            theme=KeynoteTheme(
                slide_layouts=[
                    SlideLayout(
                        name="L",
                        contents=[
                            SlideObject(
                                object=CanvasObject(shape=Shape(identifier="reused"))
                            )
                        ],
                    )
                ]
            ),
        ),
        presets=[],
    )
    with pytest.raises(
        ValueError, match=r"`Shape\.identifier` 'reused' is a duplicate"
    ):
        validate_document(doc)


def test_validate_allows_distinct_canvas_object_identifiers_across_slides() -> None:
    doc = KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[
                Slide(
                    contents=[
                        SlideObject(object=CanvasObject(shape=Shape(identifier="a")))
                    ]
                ),
                Slide(
                    contents=[
                        SlideObject(object=CanvasObject(shape=Shape(identifier="b")))
                    ]
                ),
            ],
        ),
        presets=[],
    )
    validate_document(doc)


def test_register_canvas_object_raises_on_missing_identifier_attribute() -> None:
    shape = Shape()
    del shape.__dict__["identifier"]
    with pytest.raises(AttributeError, match="identifier"):
        _register_canvas_object(shape, "path", {})


def test_validate_connection_line_anchor_resolves_within_slide_contents() -> None:
    line = ConnectionLine(
        tail=End(end_point=Position(x=0, y=0), anchor=Anchor(object_id="shape1")),
        head=End(end_point=Position(x=100, y=0), anchor=Anchor(object_id="shape2")),
    )
    doc = KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[
                Slide(
                    contents=[
                        SlideObject(
                            object=CanvasObject(shape=Shape(identifier="shape1"))
                        ),
                        SlideObject(
                            object=CanvasObject(shape=Shape(identifier="shape2"))
                        ),
                        SlideObject(object=CanvasObject(connectionLine=line)),
                    ]
                )
            ],
        ),
        presets=[],
    )
    validate_document(doc)


def test_validate_connection_line_anchor_resolves_within_group_children() -> None:
    line = ConnectionLine(
        tail=End(end_point=Position(x=0, y=0), anchor=Anchor(object_id="shape1")),
        head=End(end_point=Position(x=100, y=0), anchor=Anchor(object_id="shape2")),
    )
    group = Group(
        children=[
            CanvasObject(shape=Shape(identifier="shape1")),
            CanvasObject(shape=Shape(identifier="shape2")),
            CanvasObject(connectionLine=line),
        ]
    )
    doc = KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[Slide(contents=[SlideObject(object=CanvasObject(group=group))])],
        ),
        presets=[],
    )
    validate_document(doc)


def test_validate_connection_line_anchor_missing_in_sibling_group_raises() -> None:
    group1 = Group(children=[CanvasObject(shape=Shape(identifier="shape-in-group1"))])
    line = ConnectionLine(
        tail=End(
            end_point=Position(x=0, y=0), anchor=Anchor(object_id="shape-in-group1")
        ),
        head=End(end_point=Position(x=100, y=0)),
    )
    group2 = Group(children=[CanvasObject(connectionLine=line)])
    doc = KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[
                Slide(
                    contents=[
                        SlideObject(object=CanvasObject(group=group1)),
                        SlideObject(object=CanvasObject(group=group2)),
                    ]
                )
            ],
        ),
        presets=[],
    )
    with pytest.raises(LookupError, match="shape-in-group1"):
        validate_document(doc)


def test_validate_connection_line_anchor_missing_in_slide_layout_raises() -> None:
    line = ConnectionLine(
        tail=End(end_point=Position(x=0, y=0), anchor=Anchor(object_id="shape1")),
        head=End(
            end_point=Position(x=100, y=0), anchor=Anchor(object_id="no-such-shape")
        ),
    )
    doc = doc_with_slide_layout(
        SlideLayout(
            name="Layout",
            contents=[
                SlideObject(object=CanvasObject(shape=Shape(identifier="shape1"))),
                SlideObject(object=CanvasObject(connectionLine=line)),
            ],
        )
    )
    with pytest.raises(LookupError, match="no-such-shape"):
        validate_document(doc)


def test_validate_connection_line_anchor_resolves_within_slide_layout() -> None:
    line = ConnectionLine(
        tail=End(end_point=Position(x=0, y=0), anchor=Anchor(object_id="shape1")),
        head=End(end_point=Position(x=100, y=0), anchor=Anchor(object_id="shape2")),
    )
    doc = doc_with_slide_layout(
        SlideLayout(
            name="Layout",
            contents=[
                SlideObject(object=CanvasObject(shape=Shape(identifier="shape1"))),
                SlideObject(object=CanvasObject(shape=Shape(identifier="shape2"))),
                SlideObject(object=CanvasObject(connectionLine=line)),
            ],
        )
    )
    validate_document(doc)


def test_validate_slide_target_by_identifier_resolves_forward_reference() -> None:
    doc = KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[
                slide_with_hyperlink(SlideTarget(by_identifier="later-slide")),
                Slide(identifier="later-slide"),
            ],
        ),
        presets=[],
    )
    validate_document(doc)


def test_validate_slide_target_by_identifier_missing_raises() -> None:
    doc = KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[slide_with_hyperlink(SlideTarget(by_identifier="no-such-slide"))],
        ),
        presets=[],
    )
    with pytest.raises(LookupError, match="no-such-slide"):
        validate_document(doc)


def test_validate_detects_duplicate_slide_identifier() -> None:
    doc = KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[Slide(identifier="dup"), Slide(identifier="dup")],
        ),
        presets=[],
    )
    with pytest.raises(ValueError, match=r"`Slide\.identifier` .* is a duplicate"):
        validate_document(doc)


def test_validate_allows_distinct_slide_identifiers() -> None:
    doc = KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[Slide(identifier="s1"), Slide(identifier="s2")],
        ),
        presets=[],
    )
    validate_document(doc)


def test_validate_detects_duplicate_slide_layout_identifier() -> None:
    doc = KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[Slide()],
            theme=KeynoteTheme(
                slide_layouts=[
                    SlideLayout(name="A", identifier="dup"),
                    SlideLayout(name="B", identifier="dup"),
                ]
            ),
        ),
        presets=[],
    )
    with pytest.raises(
        ValueError, match=r"`SlideLayout\.identifier` .* is a duplicate"
    ):
        validate_document(doc)


def test_validate_allows_distinct_slide_layout_identifiers() -> None:
    doc = KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[Slide()],
            theme=KeynoteTheme(
                slide_layouts=[
                    SlideLayout(name="A", identifier="t1"),
                    SlideLayout(name="B", identifier="t2"),
                ]
            ),
        ),
        presets=[],
    )
    validate_document(doc)


def test_validate_slide_layout_and_slide_may_share_identifier() -> None:
    doc = KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[Slide(identifier="shared")],
            theme=KeynoteTheme(
                slide_layouts=[SlideLayout(name="A", identifier="shared")]
            ),
        ),
        presets=[],
    )
    validate_document(doc)


def test_validate_slide_target_positional_case_is_not_checked() -> None:
    doc = KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[slide_with_hyperlink(SlideTarget(next=True))],
        ),
        presets=[],
    )
    validate_document(doc)


def test_validate_connection_line_end_point_without_anchor_is_fine() -> None:
    line = ConnectionLine(
        tail=End(end_point=Position(x=0, y=0)),
        head=End(end_point=Position(x=100, y=0), anchor=Anchor(object_id="shape1")),
    )
    doc = KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[
                Slide(
                    contents=[
                        SlideObject(
                            object=CanvasObject(shape=Shape(identifier="shape1"))
                        ),
                        SlideObject(object=CanvasObject(connectionLine=line)),
                    ]
                )
            ],
        ),
        presets=[],
    )
    validate_document(doc)


def test_validate_connection_line_anchored_end_without_end_point_raises() -> None:
    line = ConnectionLine(
        tail=End(end_point=Position(x=0, y=0)),
        head=End(anchor=Anchor(object_id="shape1")),
    )
    doc = KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[
                Slide(
                    contents=[
                        SlideObject(
                            object=CanvasObject(shape=Shape(identifier="shape1"))
                        ),
                        SlideObject(object=CanvasObject(connectionLine=line)),
                    ]
                )
            ],
        ),
        presets=[],
    )
    with pytest.raises(
        ValueError, match=r"`ConnectionLine\.End\.end_point` is missing"
    ):
        validate_document(doc)


def _audio(identifier: str) -> Audio:
    return Audio(
        identifier=identifier,
        resource=Resource(
            base64_encoded=Base64EncodedResource(string="AA==", filename="a.m4a")
        ),
        playback_options=PlaybackOptions(),
    )


def test_validate_connection_line_anchored_to_audio_is_not_checked() -> None:
    line = ConnectionLine(
        tail=End(end_point=Position(x=0, y=0)),
        head=End(end_point=Position(x=100, y=0), anchor=Anchor(object_id="clip")),
    )
    doc = KeyxDocument(
        Presentation(
            slide_size=slide_size(),
            slides=[
                Slide(
                    contents=[
                        SlideObject(object=CanvasObject(audio=_audio("clip"))),
                        SlideObject(object=CanvasObject(connectionLine=line)),
                    ]
                )
            ],
        ),
        presets=[],
    )
    validate_document(doc)
