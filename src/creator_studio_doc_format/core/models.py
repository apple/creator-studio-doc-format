# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0

"""Generated models (Pydantic v2).
Auto-generated. Don't edit. Each field is named after its JSON key.
"""

# These models only declare fields and their JSON metadata. The codec lives in `_wire.py`.
from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Annotated, Literal

from pydantic import Field, Strict

from ._wire import ObjectModel, Override, TaggedUnionModel, wire, wire_union


@wire(
    "com.apple.apps.content-language.audio",
    version="1.0",
    fields=[
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
        ("resource", (1, 0), "req"),
        ("playback_options", (1, 0), "req"),
        ("native_audio_recording", (1, 0), "def"),
    ],
)
class Audio(ObjectModel):
    """A sound attached to a slide.

An audio object has no visible size of its own; it appears as a fixed-size icon, so Keynote ignores the size in `geometry` and only uses the position."""
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=False, description="A Boolean value that indicates whether the object's width-to-height ratio is locked when the object resizes. The lock doesn't constrain the `geometry` property. If this property is absent, images, movies, and groups default to `true`, and other objects to `false`.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")
    resource: Resource = Field(description="The resource that contains the audio data. If the resource isn't playable on the device, has no audio track, or contains video, the object has no effect.")
    playback_options: PlaybackOptions = Field(description="The playback settings for the audio, such as volume, start and end trim times, looping, and whether playback continues across slides.")
    native_audio_recording: bool = Field(default=False, description="A Boolean value that indicates whether to treat the audio as recorded into the document rather than imported as a sound file. Recorded audio can't loop back and forth, and instead plays from beginning to end: when this value is `true`, a Loop Back and Forth setting is replaced with no looping.")


@wire(
    "com.apple.apps.content-language.canvas-object-generic",
    version="1.0",
    fields=[
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
    ],
)
class GenericCanvasObject(ObjectModel):
    """An object with only the properties of CanvasObject.

It's the form `CanvasObject` reserves for a kind of object this version doesn't recognize, such as one a later version of the format introduces. Because it doesn't name a specific kind, Keynote can't rebuild an object written this way, and drops it when it reads the document, so a producer writes the specific kind instead."""
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=False, description="A Boolean value that indicates whether the object's width-to-height ratio is locked when the object resizes. The lock doesn't constrain the `geometry` property. If this property is absent, images, movies, and groups default to `true`, and other objects to `false`.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")


@wire_union(
    "com.apple.apps.content-language.canvas-object",
    version="1.2",
    cases=[
        ("audio", (1, 2), False),
        ("chart", (1, 2), False),
        ("connectionLine", (1, 0), False),
        ("genericCanvasObject", (1, 0), False),
        ("group", (1, 0), False),
        ("image", (1, 0), False),
        ("movie", (1, 2), False),
        ("shape", (1, 0), False),
        ("table", (1, 0), False),
        ("textbox", (1, 1), False),
    ],
)
class CanvasObject(TaggedUnionModel):
    """The identity, placement, and accessibility properties shared by objects you can place on a slide, in a group, or inline in text.

When authoring a Keynote Interchange Format document, you don't create these directly, but instead create objects with the `type_identifier` that include these same properties directly rather than under a key of their own. The same name is also the type that holds any one of those objects, which is what `SlideObject.object`, `Group.children`, and a paragraph's inline object contain."""
    audio: Audio | None = None
    chart: Chart | None = None
    connectionLine: ConnectionLine | None = None
    genericCanvasObject: GenericCanvasObject | None = None
    group: Group | None = None
    image: Image | None = None
    movie: Movie | None = None
    shape: Shape | None = None
    table: Table | None = None
    textbox: Textbox | None = None

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_CanvasObjectCase, ...]: ...

        def union_primary(self) -> _CanvasObjectCase | None: ...

        def union_primary_name(self) -> Literal["audio", "chart", "connectionLine", "genericCanvasObject", "group", "image", "movie", "shape", "table", "textbox"] | None: ...


@wire(
    "com.apple.apps.content-language.caption-owning-generic",
    version="1.0",
    fields=[
        ("caption", (1, 0), "opt"),
    ],
)
class GenericCaptionOwning(ObjectModel):
    """An object with only the properties of caption owning.

Every set of shared properties has one, to stand in for an object whose kind isn't recognized. Nothing in the format has the type `CaptionOwning`, though, so this object never appears in a document; its properties appear only as part of the types that adopt `CaptionOwning`."""
    caption: Label | None = Field(default=None, description="The object's caption, which Keynote always places below the object. If a caption is off, you still write it out with `Label.is_visible` set to `false`, so having a value doesn't mean the caption shows.")


@wire_union(
    "com.apple.apps.content-language.caption-owning",
    version="1.0",
    cases=[
        ("genericCaptionOwning", (1, 0), False),
    ],
)
class CaptionOwning(TaggedUnionModel):
    """The properties for defining an optional caption an object can display.

`shape`, `textbox`, `image`, `movie`, `group`, `table`, and every chart type adopt them."""
    genericCaptionOwning: GenericCaptionOwning | None = None

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_CaptionOwningCase, ...]: ...

        def union_primary(self) -> _CaptionOwningCase | None: ...

        def union_primary_name(self) -> Literal["genericCaptionOwning"] | None: ...


@wire(
    "com.apple.apps.content-language.area3-dchart",
    version="1.0",
    fields=[
        ("title", (1, 0), "opt"),
        ("caption", (1, 0), "opt"),
        ("data", (1, 0), "opt"),
        ("show_legend", (1, 0), "def"),
        ("legend", (1, 0), "opt"),
        ("series", (1, 0), "opt"),
        ("chart_colors", (1, 0), "opt"),
        ("category_axis", (1, 0), "opt"),
        ("value_axis", (1, 0), "opt"),
        ("value_axis_secondary", (1, 0), "opt"),
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
    ],
)
class Area3DChart(ObjectModel):
    """A 3D area chart.

3D appearance settings such as rotation, depth, lighting, and textures aren't included: rotation and depth take the default for this chart type, and lighting and a textured series' fill come from the chart's style."""
    title: Label | None = Field(default=None, description="The object's title.")
    caption: Label | None = Field(default=None, description="The object's caption, which Keynote always places below the object. If a caption is off, you still write it out with `Label.is_visible` set to `false`, so having a value doesn't mean the caption shows.")
    data: ChartData | None = Field(default=None, description="The chart's data grid, together with its plot direction and data-source mode. This data replaces the placeholder data a new chart starts with; when omitted, that placeholder data remains.")
    show_legend: bool = Field(default=True, description="A Boolean value that indicates whether the chart's legend appears. This value is independent of the `legend` property, which sets the legend's placement and text style rather than its visibility.")
    legend: ChartLegend | None = Field(default=None, description="The placement and label text style of the chart's legend. This value doesn't control whether the legend appears (see `show_legend`), and it only applies to a chart that has a legend.")
    series: list[ChartSeries] | None = Field(default=None, description="The styling and label formatting for individual data series. Each entry applies to the series named by its `ChartSeries.series_index`, or to the series at the same position when `ChartSeries.series_index` is omitted; entries that don't correspond to a series in the data don't have an effect.")
    chart_colors: list[ChartColor] | None = Field(default=None, description="The chart's ordered series styles. A series takes the entry at its own position, and the chart's style supplies any position without an entry or with an empty one, so the list doesn't wrap. Entries past the last series also remain. Keynote reads one entry for each series style in the chart's style and ignores any further entries.")
    category_axis: ChartCategoryAxis | None = Field(default=None, description="The category axis, along which Keynote lays out the chart's categories. When omitted, the category axis keeps the appearance it inherits from the chart's style.")
    value_axis: ChartValueAxis | None = Field(default=None, description="The primary value axis, which carries the numeric scale to measure the series against. When omitted, the value axis keeps the appearance it inherits from the chart's style.")
    value_axis_secondary: ChartValueAxis | None = Field(default=None, description="The second value axis, used only by a two-axis chart that actually plots a series against a second value scale. On any other chart type, this value doesn't have an effect.")
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=False, description="A Boolean value that indicates whether the object's width-to-height ratio is locked when the object resizes. The lock doesn't constrain the `geometry` property. If this property is absent, images, movies, and groups default to `true`, and other objects to `false`.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")


@wire(
    "com.apple.apps.content-language.area-chart",
    version="1.0",
    fields=[
        ("title", (1, 0), "opt"),
        ("caption", (1, 0), "opt"),
        ("data", (1, 0), "opt"),
        ("show_legend", (1, 0), "def"),
        ("legend", (1, 0), "opt"),
        ("series", (1, 0), "opt"),
        ("chart_colors", (1, 0), "opt"),
        ("category_axis", (1, 0), "opt"),
        ("value_axis", (1, 0), "opt"),
        ("value_axis_secondary", (1, 0), "opt"),
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
    ],
)
class AreaChart(ObjectModel):
    """A 2D area chart.

Keynote draws each series as a filled region against a shared category axis and value axis."""
    title: Label | None = Field(default=None, description="The object's title.")
    caption: Label | None = Field(default=None, description="The object's caption, which Keynote always places below the object. If a caption is off, you still write it out with `Label.is_visible` set to `false`, so having a value doesn't mean the caption shows.")
    data: ChartData | None = Field(default=None, description="The chart's data grid, together with its plot direction and data-source mode. This data replaces the placeholder data a new chart starts with; when omitted, that placeholder data remains.")
    show_legend: bool = Field(default=True, description="A Boolean value that indicates whether the chart's legend appears. This value is independent of the `legend` property, which sets the legend's placement and text style rather than its visibility.")
    legend: ChartLegend | None = Field(default=None, description="The placement and label text style of the chart's legend. This value doesn't control whether the legend appears (see `show_legend`), and it only applies to a chart that has a legend.")
    series: list[ChartSeries] | None = Field(default=None, description="The styling and label formatting for individual data series. Each entry applies to the series named by its `ChartSeries.series_index`, or to the series at the same position when `ChartSeries.series_index` is omitted; entries that don't correspond to a series in the data don't have an effect.")
    chart_colors: list[ChartColor] | None = Field(default=None, description="The chart's ordered series styles. A series takes the entry at its own position, and the chart's style supplies any position without an entry or with an empty one, so the list doesn't wrap. Entries past the last series also remain. Keynote reads one entry for each series style in the chart's style and ignores any further entries.")
    category_axis: ChartCategoryAxis | None = Field(default=None, description="The category axis, along which Keynote lays out the chart's categories. When omitted, the category axis keeps the appearance it inherits from the chart's style.")
    value_axis: ChartValueAxis | None = Field(default=None, description="The primary value axis, which carries the numeric scale to measure the series against. When omitted, the value axis keeps the appearance it inherits from the chart's style.")
    value_axis_secondary: ChartValueAxis | None = Field(default=None, description="The second value axis, used only by a two-axis chart that actually plots a series against a second value scale. On any other chart type, this value doesn't have an effect.")
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=False, description="A Boolean value that indicates whether the object's width-to-height ratio is locked when the object resizes. The lock doesn't constrain the `geometry` property. If this property is absent, images, movies, and groups default to `true`, and other objects to `false`.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")


@wire(
    "com.apple.apps.content-language.bar3-dchart",
    version="1.0",
    fields=[
        ("title", (1, 0), "opt"),
        ("caption", (1, 0), "opt"),
        ("data", (1, 0), "opt"),
        ("show_legend", (1, 0), "def"),
        ("legend", (1, 0), "opt"),
        ("series", (1, 0), "opt"),
        ("chart_colors", (1, 0), "opt"),
        ("category_axis", (1, 0), "opt"),
        ("value_axis", (1, 0), "opt"),
        ("value_axis_secondary", (1, 0), "opt"),
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
    ],
)
class Bar3DChart(ObjectModel):
    """A 3D horizontal bar chart.

3D appearance settings such as rotation, depth, lighting, and textures aren't included: rotation and depth take the default for this chart type, and lighting and a textured series' fill come from the chart's style."""
    title: Label | None = Field(default=None, description="The object's title.")
    caption: Label | None = Field(default=None, description="The object's caption, which Keynote always places below the object. If a caption is off, you still write it out with `Label.is_visible` set to `false`, so having a value doesn't mean the caption shows.")
    data: ChartData | None = Field(default=None, description="The chart's data grid, together with its plot direction and data-source mode. This data replaces the placeholder data a new chart starts with; when omitted, that placeholder data remains.")
    show_legend: bool = Field(default=True, description="A Boolean value that indicates whether the chart's legend appears. This value is independent of the `legend` property, which sets the legend's placement and text style rather than its visibility.")
    legend: ChartLegend | None = Field(default=None, description="The placement and label text style of the chart's legend. This value doesn't control whether the legend appears (see `show_legend`), and it only applies to a chart that has a legend.")
    series: list[ChartSeries] | None = Field(default=None, description="The styling and label formatting for individual data series. Each entry applies to the series named by its `ChartSeries.series_index`, or to the series at the same position when `ChartSeries.series_index` is omitted; entries that don't correspond to a series in the data don't have an effect.")
    chart_colors: list[ChartColor] | None = Field(default=None, description="The chart's ordered series styles. A series takes the entry at its own position, and the chart's style supplies any position without an entry or with an empty one, so the list doesn't wrap. Entries past the last series also remain. Keynote reads one entry for each series style in the chart's style and ignores any further entries.")
    category_axis: ChartCategoryAxis | None = Field(default=None, description="The category axis, along which Keynote lays out the chart's categories. When omitted, the category axis keeps the appearance it inherits from the chart's style.")
    value_axis: ChartValueAxis | None = Field(default=None, description="The primary value axis, which carries the numeric scale to measure the series against. When omitted, the value axis keeps the appearance it inherits from the chart's style.")
    value_axis_secondary: ChartValueAxis | None = Field(default=None, description="The second value axis, used only by a two-axis chart that actually plots a series against a second value scale. On any other chart type, this value doesn't have an effect.")
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=False, description="A Boolean value that indicates whether the object's width-to-height ratio is locked when the object resizes. The lock doesn't constrain the `geometry` property. If this property is absent, images, movies, and groups default to `true`, and other objects to `false`.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")


@wire(
    "com.apple.apps.content-language.bar-chart",
    version="1.0",
    fields=[
        ("title", (1, 0), "opt"),
        ("caption", (1, 0), "opt"),
        ("data", (1, 0), "opt"),
        ("show_legend", (1, 0), "def"),
        ("legend", (1, 0), "opt"),
        ("series", (1, 0), "opt"),
        ("chart_colors", (1, 0), "opt"),
        ("category_axis", (1, 0), "opt"),
        ("value_axis", (1, 0), "opt"),
        ("value_axis_secondary", (1, 0), "opt"),
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
    ],
)
class BarChart(ObjectModel):
    """A 2D bar chart.

Keynote draws each series as horizontal bars against a shared category axis and value axis."""
    title: Label | None = Field(default=None, description="The object's title.")
    caption: Label | None = Field(default=None, description="The object's caption, which Keynote always places below the object. If a caption is off, you still write it out with `Label.is_visible` set to `false`, so having a value doesn't mean the caption shows.")
    data: ChartData | None = Field(default=None, description="The chart's data grid, together with its plot direction and data-source mode. This data replaces the placeholder data a new chart starts with; when omitted, that placeholder data remains.")
    show_legend: bool = Field(default=True, description="A Boolean value that indicates whether the chart's legend appears. This value is independent of the `legend` property, which sets the legend's placement and text style rather than its visibility.")
    legend: ChartLegend | None = Field(default=None, description="The placement and label text style of the chart's legend. This value doesn't control whether the legend appears (see `show_legend`), and it only applies to a chart that has a legend.")
    series: list[ChartSeries] | None = Field(default=None, description="The styling and label formatting for individual data series. Each entry applies to the series named by its `ChartSeries.series_index`, or to the series at the same position when `ChartSeries.series_index` is omitted; entries that don't correspond to a series in the data don't have an effect.")
    chart_colors: list[ChartColor] | None = Field(default=None, description="The chart's ordered series styles. A series takes the entry at its own position, and the chart's style supplies any position without an entry or with an empty one, so the list doesn't wrap. Entries past the last series also remain. Keynote reads one entry for each series style in the chart's style and ignores any further entries.")
    category_axis: ChartCategoryAxis | None = Field(default=None, description="The category axis, along which Keynote lays out the chart's categories. When omitted, the category axis keeps the appearance it inherits from the chart's style.")
    value_axis: ChartValueAxis | None = Field(default=None, description="The primary value axis, which carries the numeric scale to measure the series against. When omitted, the value axis keeps the appearance it inherits from the chart's style.")
    value_axis_secondary: ChartValueAxis | None = Field(default=None, description="The second value axis, used only by a two-axis chart that actually plots a series against a second value scale. On any other chart type, this value doesn't have an effect.")
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=False, description="A Boolean value that indicates whether the object's width-to-height ratio is locked when the object resizes. The lock doesn't constrain the `geometry` property. If this property is absent, images, movies, and groups default to `true`, and other objects to `false`.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")


@wire(
    "com.apple.apps.content-language.bar-interactive-chart",
    version="1.0",
    fields=[
        ("title", (1, 0), "opt"),
        ("caption", (1, 0), "opt"),
        ("data", (1, 0), "opt"),
        ("show_legend", (1, 0), "def"),
        ("legend", (1, 0), "opt"),
        ("series", (1, 0), "opt"),
        ("chart_colors", (1, 0), "opt"),
        ("category_axis", (1, 0), "opt"),
        ("value_axis", (1, 0), "opt"),
        ("value_axis_secondary", (1, 0), "opt"),
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
    ],
)
class BarInteractiveChart(ObjectModel):
    """An interactive horizontal bar chart, which shows one data set at a time.

You can step between the data sets. The interactive control, the position of the data set name, and which data set is shown aren't included, so they take the default for this chart type."""
    title: Label | None = Field(default=None, description="The object's title.")
    caption: Label | None = Field(default=None, description="The object's caption, which Keynote always places below the object. If a caption is off, you still write it out with `Label.is_visible` set to `false`, so having a value doesn't mean the caption shows.")
    data: ChartData | None = Field(default=None, description="The chart's data grid, together with its plot direction and data-source mode. This data replaces the placeholder data a new chart starts with; when omitted, that placeholder data remains.")
    show_legend: bool = Field(default=True, description="A Boolean value that indicates whether the chart's legend appears. This value is independent of the `legend` property, which sets the legend's placement and text style rather than its visibility.")
    legend: ChartLegend | None = Field(default=None, description="The placement and label text style of the chart's legend. This value doesn't control whether the legend appears (see `show_legend`), and it only applies to a chart that has a legend.")
    series: list[ChartSeries] | None = Field(default=None, description="The styling and label formatting for individual data series. Each entry applies to the series named by its `ChartSeries.series_index`, or to the series at the same position when `ChartSeries.series_index` is omitted; entries that don't correspond to a series in the data don't have an effect.")
    chart_colors: list[ChartColor] | None = Field(default=None, description="The chart's ordered series styles. A series takes the entry at its own position, and the chart's style supplies any position without an entry or with an empty one, so the list doesn't wrap. Entries past the last series also remain. Keynote reads one entry for each series style in the chart's style and ignores any further entries.")
    category_axis: ChartCategoryAxis | None = Field(default=None, description="The category axis, along which Keynote lays out the chart's categories. When omitted, the category axis keeps the appearance it inherits from the chart's style.")
    value_axis: ChartValueAxis | None = Field(default=None, description="The primary value axis, which carries the numeric scale to measure the series against. When omitted, the value axis keeps the appearance it inherits from the chart's style.")
    value_axis_secondary: ChartValueAxis | None = Field(default=None, description="The second value axis, used only by a two-axis chart that actually plots a series against a second value scale. On any other chart type, this value doesn't have an effect.")
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=False, description="A Boolean value that indicates whether the object's width-to-height ratio is locked when the object resizes. The lock doesn't constrain the `geometry` property. If this property is absent, images, movies, and groups default to `true`, and other objects to `false`.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")


@wire(
    "com.apple.apps.content-language.bubble-chart",
    version="1.0",
    fields=[
        ("title", (1, 0), "opt"),
        ("caption", (1, 0), "opt"),
        ("data", (1, 0), "opt"),
        ("show_legend", (1, 0), "def"),
        ("legend", (1, 0), "opt"),
        ("series", (1, 0), "opt"),
        ("chart_colors", (1, 0), "opt"),
        ("value_axis_x", (1, 0), "opt"),
        ("value_axis_y", (1, 0), "opt"),
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
    ],
)
class BubbleChart(ObjectModel):
    """A bubble chart.

Keynote plots each data point against an X and a Y value axis, and its bubble area comes from a third data value rather than a series setting. See `data.shared_xvalues` for how the grid's rows or columns map onto each series."""
    title: Label | None = Field(default=None, description="The object's title.")
    caption: Label | None = Field(default=None, description="The object's caption, which Keynote always places below the object. If a caption is off, you still write it out with `Label.is_visible` set to `false`, so having a value doesn't mean the caption shows.")
    data: ChartData | None = Field(default=None, description="The chart's data grid, together with its plot direction and data-source mode. This data replaces the placeholder data a new chart starts with; when omitted, that placeholder data remains.")
    show_legend: bool = Field(default=True, description="A Boolean value that indicates whether the chart's legend appears. This value is independent of the `legend` property, which sets the legend's placement and text style rather than its visibility.")
    legend: ChartLegend | None = Field(default=None, description="The placement and label text style of the chart's legend. This value doesn't control whether the legend appears (see `show_legend`), and it only applies to a chart that has a legend.")
    series: list[ChartSeries] | None = Field(default=None, description="The styling and label formatting for individual data series. Each entry applies to the series named by its `ChartSeries.series_index`, or to the series at the same position when `ChartSeries.series_index` is omitted; entries that don't correspond to a series in the data don't have an effect.")
    chart_colors: list[ChartColor] | None = Field(default=None, description="The chart's ordered series styles. A series takes the entry at its own position, and the chart's style supplies any position without an entry or with an empty one, so the list doesn't wrap. Entries past the last series also remain. Keynote reads one entry for each series style in the chart's style and ignores any further entries.")
    value_axis_x: ChartValueAxis | None = Field(default=None, description="The horizontal (X) value axis. When omitted, the X axis keeps the appearance it inherits from the chart's style.")
    value_axis_y: ChartValueAxis | None = Field(default=None, description="The vertical (Y) value axis. When omitted, the Y axis keeps the appearance it inherits from the chart's style.")
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=False, description="A Boolean value that indicates whether the object's width-to-height ratio is locked when the object resizes. The lock doesn't constrain the `geometry` property. If this property is absent, images, movies, and groups default to `true`, and other objects to `false`.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")


@wire(
    "com.apple.apps.content-language.bubble-interactive-chart",
    version="1.0",
    fields=[
        ("title", (1, 0), "opt"),
        ("caption", (1, 0), "opt"),
        ("data", (1, 0), "opt"),
        ("show_legend", (1, 0), "def"),
        ("legend", (1, 0), "opt"),
        ("series", (1, 0), "opt"),
        ("chart_colors", (1, 0), "opt"),
        ("value_axis_x", (1, 0), "opt"),
        ("value_axis_y", (1, 0), "opt"),
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
    ],
)
class BubbleInteractiveChart(ObjectModel):
    """An interactive bubble chart, which shows one data set at a time.

You can step between the data sets. Keynote lays out the series as a bubble chart; for more information, see `data.shared_xvalues`. The interactive control, the position of the data set name, and which data set is shown aren't included, so they take the default for this chart type."""
    title: Label | None = Field(default=None, description="The object's title.")
    caption: Label | None = Field(default=None, description="The object's caption, which Keynote always places below the object. If a caption is off, you still write it out with `Label.is_visible` set to `false`, so having a value doesn't mean the caption shows.")
    data: ChartData | None = Field(default=None, description="The chart's data grid, together with its plot direction and data-source mode. This data replaces the placeholder data a new chart starts with; when omitted, that placeholder data remains.")
    show_legend: bool = Field(default=True, description="A Boolean value that indicates whether the chart's legend appears. This value is independent of the `legend` property, which sets the legend's placement and text style rather than its visibility.")
    legend: ChartLegend | None = Field(default=None, description="The placement and label text style of the chart's legend. This value doesn't control whether the legend appears (see `show_legend`), and it only applies to a chart that has a legend.")
    series: list[ChartSeries] | None = Field(default=None, description="The styling and label formatting for individual data series. Each entry applies to the series named by its `ChartSeries.series_index`, or to the series at the same position when `ChartSeries.series_index` is omitted; entries that don't correspond to a series in the data don't have an effect.")
    chart_colors: list[ChartColor] | None = Field(default=None, description="The chart's ordered series styles. A series takes the entry at its own position, and the chart's style supplies any position without an entry or with an empty one, so the list doesn't wrap. Entries past the last series also remain. Keynote reads one entry for each series style in the chart's style and ignores any further entries.")
    value_axis_x: ChartValueAxis | None = Field(default=None, description="The horizontal (X) value axis. When omitted, the X axis keeps the appearance it inherits from the chart's style.")
    value_axis_y: ChartValueAxis | None = Field(default=None, description="The vertical (Y) value axis. When omitted, the Y axis keeps the appearance it inherits from the chart's style.")
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=False, description="A Boolean value that indicates whether the object's width-to-height ratio is locked when the object resizes. The lock doesn't constrain the `geometry` property. If this property is absent, images, movies, and groups default to `true`, and other objects to `false`.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")


@wire(
    "com.apple.apps.content-language.category-comparison-chart-generic",
    version="1.0",
    fields=[
        ("category_axis", (1, 0), "opt"),
        ("value_axis", (1, 0), "opt"),
        ("value_axis_secondary", (1, 0), "opt"),
    ],
)
class GenericCategoryComparisonChart(ObjectModel):
    """A stand-in for a chart that compares categories against a value scale, when the reader doesn't recognize its kind.

Every set of shared properties has one, to stand in for an object whose kind isn't recognized. Nothing in the format has the type `CategoryComparisonChart`, though, so this object never appears in a document; its properties appear only as part of the types that adopt `CategoryComparisonChart`."""
    category_axis: ChartCategoryAxis | None = Field(default=None, description="The category axis, along which Keynote lays out the chart's categories. When omitted, the category axis keeps the appearance it inherits from the chart's style.")
    value_axis: ChartValueAxis | None = Field(default=None, description="The primary value axis, which carries the numeric scale to measure the series against. When omitted, the value axis keeps the appearance it inherits from the chart's style.")
    value_axis_secondary: ChartValueAxis | None = Field(default=None, description="The second value axis, used only by a two-axis chart that actually plots a series against a second value scale. On any other chart type, this value doesn't have an effect.")


@wire_union(
    "com.apple.apps.content-language.category-comparison-chart",
    version="1.0",
    cases=[
        ("area3Dchart", (1, 0), False),
        ("areaChart", (1, 0), False),
        ("bar3Dchart", (1, 0), False),
        ("barChart", (1, 0), False),
        ("barInteractiveChart", (1, 0), False),
        ("column3Dchart", (1, 0), False),
        ("columnChart", (1, 0), False),
        ("columnInteractiveChart", (1, 0), False),
        ("genericCategoryComparisonChart", (1, 0), False),
        ("line3Dchart", (1, 0), False),
        ("lineChart", (1, 0), False),
        ("mixedChart", (1, 0), False),
        ("radarChart", (1, 0), False),
        ("stackedArea3Dchart", (1, 0), False),
        ("stackedAreaChart", (1, 0), False),
        ("stackedBar3Dchart", (1, 0), False),
        ("stackedBarChart", (1, 0), False),
        ("stackedColumn3Dchart", (1, 0), False),
        ("stackedColumnChart", (1, 0), False),
        ("twoAxisChart", (1, 0), False),
    ],
)
class CategoryComparisonChart(TaggedUnionModel):
    """The axes shared by every chart type that compares categories against a value scale.

These chart types are the column, bar, line, and area charts; their stacked, 3D, and interactive variants; and the mixed, radar, and two-axis charts."""
    area3Dchart: Area3DChart | None = None
    areaChart: AreaChart | None = None
    bar3Dchart: Bar3DChart | None = None
    barChart: BarChart | None = None
    barInteractiveChart: BarInteractiveChart | None = None
    column3Dchart: Column3DChart | None = None
    columnChart: ColumnChart | None = None
    columnInteractiveChart: ColumnInteractiveChart | None = None
    genericCategoryComparisonChart: GenericCategoryComparisonChart | None = None
    line3Dchart: Line3DChart | None = None
    lineChart: LineChart | None = None
    mixedChart: MixedChart | None = None
    radarChart: RadarChart | None = None
    stackedArea3Dchart: StackedArea3DChart | None = None
    stackedAreaChart: StackedAreaChart | None = None
    stackedBar3Dchart: StackedBar3DChart | None = None
    stackedBarChart: StackedBarChart | None = None
    stackedColumn3Dchart: StackedColumn3DChart | None = None
    stackedColumnChart: StackedColumnChart | None = None
    twoAxisChart: TwoAxisChart | None = None

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_CategoryComparisonChartCase, ...]: ...

        def union_primary(self) -> _CategoryComparisonChartCase | None: ...

        def union_primary_name(self) -> Literal["area3Dchart", "areaChart", "bar3Dchart", "barChart", "barInteractiveChart", "column3Dchart", "columnChart", "columnInteractiveChart", "genericCategoryComparisonChart", "line3Dchart", "lineChart", "mixedChart", "radarChart", "stackedArea3Dchart", "stackedAreaChart", "stackedBar3Dchart", "stackedBarChart", "stackedColumn3Dchart", "stackedColumnChart", "twoAxisChart"] | None: ...


@wire_union(
    "com.apple.apps.content-language.chart",
    version="1.0",
    cases=[
        ("area", (1, 0), False),
        ("area_3d", (1, 0), False),
        ("bar", (1, 0), False),
        ("bar_3d", (1, 0), False),
        ("bar_interactive", (1, 0), False),
        ("bubble", (1, 0), False),
        ("bubble_interactive", (1, 0), False),
        ("column", (1, 0), False),
        ("column_3d", (1, 0), False),
        ("column_interactive", (1, 0), False),
        ("donut", (1, 0), False),
        ("line", (1, 0), False),
        ("line_3d", (1, 0), False),
        ("mixed", (1, 0), False),
        ("pie", (1, 0), False),
        ("pie_3d", (1, 0), False),
        ("radar", (1, 0), False),
        ("scatter", (1, 0), False),
        ("scatter_interactive", (1, 0), False),
        ("stacked_area", (1, 0), False),
        ("stacked_area_3d", (1, 0), False),
        ("stacked_bar", (1, 0), False),
        ("stacked_bar_3d", (1, 0), False),
        ("stacked_column", (1, 0), False),
        ("stacked_column_3d", (1, 0), False),
        ("two_axis", (1, 0), False),
    ],
)
class Chart(TaggedUnionModel):
    """An object that plots a grid of data in a visual style such as column, pie, or scatter.

Write a chart as an object with a single key, which names its chart type, such as `column` or `pie`, and holds that type's settings. The chart type decides only how Keynote plots the series: every chart type uses the same chart data, so when you change a chart's type, that change replots the existing series without rewriting the data."""
    area: AreaChart | None = Field(default=None, description="A line chart with the region between the line and the axis filled, one region for each series.")
    area_3d: Area3DChart | None = Field(default=None, description="A 3D area chart.")
    bar: BarChart | None = Field(default=None, description="Values as horizontal bars, one bar for each series within each category.")
    bar_3d: Bar3DChart | None = Field(default=None, description="A 3D bar chart.")
    bar_interactive: BarInteractiveChart | None = Field(default=None, description="An interactive bar chart, which shows one data set at a time.")
    bubble: BubbleChart | None = Field(default=None, description="A scatter chart whose third value sets the area of each point.")
    bubble_interactive: BubbleInteractiveChart | None = Field(default=None, description="An interactive bubble chart, which shows one data set at a time.")
    column: ColumnChart | None = Field(default=None, description="Values as vertical bars, one bar for each series within each category.")
    column_3d: Column3DChart | None = Field(default=None, description="A 3D column chart.")
    column_interactive: ColumnInteractiveChart | None = Field(default=None, description="An interactive column chart, which shows one data set at a time.")
    donut: DonutChart | None = Field(default=None, description="A pie chart that appears as a ring with an open center.")
    line: LineChart | None = Field(default=None, description="Values as points joined by a line, with one line for each series.")
    line_3d: Line3DChart | None = Field(default=None, description="A 3D line chart.")
    mixed: MixedChart | None = Field(default=None, description="A mixed chart.\n\nEach series can appear as columns, as a line, or as an area. For more information on mixed charts, see `ChartSeries.mixed_series_type`.")
    pie: PieChart | None = Field(default=None, description="One series as wedges of a circle, with each wedge sized by its share of the total.")
    pie_3d: Pie3DChart | None = Field(default=None, description="A 3D pie chart.")
    radar: RadarChart | None = Field(default=None, description="Categories that appear around a circle, with each series appearing as a closed outline through its values.")
    scatter: ScatterChart | None = Field(default=None, description="Each series appears as a plot of pairs of X and Y values against two value axes, rather than against categories.")
    scatter_interactive: ScatterInteractiveChart | None = Field(default=None, description="An interactive scatter chart, which shows one data set at a time.")
    stacked_area: StackedAreaChart | None = Field(default=None, description="Filled regions that stack on one another, so the outer edge is the category total.")
    stacked_area_3d: StackedArea3DChart | None = Field(default=None, description="A 3D stacked area chart.")
    stacked_bar: StackedBarChart | None = Field(default=None, description="Horizontal bars with series that stack end to end, so each bar's length is the category total.")
    stacked_bar_3d: StackedBar3DChart | None = Field(default=None, description="A 3D stacked bar chart.")
    stacked_column: StackedColumnChart | None = Field(default=None, description="Vertical bars with series that stack end to end, so each column's height is the category total.")
    stacked_column_3d: StackedColumn3DChart | None = Field(default=None, description="A 3D stacked column chart.")
    two_axis: TwoAxisChart | None = Field(default=None, description="A two-axis chart.\n\nThis type of chart plots each series against either the primary or the secondary value axis; for more information about axes, see `ChartSeries.y_axis_selection`. Each series can appear as columns, as a line, or as an area. For more information, see `ChartSeries.mixed_series_type`.")

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_ChartCase, ...]: ...

        def union_primary(self) -> _ChartCase | None: ...

        def union_primary_name(self) -> Literal["area", "area_3d", "bar", "bar_3d", "bar_interactive", "bubble", "bubble_interactive", "column", "column_3d", "column_interactive", "donut", "line", "line_3d", "mixed", "pie", "pie_3d", "radar", "scatter", "scatter_interactive", "stacked_area", "stacked_area_3d", "stacked_bar", "stacked_bar_3d", "stacked_column", "stacked_column_3d", "two_axis"] | None: ...


@wire(
    "com.apple.apps.content-language.chart-axis-common-generic",
    version="1.0",
    fields=[
        ("title", (1, 0), "opt"),
        ("title_text_style", (1, 0), "opt"),
        ("label_text_style", (1, 0), "opt"),
        ("show_labels", (1, 0), "def"),
        ("show_title", (1, 0), "def"),
        ("show_major_tickmarks", (1, 0), "def"),
        ("show_minor_tickmarks", (1, 0), "def"),
        ("labels_orientation", (1, 0), "opt"),
    ],
)
class GenericChartAxisCommon(ObjectModel):
    """A stand-in for a chart axis, when the reader doesn't recognize its kind.

Every set of shared properties has one, to stand in for an object whose kind isn't recognized. Nothing in the format has the type `ChartAxisCommon`, though, so this object never appears in a document; its properties appear only as part of the types that adopt `ChartAxisCommon`."""
    title: str | None = Field(default=None, description="The text of the axis title. Whether the title is shown is controlled separately by `show_title`.")
    title_text_style: ParagraphProperties | None = Field(default=None, description="The text style of the axis title, such as its font, size, and alignment.")
    label_text_style: ParagraphProperties | None = Field(default=None, description="The text style of the axis labels, such as their font, size, and alignment.")
    show_labels: bool = Field(default=True, description="Whether the axis's tick labels are shown.")
    show_title: bool = Field(default=False, description="Whether the axis title is shown.")
    show_major_tickmarks: bool = Field(default=True, description="Whether major tick marks are shown along the axis.")
    show_minor_tickmarks: bool = Field(default=True, description="Whether minor tick marks are shown along the axis.")
    labels_orientation: AxisLabelOrientation | None = Field(default=None, description="The rotation of the axis's labels. The five straight-axis orientations correspond to rotations of 0, 45, 90, 270, and 315 degrees, `custom` carries any other rotation, and `parallel` and `perpendicular` apply to radar charts.")


@wire_union(
    "com.apple.apps.content-language.chart-axis-common",
    version="1.0",
    cases=[
        ("chartCategoryAxis", (1, 0), False),
        ("chartValueAxis", (1, 0), False),
        ("genericChartAxisCommon", (1, 0), False),
    ],
)
class ChartAxisCommon(TaggedUnionModel):
    """The properties every chart axis shares, flattened into both the category axis and the value axis.

They cover the axis's title, its tick labels and their rotation, and its tick marks. What differs by kind of axis is on `ChartCategoryAxis` and `ChartValueAxis` themselves: the axis line and its gridlines, a category axis's label spacing, and a value axis's scale and bounds."""
    chartCategoryAxis: ChartCategoryAxis | None = None
    chartValueAxis: ChartValueAxis | None = None
    genericChartAxisCommon: GenericChartAxisCommon | None = None

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_ChartAxisCommonCase, ...]: ...

        def union_primary(self) -> _ChartAxisCommonCase | None: ...

        def union_primary_name(self) -> Literal["chartCategoryAxis", "chartValueAxis", "genericChartAxisCommon"] | None: ...


@wire_union(
    "com.apple.apps.content-language.chart-axis-common.axis-label-orientation",
    version="1.0",
    cases=[
        ("custom", (1, 0), False),
        ("horizontal", (1, 0), True),
        ("left_diagonal", (1, 0), True),
        ("left_vertical", (1, 0), True),
        ("parallel", (1, 0), True),
        ("perpendicular", (1, 0), True),
        ("right_diagonal", (1, 0), True),
        ("right_vertical", (1, 0), True),
    ],
)
class AxisLabelOrientation(TaggedUnionModel):
    """The orientation of an axis's labels relative to the axis.

Rotating the labels lets long labels stay legible without widening the chart."""
    custom: float | None = Field(default=None, description="Labels rotated by the given number of degrees, measured counterclockwise. The value is written in the range `0` to `360`; a value outside that range is read as the equivalent angle within it. An angle that matches one of the five named straight-axis orientations is written as that case instead.")
    horizontal: Literal[True] | None = Field(default=None, description="Labels drawn horizontally, with no rotation.")
    left_diagonal: Literal[True] | None = Field(default=None, description="Labels rotated diagonally, at 45 degrees.")
    left_vertical: Literal[True] | None = Field(default=None, description="Labels rotated to vertical, at 90 degrees.")
    parallel: Literal[True] | None = Field(default=None, description="Radar charts only: labels drawn along the spoke they label.")
    perpendicular: Literal[True] | None = Field(default=None, description="Radar charts only: labels drawn at right angles to the spoke they label.")
    right_diagonal: Literal[True] | None = Field(default=None, description="Labels rotated diagonally the opposite way from `left_diagonal`, at 315 degrees (equivalently -45 degrees).")
    right_vertical: Literal[True] | None = Field(default=None, description="Labels rotated to vertical the opposite way from `left_vertical`, at 270 degrees (equivalently -90 degrees).")

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_AxisLabelOrientationCase, ...]: ...

        def union_primary(self) -> _AxisLabelOrientationCase | None: ...

        def union_primary_name(self) -> Literal["custom", "horizontal", "left_diagonal", "left_vertical", "parallel", "perpendicular", "right_diagonal", "right_vertical"] | None: ...


@wire(
    "com.apple.apps.content-language.chart-category-axis",
    version="1.0",
    fields=[
        ("title", (1, 0), "opt"),
        ("title_text_style", (1, 0), "opt"),
        ("label_text_style", (1, 0), "opt"),
        ("show_labels", (1, 0), "def"),
        ("show_title", (1, 0), "def"),
        ("show_major_tickmarks", (1, 0), "def"),
        ("show_minor_tickmarks", (1, 0), "def"),
        ("labels_orientation", (1, 0), "opt"),
        ("label_format_type", (1, 0), "opt"),
        ("label_date_format", (1, 0), "opt"),
        ("label_duration_format", (1, 0), "opt"),
        ("label_number_format", (1, 0), "opt"),
        ("label_currency_format", (1, 0), "opt"),
        ("label_spacing", (1, 0), "opt"),
        ("show_axis", (1, 0), "def"),
        ("show_major_gridlines", (1, 0), "def"),
        ("show_clustered_series_labels", (1, 0), "def"),
        ("show_last_label", (1, 0), "def"),
    ],
)
class ChartCategoryAxis(ObjectModel):
    """The axis along which a chart's categories are laid out, on the chart types that have one.

Pie, donut, scatter, and bubble charts have no category axis. A category axis describes only its own appearance; the category names themselves come from the data grid's row or column labels, whichever `ChartData.plot_direction` leaves as the category direction."""
    title: str | None = Field(default=None, description="The text of the axis title. Whether the title is shown is controlled separately by `show_title`.")
    title_text_style: ParagraphProperties | None = Field(default=None, description="The text style of the axis title, such as its font, size, and alignment.")
    label_text_style: ParagraphProperties | None = Field(default=None, description="The text style of the axis labels, such as their font, size, and alignment.")
    show_labels: bool = Field(default=True, description="Whether the axis's tick labels are shown.")
    show_title: bool = Field(default=False, description="Whether the axis title is shown.")
    show_major_tickmarks: bool = Field(default=True, description="Whether major tick marks are shown along the axis.")
    show_minor_tickmarks: bool = Field(default=True, description="Whether minor tick marks are shown along the axis.")
    labels_orientation: AxisLabelOrientation | None = Field(default=None, description="The rotation of the axis's labels. The five straight-axis orientations correspond to rotations of 0, 45, 90, 270, and 315 degrees, `custom` carries any other rotation, and `parallel` and `perpendicular` apply to radar charts.")
    label_format_type: FormatType | None = Field(default=None, strict=False, description="The kind of formatting applied to the label's value. It also selects which of `label_number_format`, `label_currency_format`, `label_date_format`, and `label_duration_format` applies. `text`, `boolean`, and `base` have no equivalent for chart labels and behave like `number`, which is also what omitting this property means.")
    label_date_format: DateTimeFormat | None = Field(default=None, description="The date and time format of the label, used when `label_format_type` is `date_time`. An empty format string is treated as no format at all and isn't preserved.")
    label_duration_format: DurationFormat | None = Field(default=None, description="The label's duration format, used when `label_format_type` is `duration`. It covers automatic units, the smallest and largest unit, and the style.")
    label_number_format: NumberFormat | None = Field(default=None, description="The decimal places, negative-number style, and thousands separator of the label, used for number, percentage, and scientific labels. A value of 253 for decimal places means automatic. It's omitted for fraction, base, and custom labels, which have none of these attributes; a prefix or suffix, a fraction accuracy, and a custom format string aren't preserved. Currency labels use `label_currency_format` instead. On a stacked chart whose value axis has a `ChartValueAxis.scale` of `percent`, the value labels of each series don't use this format, and their decimal places, negative-number style, and thousands separator aren't preserved.")
    label_currency_format: CurrencyFormat | None = Field(default=None, description="The currency code, accounting style, decimal places, negative-number style, and thousands separator of the label, used when `label_format_type` is `currency`. It takes the place of `label_number_format` for currency labels, and it's what preserves the currency code; a prefix or suffix and a custom format string aren't preserved.")
    label_spacing: LabelSpacing | None = Field(default=None, description="The spacing of the category labels. `auto_fit` lets the chart pick the spacing, `show_all` shows a label for every category, and `custom` shows every Nth label. `none` is never written.")
    show_axis: bool = Field(default=True, description="Whether the category axis line itself is shown.")
    show_major_gridlines: bool = Field(default=False, description="Whether a gridline is shown at each category division.")
    show_clustered_series_labels: bool = Field(default=False, description="Whether each series' name is shown on the category axis of a clustered bar or column chart.")
    show_last_label: bool = Field(default=False, description="Whether the last category's label is always shown, even when `label_spacing` would skip it.")


@wire_union(
    "com.apple.apps.content-language.chart-category-axis.label-spacing",
    version="1.0",
    cases=[
        ("auto_fit", (1, 0), True),
        ("custom", (1, 0), False),
        ("none", (1, 0), True),
        ("show_all", (1, 0), True),
    ],
)
class LabelSpacing(TaggedUnionModel):
    """The spacing of the category labels along the axis.

A label can be shown for every category, or for a reduced set chosen to fit the space available."""
    auto_fit: Literal[True] | None = None
    custom: int | None = Field(default=None, description="Every Nth category label is shown, where N is the given value. An N of `0` is written as `auto_fit` instead, and an N of `1` as `show_all`.")
    none: Literal[True] | None = None
    show_all: Literal[True] | None = None

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_LabelSpacingCase, ...]: ...

        def union_primary(self) -> _LabelSpacingCase | None: ...

        def union_primary_name(self) -> Literal["auto_fit", "custom", "none", "show_all"] | None: ...


@wire(
    "com.apple.apps.content-language.chart-common-generic",
    version="1.0",
    fields=[
        ("title", (1, 0), "opt"),
        ("caption", (1, 0), "opt"),
        ("data", (1, 0), "opt"),
        ("show_legend", (1, 0), "def"),
        ("legend", (1, 0), "opt"),
        ("series", (1, 0), "opt"),
        ("chart_colors", (1, 0), "opt"),
    ],
)
class GenericChartCommon(ObjectModel):
    """A stand-in for a chart, when the reader doesn't recognize its kind.

Every set of shared properties has one, to stand in for an object whose kind isn't recognized. Nothing in the format has the type `ChartCommon`, though, so this object never appears in a document; its properties appear only as part of the types that adopt `ChartCommon`."""
    title: Label | None = Field(default=None, description="The object's title.")
    caption: Label | None = Field(default=None, description="The object's caption, which Keynote always places below the object. If a caption is off, you still write it out with `Label.is_visible` set to `false`, so having a value doesn't mean the caption shows.")
    data: ChartData | None = Field(default=None, description="The chart's data grid, together with its plot direction and data-source mode. This data replaces the placeholder data a new chart starts with; when omitted, that placeholder data remains.")
    show_legend: bool = Field(default=True, description="A Boolean value that indicates whether the chart's legend appears. This value is independent of the `legend` property, which sets the legend's placement and text style rather than its visibility.")
    legend: ChartLegend | None = Field(default=None, description="The placement and label text style of the chart's legend. This value doesn't control whether the legend appears (see `show_legend`), and it only applies to a chart that has a legend.")
    series: list[ChartSeries] | None = Field(default=None, description="The styling and label formatting for individual data series. Each entry applies to the series named by its `ChartSeries.series_index`, or to the series at the same position when `ChartSeries.series_index` is omitted; entries that don't correspond to a series in the data don't have an effect.")
    chart_colors: list[ChartColor] | None = Field(default=None, description="The chart's ordered series styles. A series takes the entry at its own position, and the chart's style supplies any position without an entry or with an empty one, so the list doesn't wrap. Entries past the last series also remain. Keynote reads one entry for each series style in the chart's style and ignores any further entries.")


@wire_union(
    "com.apple.apps.content-language.chart-common",
    version="1.0",
    cases=[
        ("area3Dchart", (1, 0), False),
        ("areaChart", (1, 0), False),
        ("bar3Dchart", (1, 0), False),
        ("barChart", (1, 0), False),
        ("barInteractiveChart", (1, 0), False),
        ("bubbleChart", (1, 0), False),
        ("bubbleInteractiveChart", (1, 0), False),
        ("column3Dchart", (1, 0), False),
        ("columnChart", (1, 0), False),
        ("columnInteractiveChart", (1, 0), False),
        ("donutChart", (1, 0), False),
        ("genericChartCommon", (1, 0), False),
        ("line3Dchart", (1, 0), False),
        ("lineChart", (1, 0), False),
        ("mixedChart", (1, 0), False),
        ("pie3Dchart", (1, 0), False),
        ("pieChart", (1, 0), False),
        ("radarChart", (1, 0), False),
        ("scatterChart", (1, 0), False),
        ("scatterInteractiveChart", (1, 0), False),
        ("stackedArea3Dchart", (1, 0), False),
        ("stackedAreaChart", (1, 0), False),
        ("stackedBar3Dchart", (1, 0), False),
        ("stackedBarChart", (1, 0), False),
        ("stackedColumn3Dchart", (1, 0), False),
        ("stackedColumnChart", (1, 0), False),
        ("twoAxisChart", (1, 0), False),
    ],
)
class ChartCommon(TaggedUnionModel):
    """The properties shared by every kind of chart.

These are the data grid, the styling for each series, the ordered series styles in `chart_colors`, the legend, and the title and caption from `TitleOwning` and `CaptionOwning`. Axes come from `CategoryComparisonChart` or `CorrelationChart` instead. When a chart is read, it takes its style from the theme's first chart style, and that style supplies any styling the chart doesn't set. A chart uses the title as its own built-in title and adopts `TitleOwning` alone rather than `PlaceableTitleOwning`, because it lays out that title itself, and the format offers no placement control over it."""
    area3Dchart: Area3DChart | None = None
    areaChart: AreaChart | None = None
    bar3Dchart: Bar3DChart | None = None
    barChart: BarChart | None = None
    barInteractiveChart: BarInteractiveChart | None = None
    bubbleChart: BubbleChart | None = None
    bubbleInteractiveChart: BubbleInteractiveChart | None = None
    column3Dchart: Column3DChart | None = None
    columnChart: ColumnChart | None = None
    columnInteractiveChart: ColumnInteractiveChart | None = None
    donutChart: DonutChart | None = None
    genericChartCommon: GenericChartCommon | None = None
    line3Dchart: Line3DChart | None = None
    lineChart: LineChart | None = None
    mixedChart: MixedChart | None = None
    pie3Dchart: Pie3DChart | None = None
    pieChart: PieChart | None = None
    radarChart: RadarChart | None = None
    scatterChart: ScatterChart | None = None
    scatterInteractiveChart: ScatterInteractiveChart | None = None
    stackedArea3Dchart: StackedArea3DChart | None = None
    stackedAreaChart: StackedAreaChart | None = None
    stackedBar3Dchart: StackedBar3DChart | None = None
    stackedBarChart: StackedBarChart | None = None
    stackedColumn3Dchart: StackedColumn3DChart | None = None
    stackedColumnChart: StackedColumnChart | None = None
    twoAxisChart: TwoAxisChart | None = None

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_ChartCommonCase, ...]: ...

        def union_primary(self) -> _ChartCommonCase | None: ...

        def union_primary_name(self) -> Literal["area3Dchart", "areaChart", "bar3Dchart", "barChart", "barInteractiveChart", "bubbleChart", "bubbleInteractiveChart", "column3Dchart", "columnChart", "columnInteractiveChart", "donutChart", "genericChartCommon", "line3Dchart", "lineChart", "mixedChart", "pie3Dchart", "pieChart", "radarChart", "scatterChart", "scatterInteractiveChart", "stackedArea3Dchart", "stackedAreaChart", "stackedBar3Dchart", "stackedBarChart", "stackedColumn3Dchart", "stackedColumnChart", "twoAxisChart"] | None: ...


@wire(
    "com.apple.apps.content-language.chart-common.chart-color",
    version="1.0",
    fields=[
        ("fill", (1, 0), "opt"),
    ],
)
class ChartColor(ObjectModel):
    """One entry in a chart's series styles.

An entry carries only a fill; a series' stroke isn't part of the list."""
    fill: Fill | None = None


@wire(
    "com.apple.apps.content-language.chart-data",
    version="1.0",
    fields=[
        ("plot_direction", (1, 0), "opt"),
        ("shared_xvalues", (1, 0), "def"),
        ("chart_data_source", (1, 0), "req"),
        ("column_labels", (1, 0), "opt"),
        ("row_labels", (1, 0), "opt"),
        ("rows", (1, 0), "opt"),
    ],
)
class ChartData(ObjectModel):
    """The chart's data as a grid of cells, together with how that grid maps onto the chart.

`plot_direction` decides whether the grid's rows or its columns become the series; the labels along the other direction name the categories."""
    plot_direction: PlotDirection | None = Field(default=None, strict=False, description="Whether the rows or the columns of the data grid become the chart's series. When omitted, the direction preferred by the chart type is kept.")
    shared_xvalues: bool = Field(default=True, description="Whether the grid's first row or column holds the X values every series shares. It's `true` by default; when `false`, each series carries its own X values. Y values, and a bubble series' size values, follow in either case. Only scatter and bubble charts use it; other chart types ignore it.")
    chart_data_source: ChartDataSource = Field(strict=False, description="The source of the chart's data. Only `chart_data_grid` is supported: that is the value always written, and any other value is ignored, so the grid in `rows` is used either way.")
    column_labels: list[str] | None = Field(default=None, description="The names of the grid's columns. The number of columns comes from the longest row of `rows`, so extra names are dropped and missing names become empty.")
    row_labels: list[str] | None = Field(default=None, description="The names of the grid's rows. The number of rows comes from `rows`, so extra names are dropped and missing names become empty.")
    rows: list[ChartDataRow] | None = Field(default=None, description="The grid's data rows. The grid is made rectangular: it takes the length of the longest row, and shorter rows are padded with empty cells. When `rows` is empty or omitted, the chart keeps the placeholder data it was created with.")


@wire(
    "com.apple.apps.content-language.chart-data.chart-data-row",
    version="1.0",
    fields=[
        ("values", (1, 0), "req"),
    ],
)
class ChartDataRow(ObjectModel):
    """One row of the chart's data grid, holding its cells in column order.

A row isn't necessarily a series: `plot_direction` decides whether rows or columns become the chart's series. Rows need not be the same length, because the grid is padded out to its longest row."""
    values: list[ChartDataValue] = Field(description="The row's cells, in column order. Rows need not be the same length: a short row is padded with empty cells to the length of the longest row.")


class ChartDataSource(str, Enum):
    """The stated source of a chart's values.

It's recorded for provenance only: the grid in `rows` is what is read, whatever this value is.

    chart_data_grid — The chart's data is the grid carried in `rows`. This is the only supported source, and the only value ever written.
    table_formula_references — Reserved for data drawn from table formula references and expressions. Not supported, and never written.
    uninitialized — A value for a chart whose data source hasn't been set. It's never written and, like every other value of this property, has no effect: the grid in `rows` is used either way.
    """
    CHART_DATA_GRID = "chart_data_grid"
    TABLE_FORMULA_REFERENCES = "table_formula_references"
    UNINITIALIZED = "uninitialized"


class PlotDirection(str, Enum):
    """The direction in which the data grid is read to produce the chart's series.

    columns_as_series — Each column of the grid is a series, so `column_labels` name the series and `row_labels` name the categories.
    rows_as_series — Each row of the grid is a series, so `row_labels` name the series and `column_labels` name the categories.
    """
    COLUMNS_AS_SERIES = "columns_as_series"
    ROWS_AS_SERIES = "rows_as_series"


@wire_union(
    "com.apple.apps.content-language.chart-data.chart-data-value",
    version="1.0",
    cases=[
        ("date", (1, 0), False),
        ("duration", (1, 0), False),
        ("empty", (1, 0), True),
        ("number", (1, 0), False),
    ],
)
class ChartDataValue(TaggedUnionModel):
    """A single value in the chart's data grid.

A value is a number, a date, or a duration; a cell holding anything else, text included, is read as empty."""
    date: Date | None = Field(default=None, description="A cell holding a date.")
    duration: Duration | None = Field(default=None, description="A cell holding a length of time.")
    empty: Literal[True] | None = Field(default=None, description="An empty cell. Any cell that doesn't hold a number, a date, or a duration is written as `empty`.")
    number: float | None = Field(default=None, description="A cell holding a number.")

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_ChartDataValueCase, ...]: ...

        def union_primary(self) -> _ChartDataValueCase | None: ...

        def union_primary_name(self) -> Literal["date", "duration", "empty", "number"] | None: ...


@wire(
    "com.apple.apps.content-language.chart-label-formatting-generic",
    version="1.0",
    fields=[
        ("label_format_type", (1, 0), "opt"),
        ("label_date_format", (1, 0), "opt"),
        ("label_duration_format", (1, 0), "opt"),
        ("label_number_format", (1, 0), "opt"),
        ("label_currency_format", (1, 0), "opt"),
    ],
)
class GenericChartLabelFormatting(ObjectModel):
    """A stand-in for a chart's numeric label formatting, when the reader doesn't recognize its kind.

Every set of shared properties has one, to stand in for an object whose kind isn't recognized. Nothing in the format has the type `ChartLabelFormatting`, though, so this object never appears in a document; its properties appear only as part of the types that adopt `ChartLabelFormatting`."""
    label_format_type: FormatType | None = Field(default=None, strict=False, description="The kind of formatting applied to the label's value. It also selects which of `label_number_format`, `label_currency_format`, `label_date_format`, and `label_duration_format` applies. `text`, `boolean`, and `base` have no equivalent for chart labels and behave like `number`, which is also what omitting this property means.")
    label_date_format: DateTimeFormat | None = Field(default=None, description="The date and time format of the label, used when `label_format_type` is `date_time`. An empty format string is treated as no format at all and isn't preserved.")
    label_duration_format: DurationFormat | None = Field(default=None, description="The label's duration format, used when `label_format_type` is `duration`. It covers automatic units, the smallest and largest unit, and the style.")
    label_number_format: NumberFormat | None = Field(default=None, description="The decimal places, negative-number style, and thousands separator of the label, used for number, percentage, and scientific labels. A value of 253 for decimal places means automatic. It's omitted for fraction, base, and custom labels, which have none of these attributes; a prefix or suffix, a fraction accuracy, and a custom format string aren't preserved. Currency labels use `label_currency_format` instead. On a stacked chart whose value axis has a `ChartValueAxis.scale` of `percent`, the value labels of each series don't use this format, and their decimal places, negative-number style, and thousands separator aren't preserved.")
    label_currency_format: CurrencyFormat | None = Field(default=None, description="The currency code, accounting style, decimal places, negative-number style, and thousands separator of the label, used when `label_format_type` is `currency`. It takes the place of `label_number_format` for currency labels, and it's what preserves the currency code; a prefix or suffix and a custom format string aren't preserved.")


@wire_union(
    "com.apple.apps.content-language.chart-label-formatting",
    version="1.0",
    cases=[
        ("chartCategoryAxis", (1, 0), False),
        ("chartSeries", (1, 0), False),
        ("chartValueAxis", (1, 0), False),
        ("genericChartLabelFormatting", (1, 0), False),
    ],
)
class ChartLabelFormatting(TaggedUnionModel):
    """The formatting of a chart element's numeric labels.

It's flattened into `ChartValueAxis`, `ChartCategoryAxis`, and `ChartSeries`. `label_format_type` selects which of the format properties applies. A prefix or suffix, a fraction accuracy, and a custom format string aren't preserved."""
    chartCategoryAxis: ChartCategoryAxis | None = None
    chartSeries: ChartSeries | None = None
    chartValueAxis: ChartValueAxis | None = None
    genericChartLabelFormatting: GenericChartLabelFormatting | None = None

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_ChartLabelFormattingCase, ...]: ...

        def union_primary(self) -> _ChartLabelFormattingCase | None: ...

        def union_primary_name(self) -> Literal["chartCategoryAxis", "chartSeries", "chartValueAxis", "genericChartLabelFormatting"] | None: ...


@wire(
    "com.apple.apps.content-language.chart-legend",
    version="1.0",
    fields=[
        ("geometry", (1, 0), "opt"),
        ("label_text_style", (1, 0), "opt"),
    ],
)
class ChartLegend(ObjectModel):
    """The legend of a chart.

Its position is an offset from the center of the plot area rather than a position on the slide. Whether it's shown is set by `ChartCommon.show_legend`, and its entry labels come from the chart's series."""
    geometry: Geometry | None = Field(default=None, description="The legend's position and size. `Geometry.position` is the offset from the center of the chart's plot area to the legend's top-left corner, so either coordinate can be negative, and `Geometry.size` is its width and height. `Geometry.angle`, `Geometry.flip_horizontally`, `Geometry.width_valid`, and `Geometry.height_valid` don't apply to a legend and aren't preserved.")
    label_text_style: ParagraphProperties | None = Field(default=None, description="The text style of the legend labels, such as their font, size, and alignment.")


@wire(
    "com.apple.apps.content-language.chart-series",
    version="1.0",
    fields=[
        ("label_format_type", (1, 0), "opt"),
        ("label_date_format", (1, 0), "opt"),
        ("label_duration_format", (1, 0), "opt"),
        ("label_number_format", (1, 0), "opt"),
        ("label_currency_format", (1, 0), "opt"),
        ("series_index", (1, 0), "opt"),
        ("show_value_labels", (1, 0), "def"),
        ("value_label_position", (1, 0), "opt"),
        ("value_label_text_style", (1, 0), "opt"),
        ("value_label_outside_text_style", (1, 0), "opt"),
        ("fill", (1, 0), "ovr"),
        ("stroke", (1, 0), "opt"),
        ("symbol_type", (1, 0), "opt"),
        ("symbol_stroke", (1, 0), "opt"),
        ("symbol_fill", (1, 0), "ovr"),
        ("symbol_size", (1, 0), "opt"),
        ("fill_reuse_rules", (1, 0), "opt"),
        ("fill_use_series_stroke_alpha_multiplier", (1, 0), "opt"),
        ("connection_line_type", (1, 0), "opt"),
        ("value_labels_selection", (1, 0), "opt"),
        ("show_negative_data", (1, 0), "def"),
        ("mixed_series_type", (1, 0), "opt"),
        ("y_axis_selection", (1, 0), "opt"),
    ],
)
class ChartSeries(ObjectModel):
    """The appearance and label formatting of one of a chart's data series.

It covers the series' fill, stroke, data symbols, connecting line, and value labels; the plotted values come from the chart's data grid. Many properties apply only to certain chart types and are ignored on the rest."""
    label_format_type: FormatType | None = Field(default=None, strict=False, description="The kind of formatting applied to the label's value. It also selects which of `label_number_format`, `label_currency_format`, `label_date_format`, and `label_duration_format` applies. `text`, `boolean`, and `base` have no equivalent for chart labels and behave like `number`, which is also what omitting this property means.")
    label_date_format: DateTimeFormat | None = Field(default=None, description="The date and time format of the label, used when `label_format_type` is `date_time`. An empty format string is treated as no format at all and isn't preserved.")
    label_duration_format: DurationFormat | None = Field(default=None, description="The label's duration format, used when `label_format_type` is `duration`. It covers automatic units, the smallest and largest unit, and the style.")
    label_number_format: NumberFormat | None = Field(default=None, description="The decimal places, negative-number style, and thousands separator of the label, used for number, percentage, and scientific labels. A value of 253 for decimal places means automatic. It's omitted for fraction, base, and custom labels, which have none of these attributes; a prefix or suffix, a fraction accuracy, and a custom format string aren't preserved. Currency labels use `label_currency_format` instead. On a stacked chart whose value axis has a `ChartValueAxis.scale` of `percent`, the value labels of each series don't use this format, and their decimal places, negative-number style, and thousands separator aren't preserved.")
    label_currency_format: CurrencyFormat | None = Field(default=None, description="The currency code, accounting style, decimal places, negative-number style, and thousands separator of the label, used when `label_format_type` is `currency`. It takes the place of `label_number_format` for currency labels, and it's what preserves the currency code; a prefix or suffix and a custom format string aren't preserved.")
    series_index: int | None = Field(default=None, description="The zero-based index of the data series this entry applies to. If it's omitted, the entry's own position in the series array is used; an entry whose index is negative or past the last series in the data is ignored rather than treated as an error.")
    show_value_labels: bool = Field(default=False, description="Whether each data point in this series is labeled with its value.")
    value_label_position: SeriesValueLabelPosition | None = Field(default=None, strict=False, description="The position of a data point's value label relative to the point. Not every chart type offers every position, and a position that isn't one of the values listed here isn't preserved.")
    value_label_text_style: ParagraphProperties | None = Field(default=None, description="The text style of value labels drawn inside the series element.")
    value_label_outside_text_style: ParagraphProperties | None = Field(default=None, description="The text style of value labels drawn outside the series element.")
    fill: Override[Fill] = Field(default_factory=Override.not_set, description="The fill of the series' bars, columns, wedges, or area. `null` clears the fill; omitting the key inherits it from the chart's style. It's ignored when `fill_reuse_rules` derives the fill from another color instead.")
    stroke: Stroke | None = Field(default=None, description="The stroke of the series' line, or of the border of its bars, columns, or wedges. Bubble series have no such stroke (see `symbol_stroke` instead): a stroke supplied for one is ignored and isn't preserved.")
    symbol_type: SeriesSymbolType | None = Field(default=None, strict=False, description="The shape of the data symbol drawn at each data point, or `none` for no data symbol. Data symbols exist only on 2D line, area, scatter, radar, and mixed line or area series, not on bubble or 3D series. Setting any shape other than `none` also turns data symbols on.")
    symbol_stroke: Stroke | None = Field(default=None, description="The stroke of the data symbols drawn at each data point. It applies only to series that draw data symbols, which for this purpose include bubbles.")
    symbol_fill: Override[Fill] = Field(default_factory=Override.not_set, description="The fill of the data symbols drawn at each data point. `null` clears the fill; omitting the key inherits it from the chart's style. It applies only to series that draw data symbols, which for this purpose include bubbles.")
    symbol_size: float | None = Field(default=None, description="The size of the data symbols drawn at each data point, in points. Bubble series have no data symbol size, because a bubble is sized from its data value; a size of `0` is treated as unset and isn't preserved.")
    fill_reuse_rules: list[Annotated[FillReuseRule, Strict(False)]] | None = Field(default=None, description="The rules that derive the data symbol or series fill from another of the series' colors instead of an explicit fill.")
    fill_use_series_stroke_alpha_multiplier: float | None = Field(default=None, description="The alpha applied to the series stroke color to derive the series fill when `fill_reuse_rules` contains `series_fill_use_series_stroke`. It's ignored otherwise.")
    connection_line_type: ConnectionLineType | None = Field(default=None, strict=False, description="The style of the line joining this series' data points: `none`, `straight`, or `curved`. It applies only to series that draw a joining line, such as line, scatter, bubble, and radar series.")
    value_labels_selection: ValueLabelsSelection | None = Field(default=None, strict=False, description="The values of a data point that appear in its value label on a bubble or scatter chart. It's ignored by other chart types; combinations other than the ones listed here aren't preserved.")
    show_negative_data: bool = Field(default=False, description="Whether a bubble chart shows a bubble for a negative value, sized from the value's magnitude. When it's `false`, negative values aren't plotted. It's ignored by other chart types.")
    mixed_series_type: MixedSeriesType | None = Field(default=None, strict=False, description="The shape of this series on a mixed or two-axis chart: columns, a line, or an area. It's ignored by other chart types.")
    y_axis_selection: int | None = Field(default=None, description="The value axis this series is plotted against on a two-axis chart: `0` for the primary axis and `1` for the secondary axis. It's ignored by other chart types. It's always written for a two-axis chart, including 0, because omitting the key leaves the series on its default axis, which is the secondary axis for every series after the first.")


class ValueLabelsSelection(str, Enum):
    """The values of a data point that appear in its value label.

It applies only to bubble and scatter charts."""
    NONE = "none"
    SIZE = "size"
    X = "x"
    X_AND_Y = "x_and_y"
    Y = "y"


class MixedSeriesType(str, Enum):
    """The shape a single series takes on a mixed or two-axis chart.

Each series on these charts can take a different shape, and these are the only chart types that read this value. The choice also determines which of the series' other style properties apply, since a series drawn as columns has neither data symbols nor a connecting line."""
    AREA = "area"
    COLUMN = "column"
    LINE = "line"


class SeriesSymbolType(str, Enum):
    """The shape of the data symbol drawn at each of a series' data points.

It also sets whether data symbols are drawn at all: `none` turns them off, and any other case turns them on. Only a series that draws an editable data symbol uses it; a bubble series doesn't, because its circles are sized from the data.

    yield — A triangle pointing the opposite way from `triangle`, apex toward the bottom.
    """
    CIRCLE = "circle"
    DIAMOND = "diamond"
    NONE = "none"
    PLUS = "plus"
    SQUARE = "square"
    TRIANGLE = "triangle"
    X = "x"
    YIELD = "yield"


class ConnectionLineType(str, Enum):
    """The style of the line drawn through a series' data points.

It also sets whether a line is drawn at all: `none` removes the line rather than falling back to a default. Only a series that joins its points with a line uses it; elsewhere the value is ignored and isn't written back out."""
    CURVED = "curved"
    NONE = "none"
    STRAIGHT = "straight"


class FillReuseRule(str, Enum):
    """A rule that reuses one of a series' own colors in place of an explicit fill.

It lets data symbols track the series' fill or stroke instead of carrying a color of their own."""
    SERIES_FILL_USE_SERIES_STROKE = "series_fill_use_series_stroke"
    SYMBOL_FILL_USES_SERIES_FILL = "symbol_fill_uses_series_fill"
    SYMBOL_FILL_USES_SERIES_STROKE = "symbol_fill_uses_series_stroke"


class SeriesValueLabelPosition(str, Enum):
    """The position of a data point's value label, for a series that shows value labels.

Each chart type uses only the placements that suit it and replaces any other with one it supports. A pie wedge or donut segment, for instance, keeps `inside` and `outside`, and anything else (`auto` included) comes out as the automatic centered placement."""
    AUTO = "auto"
    BOTTOM = "bottom"
    BOTTOM_LEFT = "bottom_left"
    BOTTOM_RIGHT = "bottom_right"
    CENTER = "center"
    INSIDE = "inside"
    INSIDE_BOTTOM = "inside_bottom"
    INSIDE_LEFT = "inside_left"
    INSIDE_RIGHT = "inside_right"
    INSIDE_TOP = "inside_top"
    LEFT = "left"
    OUTSIDE = "outside"
    OUTSIDE_TOP = "outside_top"
    RIGHT = "right"
    TOP = "top"
    TOP_LEFT = "top_left"
    TOP_RIGHT = "top_right"


@wire(
    "com.apple.apps.content-language.chart-value-axis",
    version="1.0",
    fields=[
        ("title", (1, 0), "opt"),
        ("title_text_style", (1, 0), "opt"),
        ("label_text_style", (1, 0), "opt"),
        ("show_labels", (1, 0), "def"),
        ("show_title", (1, 0), "def"),
        ("show_major_tickmarks", (1, 0), "def"),
        ("show_minor_tickmarks", (1, 0), "def"),
        ("labels_orientation", (1, 0), "opt"),
        ("label_format_type", (1, 0), "opt"),
        ("label_date_format", (1, 0), "opt"),
        ("label_duration_format", (1, 0), "opt"),
        ("label_number_format", (1, 0), "opt"),
        ("label_currency_format", (1, 0), "opt"),
        ("scale", (1, 0), "opt"),
        ("max", (1, 0), "opt"),
        ("min", (1, 0), "opt"),
        ("show_axis", (1, 0), "def"),
        ("show_major_gridlines", (1, 0), "def"),
        ("show_minimum_label", (1, 0), "def"),
        ("number_of_major_gridlines", (1, 0), "opt"),
        ("number_of_decades", (1, 0), "opt"),
        ("number_of_minor_gridlines", (1, 0), "opt"),
        ("show_minor_gridlines", (1, 0), "def"),
    ],
)
class ChartValueAxis(ObjectModel):
    """A numeric axis that a chart's values are measured against.

The same type serves every value axis a chart has, so a property takes effect only where that axis supports it."""
    title: str | None = Field(default=None, description="The text of the axis title. Whether the title is shown is controlled separately by `show_title`.")
    title_text_style: ParagraphProperties | None = Field(default=None, description="The text style of the axis title, such as its font, size, and alignment.")
    label_text_style: ParagraphProperties | None = Field(default=None, description="The text style of the axis labels, such as their font, size, and alignment.")
    show_labels: bool = Field(default=True, description="Whether the axis's tick labels are shown.")
    show_title: bool = Field(default=False, description="Whether the axis title is shown.")
    show_major_tickmarks: bool = Field(default=True, description="Whether major tick marks are shown along the axis.")
    show_minor_tickmarks: bool = Field(default=True, description="Whether minor tick marks are shown along the axis.")
    labels_orientation: AxisLabelOrientation | None = Field(default=None, description="The rotation of the axis's labels. The five straight-axis orientations correspond to rotations of 0, 45, 90, 270, and 315 degrees, `custom` carries any other rotation, and `parallel` and `perpendicular` apply to radar charts.")
    label_format_type: FormatType | None = Field(default=None, strict=False, description="The kind of formatting applied to the label's value. It also selects which of `label_number_format`, `label_currency_format`, `label_date_format`, and `label_duration_format` applies. `text`, `boolean`, and `base` have no equivalent for chart labels and behave like `number`, which is also what omitting this property means.")
    label_date_format: DateTimeFormat | None = Field(default=None, description="The date and time format of the label, used when `label_format_type` is `date_time`. An empty format string is treated as no format at all and isn't preserved.")
    label_duration_format: DurationFormat | None = Field(default=None, description="The label's duration format, used when `label_format_type` is `duration`. It covers automatic units, the smallest and largest unit, and the style.")
    label_number_format: NumberFormat | None = Field(default=None, description="The decimal places, negative-number style, and thousands separator of the label, used for number, percentage, and scientific labels. A value of 253 for decimal places means automatic. It's omitted for fraction, base, and custom labels, which have none of these attributes; a prefix or suffix, a fraction accuracy, and a custom format string aren't preserved. Currency labels use `label_currency_format` instead. On a stacked chart whose value axis has a `ChartValueAxis.scale` of `percent`, the value labels of each series don't use this format, and their decimal places, negative-number style, and thousands separator aren't preserved.")
    label_currency_format: CurrencyFormat | None = Field(default=None, description="The currency code, accounting style, decimal places, negative-number style, and thousands separator of the label, used when `label_format_type` is `currency`. It takes the place of `label_number_format` for currency labels, and it's what preserves the currency code; a prefix or suffix and a custom format string aren't preserved.")
    scale: AxisScale | None = Field(default=None, strict=False, description="The scale of the axis: `linear`, `log` for a logarithmic axis, or `percent`. If it's omitted, the scale is `linear`.")
    max: ChartDataValue | None = Field(default=None, description="The upper bound of the axis, which must be above `min`. A date or duration bound takes effect but isn't written back out, so only a numeric bound is kept when Keynote exports the presentation. If it's omitted, the axis scales itself to the data.")
    min: ChartDataValue | None = Field(default=None, description="The lower bound of the axis, which must be below `max`. A date or duration bound takes effect but isn't written back out, so only a numeric bound is kept when Keynote exports the presentation. If it's omitted, the axis scales itself to the data.")
    show_axis: bool = Field(default=False, description="Whether the value axis line itself is shown.")
    show_major_gridlines: bool = Field(default=True, description="Whether a gridline is shown at each major step of the axis.")
    show_minimum_label: bool = Field(default=True, description="Whether the label for the axis's lowest value is shown.")
    number_of_major_gridlines: int | None = Field(default=None, description="The number of major steps the axis is divided into, each marked by a major gridline. Omit it, or set it to 0, to let the chart choose the number of steps automatically.")
    number_of_decades: int | None = Field(default=None, description="The number of powers of ten the axis is divided into, for logarithmic axes only. Omit it, or set it to 0, to let the chart choose the number automatically.")
    number_of_minor_gridlines: int | None = Field(default=None, description="The number of minor steps between each pair of major gridlines. Omit it, or set it to 0, to keep the chart's own minor spacing.")
    show_minor_gridlines: bool = Field(default=False, description="Whether minor gridlines are shown.")


class AxisScale(str, Enum):
    """How values are spaced along the axis: evenly, or by order of magnitude so that a wide range stays readable.

    percent — Values are shown as a percentage of the total, as used by charts that stack their series to 100%.
    """
    LINEAR = "linear"
    LOG = "log"
    PERCENT = "percent"


@wire(
    "com.apple.apps.content-language.column3-dchart",
    version="1.0",
    fields=[
        ("title", (1, 0), "opt"),
        ("caption", (1, 0), "opt"),
        ("data", (1, 0), "opt"),
        ("show_legend", (1, 0), "def"),
        ("legend", (1, 0), "opt"),
        ("series", (1, 0), "opt"),
        ("chart_colors", (1, 0), "opt"),
        ("category_axis", (1, 0), "opt"),
        ("value_axis", (1, 0), "opt"),
        ("value_axis_secondary", (1, 0), "opt"),
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
    ],
)
class Column3DChart(ObjectModel):
    """A 3D vertical column chart.

3D appearance settings such as rotation, depth, lighting, and textures aren't included: rotation and depth take the default for this chart type, and lighting and a textured series' fill come from the chart's style."""
    title: Label | None = Field(default=None, description="The object's title.")
    caption: Label | None = Field(default=None, description="The object's caption, which Keynote always places below the object. If a caption is off, you still write it out with `Label.is_visible` set to `false`, so having a value doesn't mean the caption shows.")
    data: ChartData | None = Field(default=None, description="The chart's data grid, together with its plot direction and data-source mode. This data replaces the placeholder data a new chart starts with; when omitted, that placeholder data remains.")
    show_legend: bool = Field(default=True, description="A Boolean value that indicates whether the chart's legend appears. This value is independent of the `legend` property, which sets the legend's placement and text style rather than its visibility.")
    legend: ChartLegend | None = Field(default=None, description="The placement and label text style of the chart's legend. This value doesn't control whether the legend appears (see `show_legend`), and it only applies to a chart that has a legend.")
    series: list[ChartSeries] | None = Field(default=None, description="The styling and label formatting for individual data series. Each entry applies to the series named by its `ChartSeries.series_index`, or to the series at the same position when `ChartSeries.series_index` is omitted; entries that don't correspond to a series in the data don't have an effect.")
    chart_colors: list[ChartColor] | None = Field(default=None, description="The chart's ordered series styles. A series takes the entry at its own position, and the chart's style supplies any position without an entry or with an empty one, so the list doesn't wrap. Entries past the last series also remain. Keynote reads one entry for each series style in the chart's style and ignores any further entries.")
    category_axis: ChartCategoryAxis | None = Field(default=None, description="The category axis, along which Keynote lays out the chart's categories. When omitted, the category axis keeps the appearance it inherits from the chart's style.")
    value_axis: ChartValueAxis | None = Field(default=None, description="The primary value axis, which carries the numeric scale to measure the series against. When omitted, the value axis keeps the appearance it inherits from the chart's style.")
    value_axis_secondary: ChartValueAxis | None = Field(default=None, description="The second value axis, used only by a two-axis chart that actually plots a series against a second value scale. On any other chart type, this value doesn't have an effect.")
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=False, description="A Boolean value that indicates whether the object's width-to-height ratio is locked when the object resizes. The lock doesn't constrain the `geometry` property. If this property is absent, images, movies, and groups default to `true`, and other objects to `false`.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")


@wire(
    "com.apple.apps.content-language.column-chart",
    version="1.0",
    fields=[
        ("title", (1, 0), "opt"),
        ("caption", (1, 0), "opt"),
        ("data", (1, 0), "opt"),
        ("show_legend", (1, 0), "def"),
        ("legend", (1, 0), "opt"),
        ("series", (1, 0), "opt"),
        ("chart_colors", (1, 0), "opt"),
        ("category_axis", (1, 0), "opt"),
        ("value_axis", (1, 0), "opt"),
        ("value_axis_secondary", (1, 0), "opt"),
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
    ],
)
class ColumnChart(ObjectModel):
    """A 2D column chart.

Keynote draws each series as vertical columns against a shared category axis and value axis. A chart whose type this version of the format doesn't recognize is also written out as a column chart."""
    title: Label | None = Field(default=None, description="The object's title.")
    caption: Label | None = Field(default=None, description="The object's caption, which Keynote always places below the object. If a caption is off, you still write it out with `Label.is_visible` set to `false`, so having a value doesn't mean the caption shows.")
    data: ChartData | None = Field(default=None, description="The chart's data grid, together with its plot direction and data-source mode. This data replaces the placeholder data a new chart starts with; when omitted, that placeholder data remains.")
    show_legend: bool = Field(default=True, description="A Boolean value that indicates whether the chart's legend appears. This value is independent of the `legend` property, which sets the legend's placement and text style rather than its visibility.")
    legend: ChartLegend | None = Field(default=None, description="The placement and label text style of the chart's legend. This value doesn't control whether the legend appears (see `show_legend`), and it only applies to a chart that has a legend.")
    series: list[ChartSeries] | None = Field(default=None, description="The styling and label formatting for individual data series. Each entry applies to the series named by its `ChartSeries.series_index`, or to the series at the same position when `ChartSeries.series_index` is omitted; entries that don't correspond to a series in the data don't have an effect.")
    chart_colors: list[ChartColor] | None = Field(default=None, description="The chart's ordered series styles. A series takes the entry at its own position, and the chart's style supplies any position without an entry or with an empty one, so the list doesn't wrap. Entries past the last series also remain. Keynote reads one entry for each series style in the chart's style and ignores any further entries.")
    category_axis: ChartCategoryAxis | None = Field(default=None, description="The category axis, along which Keynote lays out the chart's categories. When omitted, the category axis keeps the appearance it inherits from the chart's style.")
    value_axis: ChartValueAxis | None = Field(default=None, description="The primary value axis, which carries the numeric scale to measure the series against. When omitted, the value axis keeps the appearance it inherits from the chart's style.")
    value_axis_secondary: ChartValueAxis | None = Field(default=None, description="The second value axis, used only by a two-axis chart that actually plots a series against a second value scale. On any other chart type, this value doesn't have an effect.")
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=False, description="A Boolean value that indicates whether the object's width-to-height ratio is locked when the object resizes. The lock doesn't constrain the `geometry` property. If this property is absent, images, movies, and groups default to `true`, and other objects to `false`.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")


@wire(
    "com.apple.apps.content-language.column-interactive-chart",
    version="1.0",
    fields=[
        ("title", (1, 0), "opt"),
        ("caption", (1, 0), "opt"),
        ("data", (1, 0), "opt"),
        ("show_legend", (1, 0), "def"),
        ("legend", (1, 0), "opt"),
        ("series", (1, 0), "opt"),
        ("chart_colors", (1, 0), "opt"),
        ("category_axis", (1, 0), "opt"),
        ("value_axis", (1, 0), "opt"),
        ("value_axis_secondary", (1, 0), "opt"),
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
    ],
)
class ColumnInteractiveChart(ObjectModel):
    """An interactive vertical column chart, which shows one data set at a time.

You can step between the data sets. The interactive control, the position of the data set name, and which data set is shown aren't included, so they take the default for this chart type."""
    title: Label | None = Field(default=None, description="The object's title.")
    caption: Label | None = Field(default=None, description="The object's caption, which Keynote always places below the object. If a caption is off, you still write it out with `Label.is_visible` set to `false`, so having a value doesn't mean the caption shows.")
    data: ChartData | None = Field(default=None, description="The chart's data grid, together with its plot direction and data-source mode. This data replaces the placeholder data a new chart starts with; when omitted, that placeholder data remains.")
    show_legend: bool = Field(default=True, description="A Boolean value that indicates whether the chart's legend appears. This value is independent of the `legend` property, which sets the legend's placement and text style rather than its visibility.")
    legend: ChartLegend | None = Field(default=None, description="The placement and label text style of the chart's legend. This value doesn't control whether the legend appears (see `show_legend`), and it only applies to a chart that has a legend.")
    series: list[ChartSeries] | None = Field(default=None, description="The styling and label formatting for individual data series. Each entry applies to the series named by its `ChartSeries.series_index`, or to the series at the same position when `ChartSeries.series_index` is omitted; entries that don't correspond to a series in the data don't have an effect.")
    chart_colors: list[ChartColor] | None = Field(default=None, description="The chart's ordered series styles. A series takes the entry at its own position, and the chart's style supplies any position without an entry or with an empty one, so the list doesn't wrap. Entries past the last series also remain. Keynote reads one entry for each series style in the chart's style and ignores any further entries.")
    category_axis: ChartCategoryAxis | None = Field(default=None, description="The category axis, along which Keynote lays out the chart's categories. When omitted, the category axis keeps the appearance it inherits from the chart's style.")
    value_axis: ChartValueAxis | None = Field(default=None, description="The primary value axis, which carries the numeric scale to measure the series against. When omitted, the value axis keeps the appearance it inherits from the chart's style.")
    value_axis_secondary: ChartValueAxis | None = Field(default=None, description="The second value axis, used only by a two-axis chart that actually plots a series against a second value scale. On any other chart type, this value doesn't have an effect.")
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=False, description="A Boolean value that indicates whether the object's width-to-height ratio is locked when the object resizes. The lock doesn't constrain the `geometry` property. If this property is absent, images, movies, and groups default to `true`, and other objects to `false`.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")


@wire(
    "com.apple.apps.content-language.correlation-chart-generic",
    version="1.0",
    fields=[
        ("value_axis_x", (1, 0), "opt"),
        ("value_axis_y", (1, 0), "opt"),
    ],
)
class GenericCorrelationChart(ObjectModel):
    """A stand-in for a chart that plots one value scale against another, when the reader doesn't recognize its kind.

Every set of shared properties has one, to stand in for an object whose kind isn't recognized. Nothing in the format has the type `CorrelationChart`, though, so this object never appears in a document; its properties appear only as part of the types that adopt `CorrelationChart`."""
    value_axis_x: ChartValueAxis | None = Field(default=None, description="The horizontal (X) value axis. When omitted, the X axis keeps the appearance it inherits from the chart's style.")
    value_axis_y: ChartValueAxis | None = Field(default=None, description="The vertical (Y) value axis. When omitted, the Y axis keeps the appearance it inherits from the chart's style.")


@wire_union(
    "com.apple.apps.content-language.correlation-chart",
    version="1.0",
    cases=[
        ("bubbleChart", (1, 0), False),
        ("bubbleInteractiveChart", (1, 0), False),
        ("genericCorrelationChart", (1, 0), False),
        ("scatterChart", (1, 0), False),
        ("scatterInteractiveChart", (1, 0), False),
    ],
)
class CorrelationChart(TaggedUnionModel):
    """The axes shared by every chart type that plots one value scale against another.

These chart types are the scatter and bubble charts and their interactive variants. They have an X and a Y value axis and no category axis."""
    bubbleChart: BubbleChart | None = None
    bubbleInteractiveChart: BubbleInteractiveChart | None = None
    genericCorrelationChart: GenericCorrelationChart | None = None
    scatterChart: ScatterChart | None = None
    scatterInteractiveChart: ScatterInteractiveChart | None = None

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_CorrelationChartCase, ...]: ...

        def union_primary(self) -> _CorrelationChartCase | None: ...

        def union_primary_name(self) -> Literal["bubbleChart", "bubbleInteractiveChart", "genericCorrelationChart", "scatterChart", "scatterInteractiveChart"] | None: ...


@wire(
    "com.apple.apps.content-language.donut-chart",
    version="1.0",
    fields=[
        ("title", (1, 0), "opt"),
        ("caption", (1, 0), "opt"),
        ("data", (1, 0), "opt"),
        ("show_legend", (1, 0), "def"),
        ("legend", (1, 0), "opt"),
        ("series", (1, 0), "opt"),
        ("chart_colors", (1, 0), "opt"),
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
    ],
)
class DonutChart(ObjectModel):
    """A donut chart.

Each series contributes one segment of the ring, sized by that series' first value; Keynote doesn't show later values in a series. Donut charts have no categories and no axes. The title, when shown, appears in the center of the ring."""
    title: Label | None = Field(default=None, description="The object's title.")
    caption: Label | None = Field(default=None, description="The object's caption, which Keynote always places below the object. If a caption is off, you still write it out with `Label.is_visible` set to `false`, so having a value doesn't mean the caption shows.")
    data: ChartData | None = Field(default=None, description="The chart's data grid, together with its plot direction and data-source mode. This data replaces the placeholder data a new chart starts with; when omitted, that placeholder data remains.")
    show_legend: bool = Field(default=True, description="A Boolean value that indicates whether the chart's legend appears. This value is independent of the `legend` property, which sets the legend's placement and text style rather than its visibility.")
    legend: ChartLegend | None = Field(default=None, description="The placement and label text style of the chart's legend. This value doesn't control whether the legend appears (see `show_legend`), and it only applies to a chart that has a legend.")
    series: list[ChartSeries] | None = Field(default=None, description="The styling and label formatting for individual data series. Each entry applies to the series named by its `ChartSeries.series_index`, or to the series at the same position when `ChartSeries.series_index` is omitted; entries that don't correspond to a series in the data don't have an effect.")
    chart_colors: list[ChartColor] | None = Field(default=None, description="The chart's ordered series styles. A series takes the entry at its own position, and the chart's style supplies any position without an entry or with an empty one, so the list doesn't wrap. Entries past the last series also remain. Keynote reads one entry for each series style in the chart's style and ignores any further entries.")
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=False, description="A Boolean value that indicates whether the object's width-to-height ratio is locked when the object resizes. The lock doesn't constrain the `geometry` property. If this property is absent, images, movies, and groups default to `true`, and other objects to `false`.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")


@wire(
    "com.apple.apps.content-language.line3-dchart",
    version="1.0",
    fields=[
        ("title", (1, 0), "opt"),
        ("caption", (1, 0), "opt"),
        ("data", (1, 0), "opt"),
        ("show_legend", (1, 0), "def"),
        ("legend", (1, 0), "opt"),
        ("series", (1, 0), "opt"),
        ("chart_colors", (1, 0), "opt"),
        ("category_axis", (1, 0), "opt"),
        ("value_axis", (1, 0), "opt"),
        ("value_axis_secondary", (1, 0), "opt"),
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
    ],
)
class Line3DChart(ObjectModel):
    """A 3D line chart.

3D appearance settings such as rotation, depth, lighting, and textures aren't included: rotation and depth take the default for this chart type, and lighting and a textured series' fill come from the chart's style."""
    title: Label | None = Field(default=None, description="The object's title.")
    caption: Label | None = Field(default=None, description="The object's caption, which Keynote always places below the object. If a caption is off, you still write it out with `Label.is_visible` set to `false`, so having a value doesn't mean the caption shows.")
    data: ChartData | None = Field(default=None, description="The chart's data grid, together with its plot direction and data-source mode. This data replaces the placeholder data a new chart starts with; when omitted, that placeholder data remains.")
    show_legend: bool = Field(default=True, description="A Boolean value that indicates whether the chart's legend appears. This value is independent of the `legend` property, which sets the legend's placement and text style rather than its visibility.")
    legend: ChartLegend | None = Field(default=None, description="The placement and label text style of the chart's legend. This value doesn't control whether the legend appears (see `show_legend`), and it only applies to a chart that has a legend.")
    series: list[ChartSeries] | None = Field(default=None, description="The styling and label formatting for individual data series. Each entry applies to the series named by its `ChartSeries.series_index`, or to the series at the same position when `ChartSeries.series_index` is omitted; entries that don't correspond to a series in the data don't have an effect.")
    chart_colors: list[ChartColor] | None = Field(default=None, description="The chart's ordered series styles. A series takes the entry at its own position, and the chart's style supplies any position without an entry or with an empty one, so the list doesn't wrap. Entries past the last series also remain. Keynote reads one entry for each series style in the chart's style and ignores any further entries.")
    category_axis: ChartCategoryAxis | None = Field(default=None, description="The category axis, along which Keynote lays out the chart's categories. When omitted, the category axis keeps the appearance it inherits from the chart's style.")
    value_axis: ChartValueAxis | None = Field(default=None, description="The primary value axis, which carries the numeric scale to measure the series against. When omitted, the value axis keeps the appearance it inherits from the chart's style.")
    value_axis_secondary: ChartValueAxis | None = Field(default=None, description="The second value axis, used only by a two-axis chart that actually plots a series against a second value scale. On any other chart type, this value doesn't have an effect.")
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=False, description="A Boolean value that indicates whether the object's width-to-height ratio is locked when the object resizes. The lock doesn't constrain the `geometry` property. If this property is absent, images, movies, and groups default to `true`, and other objects to `false`.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")


@wire(
    "com.apple.apps.content-language.line-chart",
    version="1.0",
    fields=[
        ("title", (1, 0), "opt"),
        ("caption", (1, 0), "opt"),
        ("data", (1, 0), "opt"),
        ("show_legend", (1, 0), "def"),
        ("legend", (1, 0), "opt"),
        ("series", (1, 0), "opt"),
        ("chart_colors", (1, 0), "opt"),
        ("category_axis", (1, 0), "opt"),
        ("value_axis", (1, 0), "opt"),
        ("value_axis_secondary", (1, 0), "opt"),
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
    ],
)
class LineChart(ObjectModel):
    """A 2D line chart.

Keynote draws each series as a line against a shared category axis and value axis."""
    title: Label | None = Field(default=None, description="The object's title.")
    caption: Label | None = Field(default=None, description="The object's caption, which Keynote always places below the object. If a caption is off, you still write it out with `Label.is_visible` set to `false`, so having a value doesn't mean the caption shows.")
    data: ChartData | None = Field(default=None, description="The chart's data grid, together with its plot direction and data-source mode. This data replaces the placeholder data a new chart starts with; when omitted, that placeholder data remains.")
    show_legend: bool = Field(default=True, description="A Boolean value that indicates whether the chart's legend appears. This value is independent of the `legend` property, which sets the legend's placement and text style rather than its visibility.")
    legend: ChartLegend | None = Field(default=None, description="The placement and label text style of the chart's legend. This value doesn't control whether the legend appears (see `show_legend`), and it only applies to a chart that has a legend.")
    series: list[ChartSeries] | None = Field(default=None, description="The styling and label formatting for individual data series. Each entry applies to the series named by its `ChartSeries.series_index`, or to the series at the same position when `ChartSeries.series_index` is omitted; entries that don't correspond to a series in the data don't have an effect.")
    chart_colors: list[ChartColor] | None = Field(default=None, description="The chart's ordered series styles. A series takes the entry at its own position, and the chart's style supplies any position without an entry or with an empty one, so the list doesn't wrap. Entries past the last series also remain. Keynote reads one entry for each series style in the chart's style and ignores any further entries.")
    category_axis: ChartCategoryAxis | None = Field(default=None, description="The category axis, along which Keynote lays out the chart's categories. When omitted, the category axis keeps the appearance it inherits from the chart's style.")
    value_axis: ChartValueAxis | None = Field(default=None, description="The primary value axis, which carries the numeric scale to measure the series against. When omitted, the value axis keeps the appearance it inherits from the chart's style.")
    value_axis_secondary: ChartValueAxis | None = Field(default=None, description="The second value axis, used only by a two-axis chart that actually plots a series against a second value scale. On any other chart type, this value doesn't have an effect.")
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=False, description="A Boolean value that indicates whether the object's width-to-height ratio is locked when the object resizes. The lock doesn't constrain the `geometry` property. If this property is absent, images, movies, and groups default to `true`, and other objects to `false`.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")


@wire(
    "com.apple.apps.content-language.mixed-chart",
    version="1.0",
    fields=[
        ("title", (1, 0), "opt"),
        ("caption", (1, 0), "opt"),
        ("data", (1, 0), "opt"),
        ("show_legend", (1, 0), "def"),
        ("legend", (1, 0), "opt"),
        ("series", (1, 0), "opt"),
        ("chart_colors", (1, 0), "opt"),
        ("category_axis", (1, 0), "opt"),
        ("value_axis", (1, 0), "opt"),
        ("value_axis_secondary", (1, 0), "opt"),
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
    ],
)
class MixedChart(ObjectModel):
    """A mixed chart, which draws individual series as columns, lines, or areas.

The series share a category axis and value axis, and each series picks its shape through its `ChartSeries.mixed_series_type` value."""
    title: Label | None = Field(default=None, description="The object's title.")
    caption: Label | None = Field(default=None, description="The object's caption, which Keynote always places below the object. If a caption is off, you still write it out with `Label.is_visible` set to `false`, so having a value doesn't mean the caption shows.")
    data: ChartData | None = Field(default=None, description="The chart's data grid, together with its plot direction and data-source mode. This data replaces the placeholder data a new chart starts with; when omitted, that placeholder data remains.")
    show_legend: bool = Field(default=True, description="A Boolean value that indicates whether the chart's legend appears. This value is independent of the `legend` property, which sets the legend's placement and text style rather than its visibility.")
    legend: ChartLegend | None = Field(default=None, description="The placement and label text style of the chart's legend. This value doesn't control whether the legend appears (see `show_legend`), and it only applies to a chart that has a legend.")
    series: list[ChartSeries] | None = Field(default=None, description="The styling and label formatting for individual data series. Each entry applies to the series named by its `ChartSeries.series_index`, or to the series at the same position when `ChartSeries.series_index` is omitted; entries that don't correspond to a series in the data don't have an effect.")
    chart_colors: list[ChartColor] | None = Field(default=None, description="The chart's ordered series styles. A series takes the entry at its own position, and the chart's style supplies any position without an entry or with an empty one, so the list doesn't wrap. Entries past the last series also remain. Keynote reads one entry for each series style in the chart's style and ignores any further entries.")
    category_axis: ChartCategoryAxis | None = Field(default=None, description="The category axis, along which Keynote lays out the chart's categories. When omitted, the category axis keeps the appearance it inherits from the chart's style.")
    value_axis: ChartValueAxis | None = Field(default=None, description="The primary value axis, which carries the numeric scale to measure the series against. When omitted, the value axis keeps the appearance it inherits from the chart's style.")
    value_axis_secondary: ChartValueAxis | None = Field(default=None, description="The second value axis, used only by a two-axis chart that actually plots a series against a second value scale. On any other chart type, this value doesn't have an effect.")
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=False, description="A Boolean value that indicates whether the object's width-to-height ratio is locked when the object resizes. The lock doesn't constrain the `geometry` property. If this property is absent, images, movies, and groups default to `true`, and other objects to `false`.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")


@wire(
    "com.apple.apps.content-language.pie3-dchart",
    version="1.0",
    fields=[
        ("title", (1, 0), "opt"),
        ("caption", (1, 0), "opt"),
        ("data", (1, 0), "opt"),
        ("show_legend", (1, 0), "def"),
        ("legend", (1, 0), "opt"),
        ("series", (1, 0), "opt"),
        ("chart_colors", (1, 0), "opt"),
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
    ],
)
class Pie3DChart(ObjectModel):
    """A 3D pie chart.

Like the 2D pie chart, it has no axes. 3D appearance settings such as rotation, depth, lighting, and textures aren't included: rotation and depth take the default for this chart type, and lighting and a textured series' fill come from the chart's style."""
    title: Label | None = Field(default=None, description="The object's title.")
    caption: Label | None = Field(default=None, description="The object's caption, which Keynote always places below the object. If a caption is off, you still write it out with `Label.is_visible` set to `false`, so having a value doesn't mean the caption shows.")
    data: ChartData | None = Field(default=None, description="The chart's data grid, together with its plot direction and data-source mode. This data replaces the placeholder data a new chart starts with; when omitted, that placeholder data remains.")
    show_legend: bool = Field(default=True, description="A Boolean value that indicates whether the chart's legend appears. This value is independent of the `legend` property, which sets the legend's placement and text style rather than its visibility.")
    legend: ChartLegend | None = Field(default=None, description="The placement and label text style of the chart's legend. This value doesn't control whether the legend appears (see `show_legend`), and it only applies to a chart that has a legend.")
    series: list[ChartSeries] | None = Field(default=None, description="The styling and label formatting for individual data series. Each entry applies to the series named by its `ChartSeries.series_index`, or to the series at the same position when `ChartSeries.series_index` is omitted; entries that don't correspond to a series in the data don't have an effect.")
    chart_colors: list[ChartColor] | None = Field(default=None, description="The chart's ordered series styles. A series takes the entry at its own position, and the chart's style supplies any position without an entry or with an empty one, so the list doesn't wrap. Entries past the last series also remain. Keynote reads one entry for each series style in the chart's style and ignores any further entries.")
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=False, description="A Boolean value that indicates whether the object's width-to-height ratio is locked when the object resizes. The lock doesn't constrain the `geometry` property. If this property is absent, images, movies, and groups default to `true`, and other objects to `false`.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")


@wire(
    "com.apple.apps.content-language.pie-chart",
    version="1.0",
    fields=[
        ("title", (1, 0), "opt"),
        ("caption", (1, 0), "opt"),
        ("data", (1, 0), "opt"),
        ("show_legend", (1, 0), "def"),
        ("legend", (1, 0), "opt"),
        ("series", (1, 0), "opt"),
        ("chart_colors", (1, 0), "opt"),
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
    ],
)
class PieChart(ObjectModel):
    """A pie chart.

Each series contributes one wedge, sized by that series' first value; Keynote doesn't show later values in a series. Pie charts have no categories and no axes."""
    title: Label | None = Field(default=None, description="The object's title.")
    caption: Label | None = Field(default=None, description="The object's caption, which Keynote always places below the object. If a caption is off, you still write it out with `Label.is_visible` set to `false`, so having a value doesn't mean the caption shows.")
    data: ChartData | None = Field(default=None, description="The chart's data grid, together with its plot direction and data-source mode. This data replaces the placeholder data a new chart starts with; when omitted, that placeholder data remains.")
    show_legend: bool = Field(default=True, description="A Boolean value that indicates whether the chart's legend appears. This value is independent of the `legend` property, which sets the legend's placement and text style rather than its visibility.")
    legend: ChartLegend | None = Field(default=None, description="The placement and label text style of the chart's legend. This value doesn't control whether the legend appears (see `show_legend`), and it only applies to a chart that has a legend.")
    series: list[ChartSeries] | None = Field(default=None, description="The styling and label formatting for individual data series. Each entry applies to the series named by its `ChartSeries.series_index`, or to the series at the same position when `ChartSeries.series_index` is omitted; entries that don't correspond to a series in the data don't have an effect.")
    chart_colors: list[ChartColor] | None = Field(default=None, description="The chart's ordered series styles. A series takes the entry at its own position, and the chart's style supplies any position without an entry or with an empty one, so the list doesn't wrap. Entries past the last series also remain. Keynote reads one entry for each series style in the chart's style and ignores any further entries.")
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=False, description="A Boolean value that indicates whether the object's width-to-height ratio is locked when the object resizes. The lock doesn't constrain the `geometry` property. If this property is absent, images, movies, and groups default to `true`, and other objects to `false`.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")


@wire(
    "com.apple.apps.content-language.radar-chart",
    version="1.0",
    fields=[
        ("title", (1, 0), "opt"),
        ("caption", (1, 0), "opt"),
        ("data", (1, 0), "opt"),
        ("show_legend", (1, 0), "def"),
        ("legend", (1, 0), "opt"),
        ("series", (1, 0), "opt"),
        ("chart_colors", (1, 0), "opt"),
        ("category_axis", (1, 0), "opt"),
        ("value_axis", (1, 0), "opt"),
        ("value_axis_secondary", (1, 0), "opt"),
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
    ],
)
class RadarChart(ObjectModel):
    """A radar chart.

Keynote arranges the categories radially around a center point and plots each series against a shared radial value scale."""
    title: Label | None = Field(default=None, description="The object's title.")
    caption: Label | None = Field(default=None, description="The object's caption, which Keynote always places below the object. If a caption is off, you still write it out with `Label.is_visible` set to `false`, so having a value doesn't mean the caption shows.")
    data: ChartData | None = Field(default=None, description="The chart's data grid, together with its plot direction and data-source mode. This data replaces the placeholder data a new chart starts with; when omitted, that placeholder data remains.")
    show_legend: bool = Field(default=True, description="A Boolean value that indicates whether the chart's legend appears. This value is independent of the `legend` property, which sets the legend's placement and text style rather than its visibility.")
    legend: ChartLegend | None = Field(default=None, description="The placement and label text style of the chart's legend. This value doesn't control whether the legend appears (see `show_legend`), and it only applies to a chart that has a legend.")
    series: list[ChartSeries] | None = Field(default=None, description="The styling and label formatting for individual data series. Each entry applies to the series named by its `ChartSeries.series_index`, or to the series at the same position when `ChartSeries.series_index` is omitted; entries that don't correspond to a series in the data don't have an effect.")
    chart_colors: list[ChartColor] | None = Field(default=None, description="The chart's ordered series styles. A series takes the entry at its own position, and the chart's style supplies any position without an entry or with an empty one, so the list doesn't wrap. Entries past the last series also remain. Keynote reads one entry for each series style in the chart's style and ignores any further entries.")
    category_axis: ChartCategoryAxis | None = Field(default=None, description="The category axis, along which Keynote lays out the chart's categories. When omitted, the category axis keeps the appearance it inherits from the chart's style.")
    value_axis: ChartValueAxis | None = Field(default=None, description="The primary value axis, which carries the numeric scale to measure the series against. When omitted, the value axis keeps the appearance it inherits from the chart's style.")
    value_axis_secondary: ChartValueAxis | None = Field(default=None, description="The second value axis, used only by a two-axis chart that actually plots a series against a second value scale. On any other chart type, this value doesn't have an effect.")
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=False, description="A Boolean value that indicates whether the object's width-to-height ratio is locked when the object resizes. The lock doesn't constrain the `geometry` property. If this property is absent, images, movies, and groups default to `true`, and other objects to `false`.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")


@wire(
    "com.apple.apps.content-language.scatter-chart",
    version="1.0",
    fields=[
        ("title", (1, 0), "opt"),
        ("caption", (1, 0), "opt"),
        ("data", (1, 0), "opt"),
        ("show_legend", (1, 0), "def"),
        ("legend", (1, 0), "opt"),
        ("series", (1, 0), "opt"),
        ("chart_colors", (1, 0), "opt"),
        ("value_axis_x", (1, 0), "opt"),
        ("value_axis_y", (1, 0), "opt"),
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
    ],
)
class ScatterChart(ObjectModel):
    """A scatter chart.

Keynote plots each data point against an X and a Y value axis rather than against a category axis. See `data.shared_xvalues` for how the grid's rows or columns map onto each series."""
    title: Label | None = Field(default=None, description="The object's title.")
    caption: Label | None = Field(default=None, description="The object's caption, which Keynote always places below the object. If a caption is off, you still write it out with `Label.is_visible` set to `false`, so having a value doesn't mean the caption shows.")
    data: ChartData | None = Field(default=None, description="The chart's data grid, together with its plot direction and data-source mode. This data replaces the placeholder data a new chart starts with; when omitted, that placeholder data remains.")
    show_legend: bool = Field(default=True, description="A Boolean value that indicates whether the chart's legend appears. This value is independent of the `legend` property, which sets the legend's placement and text style rather than its visibility.")
    legend: ChartLegend | None = Field(default=None, description="The placement and label text style of the chart's legend. This value doesn't control whether the legend appears (see `show_legend`), and it only applies to a chart that has a legend.")
    series: list[ChartSeries] | None = Field(default=None, description="The styling and label formatting for individual data series. Each entry applies to the series named by its `ChartSeries.series_index`, or to the series at the same position when `ChartSeries.series_index` is omitted; entries that don't correspond to a series in the data don't have an effect.")
    chart_colors: list[ChartColor] | None = Field(default=None, description="The chart's ordered series styles. A series takes the entry at its own position, and the chart's style supplies any position without an entry or with an empty one, so the list doesn't wrap. Entries past the last series also remain. Keynote reads one entry for each series style in the chart's style and ignores any further entries.")
    value_axis_x: ChartValueAxis | None = Field(default=None, description="The horizontal (X) value axis. When omitted, the X axis keeps the appearance it inherits from the chart's style.")
    value_axis_y: ChartValueAxis | None = Field(default=None, description="The vertical (Y) value axis. When omitted, the Y axis keeps the appearance it inherits from the chart's style.")
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=False, description="A Boolean value that indicates whether the object's width-to-height ratio is locked when the object resizes. The lock doesn't constrain the `geometry` property. If this property is absent, images, movies, and groups default to `true`, and other objects to `false`.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")


@wire(
    "com.apple.apps.content-language.scatter-interactive-chart",
    version="1.0",
    fields=[
        ("title", (1, 0), "opt"),
        ("caption", (1, 0), "opt"),
        ("data", (1, 0), "opt"),
        ("show_legend", (1, 0), "def"),
        ("legend", (1, 0), "opt"),
        ("series", (1, 0), "opt"),
        ("chart_colors", (1, 0), "opt"),
        ("value_axis_x", (1, 0), "opt"),
        ("value_axis_y", (1, 0), "opt"),
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
    ],
)
class ScatterInteractiveChart(ObjectModel):
    """An interactive scatter chart, which shows one data set at a time.

You can step between the data sets. Keynote lays out the series as a scatter chart; for more information, see `data.shared_xvalues`. The interactive control, the position of the data set name, and which data set the reader shows aren't included, so they take the default for this chart type."""
    title: Label | None = Field(default=None, description="The object's title.")
    caption: Label | None = Field(default=None, description="The object's caption, which Keynote always places below the object. If a caption is off, you still write it out with `Label.is_visible` set to `false`, so having a value doesn't mean the caption shows.")
    data: ChartData | None = Field(default=None, description="The chart's data grid, together with its plot direction and data-source mode. This data replaces the placeholder data a new chart starts with; when omitted, that placeholder data remains.")
    show_legend: bool = Field(default=True, description="A Boolean value that indicates whether the chart's legend appears. This value is independent of the `legend` property, which sets the legend's placement and text style rather than its visibility.")
    legend: ChartLegend | None = Field(default=None, description="The placement and label text style of the chart's legend. This value doesn't control whether the legend appears (see `show_legend`), and it only applies to a chart that has a legend.")
    series: list[ChartSeries] | None = Field(default=None, description="The styling and label formatting for individual data series. Each entry applies to the series named by its `ChartSeries.series_index`, or to the series at the same position when `ChartSeries.series_index` is omitted; entries that don't correspond to a series in the data don't have an effect.")
    chart_colors: list[ChartColor] | None = Field(default=None, description="The chart's ordered series styles. A series takes the entry at its own position, and the chart's style supplies any position without an entry or with an empty one, so the list doesn't wrap. Entries past the last series also remain. Keynote reads one entry for each series style in the chart's style and ignores any further entries.")
    value_axis_x: ChartValueAxis | None = Field(default=None, description="The horizontal (X) value axis. When omitted, the X axis keeps the appearance it inherits from the chart's style.")
    value_axis_y: ChartValueAxis | None = Field(default=None, description="The vertical (Y) value axis. When omitted, the Y axis keeps the appearance it inherits from the chart's style.")
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=False, description="A Boolean value that indicates whether the object's width-to-height ratio is locked when the object resizes. The lock doesn't constrain the `geometry` property. If this property is absent, images, movies, and groups default to `true`, and other objects to `false`.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")


@wire(
    "com.apple.apps.content-language.stacked-area3-dchart",
    version="1.0",
    fields=[
        ("title", (1, 0), "opt"),
        ("caption", (1, 0), "opt"),
        ("data", (1, 0), "opt"),
        ("show_legend", (1, 0), "def"),
        ("legend", (1, 0), "opt"),
        ("series", (1, 0), "opt"),
        ("chart_colors", (1, 0), "opt"),
        ("category_axis", (1, 0), "opt"),
        ("value_axis", (1, 0), "opt"),
        ("value_axis_secondary", (1, 0), "opt"),
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
    ],
)
class StackedArea3DChart(ObjectModel):
    """A 3D stacked area chart.

3D appearance settings such as rotation, depth, lighting, and textures aren't included: rotation and depth take the default for this chart type, and lighting and a textured series' fill come from the chart's style."""
    title: Label | None = Field(default=None, description="The object's title.")
    caption: Label | None = Field(default=None, description="The object's caption, which Keynote always places below the object. If a caption is off, you still write it out with `Label.is_visible` set to `false`, so having a value doesn't mean the caption shows.")
    data: ChartData | None = Field(default=None, description="The chart's data grid, together with its plot direction and data-source mode. This data replaces the placeholder data a new chart starts with; when omitted, that placeholder data remains.")
    show_legend: bool = Field(default=True, description="A Boolean value that indicates whether the chart's legend appears. This value is independent of the `legend` property, which sets the legend's placement and text style rather than its visibility.")
    legend: ChartLegend | None = Field(default=None, description="The placement and label text style of the chart's legend. This value doesn't control whether the legend appears (see `show_legend`), and it only applies to a chart that has a legend.")
    series: list[ChartSeries] | None = Field(default=None, description="The styling and label formatting for individual data series. Each entry applies to the series named by its `ChartSeries.series_index`, or to the series at the same position when `ChartSeries.series_index` is omitted; entries that don't correspond to a series in the data don't have an effect.")
    chart_colors: list[ChartColor] | None = Field(default=None, description="The chart's ordered series styles. A series takes the entry at its own position, and the chart's style supplies any position without an entry or with an empty one, so the list doesn't wrap. Entries past the last series also remain. Keynote reads one entry for each series style in the chart's style and ignores any further entries.")
    category_axis: ChartCategoryAxis | None = Field(default=None, description="The category axis, along which Keynote lays out the chart's categories. When omitted, the category axis keeps the appearance it inherits from the chart's style.")
    value_axis: ChartValueAxis | None = Field(default=None, description="The primary value axis, which carries the numeric scale to measure the series against. When omitted, the value axis keeps the appearance it inherits from the chart's style.")
    value_axis_secondary: ChartValueAxis | None = Field(default=None, description="The second value axis, used only by a two-axis chart that actually plots a series against a second value scale. On any other chart type, this value doesn't have an effect.")
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=False, description="A Boolean value that indicates whether the object's width-to-height ratio is locked when the object resizes. The lock doesn't constrain the `geometry` property. If this property is absent, images, movies, and groups default to `true`, and other objects to `false`.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")


@wire(
    "com.apple.apps.content-language.stacked-area-chart",
    version="1.0",
    fields=[
        ("title", (1, 0), "opt"),
        ("caption", (1, 0), "opt"),
        ("data", (1, 0), "opt"),
        ("show_legend", (1, 0), "def"),
        ("legend", (1, 0), "opt"),
        ("series", (1, 0), "opt"),
        ("chart_colors", (1, 0), "opt"),
        ("category_axis", (1, 0), "opt"),
        ("value_axis", (1, 0), "opt"),
        ("value_axis_secondary", (1, 0), "opt"),
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
    ],
)
class StackedAreaChart(ObjectModel):
    """A 2D stacked area chart.

Keynote stacks each series' filled region on top of the one before it against a shared category axis and value axis."""
    title: Label | None = Field(default=None, description="The object's title.")
    caption: Label | None = Field(default=None, description="The object's caption, which Keynote always places below the object. If a caption is off, you still write it out with `Label.is_visible` set to `false`, so having a value doesn't mean the caption shows.")
    data: ChartData | None = Field(default=None, description="The chart's data grid, together with its plot direction and data-source mode. This data replaces the placeholder data a new chart starts with; when omitted, that placeholder data remains.")
    show_legend: bool = Field(default=True, description="A Boolean value that indicates whether the chart's legend appears. This value is independent of the `legend` property, which sets the legend's placement and text style rather than its visibility.")
    legend: ChartLegend | None = Field(default=None, description="The placement and label text style of the chart's legend. This value doesn't control whether the legend appears (see `show_legend`), and it only applies to a chart that has a legend.")
    series: list[ChartSeries] | None = Field(default=None, description="The styling and label formatting for individual data series. Each entry applies to the series named by its `ChartSeries.series_index`, or to the series at the same position when `ChartSeries.series_index` is omitted; entries that don't correspond to a series in the data don't have an effect.")
    chart_colors: list[ChartColor] | None = Field(default=None, description="The chart's ordered series styles. A series takes the entry at its own position, and the chart's style supplies any position without an entry or with an empty one, so the list doesn't wrap. Entries past the last series also remain. Keynote reads one entry for each series style in the chart's style and ignores any further entries.")
    category_axis: ChartCategoryAxis | None = Field(default=None, description="The category axis, along which Keynote lays out the chart's categories. When omitted, the category axis keeps the appearance it inherits from the chart's style.")
    value_axis: ChartValueAxis | None = Field(default=None, description="The primary value axis, which carries the numeric scale to measure the series against. When omitted, the value axis keeps the appearance it inherits from the chart's style.")
    value_axis_secondary: ChartValueAxis | None = Field(default=None, description="The second value axis, used only by a two-axis chart that actually plots a series against a second value scale. On any other chart type, this value doesn't have an effect.")
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=False, description="A Boolean value that indicates whether the object's width-to-height ratio is locked when the object resizes. The lock doesn't constrain the `geometry` property. If this property is absent, images, movies, and groups default to `true`, and other objects to `false`.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")


@wire(
    "com.apple.apps.content-language.stacked-bar3-dchart",
    version="1.0",
    fields=[
        ("title", (1, 0), "opt"),
        ("caption", (1, 0), "opt"),
        ("data", (1, 0), "opt"),
        ("show_legend", (1, 0), "def"),
        ("legend", (1, 0), "opt"),
        ("series", (1, 0), "opt"),
        ("chart_colors", (1, 0), "opt"),
        ("category_axis", (1, 0), "opt"),
        ("value_axis", (1, 0), "opt"),
        ("value_axis_secondary", (1, 0), "opt"),
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
    ],
)
class StackedBar3DChart(ObjectModel):
    """A 3D stacked horizontal bar chart.

3D appearance settings such as rotation, depth, lighting, and textures aren't included: rotation and depth take the default for this chart type, and lighting and a textured series' fill come from the chart's style."""
    title: Label | None = Field(default=None, description="The object's title.")
    caption: Label | None = Field(default=None, description="The object's caption, which Keynote always places below the object. If a caption is off, you still write it out with `Label.is_visible` set to `false`, so having a value doesn't mean the caption shows.")
    data: ChartData | None = Field(default=None, description="The chart's data grid, together with its plot direction and data-source mode. This data replaces the placeholder data a new chart starts with; when omitted, that placeholder data remains.")
    show_legend: bool = Field(default=True, description="A Boolean value that indicates whether the chart's legend appears. This value is independent of the `legend` property, which sets the legend's placement and text style rather than its visibility.")
    legend: ChartLegend | None = Field(default=None, description="The placement and label text style of the chart's legend. This value doesn't control whether the legend appears (see `show_legend`), and it only applies to a chart that has a legend.")
    series: list[ChartSeries] | None = Field(default=None, description="The styling and label formatting for individual data series. Each entry applies to the series named by its `ChartSeries.series_index`, or to the series at the same position when `ChartSeries.series_index` is omitted; entries that don't correspond to a series in the data don't have an effect.")
    chart_colors: list[ChartColor] | None = Field(default=None, description="The chart's ordered series styles. A series takes the entry at its own position, and the chart's style supplies any position without an entry or with an empty one, so the list doesn't wrap. Entries past the last series also remain. Keynote reads one entry for each series style in the chart's style and ignores any further entries.")
    category_axis: ChartCategoryAxis | None = Field(default=None, description="The category axis, along which Keynote lays out the chart's categories. When omitted, the category axis keeps the appearance it inherits from the chart's style.")
    value_axis: ChartValueAxis | None = Field(default=None, description="The primary value axis, which carries the numeric scale to measure the series against. When omitted, the value axis keeps the appearance it inherits from the chart's style.")
    value_axis_secondary: ChartValueAxis | None = Field(default=None, description="The second value axis, used only by a two-axis chart that actually plots a series against a second value scale. On any other chart type, this value doesn't have an effect.")
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=False, description="A Boolean value that indicates whether the object's width-to-height ratio is locked when the object resizes. The lock doesn't constrain the `geometry` property. If this property is absent, images, movies, and groups default to `true`, and other objects to `false`.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")


@wire(
    "com.apple.apps.content-language.stacked-bar-chart",
    version="1.0",
    fields=[
        ("title", (1, 0), "opt"),
        ("caption", (1, 0), "opt"),
        ("data", (1, 0), "opt"),
        ("show_legend", (1, 0), "def"),
        ("legend", (1, 0), "opt"),
        ("series", (1, 0), "opt"),
        ("chart_colors", (1, 0), "opt"),
        ("category_axis", (1, 0), "opt"),
        ("value_axis", (1, 0), "opt"),
        ("value_axis_secondary", (1, 0), "opt"),
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
    ],
)
class StackedBarChart(ObjectModel):
    """A 2D stacked bar chart.

Each series contributes a segment to a single horizontal bar for each category, which Keynote measures against a shared value axis."""
    title: Label | None = Field(default=None, description="The object's title.")
    caption: Label | None = Field(default=None, description="The object's caption, which Keynote always places below the object. If a caption is off, you still write it out with `Label.is_visible` set to `false`, so having a value doesn't mean the caption shows.")
    data: ChartData | None = Field(default=None, description="The chart's data grid, together with its plot direction and data-source mode. This data replaces the placeholder data a new chart starts with; when omitted, that placeholder data remains.")
    show_legend: bool = Field(default=True, description="A Boolean value that indicates whether the chart's legend appears. This value is independent of the `legend` property, which sets the legend's placement and text style rather than its visibility.")
    legend: ChartLegend | None = Field(default=None, description="The placement and label text style of the chart's legend. This value doesn't control whether the legend appears (see `show_legend`), and it only applies to a chart that has a legend.")
    series: list[ChartSeries] | None = Field(default=None, description="The styling and label formatting for individual data series. Each entry applies to the series named by its `ChartSeries.series_index`, or to the series at the same position when `ChartSeries.series_index` is omitted; entries that don't correspond to a series in the data don't have an effect.")
    chart_colors: list[ChartColor] | None = Field(default=None, description="The chart's ordered series styles. A series takes the entry at its own position, and the chart's style supplies any position without an entry or with an empty one, so the list doesn't wrap. Entries past the last series also remain. Keynote reads one entry for each series style in the chart's style and ignores any further entries.")
    category_axis: ChartCategoryAxis | None = Field(default=None, description="The category axis, along which Keynote lays out the chart's categories. When omitted, the category axis keeps the appearance it inherits from the chart's style.")
    value_axis: ChartValueAxis | None = Field(default=None, description="The primary value axis, which carries the numeric scale to measure the series against. When omitted, the value axis keeps the appearance it inherits from the chart's style.")
    value_axis_secondary: ChartValueAxis | None = Field(default=None, description="The second value axis, used only by a two-axis chart that actually plots a series against a second value scale. On any other chart type, this value doesn't have an effect.")
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=False, description="A Boolean value that indicates whether the object's width-to-height ratio is locked when the object resizes. The lock doesn't constrain the `geometry` property. If this property is absent, images, movies, and groups default to `true`, and other objects to `false`.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")


@wire(
    "com.apple.apps.content-language.stacked-column3-dchart",
    version="1.0",
    fields=[
        ("title", (1, 0), "opt"),
        ("caption", (1, 0), "opt"),
        ("data", (1, 0), "opt"),
        ("show_legend", (1, 0), "def"),
        ("legend", (1, 0), "opt"),
        ("series", (1, 0), "opt"),
        ("chart_colors", (1, 0), "opt"),
        ("category_axis", (1, 0), "opt"),
        ("value_axis", (1, 0), "opt"),
        ("value_axis_secondary", (1, 0), "opt"),
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
    ],
)
class StackedColumn3DChart(ObjectModel):
    """A 3D stacked vertical column chart.

3D appearance settings such as rotation, depth, lighting, and textures aren't included: rotation and depth take the default for this chart type, and lighting and a textured series' fill come from the chart's style."""
    title: Label | None = Field(default=None, description="The object's title.")
    caption: Label | None = Field(default=None, description="The object's caption, which Keynote always places below the object. If a caption is off, you still write it out with `Label.is_visible` set to `false`, so having a value doesn't mean the caption shows.")
    data: ChartData | None = Field(default=None, description="The chart's data grid, together with its plot direction and data-source mode. This data replaces the placeholder data a new chart starts with; when omitted, that placeholder data remains.")
    show_legend: bool = Field(default=True, description="A Boolean value that indicates whether the chart's legend appears. This value is independent of the `legend` property, which sets the legend's placement and text style rather than its visibility.")
    legend: ChartLegend | None = Field(default=None, description="The placement and label text style of the chart's legend. This value doesn't control whether the legend appears (see `show_legend`), and it only applies to a chart that has a legend.")
    series: list[ChartSeries] | None = Field(default=None, description="The styling and label formatting for individual data series. Each entry applies to the series named by its `ChartSeries.series_index`, or to the series at the same position when `ChartSeries.series_index` is omitted; entries that don't correspond to a series in the data don't have an effect.")
    chart_colors: list[ChartColor] | None = Field(default=None, description="The chart's ordered series styles. A series takes the entry at its own position, and the chart's style supplies any position without an entry or with an empty one, so the list doesn't wrap. Entries past the last series also remain. Keynote reads one entry for each series style in the chart's style and ignores any further entries.")
    category_axis: ChartCategoryAxis | None = Field(default=None, description="The category axis, along which Keynote lays out the chart's categories. When omitted, the category axis keeps the appearance it inherits from the chart's style.")
    value_axis: ChartValueAxis | None = Field(default=None, description="The primary value axis, which carries the numeric scale to measure the series against. When omitted, the value axis keeps the appearance it inherits from the chart's style.")
    value_axis_secondary: ChartValueAxis | None = Field(default=None, description="The second value axis, used only by a two-axis chart that actually plots a series against a second value scale. On any other chart type, this value doesn't have an effect.")
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=False, description="A Boolean value that indicates whether the object's width-to-height ratio is locked when the object resizes. The lock doesn't constrain the `geometry` property. If this property is absent, images, movies, and groups default to `true`, and other objects to `false`.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")


@wire(
    "com.apple.apps.content-language.stacked-column-chart",
    version="1.0",
    fields=[
        ("title", (1, 0), "opt"),
        ("caption", (1, 0), "opt"),
        ("data", (1, 0), "opt"),
        ("show_legend", (1, 0), "def"),
        ("legend", (1, 0), "opt"),
        ("series", (1, 0), "opt"),
        ("chart_colors", (1, 0), "opt"),
        ("category_axis", (1, 0), "opt"),
        ("value_axis", (1, 0), "opt"),
        ("value_axis_secondary", (1, 0), "opt"),
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
    ],
)
class StackedColumnChart(ObjectModel):
    """A 2D stacked column chart.

Each series contributes a segment to a single vertical column for each category, which Keynote measures against a shared value axis."""
    title: Label | None = Field(default=None, description="The object's title.")
    caption: Label | None = Field(default=None, description="The object's caption, which Keynote always places below the object. If a caption is off, you still write it out with `Label.is_visible` set to `false`, so having a value doesn't mean the caption shows.")
    data: ChartData | None = Field(default=None, description="The chart's data grid, together with its plot direction and data-source mode. This data replaces the placeholder data a new chart starts with; when omitted, that placeholder data remains.")
    show_legend: bool = Field(default=True, description="A Boolean value that indicates whether the chart's legend appears. This value is independent of the `legend` property, which sets the legend's placement and text style rather than its visibility.")
    legend: ChartLegend | None = Field(default=None, description="The placement and label text style of the chart's legend. This value doesn't control whether the legend appears (see `show_legend`), and it only applies to a chart that has a legend.")
    series: list[ChartSeries] | None = Field(default=None, description="The styling and label formatting for individual data series. Each entry applies to the series named by its `ChartSeries.series_index`, or to the series at the same position when `ChartSeries.series_index` is omitted; entries that don't correspond to a series in the data don't have an effect.")
    chart_colors: list[ChartColor] | None = Field(default=None, description="The chart's ordered series styles. A series takes the entry at its own position, and the chart's style supplies any position without an entry or with an empty one, so the list doesn't wrap. Entries past the last series also remain. Keynote reads one entry for each series style in the chart's style and ignores any further entries.")
    category_axis: ChartCategoryAxis | None = Field(default=None, description="The category axis, along which Keynote lays out the chart's categories. When omitted, the category axis keeps the appearance it inherits from the chart's style.")
    value_axis: ChartValueAxis | None = Field(default=None, description="The primary value axis, which carries the numeric scale to measure the series against. When omitted, the value axis keeps the appearance it inherits from the chart's style.")
    value_axis_secondary: ChartValueAxis | None = Field(default=None, description="The second value axis, used only by a two-axis chart that actually plots a series against a second value scale. On any other chart type, this value doesn't have an effect.")
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=False, description="A Boolean value that indicates whether the object's width-to-height ratio is locked when the object resizes. The lock doesn't constrain the `geometry` property. If this property is absent, images, movies, and groups default to `true`, and other objects to `false`.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")


@wire(
    "com.apple.apps.content-language.two-axis-chart",
    version="1.0",
    fields=[
        ("title", (1, 0), "opt"),
        ("caption", (1, 0), "opt"),
        ("data", (1, 0), "opt"),
        ("show_legend", (1, 0), "def"),
        ("legend", (1, 0), "opt"),
        ("series", (1, 0), "opt"),
        ("chart_colors", (1, 0), "opt"),
        ("category_axis", (1, 0), "opt"),
        ("value_axis", (1, 0), "opt"),
        ("value_axis_secondary", (1, 0), "opt"),
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
    ],
)
class TwoAxisChart(ObjectModel):
    """A two-axis chart, which is a category chart with two independent value scales.

The two scales let Keynote measure different series against different value axes. It's the only chart type that uses `value_axis_secondary`, and, like the mixed chart, it lets each series pick its shape through its `ChartSeries.mixed_series_type` value."""
    title: Label | None = Field(default=None, description="The object's title.")
    caption: Label | None = Field(default=None, description="The object's caption, which Keynote always places below the object. If a caption is off, you still write it out with `Label.is_visible` set to `false`, so having a value doesn't mean the caption shows.")
    data: ChartData | None = Field(default=None, description="The chart's data grid, together with its plot direction and data-source mode. This data replaces the placeholder data a new chart starts with; when omitted, that placeholder data remains.")
    show_legend: bool = Field(default=True, description="A Boolean value that indicates whether the chart's legend appears. This value is independent of the `legend` property, which sets the legend's placement and text style rather than its visibility.")
    legend: ChartLegend | None = Field(default=None, description="The placement and label text style of the chart's legend. This value doesn't control whether the legend appears (see `show_legend`), and it only applies to a chart that has a legend.")
    series: list[ChartSeries] | None = Field(default=None, description="The styling and label formatting for individual data series. Each entry applies to the series named by its `ChartSeries.series_index`, or to the series at the same position when `ChartSeries.series_index` is omitted; entries that don't correspond to a series in the data don't have an effect.")
    chart_colors: list[ChartColor] | None = Field(default=None, description="The chart's ordered series styles. A series takes the entry at its own position, and the chart's style supplies any position without an entry or with an empty one, so the list doesn't wrap. Entries past the last series also remain. Keynote reads one entry for each series style in the chart's style and ignores any further entries.")
    category_axis: ChartCategoryAxis | None = Field(default=None, description="The category axis, along which Keynote lays out the chart's categories. When omitted, the category axis keeps the appearance it inherits from the chart's style.")
    value_axis: ChartValueAxis | None = Field(default=None, description="The primary value axis, which carries the numeric scale to measure the series against. When omitted, the value axis keeps the appearance it inherits from the chart's style.")
    value_axis_secondary: ChartValueAxis | None = Field(default=None, description="The second value axis, used only by a two-axis chart that actually plots a series against a second value scale. On any other chart type, this value doesn't have an effect.")
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=False, description="A Boolean value that indicates whether the object's width-to-height ratio is locked when the object resizes. The lock doesn't constrain the `geometry` property. If this property is absent, images, movies, and groups default to `true`, and other objects to `false`.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")


@wire(
    "com.apple.apps.content-language.connection-line",
    version="1.0",
    fields=[
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
        ("line_type", (1, 0), "def"),
        ("tail", (1, 0), "req"),
        ("head", (1, 0), "req"),
        ("stroke", (1, 0), "def"),
        ("opacity", (1, 0), "def"),
        ("shadow", (1, 0), "ovr"),
        ("reflection", (1, 0), "opt"),
    ],
)
class ConnectionLine(ObjectModel):
    """A line drawn from its tail end to its head end, each of which can attach to another object.

The route comes from `tail`, `head`, and (for a curved or corner line) the control position carried by `line_type`. Because the line's position and size follow from the route, `geometry` only transforms the supplied end points and control position, and is omitted when Keynote writes out a connection line."""
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=False, description="A Boolean value that indicates whether the object's width-to-height ratio is locked when the object resizes. The lock doesn't constrain the `geometry` property. If this property is absent, images, movies, and groups default to `true`, and other objects to `false`.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")
    line_type: LineType = Field(default_factory=lambda: LineType.model_validate("straight"), description="The routing style of the connection line.")
    tail: End = Field(description="The tail end of the connection line.")
    head: End = Field(description="The head end of the connection line.")
    stroke: Stroke = Field(default_factory=lambda: Stroke.model_validate({"line": {}}), description="The stroke used to draw the connection line.")
    opacity: float = Field(default=1, description="The opacity of the connection line, in the range `0` to `1`.")
    shadow: Override[Shadow] = Field(default_factory=Override.not_set, description="The shadow shown beneath the connection line.")
    reflection: Reflection | None = Field(default=None, description="The reflection shown for the connection line.")


@wire_union(
    "com.apple.apps.content-language.connection-line.line-type",
    version="1.0",
    cases=[
        ("corner", (1, 0), False),
        ("curved", (1, 0), False),
        ("straight", (1, 0), True),
    ],
)
class LineType(TaggedUnionModel):
    """How a connection line is routed between its ends.

A curved route whose control position lies almost on the line between the two ends is written back as `straight`, and that position is discarded."""
    corner: Position | None = Field(default=None, description="A route that makes right-angle turns and passes through this position, though not necessarily with a corner there. \n\nThe reader usually passes straight through a position partway between the ends.")
    curved: Position | None = Field(default=None, description="A route that bows between the ends and passes through this position.")
    straight: Literal[True] | None = Field(default=None, description="A route that makes a straight line between its ends.")

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_LineTypeCase, ...]: ...

        def union_primary(self) -> _LineTypeCase | None: ...

        def union_primary_name(self) -> Literal["corner", "curved", "straight"] | None: ...


@wire(
    "com.apple.apps.content-language.connection-line.end",
    version="1.0",
    fields=[
        ("end_point", (1, 0), "opt"),
        ("line_end", (1, 0), "def"),
        ("outset", (1, 0), "def"),
        ("anchor", (1, 0), "opt"),
    ],
)
class End(ObjectModel):
    """One end of a connection line.

`end_point` is effectively required: if a line's `tail` or `head` leaves it out, the line is dropped, even if that end supplies an `anchor`."""
    end_point: Position | None = Field(default=None, description="Where this end of the line stops, unless `anchor` attaches it to an object. Although it's marked optional, omitting it drops the whole line, even when `anchor` is present. For an attached end, give the object's center, so a curved line bows where its `line_type` puts it.")
    line_end: LineEnd = Field(default_factory=lambda: LineEnd.NONE, strict=False, description="The decoration shown at this end of the connection line, such as an arrowhead. The default is `none`.")
    outset: float = Field(default=0, description="When anchored, the size of the gap between the edge of the connected object and the start of the connection line, measured along the path in points. Defaults to 0, so the line begins at the edge of the connected object.")
    anchor: Anchor | None = Field(default=None, description="The object this end attaches to. If it's absent, the end is unattached and stays at `end_point`.")


@wire(
    "com.apple.apps.content-language.connection-line.end.anchor",
    version="1.0",
    fields=[
        ("object_id", (1, 0), "req"),
        ("magnet", (1, 0), "def"),
    ],
)
class Anchor(ObjectModel):
    """How one end of a connection line connects to another object.

The line stays connected as the other object moves. Anchors are resolved after the enclosing list of objects is read, so the target may appear after the line."""
    object_id: str = Field(description="The identifier of the object this end is connected to. The reference is resolved only among the connection line's siblings, not across the document, so the object must be a sibling of the connection line. It also can't be a connection line, a group, an audio clip, or a shape with a straight line path. If it can't be connected, this end is left unconnected at `ConnectionLine.End.end_point` and a warning is reported. An end connected to the object that fills the `title`, `body`, or `slide_number` placeholder, or a layout's `object` placeholder, is also left unconnected, but no warning is reported.")
    magnet: Magnet = Field(default_factory=lambda: Magnet.model_validate("center"), description="Which point on the connected object this end attaches to.")


@wire_union(
    "com.apple.apps.content-language.connection-line.end.anchor.magnet",
    version="1.0",
    cases=[
        ("center", (1, 0), True),
        ("east", (1, 0), True),
        ("edge", (1, 0), False),
        ("floating", (1, 0), False),
        ("north", (1, 0), True),
        ("south", (1, 0), True),
        ("west", (1, 0), True),
    ],
)
class Magnet(TaggedUnionModel):
    """The point on the anchored object that the line connects to.

Keynote connects every line the same way, whatever this value is: aimed at the object's center and stopped at its outline."""
    center: Literal[True] | None = Field(default=None, description="The object's center. It's the only value Keynote writes.")
    east: Literal[True] | None = Field(default=None, description="Not used.")
    edge: Position | None = Field(default=None, description="Not used. It stands for the line meeting the object's outline, at the position given here.")
    floating: Position | None = Field(default=None, description="Not used. It stands for the line meeting a point not tied to the object's outline, at the position given here.")
    north: Literal[True] | None = Field(default=None, description="Not used.")
    south: Literal[True] | None = Field(default=None, description="Not used.")
    west: Literal[True] | None = Field(default=None, description="Not used.")

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_MagnetCase, ...]: ...

        def union_primary(self) -> _MagnetCase | None: ...

        def union_primary_name(self) -> Literal["center", "east", "edge", "floating", "north", "south", "west"] | None: ...


@wire(
    "com.apple.apps.content-language.group",
    version="1.0",
    fields=[
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
        ("title", (1, 0), "opt"),
        ("title_is_positioned_on_top", (1, 0), "def"),
        ("caption", (1, 0), "opt"),
        ("children", (1, 0), "req"),
    ],
)
class Group(ObjectModel):
    """An ordered set of objects that behave as one when selected, moved, or transformed.

The group's position and size are those of the smallest rectangle enclosing its children, so the reader uses only the rotation and flip from its `geometry`."""
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=True, description="Whether the group's width-to-height ratio is locked when the group is resized. The lock doesn't constrain the `geometry` property. The default is `true`, and a group behaves as locked regardless of this value if any object inside it has a locked aspect ratio.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")
    title: Label | None = Field(default=None, description="The object's title.")
    title_is_positioned_on_top: bool = Field(default=True, description="When `true`, the title appears above the object; when `false`, the title appears below the object, above the caption if there is one. Defaults to `true`. Keynote ignores this when the object has none, or when it's hidden with `Label.is_visible` set to `false`; Keynote places a hidden title above the object, where it appears when it shows again.")
    caption: Label | None = Field(default=None, description="The object's caption, which Keynote always places below the object. If a caption is off, you still write it out with `Label.is_visible` set to `false`, so having a value doesn't mean the caption shows.")
    children: list[CanvasObject] = Field(min_length=1, description="The objects in this group, in order from rearmost to frontmost; at least one is required. A child that can't be read is dropped and its siblings are kept. A group with a single child is written back as that single object, and a group with no valid children is skipped. On a slide or slide layout, a group that's left with a single child when it's read is ungrouped too, along with every group that contains it. A group removed this way, on writing or on reading, loses its own `title`, `caption`, `description`, and `aspect_ratio_locked`.")


@wire(
    "com.apple.apps.content-language.image",
    version="1.0",
    fields=[
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
        ("title", (1, 0), "opt"),
        ("title_is_positioned_on_top", (1, 0), "def"),
        ("caption", (1, 0), "opt"),
        ("resource", (1, 0), "req"),
        ("mask", (1, 0), "opt"),
        ("instant_alpha_path", (1, 0), "opt"),
        ("stroke", (1, 0), "def"),
        ("opacity", (1, 0), "def"),
        ("shadow", (1, 0), "ovr"),
        ("reflection", (1, 0), "opt"),
        ("is_placeholder", (1, 0), "def"),
        ("was_media_replaced", (1, 0), "def"),
    ],
)
class Image(ObjectModel):
    """A picture defined by a resource with optional styling.

When `geometry` is absent, the reader places the image at the natural size of `resource`. When Keynote exports a presentation, it writes an object the format has no type for as an image. A 3D object, a drawing, an image gallery, a web video, a live video, or a comment on a slide becomes a picture of the object as it appears, with its rotation, flip, title, and caption drawn in, so the image has no `title` or `caption`, and its `geometry` is an unrotated rectangle enclosing the whole picture, including any shadow or reflection. Keynote also writes such an image without a `description`, so the object's accessibility description is lost. A comment appears in its image only if comments are shown when someone exports the presentation; otherwise the image is empty."""
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=True, description="Whether the image's width-to-height ratio is locked when the image is resized. The lock doesn't constrain the `geometry` property. The default is `true`.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")
    title: Label | None = Field(default=None, description="The object's title.")
    title_is_positioned_on_top: bool = Field(default=True, description="When `true`, the title appears above the object; when `false`, the title appears below the object, above the caption if there is one. Defaults to `true`. Keynote ignores this when the object has none, or when it's hidden with `Label.is_visible` set to `false`; Keynote places a hidden title above the object, where it appears when it shows again.")
    caption: Label | None = Field(default=None, description="The object's caption, which Keynote always places below the object. If a caption is off, you still write it out with `Label.is_visible` set to `false`, so having a value doesn't mean the caption shows.")
    resource: Resource = Field(description="The resource containing the image's data. The resource data must decode to a single-frame image; use `Movie` for multi-frame images. A multi-frame animated image, such as an animated GIF, is rejected and the object is dropped. When Keynote writes an image changed with Adjust Image, the resource holds the image with those changes applied, not the original.")
    mask: Mask | None = Field(default=None, description="A cropping mask that is applied to the image before it's shown. The mask's `geometry` is the visible frame, while the image's own `geometry` places the image resource. Decorations are shown relative to the intersection of the mask and the image. If absent, the image isn't cropped.")
    instant_alpha_path: InstantAlphaPath | None = Field(default=None, description="A cropping path applied to the image before it's shown, removing the image's background.")
    stroke: Stroke = Field(default_factory=lambda: Stroke.model_validate("empty"), description="A border stroke drawn around the image. Defaults to no border.")
    opacity: float = Field(default=1, description="The image's opacity, in the range `0` to `1`.")
    shadow: Override[Shadow] = Field(default_factory=Override.not_set, description="The shadow shown beneath the image.")
    reflection: Reflection | None = Field(default=None, description="The reflection shown for the image.")
    is_placeholder: bool = Field(default=False, description="Whether this image is a media placeholder, meant to be replaced with another image. When `false`, `was_media_replaced` is ignored and treated as `false`.")
    was_media_replaced: bool = Field(default=False, description="If this image is a placeholder, whether the resource in it was replaced.")


@wire(
    "com.apple.apps.content-language.image.mask",
    version="1.0",
    fields=[
        ("geometry", (1, 0), "opt"),
        ("path", (1, 0), "opt"),
    ],
)
class Mask(ObjectModel):
    """The crop applied to an image, clipping the resource to a path within the mask's own geometry.

The part outside the crop is retained in the file rather than trimmed away. A mask whose path encloses no area would hide the image completely, so it's discarded when it's read, and the image isn't cropped."""
    geometry: Geometry | None = Field(default=None, description="The geometry of the frame used to crop the image's resource, in the same coordinate space as the image's own `geometry`. Either this or `path` must be present.")
    path: Path | None = Field(default=None, description="The path used to crop the image's resource, anchored within `geometry` if present. Either this or `geometry` must be present; if absent and `geometry` is used, the path is assumed to be rectangular.")


@wire(
    "com.apple.apps.content-language.image.instant-alpha-path",
    version="1.0",
    fields=[
        ("path", (1, 0), "req"),
        ("size", (1, 0), "opt"),
    ],
)
class InstantAlphaPath(ObjectModel):
    """A masking path applied to an image to clip out its background, with only the area it encloses shown.

A `path` that comes out empty, encloses no area, or lies outside the image is discarded, and the image keeps its background."""
    path: str = Field(description="The outline of the visible area, in the syntax of an SVG `<path>` element's `d` attribute, with these differences: only the moveto (`M`), lineto (`L`), cubic and quadratic curveto (`C` and `Q`), and closepath (`Z`) commands are read; every segment must have its own command letter; separators must be spaces; and a lowercase command is read as absolute rather than relative. The value must begin with a moveto command. Reading stops at the first token that can't be read; the outline up to there is kept, including the interrupted segment, with its missing numbers taken as 0.")
    size: Size | None = Field(default=None, description="If present, `path` is treated as relative to a rectangle at the origin with this size, and then stretched to cover the natural size of the image. If absent, it's assumed to equal the natural size of the image.")


@wire(
    "com.apple.apps.content-language.label",
    version="1.0",
    fields=[
        ("layout_properties", (1, 0), "opt"),
        ("paragraph_properties", (1, 0), "opt"),
        ("text", (1, 0), "opt"),
        ("is_visible", (1, 0), "def"),
    ],
)
class Label(ObjectModel):
    """Styled text that the reader uses as a title or caption on an object."""
    layout_properties: LayoutProperties | None = Field(default=None, description="The layout overrides, such as insets and columns, for the label's text. If it's absent, the theme's text layout settings are used.")
    paragraph_properties: ParagraphProperties | None = Field(default=None, description="The paragraph-level style, such as alignment and spacing, for the label's text. If it's absent, the theme's paragraph style is used.")
    text: Text | None = Field(default=None, description="The text of the title or caption.")
    is_visible: bool = Field(default=True, description="Whether the title or caption is visible. Defaults to `true`; when `false`, the title or caption is hidden but its text and styling are preserved.")


@wire(
    "com.apple.apps.content-language.movie",
    version="1.0",
    fields=[
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
        ("title", (1, 0), "opt"),
        ("title_is_positioned_on_top", (1, 0), "def"),
        ("caption", (1, 0), "opt"),
        ("resource", (1, 0), "req"),
        ("poster_image", (1, 0), "opt"),
        ("poster_time", (1, 0), "def"),
        ("playback_options", (1, 0), "req"),
        ("stroke", (1, 0), "def"),
        ("opacity", (1, 0), "def"),
        ("shadow", (1, 0), "ovr"),
        ("reflection", (1, 0), "opt"),
    ],
)
class Movie(ObjectModel):
    """A movie or animated image defined by a resource with optional styling.

When `geometry` is omitted, the object takes the resource's natural size, falling back to 640 × 480 points when the reader cannot measure that size. Placed inline in the text of a text box or shape, an unplayable movie removes that whole text box or shape, including all of its text; in a slide's presenter notes, it stops the document from loading."""
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=True, description="Whether the movie's width-to-height ratio is locked when the movie is resized. The lock doesn't constrain the `geometry` property. The default is `true`.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")
    title: Label | None = Field(default=None, description="The object's title.")
    title_is_positioned_on_top: bool = Field(default=True, description="When `true`, the title appears above the object; when `false`, the title appears below the object, above the caption if there is one. Defaults to `true`. Keynote ignores this when the object has none, or when it's hidden with `Label.is_visible` set to `false`; Keynote places a hidden title above the object, where it appears when it shows again.")
    caption: Label | None = Field(default=None, description="The object's caption, which Keynote always places below the object. If a caption is off, you still write it out with `Label.is_visible` set to `false`, so having a value doesn't mean the caption shows.")
    resource: Resource = Field(description="The resource containing the movie's data. The resource must decode to a multi-frame animated image or to a movie with a video track, playable on the device where the file is imported; if not, the object is skipped.")
    poster_image: Resource | None = Field(default=None, description="The resource containing the data for the movie's poster image. The poster image is shown when the movie isn't playing; this resource is used only as a fallback when a poster image can't be generated from `poster_time`.")
    poster_time: Duration = Field(default_factory=lambda: Duration.model_validate({"seconds": 0}), description="A time, limited to the movie's duration, used to determine which frame of the movie is shown when the movie isn't playing. The default is 0, the first frame, which is also used for a negative or otherwise unusable time.")
    playback_options: PlaybackOptions = Field(description="Playback settings for the movie, such as volume, start and end trim times, looping, and whether playback continues across slides.")
    stroke: Stroke = Field(default_factory=lambda: Stroke.model_validate("empty"), description="The border stroke drawn around the movie. The default is no border.")
    opacity: float = Field(default=1, description="The opacity value of the movie, in the range `0` to `1`.")
    shadow: Override[Shadow] = Field(default_factory=Override.not_set, description="The shadow shown beneath the movie.")
    reflection: Reflection | None = Field(default=None, description="The reflection shown for the movie.")


@wire(
    "com.apple.apps.content-language.placeable-title-owning-generic",
    version="1.0",
    fields=[
        ("title", (1, 0), "opt"),
        ("title_is_positioned_on_top", (1, 0), "def"),
    ],
)
class GenericPlaceableTitleOwning(ObjectModel):
    """A stand-in for an object with a free-standing title label, when the reader doesn't recognize its kind.

Every set of shared properties has one, to stand in for an object when the reader doesn't recognize its kind. Nothing in the format has the type `PlaceableTitleOwning`, though, so this object never appears in a document; its properties appear only as part of the types that adopt `PlaceableTitleOwning`."""
    title: Label | None = Field(default=None, description="The object's title.")
    title_is_positioned_on_top: bool = Field(default=True, description="When `true`, the title appears above the object; when `false`, the title appears below the object, above the caption if there is one. Defaults to `true`. Keynote ignores this when the object has none, or when it's hidden with `Label.is_visible` set to `false`; Keynote places a hidden title above the object, where it appears when it shows again.")


@wire_union(
    "com.apple.apps.content-language.placeable-title-owning",
    version="1.0",
    cases=[
        ("genericPlaceableTitleOwning", (1, 0), False),
    ],
)
class PlaceableTitleOwning(TaggedUnionModel):
    """The properties for defining a title an object can display, positioned above or below the object.

They extend `TitleOwning` and are used by objects whose title is a free-standing label."""
    genericPlaceableTitleOwning: GenericPlaceableTitleOwning | None = None

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_PlaceableTitleOwningCase, ...]: ...

        def union_primary(self) -> _PlaceableTitleOwningCase | None: ...

        def union_primary_name(self) -> Literal["genericPlaceableTitleOwning"] | None: ...


@wire(
    "com.apple.apps.content-language.shape",
    version="1.0",
    fields=[
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
        ("title", (1, 0), "opt"),
        ("title_is_positioned_on_top", (1, 0), "def"),
        ("caption", (1, 0), "opt"),
        ("path", (1, 0), "opt"),
        ("tail", (1, 0), "def"),
        ("head", (1, 0), "def"),
        ("fill", (1, 0), "opt"),
        ("stroke", (1, 0), "def"),
        ("opacity", (1, 0), "def"),
        ("shadow", (1, 0), "ovr"),
        ("reflection", (1, 0), "opt"),
        ("layout_properties", (1, 0), "opt"),
        ("paragraph_properties", (1, 0), "opt"),
        ("text", (1, 0), "opt"),
    ],
)
class Shape(ObjectModel):
    """A path with a fill and a stroke.

When `geometry` is absent, the geometry defaults to the smallest rectangle that encloses the path. Shapes can have an open or a closed path; a path is _open_ when it has a single subpath, no `closepath` command, and ends that don't meet. Open shapes can have endpoints, `head` and `tail`. Keynote reads a `path` that is a single, straight, open segment as a line and takes its styling from the line presets. A shape with either `Geometry.width_valid` or `Geometry.height_valid` set to `false` becomes an auto-sizing text box. Paths that aren't straight lines can contain text that appears inside the shape."""
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=False, description="A Boolean value that indicates whether the object's width-to-height ratio is locked when the object resizes. The lock doesn't constrain the `geometry` property. If this property is absent, images, movies, and groups default to `true`, and other objects to `false`.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")
    title: Label | None = Field(default=None, description="The object's title.")
    title_is_positioned_on_top: bool = Field(default=True, description="When `true`, the title appears above the object; when `false`, the title appears below the object, above the caption if there is one. Defaults to `true`. Keynote ignores this when the object has none, or when it's hidden with `Label.is_visible` set to `false`; Keynote places a hidden title above the object, where it appears when it shows again.")
    caption: Label | None = Field(default=None, description="The object's caption, which Keynote always places below the object. If a caption is off, you still write it out with `Label.is_visible` set to `false`, so having a value doesn't mean the caption shows.")
    path: Path | None = Field(default=None, description="The path that forms the shape's outline. Either this value or `geometry` must be present. If absent, Keynote assume this shape to be a rectangle the same size as `geometry`.")
    tail: LineEnd = Field(default_factory=lambda: LineEnd.NONE, strict=False, description="The tail end of the shape, which is a line-end decoration, such as an arrowhead, at the first point of the shape's `path`. Keynote only display it for an open path. The default is `none`.")
    head: LineEnd = Field(default_factory=lambda: LineEnd.NONE, strict=False, description="The head end of the shape, which is a line-end decoration, such as an arrowhead, at the last point of the shape's `path`. Keynote only displays it for an open path. The default is `none`.")
    fill: Fill | None = Field(default=None, description="The fill of the shape's interior. If absent, it uses the the fill from the shape's preset style.")
    stroke: Stroke = Field(default_factory=lambda: Stroke.model_validate({"line": {}}), description="The stroke that appears along the shape's path.")
    opacity: float = Field(default=1, description="The shape's opacity, in the range `0` to `1`.")
    shadow: Override[Shadow] = Field(default_factory=Override.not_set, description="The shadow beneath the shape.")
    reflection: Reflection | None = Field(default=None, description="The reflection for the shape.")
    layout_properties: LayoutProperties | None = Field(default=None, description="Layout overrides, such as insets and columns, for the shape's text.")
    paragraph_properties: ParagraphProperties | None = Field(default=None, description="Paragraph-level style, such as alignment and spacing, for the shape's text.")
    text: Text | None = Field(default=None, description="The text inside the shape.")


@wire(
    "com.apple.apps.content-language.table",
    version="1.0",
    fields=[
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
        ("title", (1, 0), "opt"),
        ("caption", (1, 0), "opt"),
        ("table_name_border_enabled", (1, 0), "def"),
        ("number_of_columns", (1, 0), "req"),
        ("number_of_rows", (1, 0), "req"),
        ("number_of_header_rows", (1, 0), "def"),
        ("number_of_header_columns", (1, 0), "def"),
        ("number_of_footer_rows", (1, 0), "def"),
        ("default_column_width", (1, 0), "def"),
        ("default_row_height", (1, 0), "def"),
        ("visual_properties", (1, 0), "opt"),
        ("column_headers", (1, 0), "opt"),
        ("content", (1, 0), "opt"),
        ("merges", (1, 0), "opt"),
        ("conditional_style_sets", (1, 0), "opt"),
        ("custom_formats", (1, 0), "opt"),
        ("transformation", (1, 0), "opt"),
    ],
)
class Table(ObjectModel):
    """A table of cells, nested two levels deep.

`content` holds the table's rows, ordered top to bottom, and each row's `cells` holds that row's cells, ordered left to right. The first `number_of_header_rows` rows are header rows, and the last `number_of_footer_rows` are footer rows. Rows and cells that carry nothing may be omitted, so `Table.Row.row_index` and `Table.Cell.column_index` mark where a run resumes after a gap. On a slide, a table whose `title` is absent, has no text, or reads `Unnamed` or `Unnamed Table` gets a default name such as Table `1` as its built-in title, and Keynote renames tables there that share a name the same way until each has its own; which of them keeps the name isn't defined, and Keynote reports no warning."""
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=False, description="A Boolean value that indicates whether the object's width-to-height ratio is locked when the object resizes. The lock doesn't constrain the `geometry` property. If this property is absent, images, movies, and groups default to `true`, and other objects to `false`.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")
    title: Label | None = Field(default=None, description="The object's title.")
    caption: Label | None = Field(default=None, description="The object's caption, which Keynote always places below the object. If a caption is off, you still write it out with `Label.is_visible` set to `false`, so having a value doesn't mean the caption shows.")
    table_name_border_enabled: bool = Field(default=False, description="Whether a border is drawn around the table's name (title) box. The border uses the header row's border stroke, `Table.VisualProperties.header_row_stroke_properties.border_stroke`.")
    number_of_columns: int = Field(description="The total number of columns in the table, including header, body, and hidden columns. A count below 1, or above the largest supported column count, is adjusted to the nearest supported count rather than rejected.")
    number_of_rows: int = Field(description="The total number of rows in the table, including header, body, footer, hidden, and filtered rows. A count below 1, or above the largest supported row count, is adjusted to the nearest supported count rather than rejected.")
    number_of_header_rows: int = Field(default=0, description="The number of header rows at the top of the table, which are styled separately from body rows and typically contain column titles. A negative count, or one greater than `number_of_rows`, is adjusted to fit rather than rejected.")
    number_of_header_columns: int = Field(default=0, description="The number of header columns at the leading edge of the table, which are styled separately from body columns and typically contain row labels. A negative count, or one greater than `number_of_columns`, is adjusted to fit rather than rejected.")
    number_of_footer_rows: int = Field(default=0, description="The number of footer rows at the bottom of the table, which are styled separately from body rows and typically contain totals or summaries. A negative count is treated as zero, and if `number_of_header_rows` plus `number_of_footer_rows` would exceed `number_of_rows`, the footer count is reduced to fit rather than rejected.")
    default_column_width: float = Field(default=98, description="The default column width, in points, which must be greater than 0. It's used for any column that doesn't override it with `Table.ColumnHeader.column_width`.")
    default_row_height: float = Field(default=20, description="The default row height, in points, which must be greater than 0. It's used for any row that doesn't override it with `Table.Row.row_height`.")
    visual_properties: VisualProperties | None = Field(default=None, description="The default styles for the whole table. These are table-level properties, such as strokes and alternating row fills, plus default cell and text properties for each region (body, header rows, header columns, and footer rows). Cell- and column-level overrides take precedence over these defaults.")
    column_headers: list[ColumnHeader] | None = Field(default=None, description="The metadata for each column, including its stable column ID, its display title, its default cell format, style, and text, and an optional column width override. It provides the column identity that formula references and merges use. There's one entry for each column, in left-to-right order, so an entry's position here is that column's position in every row's `cells`.")
    content: list[Row] | None = Field(default=None, description="The table's rows as displayed, including header and footer rows; trailing blank rows can be omitted. Hidden and filtered rows are included, marked by their `Table.Row.visibility_state`.")
    merges: list[CellRange] | None = Field(default=None, description="The cell ranges that are each visually merged into a single cell. The content is in the top-left cell, and the other cells in the range are blank. Each range names its corners by this table's row and column IDs. If a corner names a row or column the table doesn't have, or a range's end comes before its start, Keynote drops the whole table, with a warning, instead of loading the table without that merge.")
    conditional_style_sets: list[ConditionalStyleSet] | None = Field(default=None, description="The shared sets of conditional highlighting rules. Cells reference a set by ID in `Table.Cell.conditional_style_set_identifier`, so the same rules can be reused across many cells without duplication.")
    custom_formats: list[CustomFormat] | None = Field(default=None, description="The shared custom-format definitions. Cells whose `cell_format.format_type` is `custom` reference one of these by ID in `cell_format.custom_format_identifier`, so the same format definition can be reused across many cells without duplication.")
    transformation: TransformationInfo | None = Field(default=None, description="The filter and sort rules applied to this table, in `filter_set` and `sort`; `content` holds the result.")


@wire(
    "com.apple.apps.content-language.table.column-header",
    version="1.0",
    fields=[
        ("column_identifier", (1, 0), "opt"),
        ("title", (1, 0), "opt"),
        ("cell_format", (1, 0), "opt"),
        ("column_width", (1, 0), "opt"),
        ("cell_properties", (1, 0), "opt"),
        ("text_properties", (1, 0), "opt"),
        ("visibility_state", (1, 0), "def"),
        ("kind", (1, 0), "def"),
    ],
)
class ColumnHeader(ObjectModel):
    """The metadata for a column in a table.

Its default formatting and styling apply to the body cells in the column."""
    column_identifier: str | None = Field(default=None, description="The column's stable identifier. Formula references (`Table.Cell.Formula.CellReference.start_column_identifier` and `Table.Cell.Formula.CellReference.end_column_identifier`) and merge ranges use it, so inserting or removing columns doesn't invalidate references.")
    title: str | None = Field(default=None, description="The column's display title. By default, it mirrors the value of the column's first header cell; for a column with no header or a blank header, a generic name (for example, `Column C`) may be used.")
    cell_format: CellFormat | None = Field(default=None, description="The default data format (such as number, currency, or date) for body cells in the column. Header and footer rows aren't affected. `Table.Cell.cell_format` overrides it for an individual cell.")
    column_width: float | None = Field(default=None, description="The width of the column, in points, which must be greater than 0. If it's present, it overrides `Table.default_column_width` for this column only.")
    cell_properties: CellProperties | None = Field(default=None, description="The default cell styling (fill, alignment, padding, and wrap) for body cells in the column. `Table.Cell.cell_properties` overrides it for an individual cell.")
    text_properties: ParagraphProperties | None = Field(default=None, description="The default paragraph and text style for body cells in the column. `Table.Cell.text_properties` overrides it for an individual cell.")
    visibility_state: TableColumnHeaderVisibilityState = Field(default_factory=lambda: TableColumnHeaderVisibilityState.VISIBLE, strict=False, description="Whether this column is visible. Hidden columns are still counted by `number_of_columns`.")
    kind: TableColumnHeaderKind = Field(default_factory=lambda: TableColumnHeaderKind.model_validate("body"), description="The column's structural role: `body` for an ordinary data column. The other roles (group label, subtotal, and grand total) are reserved for pivot tables, which version 1.0 doesn't support.")


class TableColumnHeaderVisibilityState(str, Enum):
    """A string that indicates whether a column is visible.

    user_hidden — The user hid the with the Hide Column command.
    visible — The column is shown.
    """
    USER_HIDDEN = "user_hidden"
    VISIBLE = "visible"


@wire_union(
    "com.apple.apps.content-language.table.column-header.kind",
    version="1.0",
    cases=[
        ("body", (1, 0), True),
        ("grand_total", (1, 0), True),
        ("group_label", (1, 0), False),
        ("group_subtotal", (1, 0), True),
    ],
)
class TableColumnHeaderKind(TaggedUnionModel):
    """The structural role of a column.

The default is `body`; the other cases are reserved for pivot tables, which version 1.0 doesn't support."""
    body: Literal[True] | None = Field(default=None, description="An ordinary data column.")
    grand_total: Literal[True] | None = Field(default=None, description="A pivot table's grand-total column, which version 1.0 doesn't support.")
    group_label: TableColumnHeaderGroupLabel | None = Field(default=None, description="A pivot table's group-label column, which version 1.0 doesn't support. Its `GroupLabel` value holds the grouping row identifier and the group value.")
    group_subtotal: Literal[True] | None = Field(default=None, description="A pivot table's subtotal column for one group, which version 1.0 doesn't support.")

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_TableColumnHeaderKindCase, ...]: ...

        def union_primary(self) -> _TableColumnHeaderKindCase | None: ...

        def union_primary_name(self) -> Literal["body", "grand_total", "group_label", "group_subtotal"] | None: ...


@wire(
    "com.apple.apps.content-language.table.column-header.group-label",
    version="1.0",
    fields=[
        ("grouping_row_identifier", (1, 0), "req"),
        ("group_value", (1, 0), "req"),
        ("is_collapsed", (1, 0), "def"),
        ("nesting_level", (1, 0), "def"),
    ],
)
class TableColumnHeaderGroupLabel(ObjectModel):
    """The group that a pivot table's group-label column stands for.

It's reserved for pivot tables, which version 1.0 doesn't support. A column whose kind is `group_label` carries it. It identifies the row in the source data being grouped on and the group the column represents."""
    grouping_row_identifier: str = Field(description="The stable `Table.Row.row_identifier` of the row in `transformation.base_table.content` whose value drives this grouping along the column axis.")
    group_value: str = Field(description="The raw lookup key for this group (for example, `West`). It's distinct from any formatted display string in the column header cell: the formatted form is in the corresponding cells, and this is the key used for grouping and sorting, and it identifies the group.")
    is_collapsed: bool = Field(default=False, description="Whether this group is collapsed.")
    nesting_level: int = Field(default=0, description="The zero-based nesting depth among the column-axis groupings. A value of `0` is the outermost grouping, and deeper levels nest inside it.")


@wire(
    "com.apple.apps.content-language.table.row",
    version="1.0",
    fields=[
        ("row_index", (1, 0), "opt"),
        ("row_identifier", (1, 0), "opt"),
        ("row_height", (1, 0), "opt"),
        ("cell_properties", (1, 0), "opt"),
        ("text_properties", (1, 0), "opt"),
        ("cells", (1, 0), "opt"),
        ("visibility_state", (1, 0), "def"),
        ("kind", (1, 0), "def"),
    ],
)
class Row(ObjectModel):
    """A row in a table.

It holds the row's cells, optional row-level defaults (`row_height`, `cell_properties`, and `text_properties`), and the stable `row_identifier` that formula references and merges use."""
    row_index: int | None = Field(default=None, description="The zero-based position of the row in the table, from `0` through `Table.number_of_rows` minus 1. It's required only in a sparse table, to mark the first non-blank row after a gap; the rows that follow are positioned sequentially.")
    row_identifier: str | None = Field(default=None, description="The row's stable identifier. Formula references (`Table.Cell.Formula.CellReference.start_row_identifier` and `Table.Cell.Formula.CellReference.end_row_identifier`) and merge ranges use it, so references survive row insertions and deletions.")
    row_height: float | None = Field(default=None, description="The height of the row, in points, which must be greater than 0. If it's present, it overrides `Table.default_row_height` for this row only.")
    cell_properties: CellProperties | None = Field(default=None, description="The default cell styling for cells in the row. It overrides the table and column defaults, and `Table.Cell.cell_properties` overrides it for an individual cell.")
    text_properties: ParagraphProperties | None = Field(default=None, description="The default paragraph and text style for cells in the row. It overrides the table and column defaults, and `Table.Cell.text_properties` overrides it for an individual cell.")
    cells: list[Cell] | None = Field(default=None, description="The cells in the row, ordered from left to right. The list is sparse: trailing blank cells can be omitted, and a gap in the middle is marked by `Table.Cell.column_index` on the next non-blank cell.")
    visibility_state: TableRowVisibilityState = Field(default_factory=lambda: TableRowVisibilityState.VISIBLE, strict=False, description="Whether this row is visible, and if not, whether the user hid it or the active filter excluded it. Rows that aren't visible remain in `content`.")
    kind: TableRowKind = Field(default_factory=lambda: TableRowKind.model_validate("body"), description="The row's structural role: `body` for an ordinary data row. The other roles (group label, subtotal, and grand total) are reserved for categorized and pivot tables, which version 1.0 doesn't support.")


class TableRowVisibilityState(str, Enum):
    """Whether a row is visible, and if not, whether it was hidden explicitly or excluded by the active filter.

    filtered — The row didn't pass the active filter rules in `transformation.filter_set`. Disabling the filter or removing the failing rule makes the row visible again.
    user_hidden — The user hid the row with the Hide Row command.
    visible — The row is shown.
    """
    FILTERED = "filtered"
    USER_HIDDEN = "user_hidden"
    VISIBLE = "visible"


@wire_union(
    "com.apple.apps.content-language.table.row.kind",
    version="1.0",
    cases=[
        ("body", (1, 0), True),
        ("grand_total", (1, 0), True),
        ("group_label", (1, 0), False),
        ("group_subtotal", (1, 0), True),
    ],
)
class TableRowKind(TaggedUnionModel):
    """The structural role of a row.

The default is `body`; the other cases are reserved for categorized and pivot tables, which version 1.0 doesn't support."""
    body: Literal[True] | None = Field(default=None, description="An ordinary data row.")
    grand_total: Literal[True] | None = Field(default=None, description="A grand-total row in a categorized or pivot table, which version 1.0 doesn't support.")
    group_label: TableRowGroupLabel | None = Field(default=None, description="A category header row, or a pivot table's row-axis group label; version 1.0 supports neither. Its `GroupLabel` value identifies the grouping column and the group the row represents.")
    group_subtotal: Literal[True] | None = Field(default=None, description="A subtotal row for one group in a categorized or pivot table, which version 1.0 doesn't support.")

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_TableRowKindCase, ...]: ...

        def union_primary(self) -> _TableRowKindCase | None: ...

        def union_primary_name(self) -> Literal["body", "grand_total", "group_label", "group_subtotal"] | None: ...


@wire(
    "com.apple.apps.content-language.table.row.group-label",
    version="1.0",
    fields=[
        ("grouping_column_identifier", (1, 0), "req"),
        ("group_value", (1, 0), "req"),
        ("is_collapsed", (1, 0), "def"),
        ("nesting_level", (1, 0), "def"),
    ],
)
class TableRowGroupLabel(ObjectModel):
    """The group that a category header row, or a pivot table's row-axis group label, stands for.

It's reserved for categorized and pivot tables, which version 1.0 doesn't support. A row whose kind is `group_label` carries it. It identifies the column being grouped on and the group the row represents."""
    grouping_column_identifier: str = Field(description="The stable `Table.ColumnHeader.column_identifier` of the column in `transformation.base_table.column_headers` whose value drives this grouping.")
    group_value: str = Field(description="The raw lookup key for this group (for example, `West`). The formatted form is in the `value` of the row's first cell; this is the key used for grouping and sorting, and it identifies the group.")
    is_collapsed: bool = Field(default=False, description="Whether this group is collapsed.")
    nesting_level: int = Field(default=0, description="The zero-based nesting depth among the row-axis groupings. A value of `0` is the outermost grouping, and deeper levels nest inside it.")


@wire(
    "com.apple.apps.content-language.table.cell-properties",
    version="1.0",
    fields=[
        ("text_wrap", (1, 0), "opt"),
        ("vertical_alignment", (1, 0), "opt"),
        ("padding", (1, 0), "opt"),
        ("fill", (1, 0), "ovr"),
    ],
)
class CellProperties(ObjectModel):
    """The styling of a table cell, other than its strokes.

Strokes are kept separately, in `Table.Cell.Strokes`, so individual edges can be overridden."""
    text_wrap: bool | None = Field(default=None, description="Whether text that exceeds the column width wraps to more lines (`true`) or clip (`false`).")
    vertical_alignment: VerticalAlignmentType | None = Field(default=None, strict=False, description="The vertical alignment of content in the cell (top, middle, or bottom).")
    padding: Insets | None = Field(default=None, description="The inset of the cell's content from the cell's edges, in points (top, leading, bottom, and trailing).")
    fill: Override[Fill] = Field(default_factory=Override.not_set, description="The cell's background fill (color, gradient, or image). If it's absent, the fill is inherited; an explicit `null` gives the cell no fill, which isn't the same as a fill at 0% opacity.")


@wire(
    "com.apple.apps.content-language.table.cell",
    version="1.0",
    fields=[
        ("value", (1, 0), "def"),
        ("unformatted_value", (1, 0), "opt"),
        ("cell_format", (1, 0), "opt"),
        ("cell_properties", (1, 0), "opt"),
        ("text_properties", (1, 0), "opt"),
        ("strokes", (1, 0), "opt"),
        ("anchored_objects", (1, 0), "opt"),
        ("column_index", (1, 0), "opt"),
        ("formula", (1, 0), "opt"),
        ("spill_range", (1, 0), "opt"),
        ("conditional_style_set_identifier", (1, 0), "opt"),
    ],
)
class Cell(ObjectModel):
    """A cell in a table.

Its value is carried as a formatted display string in `value`, a typed underlying value in `unformatted_value`, or both. It can also have a formula and per-cell style and format overrides."""
    value: str = Field(default="", description="The cell's content as a pre-formatted string (for example, `$1,234.56`, `12/25/2024`, or `42%`). It's the simplest representation, intended for readers that render the cell as plain text. For the typed value, use `unformatted_value`.")
    unformatted_value: UnformattedValue | None = Field(default=None, description="The cell's typed underlying value (`number`, `text`, `date`, `boolean`, or `rich_text`), which lets a reader recover the value's type when `value` is only the formatted string. It's absent when the value has no typed form: a formula that evaluated to an error arrives with `formula` set and an empty `value`, so an absent typed value doesn't mean the cell is empty.")
    cell_format: CellFormat | None = Field(default=None, description="The cell's value-formatting override. If it's set, it overrides the column-level default in `Table.ColumnHeader.cell_format` for this cell only.")
    cell_properties: CellProperties | None = Field(default=None, description="The cell's styling override (fill, alignment, padding, and wrap). If it's set, it overrides the table-, column-, and row-level defaults for this cell only.")
    text_properties: ParagraphProperties | None = Field(default=None, description="The cell's paragraph and text style override (font, size, color, and alignment). If it's set, it overrides the table-, column-, and row-level defaults for this cell only.")
    strokes: Strokes | None = Field(default=None, description="The cell's stroke overrides for each edge (top, bottom, left, and right). An omitted edge falls back to the table-level stroke for the cell's region.")
    anchored_objects: list[str] | None = Field(default=None, description="The IDs of the objects, such as shapes and images, that are anchored to the cell. Keynote ignores them.")
    column_index: int | None = Field(default=None, description="The zero-based column position of the cell in its row, from `0` through `Table.number_of_columns` minus 1. It's only required in a sparse row, to mark the first non-blank cell after a gap; the cells that follow are positioned sequentially.")
    formula: Formula | None = Field(default=None, description="The formula that produces the cell's value. If it's present, `value` and `unformatted_value` contain the most recently computed result of evaluating the formula.")
    spill_range: RowColumnIdRange | None = Field(default=None, description="The range that the cell's `formula` populates when it spills, with this cell at its top left. It's only meaningful for a cell whose formula spills, and it's absent when the spill is blocked. The other cells in the range hold the last spilled result and are replaced on re-evaluation. A corner ID matching no row or column of this table is ignored without a warning, and the cells it would have covered keep the values written for them.")
    conditional_style_set_identifier: str | None = Field(default=None, description="The ID of a shared conditional style set, declared in `Table.conditional_style_sets`, that applies to the cell. The first rule in the set whose condition is true for this cell determines its conditional styling. An identifier matching no set is ignored without a warning, and the cell keeps its regular styling.")


@wire_union(
    "com.apple.apps.content-language.table.cell.unformatted-value",
    version="1.0",
    cases=[
        ("boolean", (1, 0), False),
        ("date", (1, 0), False),
        ("number", (1, 0), False),
        ("rich_text", (1, 0), False),
        ("text", (1, 0), False),
    ],
)
class UnformattedValue(TaggedUnionModel):
    """The unformatted value of a cell, which can be one of several data types."""
    boolean: bool | None = Field(default=None, description="A Boolean value of true or false.")
    date: Date | None = Field(default=None, description="A date value, a time value, or both.")
    number: float | None = Field(default=None, description="A numeric value that's an integer or decimal. \n\nThe cell's `value` property carries the formatted string. A duration cell's number is a count of seconds, so check `cell_format` before using it in arithmetic.")
    rich_text: Text | None = Field(default=None, description="Rich text with styling, such as paragraph and character styles.")
    text: str | None = Field(default=None, description="A plain text value with no styling. \n\nFor styled text, use `rich_text` instead.")

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_UnformattedValueCase, ...]: ...

        def union_primary(self) -> _UnformattedValueCase | None: ...

        def union_primary_name(self) -> Literal["boolean", "date", "number", "rich_text", "text"] | None: ...


@wire_union(
    "com.apple.apps.content-language.table.cell.formula",
    version="1.0",
    cases=[
        ("display_string", (1, 0), False),
        ("id_based", (1, 0), False),
    ],
)
class Formula(TaggedUnionModel):
    """The form in which a cell's formula is carried.

The `display_string` form is the one to write: it's the only one a reader resolves in version 1.0. An `id_based` formula is accepted, but its references aren't substituted into the expression, so it reaches the reader with its placeholder tokens intact."""
    display_string: str | None = Field(default=None, description="Formula text in A1 notation.\n\n Keynote writes this text in A1 notation, for example, `=SUM(A1:A10)`, `=B$1*$C2`, where coordinates count from the table's top-left cell, header rows and columns included, and `$` pins a row or column. A reference into another table is prefixed with that table's name (`Table 2::A1`). Keynote writes function names and the argument and decimal separators, among other things, in the presentation's language and region, and reads them in the language and region the presentation opens with, usually the device's; English function names are also accepted. A formula that doesn't parse is dropped without a warning and the cell keeps the value given for it, while one that names an unknown function is kept and the cell shows an error.")
    id_based: IdBasedFormula | None = Field(default=None, description="A formula expression whose cell references are carried separately as row and column IDs. \n\n This expression means they survive insertions and deletions of rows or columns. A reader in version 1.0 leaves the expression's placeholder tokens unsubstituted, so a formula written this way arrives with the tokens still in place.")

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_FormulaCase, ...]: ...

        def union_primary(self) -> _FormulaCase | None: ...

        def union_primary_name(self) -> Literal["display_string", "id_based"] | None: ...


@wire(
    "com.apple.apps.content-language.table.cell.formula.id-based-formula",
    version="1.0",
    fields=[
        ("expression", (1, 0), "req"),
        ("references", (1, 0), "opt"),
    ],
)
class IdBasedFormula(ObjectModel):
    """A formula whose cell references are stored separately, by row and column ID.

Because they're stored by ID, the references survive insertions and deletions of rows or columns."""
    expression: str = Field(description="The formula expression, with placeholder tokens in place of cell references. Placeholders have the form `{refN}`, zero-indexed. For example, in `=SUM({ref0}) + {ref1}`, `{ref0}` resolves to the range carried by `references[0]` and `{ref1}` to `references[1]`.")
    references: list[CellReference] | None = Field(default=None, description="The cell references used by the expression, one entry for each placeholder. Their order must match the `{refN}` indices in `expression`.")


@wire(
    "com.apple.apps.content-language.table.cell.formula.cell-reference",
    version="1.0",
    fields=[
        ("placeholder", (1, 0), "req"),
        ("display_notation", (1, 0), "opt"),
        ("start_row_identifier", (1, 0), "req"),
        ("start_column_identifier", (1, 0), "req"),
        ("end_row_identifier", (1, 0), "opt"),
        ("end_column_identifier", (1, 0), "opt"),
        ("is_row_absolute", (1, 0), "def"),
        ("is_column_absolute", (1, 0), "def"),
        ("is_end_row_absolute", (1, 0), "def"),
        ("is_end_column_absolute", (1, 0), "def"),
        ("table_identifier", (1, 0), "opt"),
    ],
)
class CellReference(ObjectModel):
    """A reference to a single cell or a rectangular range of cells.

It's addressed by row and column ID rather than by index, so it stays stable across structural edits."""
    placeholder: str = Field(description="The placeholder token in the expression that this reference fills in, of the form `{refN}` (for example, `{ref0}` or `{ref1}`).")
    display_notation: str | None = Field(default=None, description="The original A1-style notation, preserved for display only (for example, `A1`, `B2:D5`, or `$A$1`). It isn't used during evaluation.")
    start_row_identifier: str = Field(description="The row ID of a single cell, or of the top-left cell of a range. It must match a `Table.Row.row_identifier` in this table or, for a cross-table reference, in the table identified by `table_identifier`.")
    start_column_identifier: str = Field(description="The column ID of a single cell, or of the top-left cell of a range. It must match a `Table.ColumnHeader.column_identifier` in the referenced table.")
    end_row_identifier: str | None = Field(default=None, description="The row ID of the bottom-right cell of a range. Omit it for a single-cell reference.")
    end_column_identifier: str | None = Field(default=None, description="The column ID of the bottom-right cell of a range. Omit it for a single-cell reference.")
    is_row_absolute: bool = Field(default=False, description="Whether the start row reference is absolute. It's `true` if the original notation pinned the row (for example, `A$1`) and `false` for a relative reference (`A1`).")
    is_column_absolute: bool = Field(default=False, description="Whether the start column reference is absolute. It's `true` if the original notation pinned the column (for example, `$A1`) and `false` for a relative reference (`A1`).")
    is_end_row_absolute: bool = Field(default=False, description="Whether the end row reference of a range is absolute. It's only meaningful when `end_row_identifier` is set.")
    is_end_column_absolute: bool = Field(default=False, description="Whether the end column reference of a range is absolute. It's only meaningful when `end_column_identifier` is set.")
    table_identifier: str | None = Field(default=None, description="The identifier of another table, for a cross-table reference. It matches the `Table.identifier` of that table. Omit it for a reference within the same table. An example in A1 notation is `Table 2::A1`.")


@wire(
    "com.apple.apps.content-language.table.cell.strokes",
    version="1.0",
    fields=[
        ("top", (1, 0), "opt"),
        ("bottom", (1, 0), "opt"),
        ("left", (1, 0), "opt"),
        ("right", (1, 0), "opt"),
    ],
)
class Strokes(ObjectModel):
    """The stroke overrides for the edges of a cell.

An omitted edge falls back to the table-level stroke for the cell's region (body, header, or footer)."""
    top: Stroke | None = Field(default=None, description="The stroke along the top edge of the cell.")
    bottom: Stroke | None = Field(default=None, description="The stroke along the bottom edge of the cell.")
    left: Stroke | None = Field(default=None, description="The stroke along the left edge of the cell.")
    right: Stroke | None = Field(default=None, description="The stroke along the right edge of the cell.")


@wire_union(
    "com.apple.apps.content-language.table.cell-range",
    version="1.0",
    cases=[
        ("row_column_id_range", (1, 0), False),
    ],
)
class CellRange(TaggedUnionModel):
    """A rectangular range of cells in a table.

It's addressed by row and column IDs, so it stays stable across structural edits. It's defined so that future versions can add other ways to address a range. Fields that use it include `Table.merges` (visually combined cells) and `Table.Cell.spill_range` (the range a spilling formula populates)."""
    row_column_id_range: RowColumnIdRange | None = Field(default=None, description="A range addressed by the row ID and column ID of its top-left and bottom-right cells.")

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_CellRangeCase, ...]: ...

        def union_primary(self) -> _CellRangeCase | None: ...

        def union_primary_name(self) -> Literal["row_column_id_range"] | None: ...


@wire(
    "com.apple.apps.content-language.table.cell-range.row-column-id-range",
    version="1.0",
    fields=[
        ("top_left_row_identifier", (1, 0), "req"),
        ("top_left_column_identifier", (1, 0), "req"),
        ("bottom_right_row_identifier", (1, 0), "req"),
        ("bottom_right_column_identifier", (1, 0), "req"),
    ],
)
class RowColumnIdRange(ObjectModel):
    """A range addressed by the row and column IDs of its top-left and bottom-right cells.

Using IDs rather than indexes keeps the range stable across row and column insertions and deletions. Resolve each ID against the `row_identifier`s of the rows in `content` and the `column_identifier`s in `column_headers`; a range can name a row that `content` omits, and such a range can't be located."""
    top_left_row_identifier: str = Field(description="The row ID of the top-left cell of the range.")
    top_left_column_identifier: str = Field(description="The column ID of the top-left cell of the range.")
    bottom_right_row_identifier: str = Field(description="The row ID of the bottom-right cell of the range.")
    bottom_right_column_identifier: str = Field(description="The column ID of the bottom-right cell of the range.")


@wire(
    "com.apple.apps.content-language.table.visual-properties",
    version="1.0",
    fields=[
        ("overall_properties", (1, 0), "opt"),
        ("body_cell_properties", (1, 0), "opt"),
        ("body_text_properties", (1, 0), "opt"),
        ("body_stroke_properties", (1, 0), "opt"),
        ("header_row_cell_properties", (1, 0), "opt"),
        ("header_row_text_properties", (1, 0), "opt"),
        ("header_row_stroke_properties", (1, 0), "opt"),
        ("header_column_cell_properties", (1, 0), "opt"),
        ("header_column_text_properties", (1, 0), "opt"),
        ("header_column_stroke_properties", (1, 0), "opt"),
        ("footer_row_cell_properties", (1, 0), "opt"),
        ("footer_row_text_properties", (1, 0), "opt"),
        ("footer_row_stroke_properties", (1, 0), "opt"),
    ],
)
class VisualProperties(ObjectModel):
    """The default styling of a table, broken down by region.

It holds one set of table-wide settings, `overall_properties`, plus paired cell, text, and stroke settings for the body and for each header and footer region. A header or footer region's settings override the body defaults; per-row, per-column, and per-cell overrides take precedence over everything here."""
    overall_properties: OverallProperties | None = Field(default=None, description="The table-wide style settings, which include alternating-row fill, writing direction, auto-resize, rounded corners, and other settings for the whole table. Strokes are set in each region's stroke properties (`body_stroke_properties` and its header-row, header-column, and footer-row counterparts), and cell settings in the matching cell properties.")
    body_cell_properties: CellProperties | None = Field(default=None, description="The default cell styling (fill, alignment, padding, and wrap) applied to body cells: the cells outside the header rows, header columns, and footer rows.")
    body_text_properties: ParagraphProperties | None = Field(default=None, description="The default paragraph and text style (font, size, color, and alignment) applied to body cells.")
    body_stroke_properties: BodyStrokeProperties | None = Field(default=None, description="The outer borders and interior gridlines of the body region, and their visibility toggles.")
    header_row_cell_properties: CellProperties | None = Field(default=None, description="The default cell styling for header rows. It overrides `body_cell_properties` for the cells in the top `Table.number_of_header_rows` rows.")
    header_row_text_properties: ParagraphProperties | None = Field(default=None, description="The default text style for header rows. It overrides `body_text_properties` for the cells in the top `Table.number_of_header_rows` rows.")
    header_row_stroke_properties: HeaderFooterStrokeProperties | None = Field(default=None, description="The outer border, body separator, and interior gridlines of the header-rows region, plus visibility toggles.")
    header_column_cell_properties: CellProperties | None = Field(default=None, description="The default cell styling for header columns. It overrides `body_cell_properties` for the cells in the leading `Table.number_of_header_columns` columns.")
    header_column_text_properties: ParagraphProperties | None = Field(default=None, description="The default text style for header columns. It overrides `body_text_properties` for the cells in the leading `Table.number_of_header_columns` columns.")
    header_column_stroke_properties: HeaderFooterStrokeProperties | None = Field(default=None, description="The outer border, body separator, and interior gridlines of the header-columns region, plus visibility toggles.")
    footer_row_cell_properties: CellProperties | None = Field(default=None, description="The default cell styling for footer rows. It overrides `body_cell_properties` for the cells in the bottom `Table.number_of_footer_rows` rows.")
    footer_row_text_properties: ParagraphProperties | None = Field(default=None, description="The default text style for footer rows. It overrides `body_text_properties` for the cells in the bottom `Table.number_of_footer_rows` rows.")
    footer_row_stroke_properties: HeaderFooterStrokeProperties | None = Field(default=None, description="The outer border, body separator, and interior gridlines of the footer-rows region, plus visibility toggles.")


@wire(
    "com.apple.apps.content-language.table.visual-properties.overall-properties",
    version="1.0",
    fields=[
        ("behaves_like_spreadsheet", (1, 0), "opt"),
        ("auto_resize", (1, 0), "opt"),
        ("writing_direction", (1, 0), "opt"),
        ("has_alternating_rows", (1, 0), "opt"),
        ("alternating_rows_fill", (1, 0), "ovr"),
        ("rounded_corners", (1, 0), "opt"),
        ("stroke_presets", (1, 0), "opt"),
    ],
)
class OverallProperties(ObjectModel):
    """The style settings that apply to a whole table.

A `preset_identifier` here is matched against the overall style of each table style collection in the document stylesheet by the numeric slot in the identifier rather than by the whole string, so an identifier not in that form resolves to the first slot. When no collection matches, the first table style in the stylesheet is used."""
    behaves_like_spreadsheet: bool | None = Field(default=None, description="Whether the table uses spreadsheet-style interaction (cell selection, navigation, and fill handles). Keynote writes `false`; when no value is given, `true` is used.")
    auto_resize: bool | None = Field(default=None, description="Whether the table grows and shrinks to fit its content rather than keeping fixed row and column sizes.")
    writing_direction: WritingDirectionType | None = Field(default=None, strict=False, description="The default writing direction for the table (left-to-right, right-to-left, or natural).")
    has_alternating_rows: bool | None = Field(default=None, description="Whether every other body row is filled with `alternating_rows_fill` to produce a banded look.")
    alternating_rows_fill: Override[Fill] = Field(default_factory=Override.not_set, description="The fill applied to alternating body rows when `has_alternating_rows` is `true`. If it's absent, it's inherited; an explicit `null` leaves the alternating rows unfilled, which isn't the same as a fill at 0% opacity.")
    rounded_corners: bool | None = Field(default=None, description="Whether the table outline uses rounded corners. Keynote always writes `false` and ignores the value when it reads a document.")
    stroke_presets: list[StrokePreset] | None = Field(default=None, description="The border and gridline stroke presets available for this table, in order. They are choices that can be applied, not a description of the table's borders and gridlines. A list shorter than 15 entries is padded with generated presets, and a longer one is truncated.")


@wire(
    "com.apple.apps.content-language.table.visual-properties.body-stroke-properties",
    version="1.0",
    fields=[
        ("horizontal_border_stroke", (1, 0), "opt"),
        ("vertical_border_stroke", (1, 0), "opt"),
        ("horizontal_stroke", (1, 0), "opt"),
        ("vertical_stroke", (1, 0), "opt"),
        ("border_strokes_visible", (1, 0), "opt"),
        ("horizontal_strokes_visible", (1, 0), "opt"),
        ("vertical_strokes_visible", (1, 0), "opt"),
    ],
)
class BodyStrokeProperties(ObjectModel):
    """The borders and gridlines of a table's body region, and their visibility."""
    horizontal_border_stroke: Stroke | None = Field(default=None, description="The outer top and bottom borders of the body region.")
    vertical_border_stroke: Stroke | None = Field(default=None, description="The outer left and right borders of the body region.")
    horizontal_stroke: Stroke | None = Field(default=None, description="The horizontal gridlines between body rows (interior only; the outer borders are `horizontal_border_stroke`).")
    vertical_stroke: Stroke | None = Field(default=None, description="The vertical gridlines between body columns (interior only; the outer borders are `vertical_border_stroke`).")
    border_strokes_visible: bool | None = Field(default=None, description="Whether the body's outer border strokes (`horizontal_border_stroke` and `vertical_border_stroke`) are visible. It's the main visibility setting for both.")
    horizontal_strokes_visible: bool | None = Field(default=None, description="Whether the body's horizontal gridlines are visible. It's their main visibility setting.")
    vertical_strokes_visible: bool | None = Field(default=None, description="Whether the body's vertical gridlines are visible. It's their main visibility setting.")


@wire(
    "com.apple.apps.content-language.table.visual-properties.header-footer-stroke-properties",
    version="1.0",
    fields=[
        ("border_stroke", (1, 0), "opt"),
        ("separator_stroke", (1, 0), "opt"),
        ("horizontal_stroke", (1, 0), "opt"),
        ("vertical_stroke", (1, 0), "opt"),
        ("separator_visible", (1, 0), "opt"),
        ("across_strokes_visible", (1, 0), "opt"),
    ],
)
class HeaderFooterStrokeProperties(ObjectModel):
    """The borders, gridlines, and visibility toggles of a table's header or footer region.

The same type is used for header rows, header columns, and footer rows; the region it describes depends on which of the table's visual properties holds it."""
    border_stroke: Stroke | None = Field(default=None, description="The outer border around the region.")
    separator_stroke: Stroke | None = Field(default=None, description="The stroke that separates this region from the adjacent body.")
    horizontal_stroke: Stroke | None = Field(default=None, description="The horizontal gridlines between cells inside the region.")
    vertical_stroke: Stroke | None = Field(default=None, description="The vertical gridlines between cells inside the region.")
    separator_visible: bool | None = Field(default=None, description="Whether `separator_stroke` is visible.")
    across_strokes_visible: bool | None = Field(default=None, description="Whether the strokes that run across the region are visible: the vertical strokes for header and footer rows, and the horizontal strokes for header columns.")


@wire(
    "com.apple.apps.content-language.table.visual-properties.stroke-preset",
    version="1.0",
    fields=[
        ("horizontal_stroke", (1, 0), "opt"),
        ("vertical_stroke", (1, 0), "opt"),
        ("exterior_stroke", (1, 0), "opt"),
        ("visible_edges", (1, 0), "opt"),
    ],
)
class StrokePreset(ObjectModel):
    """One of a table's stroke presets.

Applying the preset strokes each edge listed in `visible_edges` and clears every edge not listed. Interior edges take `horizontal_stroke` or `vertical_stroke`, and outer edges take `exterior_stroke`."""
    horizontal_stroke: Stroke | None = Field(default=None, description="The stroke applied to the interior horizontal gridlines this preset turns on.")
    vertical_stroke: Stroke | None = Field(default=None, description="The stroke applied to the interior vertical gridlines this preset turns on.")
    exterior_stroke: Stroke | None = Field(default=None, description="The stroke applied to the outer border edges this preset turns on.")
    visible_edges: list[Annotated[Edge, Strict(False)]] | None = Field(default=None, description="The edges this preset strokes; every edge left out is cleared when the preset is applied. Order isn't meaningful and each edge must appear at most once. An empty list is the *no borders* preset.")


class Edge(str, Enum):
    """An edge of the stroked range that a stroke preset can turn on.

The four outer edges are stroked with `exterior_stroke`; the two interior cases are stroked with `horizontal_stroke` and `vertical_stroke`.

    bottom — Outer bottom edge.
    horizontal — Interior horizontal gridlines (between rows).
    left — Outer left edge.
    right — Outer right edge.
    top — Outer top edge.
    vertical — Interior vertical gridlines (between columns). Shown in Keynote as “Center borders.”
    """
    BOTTOM = "bottom"
    HORIZONTAL = "horizontal"
    LEFT = "left"
    RIGHT = "right"
    TOP = "top"
    VERTICAL = "vertical"


@wire(
    "com.apple.apps.content-language.table.cell-format",
    version="1.0",
    fields=[
        ("format_type", (1, 0), "opt"),
        ("number_format", (1, 0), "opt"),
        ("currency_format", (1, 0), "opt"),
        ("fraction_format", (1, 0), "opt"),
        ("base_format", (1, 0), "opt"),
        ("bool_format", (1, 0), "opt"),
        ("duration_format", (1, 0), "opt"),
        ("date_time_format", (1, 0), "opt"),
        ("custom_format_identifier", (1, 0), "opt"),
    ],
)
class CellFormat(ObjectModel):
    """The display format of a cell's value.

`format_type` selects the kind of format, and the matching sub-format property (`number_format`, `currency_format`, and so on) holds the options for that kind. Sub-formats for a different kind are ignored."""
    format_type: FormatType | None = Field(default=None, strict=False, description="The kind of formatting to apply (such as number, currency, or date). It determines which sub-format property is read. Keynote doesn't write `automatic`: a cell set to Automatic is written with the format its value is displayed in, such as `number` or `date_time`, and opens set to that format rather than to Automatic, unless that format is `text`.")
    number_format: NumberFormat | None = Field(default=None, description="The options for the `number`, `percentage`, and `scientific` format types.")
    currency_format: CurrencyFormat | None = Field(default=None, description="The options for the `currency` format type (such as the currency code and accounting style).")
    fraction_format: FractionFormat | None = Field(default=None, description="The options for the `fraction` format type (for example, display as halves, as eighths, or with an up-to-three-digit numerator).")
    base_format: BaseFormat | None = Field(default=None, description="The options for the `base` format type (numeric base 2 through 36; for example, binary, octal, or hexadecimal).")
    bool_format: BoolFormat | None = Field(default=None, description="The options for the `boolean` format type (the strings to display for true and false).")
    duration_format: DurationFormat | None = Field(default=None, description="The options for the `duration` format type (its unit range and style).")
    date_time_format: DateTimeFormat | None = Field(default=None, description="The options for the `date_time` format type (its format string).")
    custom_format_identifier: str | None = Field(default=None, description="The identifier of a shared custom format, declared in `Table.custom_formats`, that applies to this cell. It's used only when `format_type` is `custom` and is ignored for built-in format types.")


class FormatType(str, Enum):
    """The kind of formatting to apply to a cell's value.

Each case selects which sub-format property of the cell format is read.

    automatic — Inferred from the value's data type: numbers display as numbers, dates as dates, and so on.
    base — Display in a chosen numeric base (for example, binary, octal, hexadecimal). Shown in Keynote as Numeral System.
    boolean — Display as TRUE or FALSE (or as user-specified strings set in the Boolean format options).
    currency — Currency formatting with a currency symbol or code and optional accounting style.
    custom — User-defined format string with optional conditional rules (see the table's custom formats).
    date_time — A date, a time, or both, formatted with a date and time format string.
    duration — Duration in chosen units (weeks, days, hours, and so on).
    fraction — Display as a fraction at a chosen accuracy (such as halves, eighths, or up to a number of digits).
    number — Plain numeric formatting (decimal places, thousands separator, negative number style).
    percentage — Numeric formatting where the displayed value is the underlying value multiplied by 100, suffixed with “%.”
    scientific — Scientific notation (for example, 1.23E+04).
    text — Treat the value as raw text (no numeric or date interpretation). A reader in version 1.0 doesn't apply this format, so a cell written with it opens with the `automatic` format instead.
    """
    AUTOMATIC = "automatic"
    BASE = "base"
    BOOLEAN = "boolean"
    CURRENCY = "currency"
    CUSTOM = "custom"
    DATE_TIME = "date_time"
    DURATION = "duration"
    FRACTION = "fraction"
    NUMBER = "number"
    PERCENTAGE = "percentage"
    SCIENTIFIC = "scientific"
    TEXT = "text"


class NegativeNumberStyle(str, Enum):
    """A style for displaying negative numbers.

    minus — Prefix with a minus sign (for example, -1,234.56).
    none — No special treatment for negative values.
    parentheses — Wrap in parentheses with no minus sign (for example, (1,234.56)).
    red — Display in red text with a minus sign.
    red_and_parentheses — Wrap in parentheses and display in red text.
    """
    MINUS = "minus"
    NONE = "none"
    PARENTHESES = "parentheses"
    RED = "red"
    RED_AND_PARENTHESES = "red_and_parentheses"


@wire(
    "com.apple.apps.content-language.table.cell-format.number-format",
    version="1.0",
    fields=[
        ("decimal_places", (1, 0), "def"),
        ("negative_number_style", (1, 0), "def"),
        ("use_thousands_separator", (1, 0), "def"),
    ],
)
class NumberFormat(ObjectModel):
    """Options for plain numeric, percentage, and scientific formatting."""
    decimal_places: int = Field(default=2, description="The number of decimal places to display, `0` through 30; a negative value is treated as zero rather than rejected. The value 253 means automatic (as many decimal places as the value needs) rather than a digit count.")
    negative_number_style: NegativeNumberStyle = Field(default_factory=lambda: NegativeNumberStyle.MINUS, strict=False, description="The display style for negative numbers.")
    use_thousands_separator: bool = Field(default=True, description="Whether to insert a thousands separator (for example, 1,234,567).")


@wire(
    "com.apple.apps.content-language.table.cell-format.currency-format",
    version="1.0",
    fields=[
        ("decimal_places", (1, 0), "def"),
        ("negative_number_style", (1, 0), "def"),
        ("use_thousands_separator", (1, 0), "def"),
        ("accounting_style", (1, 0), "def"),
        ("currency_code", (1, 0), "def"),
    ],
)
class CurrencyFormat(ObjectModel):
    """Options for currency formatting."""
    decimal_places: int = Field(default=2, description="The number of decimal places to display, `0` through 30; a negative value is treated as zero rather than rejected. The value 253 means automatic (as many decimal places as the value needs) rather than a digit count.")
    negative_number_style: NegativeNumberStyle = Field(default_factory=lambda: NegativeNumberStyle.MINUS, strict=False, description="The display style for negative amounts.")
    use_thousands_separator: bool = Field(default=True, description="Whether to insert a thousands separator (for example, $1,234,567.00).")
    accounting_style: bool = Field(default=False, description="Whether to use accounting style: currency symbol left-aligned and negative values in parentheses.")
    currency_code: str = Field(default="USD", description="The ISO 4217 currency code (for example, `USD`, `EUR`, or `JPY`) that determines the symbol shown.")


@wire(
    "com.apple.apps.content-language.table.cell-format.fraction-format",
    version="1.0",
    fields=[
        ("accuracy", (1, 0), "def"),
    ],
)
class FractionFormat(ObjectModel):
    """Options for fraction formatting, such as showing a decimal as a fraction."""
    accuracy: Accuracy = Field(default_factory=lambda: Accuracy.UP_TO_THREE_DIGITS, strict=False, description="The precision to use for the fraction representation.")


class Accuracy(str, Enum):
    """The granularity of a fraction display.

It's either a maximum digit count for the numerator and denominator, or a fixed denominator such as halves or quarters.

    conflicting — A value that marks a range of cells with mixed fraction accuracies. It's not a value to set on a single cell.
    eighths — Fixed denominator of 8.
    halves — Fixed denominator of 2 (for example, 0/2, 1/2).
    hundredths — Fixed denominator of 100.
    quarters — Fixed denominator of 4 (for example, 1/4, 3/4).
    sixteenths — Fixed denominator of 16.
    tenths — Fixed denominator of 10.
    up_to_one_digit — At most one digit in the numerator and denominator (for example, 1/2, 3/4).
    up_to_three_digits — At most three digits in the numerator and denominator.
    up_to_two_digits — At most two digits in the numerator and denominator (for example, 5/16, 22/87).
    """
    CONFLICTING = "conflicting"
    EIGHTHS = "eighths"
    HALVES = "halves"
    HUNDREDTHS = "hundredths"
    QUARTERS = "quarters"
    SIXTEENTHS = "sixteenths"
    TENTHS = "tenths"
    UP_TO_ONE_DIGIT = "up_to_one_digit"
    UP_TO_THREE_DIGITS = "up_to_three_digits"
    UP_TO_TWO_DIGITS = "up_to_two_digits"


@wire(
    "com.apple.apps.content-language.table.cell-format.base-format",
    version="1.0",
    fields=[
        ("base", (1, 0), "def"),
        ("base_places", (1, 0), "def"),
        ("base_use_minus_sign", (1, 0), "def"),
    ],
)
class BaseFormat(ObjectModel):
    """Options for formatting a number in a numeral system such as binary, octal, or hexadecimal."""
    base: int = Field(default=10, description="The numeric base, 1-36 (for example, 2 for binary, 8 for octal, or 16 for hexadecimal). A value outside that range is adjusted to the nearest supported base rather than rejected.")
    base_places: int = Field(default=0, description="The minimum number of digits to display, padding with leading zeros if needed. Values are supported from `0` to 32; anything outside that range is adjusted to the nearest supported value rather than rejected.")
    base_use_minus_sign: bool = Field(default=True, description="Whether negative values are shown with a leading minus sign. If `false`, they are shown using two's complement in the chosen base.")


@wire(
    "com.apple.apps.content-language.table.cell-format.bool-format",
    version="1.0",
    fields=[
        ("true_string", (1, 0), "req"),
        ("false_string", (1, 0), "req"),
    ],
)
class BoolFormat(ObjectModel):
    """Options for Boolean formatting, including the strings shown in place of true and false."""
    true_string: str = Field(description="The string displayed when the cell value is true (for example, `TRUE`, `Yes`, or `✓`). It's only read when the cell's `format_type` is `boolean`.")
    false_string: str = Field(description="The string displayed when the cell value is false (for example, `FALSE`, `No`, or `✗`). It's only read when the cell's `format_type` is `boolean`.")


@wire(
    "com.apple.apps.content-language.table.cell-format.duration-format",
    version="1.0",
    fields=[
        ("use_automatic_units", (1, 0), "def"),
        ("smallest_unit", (1, 0), "def"),
        ("largest_unit", (1, 0), "def"),
        ("style", (1, 0), "def"),
    ],
)
class DurationFormat(ObjectModel):
    """Options for duration formatting.

They set how a span of time is broken into units and displayed."""
    use_automatic_units: bool = Field(default=True, description="Whether units are chosen automatically based on the duration's magnitude. If it's `false`, `smallest_unit` and `largest_unit` are used.")
    smallest_unit: Unit = Field(default_factory=lambda: Unit.SECOND, strict=False, description="The smallest unit to include in the displayed duration. It's used only when `use_automatic_units` is `false`.")
    largest_unit: Unit = Field(default_factory=lambda: Unit.HOUR, strict=False, description="The largest unit to include in the displayed duration. It's used only when `use_automatic_units` is `false`.")
    style: Style = Field(default_factory=lambda: Style.SHORT, strict=False, description="The formatting style, which can be compact (“1h”), short (“1 hr”), or long (“1 hour”).")


class Unit(str, Enum):
    """A duration unit.

    day — Days
    hour — Hours
    millisecond — Milliseconds
    minute — Minutes
    none — No unit
    second — Seconds
    week — Weeks
    """
    DAY = "day"
    HOUR = "hour"
    MILLISECOND = "millisecond"
    MINUTE = "minute"
    NONE = "none"
    SECOND = "second"
    WEEK = "week"


class Style(str, Enum):
    """The length of the unit labels in a displayed duration.

    compact — Single-letter labels with no space (for example, “1h 30m”). Shown in Keynote as None, since the option suppresses unit labels entirely.
    long — Full-word labels (for example, “1 hour 30 minutes”).
    short — Abbreviated labels (for example, “1 hr 30 min”).
    """
    COMPACT = "compact"
    LONG = "long"
    SHORT = "short"


@wire(
    "com.apple.apps.content-language.table.cell-format.date-time-format",
    version="1.0",
    fields=[
        ("format_string", (1, 0), "req"),
    ],
)
class DateTimeFormat(ObjectModel):
    """Options for date and time formatting."""
    format_string: str = Field(description="The date and time format pattern, in Unicode date format (for example, `MMM d, yyyy h:mm a`).")


@wire(
    "com.apple.apps.content-language.table.date",
    version="1.0",
    fields=[
        ("time_interval_since1970", (1, 0), "req"),
    ],
)
class Date(ObjectModel):
    """An absolute point in time.

Its time zone is implicitly UTC, and the reader determines the locale it's displayed in."""
    time_interval_since1970: float = Field(description="The number of seconds, with fractional precision, since 1970-01-01 00:00:00 UTC. A negative value represents a date before 1970.")


@wire(
    "com.apple.apps.content-language.table.predicate",
    version="1.0",
    fields=[
        ("predicate_type", (1, 0), "req"),
        ("value1", (1, 0), "opt"),
        ("value2", (1, 0), "opt"),
        ("qualifier", (1, 0), "opt"),
        ("date_qualifier1", (1, 0), "opt"),
        ("date_qualifier2", (1, 0), "opt"),
        ("duration_unit1", (1, 0), "opt"),
        ("duration_unit2", (1, 0), "opt"),
        ("value_list", (1, 0), "opt"),
    ],
)
class Predicate(ObjectModel):
    """A condition that's evaluated against a single cell's value.

Some predicates evaluate the cell relative to its column instead. Predicates are used by conditional highlighting rules and, in future versions, by table filter rules."""
    predicate_type: PredicateType = Field(strict=False, description="The kind of comparison or test to perform. It determines which of `value1`, `value2`, `value_list`, `qualifier`, `date_qualifier1`, `date_qualifier2`, `duration_unit1`, and `duration_unit2` are required.")
    value1: Value | None = Field(default=None, description="The value the predicate compares the cell against. Predicates that take no operand, such as `is_blank` or `date_is_today`, ignore it, and the top and bottom predicates use it as the threshold count N. Its `Value` case must match the data type `predicate_type` operates on. For example, `text_contains` expects text.")
    value2: Value | None = Field(default=None, description="The second comparison value. It's required only for range predicates (`value_between`, `value_not_between`, `date_is_between`, `duration_is_between`, `date_between_relative`, `duration_is_not_between`). It must use the same `Value` case as `value1`.")
    qualifier: Qualifier | None = Field(default=None, strict=False, description="The case sensitivity of a text predicate (`text_contains`, `text_begins_with`, `text_ends_with`, `text_is`, `text_is_not`, `text_does_not_contain`, `text_not_starts_with`, `text_not_ends_with`). If it's omitted, it defaults to `case_insensitive`.")
    date_qualifier1: DateQualifier | None = Field(default=None, strict=False, description="The time unit for the first value of relative date predicates (`date_is_in_the_last`, `date_is_in_the_next`, `date_before_relative`, `date_after_relative`, `date_between_relative`, `date_in_this`). For example, a `value1` of 5 with a `date_qualifier1` of `years` means “5 years.” It's required for these predicates.")
    date_qualifier2: DateQualifier | None = Field(default=None, strict=False, description="The time unit for the second value of relative-date range predicates (`date_between_relative`). It's required only when both ends of the range need separate units.")
    duration_unit1: DurationUnit | None = Field(default=None, strict=False, description="The display unit for the first value of duration predicates. The duration value itself is stored as a number of seconds, and this unit determines how to interpret it; for example, 3600 seconds with a `duration_unit1` of `hour` means “1 hour.” It's required for duration predicates.")
    duration_unit2: DurationUnit | None = Field(default=None, strict=False, description="The display unit for the second value of duration range predicates (`duration_is_between`, `duration_is_not_between`). It's required when those predicates are used.")
    value_list: list[Value] | None = Field(default=None, description="The ordered list of typed values that the `in_list` and `not_in_list` predicates compare the cell against. All entries must use the same `Value` case. If it's present, `value1` and `value2` are ignored.")


class PredicateType(str, Enum):
    """The type of conditional test to perform.

    date_after_relative — Cell date is after a relative offset of `value1` time units (the unit is given by `date_qualifier1`).
    date_before_relative — Cell date is before a relative offset of `value1` time units (the unit is given by `date_qualifier1`).
    date_between_relative — Cell date is between two relative offsets of `value1` and `value2` time units.
    date_in_this — Cell date is in the day, week, month, or year (the unit is given by `date_qualifier1`).
    date_is_after — Cell date is after `value1`.
    date_is_before — Cell date is before `value1`.
    date_is_between — Cell date is between `value1` and `value2`.
    date_is_exactly — Cell date is exactly `value1`.
    date_is_in_the_last — Cell date is within the last `value1` units (the unit is given by `date_qualifier1`).
    date_is_in_the_next — Cell date is within the next `value1` units (the unit is given by `date_qualifier1`).
    date_is_the_date — Cell date is on the same calendar day as `value1`. It's distinct from `date_is_exactly`.
    date_is_today — Cell date is today.
    date_is_tomorrow — Cell date is tomorrow.
    date_is_yesterday — Cell date is yesterday.
    distincts — Cell is one of the distinct values in the column.
    duplicates — Cell value is duplicated elsewhere in the column.
    duration_above_average — Cell duration is above the average.
    duration_below_average — Cell duration is below the average.
    duration_bottom — Cell duration is in the bottom N values (or bottom N percent) of its column. The threshold N is given by `value1`.
    duration_is_between — Cell duration is between `value1` and `value2`.
    duration_is_equal — Cell duration equals `value1`.
    duration_is_greater_than — Cell duration is greater than `value1`.
    duration_is_greater_than_or_equal — Cell duration is greater than or equal to `value1`.
    duration_is_less_than — Cell duration is less than `value1`.
    duration_is_less_than_or_equal — Cell duration is less than or equal to `value1`.
    duration_is_not_between — Cell duration isn't between `value1` and `value2`.
    duration_is_not_equal — Cell duration doesn't equal `value1`.
    duration_top — Cell duration is in the top N values (or top N percent) of its column. The threshold N is given by `value1`.
    formula — Cell matches an arbitrary formula-based predicate. The formula text is given by `value1`, in the consuming application's formula syntax.
    in_list — Cell value matches any value in `value_list`.
    is_blank — Cell is blank.
    is_checked — Cell checkbox is checked.
    is_false — Cell value is FALSE.
    is_negative — Cell numeric value is negative (< 0).
    is_not_blank — Cell isn't blank.
    is_not_checked — Cell checkbox isn't checked.
    is_positive — Cell numeric value is zero or positive (>= 0).
    is_true — Cell value is TRUE.
    not_in_list — Cell value matches none of the values in `value_list`.
    pivot_source_filtered_for_column — The column is filtered by a pivot table's source predicates. It's reserved for pivot tables, which version 1.0 doesn't support.
    pivot_source_filtered_for_row — The row is filtered by a pivot table's source predicates. It's reserved for pivot tables, which version 1.0 doesn't support.
    text_begins_with — Cell text begins with `value1`.
    text_contains — Cell text contains `value1`.
    text_does_not_contain — Cell text doesn't contain `value1`.
    text_ends_with — Cell text ends with `value1`.
    text_is — Cell text is exactly `value1`.
    text_is_not — Cell text isn't `value1`.
    text_not_ends_with — Cell text doesn't end with `value1`.
    text_not_starts_with — Cell text doesn't begin with `value1`.
    uniques — Cell value is unique in the column.
    value_above_average — Cell value is above the column or row average.
    value_below_average — Cell value is below the column or row average.
    value_between — Cell value is between `value1` and `value2` (inclusive).
    value_bottom — Cell value is in the bottom N values (or bottom N percent) of its column. The threshold N is given by `value1`.
    value_equal — Cell value equals `value1`.
    value_greater_than — Cell value is greater than `value1`.
    value_greater_than_or_equal — Cell value is greater than or equal to `value1`.
    value_less_than — Cell value is less than `value1`.
    value_less_than_or_equal — Cell value is less than or equal to `value1`.
    value_not_between — Cell value isn't between `value1` and `value2`.
    value_not_equal — Cell value doesn't equal `value1`.
    value_top — Cell value is in the top N values (or top N percent) of its column. The threshold N is given by `value1`.
    """
    DATE_AFTER_RELATIVE = "date_after_relative"
    DATE_BEFORE_RELATIVE = "date_before_relative"
    DATE_BETWEEN_RELATIVE = "date_between_relative"
    DATE_IN_THIS = "date_in_this"
    DATE_IS_AFTER = "date_is_after"
    DATE_IS_BEFORE = "date_is_before"
    DATE_IS_BETWEEN = "date_is_between"
    DATE_IS_EXACTLY = "date_is_exactly"
    DATE_IS_IN_THE_LAST = "date_is_in_the_last"
    DATE_IS_IN_THE_NEXT = "date_is_in_the_next"
    DATE_IS_THE_DATE = "date_is_the_date"
    DATE_IS_TODAY = "date_is_today"
    DATE_IS_TOMORROW = "date_is_tomorrow"
    DATE_IS_YESTERDAY = "date_is_yesterday"
    DISTINCTS = "distincts"
    DUPLICATES = "duplicates"
    DURATION_ABOVE_AVERAGE = "duration_above_average"
    DURATION_BELOW_AVERAGE = "duration_below_average"
    DURATION_BOTTOM = "duration_bottom"
    DURATION_IS_BETWEEN = "duration_is_between"
    DURATION_IS_EQUAL = "duration_is_equal"
    DURATION_IS_GREATER_THAN = "duration_is_greater_than"
    DURATION_IS_GREATER_THAN_OR_EQUAL = "duration_is_greater_than_or_equal"
    DURATION_IS_LESS_THAN = "duration_is_less_than"
    DURATION_IS_LESS_THAN_OR_EQUAL = "duration_is_less_than_or_equal"
    DURATION_IS_NOT_BETWEEN = "duration_is_not_between"
    DURATION_IS_NOT_EQUAL = "duration_is_not_equal"
    DURATION_TOP = "duration_top"
    FORMULA = "formula"
    IN_LIST = "in_list"
    IS_BLANK = "is_blank"
    IS_CHECKED = "is_checked"
    IS_FALSE = "is_false"
    IS_NEGATIVE = "is_negative"
    IS_NOT_BLANK = "is_not_blank"
    IS_NOT_CHECKED = "is_not_checked"
    IS_POSITIVE = "is_positive"
    IS_TRUE = "is_true"
    NOT_IN_LIST = "not_in_list"
    PIVOT_SOURCE_FILTERED_FOR_COLUMN = "pivot_source_filtered_for_column"
    PIVOT_SOURCE_FILTERED_FOR_ROW = "pivot_source_filtered_for_row"
    TEXT_BEGINS_WITH = "text_begins_with"
    TEXT_CONTAINS = "text_contains"
    TEXT_DOES_NOT_CONTAIN = "text_does_not_contain"
    TEXT_ENDS_WITH = "text_ends_with"
    TEXT_IS = "text_is"
    TEXT_IS_NOT = "text_is_not"
    TEXT_NOT_ENDS_WITH = "text_not_ends_with"
    TEXT_NOT_STARTS_WITH = "text_not_starts_with"
    UNIQUES = "uniques"
    VALUE_ABOVE_AVERAGE = "value_above_average"
    VALUE_BELOW_AVERAGE = "value_below_average"
    VALUE_BETWEEN = "value_between"
    VALUE_BOTTOM = "value_bottom"
    VALUE_EQUAL = "value_equal"
    VALUE_GREATER_THAN = "value_greater_than"
    VALUE_GREATER_THAN_OR_EQUAL = "value_greater_than_or_equal"
    VALUE_LESS_THAN = "value_less_than"
    VALUE_LESS_THAN_OR_EQUAL = "value_less_than_or_equal"
    VALUE_NOT_BETWEEN = "value_not_between"
    VALUE_NOT_EQUAL = "value_not_equal"
    VALUE_TOP = "value_top"


@wire_union(
    "com.apple.apps.content-language.table.predicate.value",
    version="1.0",
    cases=[
        ("date", (1, 0), False),
        ("duration", (1, 0), False),
        ("number", (1, 0), False),
        ("reference", (1, 0), False),
        ("text", (1, 0), False),
    ],
)
class Value(TaggedUnionModel):
    """A typed comparison value.

 This value is carried in `Table.Predicate.value1` or `Table.Predicate.value2`.

Its case must match the data type the predicate operates on."""
    date: Date | None = Field(default=None, description="Absolute date value, used by absolute date predicates.\n\n Examples of these values are `date_is_before`, `date_is_after`, `date_is_between`, `date_is_exactly`, and `date_is_the_date`.")
    duration: float | None = Field(default=None, description="Duration value in seconds, used by duration predicates. The accompanying `Table.Predicate.duration_unit1` (or `duration_unit2`) determines how to interpret the value.")
    number: float | None = Field(default=None, description="Numeric value, used by value-comparison predicates, for example, `value_equal`, `value_greater_than`, and `value_between`, and by relative date predicates that take a unit count, for example, `date_is_in_the_last`.")
    reference: Reference | None = Field(default=None, description="The comparison operand is another cell rather than a literal value (for example, “date is before [B2]”). A reader compares the referenced cell's value at evaluation time. A version 1.0 reader doesn't support a cell operand: a rule that compares against a `reference` in `value1` or `value2` is dropped and a warning is reported, and a `reference` entry in `value_list` is skipped.")
    text: str | None = Field(default=None, description="Text value, used by text-matching predicates (such as `text_contains`, `text_begins_with`, `text_ends_with`, and `text_is`).")

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_ValueCase, ...]: ...

        def union_primary(self) -> _ValueCase | None: ...

        def union_primary_name(self) -> Literal["date", "duration", "number", "reference", "text"] | None: ...


@wire(
    "com.apple.apps.content-language.table.predicate.reference",
    version="1.0",
    fields=[
        ("row_identifier", (1, 0), "req"),
        ("column_identifier", (1, 0), "req"),
        ("is_row_absolute", (1, 0), "def"),
        ("is_column_absolute", (1, 0), "def"),
        ("table_identifier", (1, 0), "opt"),
    ],
)
class Reference(ObjectModel):
    """A reference to a single cell, used as a predicate's comparison operand.

It addresses the cell by row and column ID, so the reference stays stable across structural edits. Range references aren't supported here; predicate operands are always single scalar values."""
    row_identifier: str = Field(description="The row ID of the referenced cell. It must match a `Table.Row.row_identifier` in this table or, for a cross-table reference, in the table identified by `table_identifier`.")
    column_identifier: str = Field(description="The column ID of the referenced cell. It must match a `Table.ColumnHeader.column_identifier` in the referenced table.")
    is_row_absolute: bool = Field(default=False, description="Whether the row reference is absolute. It's `true` if the original notation pinned the row (for example, `A$1`), and `false` if the row is relative (`A1`).")
    is_column_absolute: bool = Field(default=False, description="Whether the column reference is absolute. It's `true` if the original notation pinned the column (for example, `$A1`), and `false` if the column is relative (`A1`).")
    table_identifier: str | None = Field(default=None, description="The identifier of another table, for a cross-table reference. It matches the `Table.identifier` of that table. Omit it for a reference within the same table.")


class Qualifier(str, Enum):
    """A qualifier for text-matching predicates.

    case_insensitive — Match is case insensitive.
    case_sensitive — Match is case sensitive.
    """
    CASE_INSENSITIVE = "case_insensitive"
    CASE_SENSITIVE = "case_sensitive"


class DateQualifier(str, Enum):
    """A time unit for relative date predicates, as in “in the last 5 years.”

It's used by predicates that take a unit count as their value, such as `date_is_in_the_last`, `date_is_in_the_next`, `date_before_relative`, `date_after_relative`, `date_between_relative`, and `date_in_this`.

    ago — The unit count is in the past, for use with the `date_before_relative` and `date_after_relative` predicates.
    days — Days
    from_now — The unit count is in the future, for use with the `date_before_relative` and `date_after_relative` predicates.
    months — Months
    quarters — Quarters
    weeks — Weeks
    years — Years
    """
    AGO = "ago"
    DAYS = "days"
    FROM_NOW = "from_now"
    MONTHS = "months"
    QUARTERS = "quarters"
    WEEKS = "weeks"
    YEARS = "years"


class DurationUnit(str, Enum):
    """The display unit for a duration predicate's values.

The duration value itself is stored as a number of seconds; this unit indicates how to interpret and render that value. For example, a value of 7200 with the unit `hour` means “2 hours.” It's required for a predicate with duration values to be read back correctly.

    day — Days
    hour — Hours
    millisecond — Milliseconds
    minute — Minutes
    second — Seconds
    week — Weeks
    """
    DAY = "day"
    HOUR = "hour"
    MILLISECOND = "millisecond"
    MINUTE = "minute"
    SECOND = "second"
    WEEK = "week"


@wire(
    "com.apple.apps.content-language.table.custom-format",
    version="1.0",
    fields=[
        ("identifier", (1, 0), "req"),
        ("format_name", (1, 0), "opt"),
        ("format_string", (1, 0), "req"),
        ("format_type", (1, 0), "def"),
        ("number_format_data", (1, 0), "opt"),
        ("conditions", (1, 0), "opt"),
    ],
)
class CustomFormat(ObjectModel):
    """A user-defined format for a cell.

A custom format has a format pattern string and optional conditional rules that switch the pattern based on the cell's value. It's used when `Table.CellFormat.format_type` is `custom`. Custom formats are stored in `Table.custom_formats`, and individual cells refer to one through `cell_format.custom_format_identifier`, so a single definition can be reused by many cells."""
    identifier: str = Field(description="The unique identifier of the custom format. Cells refer to it through `Table.CellFormat.custom_format_identifier`.")
    format_name: str | None = Field(default=None, description="The name of the custom format as shown in Keynote's Data Format pop-up menu (for example, `My Sales Format`). It's optional and purely cosmetic.")
    format_string: str = Field(description="The format pattern, whose syntax depends on `format_type`. Number formats use placeholder tokens such as `#,###.00` or `#,###K`, date and time formats use Unicode date patterns such as `MMM d, yyyy`, and text formats use `@` as the value placeholder.")
    format_type: CustomFormatType = Field(default_factory=lambda: CustomFormatType.NUMBER, strict=False, description="The kind of value the format applies to. It determines how `format_string` is interpreted and which other properties are used.")
    number_format_data: NumberFormatData | None = Field(default=None, description="The parsed details of `format_string`, such as placeholder counts and the scale factor, used to render numeric custom formats. It's used only when `format_type` is `number`.")
    conditions: list[CustomFormatCondition] | None = Field(default=None, description="The conditional rules that swap in a different format string when the cell value meets a threshold condition, for example, to format negative values differently from positive ones. They're used only when `format_type` is `number`.")


class CustomFormatType(str, Enum):
    """The kind of value the custom format applies to.

    date_time — Custom format for date and time values; only `format_string` applies.
    number — Custom format for numeric values; `number_format_data` and `conditions` may be set.
    text — Custom format for text values; only `format_string` applies.
    """
    DATE_TIME = "date_time"
    NUMBER = "number"
    TEXT = "text"


@wire(
    "com.apple.apps.content-language.table.custom-format.number-format-data",
    version="1.0",
    fields=[
        ("scale_factor", (1, 0), "def"),
        ("fraction_accuracy", (1, 0), "opt"),
        ("interstitial_strings", (1, 0), "opt"),
        ("interstitial_string_insertion_indexes", (1, 0), "opt"),
        ("minimum_integer_width", (1, 0), "def"),
        ("decimal_width", (1, 0), "def"),
        ("number_of_non_space_integer_placeholder_digits", (1, 0), "def"),
        ("number_of_non_space_decimal_placeholder_digits", (1, 0), "def"),
        ("index_from_right_of_last_digit_placeholder", (1, 0), "def"),
        ("number_of_hash_decimal_placeholders", (1, 0), "def"),
        ("total_number_of_decimal_placeholders_in_format", (1, 0), "def"),
        ("currency_code", (1, 0), "opt"),
        ("show_thousands_separator", (1, 0), "def"),
        ("use_accounting_style", (1, 0), "def"),
        ("requires_fraction_replacement", (1, 0), "def"),
        ("format_contains_integer_token", (1, 0), "def"),
        ("is_complex_format", (1, 0), "def"),
    ],
)
class NumberFormatData(ObjectModel):
    """Details that the reader precomputes from a custom number format's format string.

They include placeholder counts, padding widths, the scale factor, and currency and separator settings, and they let a reader render the format without having to re-parse the `format_string`. They're shared between `Table.CustomFormat` and `Table.CustomFormat.CustomFormatCondition`."""
    scale_factor: float = Field(default=1, description="The multiplier applied to the value before it's rendered, used for unit-suffixed formats. For example, `#,###K` has a `scale_factor` of 0.001, so 1500 displays as “1.5K”, and a percentage uses 100. The default is 1.0, which means no scaling.")
    fraction_accuracy: Accuracy | None = Field(default=None, strict=False, description="The fraction display granularity. It's set only when the `format_string` includes a fraction token such as `# ?/?`.")
    interstitial_strings: list[str] | None = Field(default=None, description="The literal text fragments embedded in the format string between digit placeholders (for example, the `,`, the `K`, or any quoted text). They're indexed against `interstitial_string_insertion_indexes`.")
    interstitial_string_insertion_indexes: list[int] | None = Field(default=None, description="The digit positions at which each `interstitial_strings` entry is inserted. It parallels `interstitial_strings`, so their length and order must match.")
    minimum_integer_width: int = Field(default=0, description="The minimum number of integer digits to render. A value with fewer digits is padded with zeros; for example, `0000` displays 42 as “0042”.")
    decimal_width: int = Field(default=0, description="The number of decimal-side digit placeholders in the format string, which is the count of `0`, `#`, and `?` characters after the decimal point.")
    number_of_non_space_integer_placeholder_digits: int = Field(default=0, description="The number of integer-side digit placeholders that aren't space-padded (that is, `0` and `#` but not `?`). It's used to decide which digit positions are filled and which are left blank.")
    number_of_non_space_decimal_placeholder_digits: int = Field(default=0, description="The number of decimal-side digit placeholders that aren't space-padded (that is, `0` and `#` but not `?`).")
    index_from_right_of_last_digit_placeholder: int = Field(default=0, description="The position of the rightmost digit placeholder, counted from the right of the `format_string`. It's used to locate where digits stop and trailing literal text begins.")
    number_of_hash_decimal_placeholders: int = Field(default=0, description="The number of `#` placeholders after the decimal point, which suppress trailing zeros.")
    total_number_of_decimal_placeholders_in_format: int = Field(default=0, description="The total number of decimal-side digit placeholders: `0`, `#`, and `?` combined.")
    currency_code: str | None = Field(default=None, description="The ISO 4217 currency code, such as `USD` or `EUR`, when the `format_string` contains a currency symbol token. It determines the symbol that's shown.")
    show_thousands_separator: bool = Field(default=False, description="Whether the `format_string` includes a thousands separator (typically a `,` between integer placeholders).")
    use_accounting_style: bool = Field(default=False, description="Whether to render in accounting style: currency symbol left-aligned with padding, negative values in parentheses.")
    requires_fraction_replacement: bool = Field(default=False, description="Whether the `format_string` contains a fraction token, such as `?/?`, that must be replaced with a computed fraction at render time.")
    format_contains_integer_token: bool = Field(default=False, description="Whether the `format_string` includes at least one integer-side digit placeholder (`0`, `#`, or `?` before the decimal point).")
    is_complex_format: bool = Field(default=False, description="Whether the format needs custom rendering rather than a standard number formatter (for fractions, space-padded placeholders, or interstitial literal strings).")


@wire(
    "com.apple.apps.content-language.table.custom-format.custom-format-condition",
    version="1.0",
    fields=[
        ("condition_type", (1, 0), "req"),
        ("condition_value", (1, 0), "req"),
        ("format_string", (1, 0), "req"),
        ("number_format_data", (1, 0), "opt"),
    ],
)
class CustomFormatCondition(ObjectModel):
    """A conditional rule on a custom number format.

The rule swaps in a different `format_string` when the comparison of the cell value with `condition_value` is true, for example, to show negative values in parentheses."""
    condition_type: ConditionType = Field(strict=False, description="The comparison operator (`equal`, `less_than`, `greater_than`, `less_than_or_equal_to`, or `greater_than_or_equal_to`) applied between the cell value and `condition_value`.")
    condition_value: float = Field(description="The numeric threshold the cell value is compared against using `condition_type` (for example, `0` to test for negative values).")
    format_string: str = Field(description="The format pattern applied when the condition is true. It uses the same syntax as `Table.CustomFormat.format_string`.")
    number_format_data: NumberFormatData | None = Field(default=None, description="The precomputed parse details of `format_string`, used at render time when this condition is active. See `Table.CustomFormat.NumberFormatData`.")


class ConditionType(str, Enum):
    """A comparison operator used by a custom-format condition.

    equal — Cell value equals `condition_value`.
    greater_than — Cell value is greater than `condition_value`.
    greater_than_or_equal_to — Cell value is greater than or equal to `condition_value`.
    less_than — Cell value is less than `condition_value`.
    less_than_or_equal_to — Cell value is less than or equal to `condition_value`.
    """
    EQUAL = "equal"
    GREATER_THAN = "greater_than"
    GREATER_THAN_OR_EQUAL_TO = "greater_than_or_equal_to"
    LESS_THAN = "less_than"
    LESS_THAN_OR_EQUAL_TO = "less_than_or_equal_to"


@wire(
    "com.apple.apps.content-language.table.conditional-style-set",
    version="1.0",
    fields=[
        ("identifier", (1, 0), "req"),
        ("rules", (1, 0), "req"),
    ],
)
class ConditionalStyleSet(ObjectModel):
    """A shared set of conditional highlighting rules that multiple cells can reference."""
    identifier: str = Field(description="The unique identifier of the conditional style set.")
    rules: list[TableConditionalStyleSetRule] = Field(description="The ordered list of conditional highlighting rules, with a maximum of 15. The first rule whose predicate is true for the cell is applied, and the rules after it aren't.")


@wire(
    "com.apple.apps.content-language.table.conditional-style-set.rule",
    version="1.0",
    fields=[
        ("predicate", (1, 0), "req"),
        ("cell_style", (1, 0), "opt"),
        ("text_style", (1, 0), "opt"),
        ("preset_kind", (1, 0), "opt"),
    ],
)
class TableConditionalStyleSetRule(ObjectModel):
    """A single conditional highlighting rule with a predicate and styling to apply when the predicate is true."""
    predicate: Predicate = Field(description="The condition that determines when this rule applies.")
    cell_style: CellProperties | None = Field(default=None, description="The cell styling to apply when the predicate is true.")
    text_style: ParagraphProperties | None = Field(default=None, description="The text styling to apply when the predicate is true.")
    preset_kind: PresetKind | None = Field(default=None, strict=False, description="The built-in conditional-highlighting preset this rule represents. A named preset supplies the styling when `cell_style` and `text_style` are omitted; when either is present, it overrides the preset. `custom`, or no value at all, makes the rule fully custom.")


class PresetKind(str, Enum):
    """The built-in conditional-highlighting preset that a rule represents.

It lets readers associate the rule with a known visual style.

    blue_fill — Blue cell fill with white text.
    blue_text — Blue text preset.
    bold — Bold text preset.
    custom — A fully custom style, set entirely by `cell_style` and `text_style`.
    gray_text — Gray text preset.
    green_fill — Green cell fill with white text.
    green_text — Green text preset.
    italics — Italic text preset.
    orange_fill — Orange cell fill with white text.
    red_fill — Red cell fill with white text.
    red_text — Red text preset.
    teal_fill — Teal cell fill with white text.
    yellow_fill — Yellow cell fill with white text.
    """
    BLUE_FILL = "blue_fill"
    BLUE_TEXT = "blue_text"
    BOLD = "bold"
    CUSTOM = "custom"
    GRAY_TEXT = "gray_text"
    GREEN_FILL = "green_fill"
    GREEN_TEXT = "green_text"
    ITALICS = "italics"
    ORANGE_FILL = "orange_fill"
    RED_FILL = "red_fill"
    RED_TEXT = "red_text"
    TEAL_FILL = "teal_fill"
    YELLOW_FILL = "yellow_fill"


@wire(
    "com.apple.apps.content-language.table.transformation-info",
    version="1.0",
    fields=[
        ("base_table", (1, 0), "opt"),
        ("structure", (1, 0), "opt"),
        ("filter_set", (1, 0), "opt"),
        ("sort", (1, 0), "opt"),
    ],
)
class TransformationInfo(ObjectModel):
    """Information about how the reader derives a table.

In version 1.0, it holds the filter and sort rules applied to the table, in `filter_set` and `sort`, and the table's `content` holds the result. `base_table` and `structure` are reserved for categorized and pivot tables, which version 1.0 doesn't support."""
    base_table: Table | None = Field(default=None, description="The source data this table was derived from. It's reserved for categorized and pivot tables, which version 1.0 doesn't support. Its rows and columns carry their own identifiers, independent of the ones this table's `content`, `column_headers`, and `merges` use.")
    structure: Structure | None = Field(default=None, description="The structural shape of this table, reserved for categorized and pivot tables, which version 1.0 doesn't support. Without it, the table is a plain grid of rows and columns, which may still have `filter_set` or `sort`.")
    filter_set: FilterSet | None = Field(default=None, description="The filter configuration applied to this table, grouped by column. When it's present, rows whose `Table.Row.visibility_state` is `filtered` didn't pass the set.")
    sort: Sort | None = Field(default=None, description="The sort rules applied to this table, independent of `filter_set`. The rows in `content` are already in sorted order.")


@wire_union(
    "com.apple.apps.content-language.table.transformation-info.structure",
    version="1.0",
    cases=[
        ("categorized", (1, 0), False),
        ("pivot", (1, 0), False),
    ],
)
class Structure(TaggedUnionModel):
    """The structural transformation of a table.

It's reserved for categorized and pivot tables, which version 1.0 doesn't support. `filter_set` and `sort` are separate settings, and apply to a plain table without it."""
    categorized: CategoryRules | None = Field(default=None, description="A categorized table, which version 1.0 doesn't support. \n\n`CategoryRules` is reserved to describe how its rows are grouped.")
    pivot: PivotRules | None = Field(default=None, description="A pivot table, which version 1.0 doesn't support. \n\n`PivotRules` is reserved to describe its row, column, and value axes.")

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_StructureCase, ...]: ...

        def union_primary(self) -> _StructureCase | None: ...

        def union_primary_name(self) -> Literal["categorized", "pivot"] | None: ...


@wire(
    "com.apple.apps.content-language.table.filter-set",
    version="1.0",
    fields=[
        ("is_enabled", (1, 0), "def"),
        ("combine_mode", (1, 0), "def"),
        ("filters", (1, 0), "req"),
    ],
)
class FilterSet(ObjectModel):
    """The complete filter configuration for a table.

It holds the per-column filters and how they combine. Rows that don't pass the set stay in `content`, with `Table.Row.visibility_state` set to `filtered`."""
    is_enabled: bool = Field(default=True, description="Whether the filter set is enabled. When it's `false`, the filter set is preserved but every row passes, and no row has `Table.Row.visibility_state` set to `filtered`.")
    combine_mode: CombineMode = Field(default_factory=lambda: CombineMode.AND, strict=False, description="The way the per-column `filters` combine to decide whether a row passes the set. With `and`, the row must pass every column's filter; with `or`, the row passes if it passes any one column's filter. Within a single column's filter, the rules are always combined with OR: a row passes that column's filter when any of its rules match.")
    filters: list[Filter] = Field(description="The column filters, with at most one entry for each column. Each entry carries the rules that apply to its column. The order isn't significant.")


class CombineMode(str, Enum):
    """The rule for combining the per-column filters in a filter set to decide whether a row passes.

    and — Logical AND: a row passes only if it passes every column's filter.
    or — Logical OR: a row passes if it passes any column's filter.
    """
    AND = "and"
    OR = "or"


@wire(
    "com.apple.apps.content-language.table.filter-set.filter",
    version="1.0",
    fields=[
        ("column_identifier", (1, 0), "req"),
        ("rules", (1, 0), "req"),
    ],
)
class Filter(ObjectModel):
    """The filter for a single column.

It names the column being filtered and holds the ordered rules applied to its values. A row passes the filter when at least one of `rules` matches; the rules within a single-column filter are always combined with OR."""
    column_identifier: str = Field(description="The stable identifier of the column whose values every rule in this filter is evaluated against. It matches a `Table.ColumnHeader.column_identifier`.")
    rules: list[TableFilterSetFilterRule] = Field(description="The ordered list of predicates applied to the column's values. A row passes this filter when at least one rule's predicate matches; within a single-column filter, rules are implicitly combined with OR.")


@wire(
    "com.apple.apps.content-language.table.filter-set.filter.rule",
    version="1.0",
    fields=[
        ("predicate", (1, 0), "req"),
    ],
)
class TableFilterSetFilterRule(ObjectModel):
    """A single predicate evaluated against a row's value in the enclosing filter's column."""
    predicate: Predicate = Field(description="The predicate evaluated against the row's value in the enclosing filter's column. It can use any predicate type, including filter-specific cases such as `in_list` and `duplicates`.")


@wire(
    "com.apple.apps.content-language.table.sort",
    version="1.0",
    fields=[
        ("scope", (1, 0), "def"),
        ("rules", (1, 0), "req"),
    ],
)
class Sort(ObjectModel):
    """The sort rules that the reader applies to the rows of a table's content.

Those rows are already in sorted order. Header and footer rows are never sorted, regardless of `scope`."""
    scope: Scope = Field(default_factory=lambda: Scope.ENTIRE_TABLE, strict=False, description="The scope the user originally configured the sort with. It affects how the sort is applied if it's run again. It doesn't change the rendered `content`, which is already in sorted order.")
    rules: list[TableSortRule] = Field(description="The ordered list of sort rules. A rule's position in the array determines its precedence: index `0` is the primary sort key, index `1` is the tiebreaker, and so on.")


class Scope(str, Enum):
    """The scope of a sort, as the user originally configured it.

    entire_table — Sort applied to all body rows of the table.
    selected_rows — Sort applied only to the rows that were selected when the sort was created.
    """
    ENTIRE_TABLE = "entire_table"
    SELECTED_ROWS = "selected_rows"


@wire(
    "com.apple.apps.content-language.table.sort.rule",
    version="1.0",
    fields=[
        ("column_identifier", (1, 0), "req"),
        ("direction", (1, 0), "def"),
    ],
)
class TableSortRule(ObjectModel):
    """A single sort key."""
    column_identifier: str = Field(description="The stable identifier of the column the rule sorts by. It matches a `Table.ColumnHeader.column_identifier`.")
    direction: Direction = Field(default_factory=lambda: Direction.ASCENDING, strict=False, description="The sort direction for this key.")


class Direction(str, Enum):
    """A sort direction.

    ascending — Smallest or earliest first.
    descending — Largest or latest first.
    """
    ASCENDING = "ascending"
    DESCENDING = "descending"


@wire(
    "com.apple.apps.content-language.table.pivot-rules",
    version="1.0",
    fields=[
    ],
)
class PivotRules(ObjectModel):
    """A placeholder for a pivot table's rules, which version 1.0 doesn't support.

It's the value of `Table.TransformationInfo.Structure.pivot`, so that a later version can describe how rows, columns, and values map to the pivot's row axis, column axis, and value cells. It has no properties yet."""


@wire(
    "com.apple.apps.content-language.table.category-rules",
    version="1.0",
    fields=[
    ],
)
class CategoryRules(ObjectModel):
    """An empty object for a categorized table's rules, which version 1.0 doesn't support.

It's the value of the `Table.TransformationInfo.Structure.categorized` case, so that a later version can describe the grouping columns, subtotal aggregations, and group-sort settings. It has no properties yet."""


@wire(
    "com.apple.apps.content-language.textbox",
    version="1.0",
    fields=[
        ("identifier", (1, 0), "opt"),
        ("geometry", (1, 0), "opt"),
        ("aspect_ratio_locked", (1, 0), "def"),
        ("description", (1, 0), "opt"),
        ("title", (1, 0), "opt"),
        ("title_is_positioned_on_top", (1, 0), "def"),
        ("caption", (1, 0), "opt"),
        ("fill", (1, 0), "opt"),
        ("stroke", (1, 0), "def"),
        ("opacity", (1, 0), "def"),
        ("shadow", (1, 0), "ovr"),
        ("reflection", (1, 0), "opt"),
        ("layout_properties", (1, 0), "opt"),
        ("paragraph_properties", (1, 0), "opt"),
        ("text", (1, 0), "opt"),
    ],
)
class Textbox(ObjectModel):
    """A container for text that someone places directly on a slide or slide layout.

It takes its typography and background from the text-box presets rather than the shape presets. A `shape` can hold text too."""
    identifier: str | None = Field(default=None, description="An identifier for this object that other objects use to refer to it. This identifier must be unique across the whole document.")
    geometry: Geometry | None = Field(default=None, description="The object's position and size. If this value is absent, Keynote places the object automatically, with a default position and size for its kind.")
    aspect_ratio_locked: bool = Field(default=False, description="A Boolean value that indicates whether the object's width-to-height ratio is locked when the object resizes. The lock doesn't constrain the `geometry` property. If this property is absent, images, movies, and groups default to `true`, and other objects to `false`.")
    description: str | None = Field(default=None, description="The accessibility description for the object, read aloud by assistive technologies such as VoiceOver.")
    title: Label | None = Field(default=None, description="The object's title.")
    title_is_positioned_on_top: bool = Field(default=True, description="When `true`, the title appears above the object; when `false`, the title appears below the object, above the caption if there is one. Defaults to `true`. Keynote ignores this when the object has none, or when it's hidden with `Label.is_visible` set to `false`; Keynote places a hidden title above the object, where it appears when it shows again.")
    caption: Label | None = Field(default=None, description="The object's caption, which Keynote always places below the object. If a caption is off, you still write it out with `Label.is_visible` set to `false`, so having a value doesn't mean the caption shows.")
    fill: Fill | None = Field(default=None, description="The fill inside the text box. If absent, the fill from the text box's preset style is used.")
    stroke: Stroke = Field(default_factory=lambda: Stroke.model_validate({"line": {}}), description="The border around the text box's shape.")
    opacity: float = Field(default=1, description="The text box's opacity, in the range `0` to `1`.")
    shadow: Override[Shadow] = Field(default_factory=Override.not_set, description="The shadow shown beneath the text box.")
    reflection: Reflection | None = Field(default=None, description="The reflection shown for the text box.")
    layout_properties: LayoutProperties | None = Field(default=None, description="Layout overrides, such as insets and columns, for the text box's text.")
    paragraph_properties: ParagraphProperties | None = Field(default=None, description="Paragraph-level style, such as alignment and spacing, for the text box's text.")
    text: Text | None = Field(default=None, description="The text in the text box.")


@wire(
    "com.apple.apps.content-language.title-owning-generic",
    version="1.0",
    fields=[
        ("title", (1, 0), "opt"),
    ],
)
class GenericTitleOwning(ObjectModel):
    """An object with only the properties of title owning.

Every set of shared properties has one, to stand in for an object whose kind isn't recognized. Nothing in the format has the type `TitleOwning`, though, so this object never appears in a document; its properties appear only as part of the types that adopt `TitleOwning`."""
    title: Label | None = Field(default=None, description="The object's title.")


@wire_union(
    "com.apple.apps.content-language.title-owning",
    version="1.0",
    cases=[
        ("genericTitleOwning", (1, 0), False),
    ],
)
class TitleOwning(TaggedUnionModel):
    """The properties for defining a title that an object can display.

`table` and every type of `Chart` keep only the title's characters and its `Label.paragraph_properties`, so styling that varies from one run to the next inside `Label.text` is discarded."""
    genericTitleOwning: GenericTitleOwning | None = None

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_TitleOwningCase, ...]: ...

        def union_primary(self) -> _TitleOwningCase | None: ...

        def union_primary_name(self) -> Literal["genericTitleOwning"] | None: ...


@wire(
    "com.apple.apps.content-language.geometry",
    version="1.0",
    fields=[
        ("position", (1, 0), "req"),
        ("size", (1, 0), "req"),
        ("angle", (1, 0), "def"),
        ("flip_horizontally", (1, 0), "def"),
        ("width_valid", (1, 0), "def"),
        ("height_valid", (1, 0), "def"),
    ],
)
class Geometry(ObjectModel):
    """The bounding box in which an object is positioned.

`position` and `size` are in points. `position` is measured after rotation and `size` before it, so the object's center is the center of the rotated bounding box whose top-left corner is `position`."""
    position: Position = Field(description="The top-left corner of the object's axis-aligned bounding box, measured after rotation is applied. Coordinates are absolute within the containing slide, even for an object nested inside a group.")
    size: Size = Field(description="The width and height of the object's bounding box, in points, before rotation and flipping are applied. The width or height may be zero for objects without an intrinsic size, such as audio.")
    angle: float = Field(default=0, description="The rotation of the object's bounding box around its center, in degrees measured counterclockwise. It's written in the range `0` to `360` (exclusive); values outside that range are mapped to the equivalent angle within it.")
    flip_horizontally: bool = Field(default=False, description="Whether the object is mirrored across the vertical axis through its center, before rotation by `angle` is applied. A vertical flip is represented by combining a horizontal flip with a 180-degree rotation.")
    width_valid: bool = Field(default=True, description="Whether the object's width is valid. When `false` for an object that can compute its own width, the natural width that fits its text is used instead of the width in `size`.")
    height_valid: bool = Field(default=True, description="Whether the object's height is valid. When `false` for an object that can compute its own height, the natural height that fits its text is used instead of the height in `size`.")


@wire_union(
    "com.apple.apps.content-language.path",
    version="1.0",
    cases=[
        ("bezier", (1, 0), False),
    ],
)
class Path(TaggedUnionModel):
    """A path that traces the outline of a shape or of an image's mask.

Only one form is defined so far; later versions of the format can add others without changing how a shape or an image mask refers to its outline."""
    bezier: BezierPath | None = Field(default=None, description="A path described by an SVG path string. This is the only supported path representation.")

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_PathCase, ...]: ...

        def union_primary(self) -> _PathCase | None: ...

        def union_primary_name(self) -> Literal["bezier"] | None: ...


@wire(
    "com.apple.apps.content-language.path.bezier-path",
    version="1.0",
    fields=[
        ("path", (1, 0), "req"),
        ("space", (1, 0), "opt"),
    ],
)
class BezierPath(ObjectModel):
    """A path as an SVG path string, together with the coordinate space in which its points are expressed."""
    path: str = Field(description="The path as SVG path data: the value of the `d` attribute of a `<path>` element; it must be non-empty and must begin with a moveto command. Any standard path command is accepted when reading, but only absolute moveto, lineto, curveto, and closepath commands are produced when writing, so the exact command sequence isn't guaranteed to be preserved.")
    space: Rect | None = Field(default=None, description="If present, `path` is treated as relative to this rectangle, and then stretched proportionally to cover the bounding box of the owner's geometry (`Image.Mask.geometry` for an image mask) before the owner's flip and rotation apply. The owner's size and position then become the bounds of the mapped path, so when `space` differs from the path's tight bounds, the owner's written size and position aren't preserved, unless the owner sizes itself to fit its text. When absent, the path's tight bounds are used. When the owner has no geometry, `space` must equal those bounds, and the points are then absolute coordinates in the containing slide.")


@wire(
    "com.apple.apps.content-language.position",
    version="1.0",
    fields=[
        ("x", (1, 0), "req"),
        ("y", (1, 0), "req"),
    ],
)
class Position(ObjectModel):
    """A point, in points, in whichever coordinate space the property using it defines, measured downward from that space's top-left corner."""
    x: float = Field(description="The horizontal coordinate, in points, increasing to the right.")
    y: float = Field(description="The vertical coordinate, in points, increasing downward.")


@wire(
    "com.apple.apps.content-language.rect",
    version="1.0",
    fields=[
        ("position", (1, 0), "req"),
        ("size", (1, 0), "req"),
    ],
)
class Rect(ObjectModel):
    """An axis-aligned rectangle in whichever coordinate space the property using it defines."""
    position: Position = Field(description="The top-left corner of the rectangle.")
    size: Size = Field(description="The width and height of the rectangle.")


@wire(
    "com.apple.apps.content-language.size",
    version="1.0",
    fields=[
        ("width", (1, 0), "req"),
        ("height", (1, 0), "req"),
    ],
)
class Size(ObjectModel):
    """A width and height in whichever coordinate space the property using it defines.

A size is always unrotated; `Geometry` covers how an object's size relates to its rotation and its position."""
    width: float = Field(description="The width, in points.")
    height: float = Field(description="The height, in points.")


@wire(
    "com.apple.apps.content-language.keynote-theme",
    version="1.0",
    fields=[
        ("name", (1, 0), "opt"),
        ("locale", (1, 0), "opt"),
        ("slide_layouts", (1, 0), "opt"),
    ],
)
class KeynoteTheme(ObjectModel):
    """The Keynote theme a presentation is based on.

A theme provides the presentation's default slide layouts, styles, and background. It's chosen by its `name`, as shown in Keynote, and `slide_layouts` can replace the layouts it provides."""
    name: str | None = Field(default=None, description="The name of the theme to base the presentation on, as shown in Keynote's theme chooser (for example, `White` or `Gradient`). Because the name is localized, pair it with `locale`. Themes in My Themes are matched before built-in ones, and a name that matches nothing, like an absent name, falls back to the White theme. When Keynote exports a presentation whose custom theme isn't in My Themes, it writes `White` here, so the presentation opens in the White theme even where that theme is available.")
    locale: str | None = Field(default=None, description="The locale of the theme name given in `name`. If it's absent, the system locale is used. The value is a BCP 47 language identifier, such as `en_US` or `en-u-nu-thai-ca-buddhist`, or an ICU-style identifier, such as `en@calendar=buddhist;numbers=thai`.")
    slide_layouts: list[SlideLayout] | None = Field(default=None, min_length=1, description="The slide layouts to use in place of the ones the theme provides. If it's present, the list replaces the theme's own layouts entirely and must contain at least one entry. Each entry's `name` must be unique within the theme, because a slide selects its layout by identifier or name. If it's absent, it defaults to the theme's layouts.")


@wire(
    "com.apple.apps.content-language.presentation",
    version="1.0",
    fields=[
        ("theme", (1, 0), "opt"),
        ("slide_size", (1, 0), "opt"),
        ("slides", (1, 0), "req"),
        ("stylesheet", (1, 0), "opt"),
    ],
)
class Presentation(ObjectModel):
    """A document's root object, which describes one Keynote presentation."""
    theme: KeynoteTheme | None = Field(default=None, description="The theme that supplies the presentation's slide layouts, styles, and backgrounds. If it's absent, the default is Keynote's White theme.")
    slide_size: Size | None = Field(default=None, description="The size of every slide in the presentation, in points. If it's absent, a reader must supply the size, for example, from the theme, or reject the document.")
    slides: list[Slide] = Field(min_length=1, description="The presentation's slides, in presentation order. Grouping in the slide navigator is expressed by each slide's `Slide.depth` rather than by nesting arrays.")
    stylesheet: Stylesheet | None = Field(default=None, description="The presentation's named styles: character, paragraph, list, line, shape, text box, image, movie, and table styles. The presentation's objects and text can refer to these by their preset identifier. If this value is absent, Keynote uses the theme's styles.")


@wire(
    "com.apple.apps.content-language.slide",
    version="1.0",
    fields=[
        ("identifier", (1, 0), "opt"),
        ("layout", (1, 0), "opt"),
        ("contents", (1, 0), "opt"),
        ("background", (1, 0), "ovr"),
        ("depth", (1, 0), "opt"),
        ("note", (1, 0), "opt"),
    ],
)
class Slide(ObjectModel):
    """A slide in a presentation."""
    identifier: str | None = Field(default=None, description="The slide's identifier, which a link can use to point at the slide. Keynote writes a UUID string to this value; opening a presentation gives every slide a fresh identifier, so a value you supply for this identifier isn't kept.")
    layout: str | None = Field(default=None, description="The slide layout of the slide. Keynote matches this value against each layout's `SlideLayout.identifier`, then its `SlideLayout.name`. If nothing matches, it uses the theme's first layout and reports a warning; if it's absent, it uses the first layout.")
    contents: list[SlideObject] | None = Field(default=None, description="The objects on the slide, ordered back to front, with the first one farthest back. This list includes objects that belong to the slide's layout, with `SlideObject.source_kind` set to `layout`, only when that layout sets `SlideLayout.slide_objects_layer_with_layout`; otherwise, this list doesn't include those objects, and the slide draws them behind everything in this list.")
    background: Override[SlideBackground] = Field(default_factory=Override.not_set, description="Define the slide background as a color, gradient, or image, which overrides the default background inherited from the layout. A value of `null` removes the background entirely; if you omit the key, the slide retains the background associated with the specified layout.")
    depth: int | None = Field(default=None, description="The slide's indentation level in the slide navigator, on a scale of `1` to `6`. A slide indented deeper than the one before it becomes its child. Keynote clamps rather than rejects a depth more than `6` or more than one level below the preceding slide, and the first slide is always at the top level. The default indentation level is `1`.")
    note: Text | None = Field(default=None, description="The slide's presenter notes contains only text. Keynote removes inline objects with a warning, except for connection lines and non-table objects with an identifier, which prevent the document from loading. Image bullets whose image is missing and inline objects that aren't importable also halt loading, in contrast to slides, where they merely remove the text box. A paragraph that lacks a `Paragraph.style` defaults to the theme's Presenter Notes style, or the presentation's custom style if previously overridden, and Keynote omits `Paragraph.style` for paragraphs that already use the presentation's Presenter Notes style.")


@wire_union(
    "com.apple.apps.content-language.slide-background",
    version="1.0",
    cases=[
        ("standard", (1, 0), False),
    ],
)
class SlideBackground(TaggedUnionModel):
    """The background of a slide."""
    standard: Fill | None = Field(default=None, description="A static color, gradient, or image fill. When Keynote exports a presentation, it writes a dynamic background as this case too: an image fill holding one still frame of it, or a color fill when that frame can't be drawn.")

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_SlideBackgroundCase, ...]: ...

        def union_primary(self) -> _SlideBackgroundCase | None: ...

        def union_primary_name(self) -> Literal["standard"] | None: ...


@wire(
    "com.apple.apps.content-language.slide-layout",
    version="1.1",
    fields=[
        ("identifier", (1, 0), "opt"),
        ("name", (1, 0), "req"),
        ("contents", (1, 0), "opt"),
        ("background", (1, 0), "opt"),
        ("slide_objects_layer_with_layout", (1, 1), "def"),
    ],
)
class SlideLayout(ObjectModel):
    """A slide layout in a Keynote theme.

It provides the default arrangement of placeholders, styles, and background for the slides that refer to it by identifier or name."""
    identifier: str | None = Field(default=None, description="The layout's identifier, which `Slide.layout` is matched against before `name`. Keynote writes a UUID string here, but any string is accepted. Keep it unique within the theme, since two layouts sharing one can't be told apart.")
    name: str = Field(description="The name of the layout as shown in Keynote's layout list, such as `Title & Subtitle`. It's matched by `Slide.layout` when no identifier matches. Keep it unique within the theme, since duplicate names can't be differentiated.")
    contents: list[SlideObject] | None = Field(default=None, description="The objects on the layout, ordered back to front (the first one is farthest back).")
    background: SlideBackground | None = Field(default=None, description="The layout's background. Slides based on this layout inherit it unless they specify their own background. A background that can't be read (for example, a background image that is missing or isn't a valid image) removes the whole layout, including everything on it, and a warning is reported; slides that would have used the layout are given a different one (see `Slide.layout`).")
    slide_objects_layer_with_layout: bool = Field(default=False, description="Whether slides using this layout let their own objects layer with the layout's objects (`true`), or always show their objects in front of every layout object (`false`). When `false`, all layout objects are drawn behind all slide objects regardless of `contents` order.")


@wire(
    "com.apple.apps.content-language.slide-object",
    version="1.0",
    fields=[
        ("instructional_text", (1, 0), "opt"),
        ("is_locked", (1, 0), "def"),
        ("object", (1, 0), "req"),
        ("placeholder_info", (1, 0), "opt"),
        ("source_kind", (1, 0), "opt"),
    ],
)
class SlideObject(ObjectModel):
    """An object on a slide or slide layout, with slide-specific information about it."""
    instructional_text: str | None = Field(default=None, description="The placeholder text shown in the object while it's empty, such as “Title Text” or “Double-click to edit.” It stops showing as soon as the object has content of its own.")
    is_locked: bool = Field(default=False, description="Whether the object is locked to prevent editing. It's ignored when the document is read, so the object always opens unlocked.")
    object: CanvasObject = Field(description="The object itself, such as a shape, text box, image, movie, audio clip, table, chart, connection line, or group.")
    placeholder_info: PlaceholderInfo | None = Field(default=None, description="The placeholder the object acts as, predefined or tagged. Setting it marks the object as a placeholder. A tagged placeholder is always shown, and `PlaceholderDefinition` gives the restrictions on a predefined one. When several objects use the same predefined placeholder, only the first is kept and the rest are dropped from the slide without a warning.")
    source_kind: SourceKind | None = Field(default=None, strict=False, description="The source of the object. If it's absent, the object is treated as the slide's own. For the `layout` kind, the object's identifier is matched against the corresponding object in the layout the slide names; an identifier that matches nothing there creates a second, slide-owned copy alongside the layout's object.")


@wire_union(
    "com.apple.apps.content-language.slide-object.placeholder-info",
    version="1.0",
    cases=[
        ("defined", (1, 0), False),
        ("tagged", (1, 0), False),
    ],
)
class PlaceholderInfo(TaggedUnionModel):
    """The placeholder an object acts as on its slide.

It's either one of the predefined placeholders that a layout can turn on and off, or a placeholder identified by a custom tag."""
    defined: PlaceholderDefinition | None = Field(default=None, description="One of the predefined placeholders that someone can turn on and off on any slide.")
    tagged: str | None = Field(default=None, description="A placeholder that has a tag associated with it. It can be an image, a movie, a shape, or a text box.")

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_PlaceholderInfoCase, ...]: ...

        def union_primary(self) -> _PlaceholderInfoCase | None: ...

        def union_primary_name(self) -> Literal["defined", "tagged"] | None: ...


@wire(
    "com.apple.apps.content-language.slide-object.placeholder-info.placeholder-definition",
    version="1.0",
    fields=[
        ("kind", (1, 0), "req"),
        ("is_visible", (1, 0), "def"),
    ],
)
class PlaceholderDefinition(ObjectModel):
    """The predefined placeholder an object fills.

Only a shape or a text box is accepted, and one with `is_visible` set to `false` is still used as the placeholder, keeping its geometry, style, and text. An object of any other kind leaves the placeholder unfilled: it stays on the slide as ordinary content while `is_visible` is `true`, and is dropped altogether when it's `false`."""
    kind: SlideObjectPlaceholderInfoPlaceholderDefinitionKind = Field(strict=False, description="The predefined placeholder this object fills.")
    is_visible: bool = Field(default=True, description="Whether this placeholder is turned on for the slide. The default is `true`. When it's `false`, the entry is still listed in `Slide.contents`, with its geometry and text, but isn't shown.")


class SlideObjectPlaceholderInfoPlaceholderDefinitionKind(str, Enum):
    """The predefined placeholders that someone can turn on and off on any slide.

    body — The slide's main body text.
    object — The object placeholder, a reserved area in which someone can place media or other content.
    slide_number — The slide number, which updates automatically.
    title — The slide's title text.
    """
    BODY = "body"
    OBJECT = "object"
    SLIDE_NUMBER = "slide_number"
    TITLE = "title"


class SourceKind(str, Enum):
    """The source of an object.

`layout` means it appears on the slide because it belongs to the slide's layout; `placeholder` means it appears because the corresponding layout placeholder was turned on; and `user` means someone added it to the slide directly."""
    LAYOUT = "layout"
    PLACEHOLDER = "placeholder"
    USER = "user"


@wire_union(
    "com.apple.apps.content-language.resource",
    version="1.0",
    cases=[
        ("base64_encoded", (1, 0), False),
        ("indirect", (1, 0), False),
    ],
)
class Resource(TaggedUnionModel):
    """The data used for image, movie, and audio media, and for image fills and image bullets.

Resources can be carried inline (`base64_encoded`), which makes the JSON self-contained, or refer to files stored alongside the JSON in the archive (`indirect`), which keeps large assets out of the JSON but can be read only when those files are present. What happens when bytes can't be read (an `indirect` name that matches no file, or a `base64_encoded` string that isn't valid Base64) depends on where the resource is used. An image, movie, or audio object whose media can't be read is dropped with a warning, though a `Movie.poster_image` that can't be read doesn't drop the movie. Such an object placed inline in the text of a text box or shape removes the whole text box or shape, including all of its text, and so does an image bullet in that text. An image fill in a `SlideLayout.background` removes that whole layout, and one anywhere else is left out. An image bullet or such an object in a slide's presenter notes (`Slide.note`), or an image bullet in a list style in `Presentation.stylesheet`, stops the document from loading."""
    base64_encoded: Base64EncodedResource | None = Field(default=None, description="Data carried inline in the resource.")
    indirect: IndirectResource | None = Field(default=None, description="Data stored in a separate file, identified by name rather than carried in the resource.")

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_ResourceCase, ...]: ...

        def union_primary(self) -> _ResourceCase | None: ...

        def union_primary_name(self) -> Literal["base64_encoded", "indirect"] | None: ...


@wire(
    "com.apple.apps.content-language.resource.indirect-resource",
    version="2.0",
    fields=[
        ("identifier", (1, 0), "opt"),
        ("filename", (1, 0), "req"),
        ("premium_resource_info", (2, 0), "opt"),
    ],
)
class IndirectResource(ObjectModel):
    """A resource whose bytes are stored in a separate file rather than in the JSON.

In a `.keyx` file, the `identifier` names a file in the archive's `Data` directory. A name the reader can't resolve is an error rather than an empty asset; what happens then depends on where the resource is used (see `Resource`)."""
    identifier: str | None = Field(default=None, description="The name of the file inside the archive's `Data` directory that contains the data for this resource. If missing, `filename` is used as the identifier. When no data can be found for it, the resource can't be loaded (see `Resource` for what happens then).")
    filename: str = Field(description="The filename shown for the resource, including its filename extension, in the user interface. This value need not match `identifier`; see `identifier` for what happens when that's absent. The extension is significant: it's preserved when the resource is stored.")
    premium_resource_info: PremiumResourceInfo | None = Field(default=None, description="Additional metadata for premium resources from the Content Hub.")


@wire(
    "com.apple.apps.content-language.resource.base64-encoded-resource",
    version="2.0",
    fields=[
        ("string", (1, 0), "req"),
        ("filename", (1, 0), "req"),
        ("premium_resource_info", (2, 0), "opt"),
    ],
)
class Base64EncodedResource(ObjectModel):
    """A resource whose bytes are carried as Base64 in the resource itself, so the JSON needs no companion files.

If `string` doesn't decode, what happens depends on where the resource is used (see `Resource`)."""
    string: str = Field(description="The resource's bytes as a Base64-encoded string. If the string can't be decoded, reading fails.")
    filename: str = Field(description="The filename shown for the resource, including its filename extension, in the user interface. It becomes the name of the resource decoded from `string`.")
    premium_resource_info: PremiumResourceInfo | None = Field(default=None, description="Additional metadata for premium resources from the Content Hub.")


@wire(
    "com.apple.apps.content-language.resource.premium-resource-info",
    version="1.0",
    fields=[
        ("asset_uuid", (1, 0), "req"),
        ("is_derived_asset", (1, 0), "req"),
        ("may_need_watermark", (1, 0), "req"),
    ],
)
class PremiumResourceInfo(ObjectModel):
    """Additional metadata that marks a resource as premium content that the reader originally sourced from the content hub.

It carries the watermarking terms attached to the resource."""
    asset_uuid: str = Field(description="The UUID of the premium resource's asset in the media library, written as a standard UUID string. If the value isn't a valid UUID, it's ignored, and the resource then loses its media library association and its watermark information.")
    is_derived_asset: bool = Field(description="Whether the resource was edited or otherwise derived from its original Content Hub data; if `false`, it's the unmodified original.")
    may_need_watermark: bool = Field(description="Whether the resource may be shown with a watermark for customers without an active subscription. When the document is read, the resource is treated as newly added, so such a customer can see a watermark on media that the original presentation showed without one.")


@wire(
    "com.apple.apps.content-language.stylesheet",
    version="1.0",
    fields=[
        ("line_styles", (1, 0), "opt"),
        ("shape_styles", (1, 0), "opt"),
        ("textbox_styles", (1, 0), "opt"),
        ("image_styles", (1, 0), "opt"),
        ("movie_styles", (1, 0), "opt"),
        ("table_style_collections", (1, 0), "opt"),
        ("character_styles", (1, 0), "opt"),
        ("paragraph_styles", (1, 0), "opt"),
        ("list_styles", (1, 0), "opt"),
    ],
)
class Stylesheet(ObjectModel):
    """A collection of styles to use as presets for various objects in a document."""
    line_styles: list[ShapeStyle] | None = Field(default=None, description="The preset styles that you can apply to lines and connection lines. If you omit this property, it defaults to the document's built-in line styles.")
    shape_styles: list[ShapeStyle] | None = Field(default=None, description="The preset styles that you can apply to shapes. If you omit this property, it defaults to the document's built-in shape styles.")
    textbox_styles: list[ShapeStyle] | None = Field(default=None, description="The preset styles that you can apply to text boxes. If you omit this property, it defaults to the document's built-in text box styles.")
    image_styles: list[MediaStyle] | None = Field(default=None, description="The preset styles that you can apply to images. If you omit this property, it defaults to the document's built-in image styles.")
    movie_styles: list[MediaStyle] | None = Field(default=None, description="The preset styles that you can apply to movies. If you omit this property, it defaults to the document's built-in movie styles.")
    table_style_collections: list[TableStyleCollection] | None = Field(default=None, description="The preset table styles. Each entry groups the styles that make up one table style preset: the table as a whole, its cell borders, and the cell and text styles that the body, header rows, header columns, and footer rows use.")
    character_styles: list[CharacterStyle] | None = Field(default=None, description="The preset character styles that you can apply to a range of text. If you omit this property, it defaults to the document's built-in character styles.")
    paragraph_styles: list[ParagraphStyle] | None = Field(default=None, description="The preset paragraph styles that you can apply to whole paragraphs. If you omit this property, it defaults to the document's built-in paragraph styles.")
    list_styles: list[ListStyle] | None = Field(default=None, description="The preset list styles, which control bullets and numbering. If you omit this property, it defaults to the document's built-in list styles.")


@wire(
    "com.apple.apps.content-language.stylesheet.shape-style",
    version="1.0",
    fields=[
        ("name", (1, 0), "opt"),
        ("properties", (1, 0), "req"),
    ],
)
class ShapeStyle(ObjectModel):
    """A preset for shapes, text boxes, lines, and connection lines.

It covers fill, border, opacity, shadow, reflection, and the default layout of the text inside."""
    name: str | None = Field(default=None, description="The name of the style as shown in Keynote. It's absent for styles that have no name.")
    properties: ShapeProperties = Field(description="The properties that make up the style. When a `preset_identifier` is present, the entry is only a reference and carries no property values; otherwise, this is the style's complete set of resolved properties.")


@wire(
    "com.apple.apps.content-language.stylesheet.shape-style.shape-properties",
    version="1.0",
    fields=[
        ("stroke", (1, 0), "ovr"),
        ("opacity", (1, 0), "ovr"),
        ("reflection", (1, 0), "ovr"),
        ("shadow", (1, 0), "ovr"),
        ("fill", (1, 0), "ovr"),
        ("head", (1, 0), "ovr"),
        ("tail", (1, 0), "ovr"),
        ("layout_properties", (1, 0), "opt"),
        ("paragraph_properties", (1, 0), "opt"),
    ],
)
class ShapeProperties(ObjectModel):
    """The appearance that a shape style applies."""
    stroke: Override[Stroke] = Field(default_factory=Override.not_set, description="The stroke or border drawn around the shape or, for a line or connection line, the stroke drawn along the line itself.")
    opacity: Override[float] = Field(default_factory=Override.not_set, description="The opacity of the shape, in the range `0` to `1`.")
    reflection: Override[Reflection] = Field(default_factory=Override.not_set, description="The reflection of the shape.")
    shadow: Override[Shadow] = Field(default_factory=Override.not_set, description="The shadow cast behind the shape.")
    fill: Override[Fill] = Field(default_factory=Override.not_set, description="The fill used to decorate the interior of the shape. `null` clears the fill; if the key is omitted, the fill is inherited, and with no fill to inherit, the shape is unfilled.")
    head: Override[LineEnd] = Field(default_factory=Override.not_set, description="The head end of a line or connection line, drawn at its end point.")
    tail: Override[LineEnd] = Field(default_factory=Override.not_set, description="The tail end of a line or connection line, drawn at its start point.")
    layout_properties: LayoutProperties | None = Field(default=None, description="A set of properties defining how text is laid out inside the shape: padding, columns, and vertical alignment. It's absent when the style sets none of these.")
    paragraph_properties: ParagraphProperties | None = Field(default=None, description="A set of properties that define the default paragraph formatting for text inside the shape. It's absent when the style carries no default.")


@wire(
    "com.apple.apps.content-language.stylesheet.media-style",
    version="1.0",
    fields=[
        ("name", (1, 0), "opt"),
        ("properties", (1, 0), "req"),
    ],
)
class MediaStyle(ObjectModel):
    """A preset for images and movies.

It covers border, opacity, shadow, and reflection."""
    name: str | None = Field(default=None, description="The name of the style as shown in Keynote. It's absent for styles that have no name.")
    properties: MediaProperties = Field(description="The properties that make up the style. When a `preset_identifier` is present, the entry is only a reference and carries no property values; otherwise, this is the style's complete set of resolved properties.")


@wire(
    "com.apple.apps.content-language.stylesheet.media-style.media-properties",
    version="1.0",
    fields=[
        ("stroke", (1, 0), "ovr"),
        ("opacity", (1, 0), "ovr"),
        ("reflection", (1, 0), "ovr"),
        ("shadow", (1, 0), "ovr"),
    ],
)
class MediaProperties(ObjectModel):
    """The appearance that a media style applies."""
    stroke: Override[Stroke] = Field(default_factory=Override.not_set, description="The stroke or border drawn around an image or movie.")
    opacity: Override[float] = Field(default_factory=Override.not_set, description="The opacity of the image or movie, in the range `0` to `1`.")
    reflection: Override[Reflection] = Field(default_factory=Override.not_set, description="The reflection of the image or movie.")
    shadow: Override[Shadow] = Field(default_factory=Override.not_set, description="The shadow cast behind the image or movie.")


@wire(
    "com.apple.apps.content-language.stylesheet.table-style-collection",
    version="1.0",
    fields=[
        ("table_name_shape_style", (1, 0), "opt"),
        ("table_name_style", (1, 0), "opt"),
        ("overall_style", (1, 0), "req"),
        ("body_cell_style", (1, 0), "req"),
        ("body_text_style", (1, 0), "req"),
        ("body_stroke_style", (1, 0), "req"),
        ("header_row_cell_style", (1, 0), "req"),
        ("header_row_text_style", (1, 0), "req"),
        ("header_row_stroke_style", (1, 0), "req"),
        ("header_column_cell_style", (1, 0), "req"),
        ("header_column_text_style", (1, 0), "req"),
        ("header_column_stroke_style", (1, 0), "req"),
        ("footer_row_cell_style", (1, 0), "req"),
        ("footer_row_text_style", (1, 0), "req"),
        ("footer_row_stroke_style", (1, 0), "req"),
        ("category_level1_cell_style", (1, 0), "opt"),
        ("category_level1_text_style", (1, 0), "opt"),
        ("category_level2_cell_style", (1, 0), "opt"),
        ("category_level2_text_style", (1, 0), "opt"),
        ("category_level3_cell_style", (1, 0), "opt"),
        ("category_level3_text_style", (1, 0), "opt"),
        ("category_level4_cell_style", (1, 0), "opt"),
        ("category_level4_text_style", (1, 0), "opt"),
        ("category_level5_cell_style", (1, 0), "opt"),
        ("category_level5_text_style", (1, 0), "opt"),
        ("label_level1_cell_style", (1, 0), "opt"),
        ("label_level1_text_style", (1, 0), "opt"),
        ("label_level2_cell_style", (1, 0), "opt"),
        ("label_level2_text_style", (1, 0), "opt"),
        ("label_level3_cell_style", (1, 0), "opt"),
        ("label_level3_text_style", (1, 0), "opt"),
        ("label_level4_cell_style", (1, 0), "opt"),
        ("label_level4_text_style", (1, 0), "opt"),
        ("label_level5_cell_style", (1, 0), "opt"),
        ("label_level5_text_style", (1, 0), "opt"),
        ("pivot_body_summary_row_cell_style", (1, 0), "opt"),
        ("pivot_body_summary_column_cell_style", (1, 0), "opt"),
        ("pivot_header_column_summary_cell_style", (1, 0), "opt"),
    ],
)
class TableStyleCollection(ObjectModel):
    """The styles that make up one table style preset.

Each style applies to one region of a table, and the category and label styles are numbered by grouping depth, with `1` the outermost. The category and pivot styles apply to categorized and pivot tables, which version 1.0 doesn't support. An omitted style is filled in from the collection's other styles."""
    table_name_shape_style: ShapeStyle | None = None
    table_name_style: ParagraphStyle | None = None
    overall_style: OverallStyle
    body_cell_style: CellStyle
    body_text_style: ParagraphStyle
    body_stroke_style: BodyStrokeStyle
    header_row_cell_style: CellStyle
    header_row_text_style: ParagraphStyle
    header_row_stroke_style: HeaderFooterStrokeStyle
    header_column_cell_style: CellStyle
    header_column_text_style: ParagraphStyle
    header_column_stroke_style: HeaderFooterStrokeStyle
    footer_row_cell_style: CellStyle
    footer_row_text_style: ParagraphStyle
    footer_row_stroke_style: HeaderFooterStrokeStyle
    category_level1_cell_style: CellStyle | None = Field(default=None, description="The cell styling for the group rows of a categorized table at grouping depth 1.")
    category_level1_text_style: ParagraphStyle | None = Field(default=None, description="The text style used in the group rows of a categorized table at grouping depth 1.")
    category_level2_cell_style: CellStyle | None = Field(default=None, description="The cell styling for the group rows of a categorized table at grouping depth 2.")
    category_level2_text_style: ParagraphStyle | None = Field(default=None, description="The text style used in the group rows of a categorized table at grouping depth 2.")
    category_level3_cell_style: CellStyle | None = Field(default=None, description="The cell styling for the group rows of a categorized table at grouping depth 3.")
    category_level3_text_style: ParagraphStyle | None = Field(default=None, description="The text style used in the group rows of a categorized table at grouping depth 3.")
    category_level4_cell_style: CellStyle | None = Field(default=None, description="The cell styling for the group rows of a categorized table at grouping depth 4.")
    category_level4_text_style: ParagraphStyle | None = Field(default=None, description="The text style used in the group rows of a categorized table at grouping depth 4.")
    category_level5_cell_style: CellStyle | None = Field(default=None, description="The cell styling for the group rows of a categorized table at grouping depth 5.")
    category_level5_text_style: ParagraphStyle | None = Field(default=None, description="The text style used in the group rows of a categorized table at grouping depth 5.")
    label_level1_cell_style: CellStyle | None = Field(default=None, description="The cell styling for the row of captions naming a group's summary values, at grouping depth 1.")
    label_level1_text_style: ParagraphStyle | None = Field(default=None, description="The text style used in the row of captions naming a group's summary values, at grouping depth 1.")
    label_level2_cell_style: CellStyle | None = Field(default=None, description="The cell styling for the row of captions naming a group's summary values, at grouping depth 2.")
    label_level2_text_style: ParagraphStyle | None = Field(default=None, description="The text style used in the row of captions naming a group's summary values, at grouping depth 2.")
    label_level3_cell_style: CellStyle | None = Field(default=None, description="The cell styling for the row of captions naming a group's summary values, at grouping depth 3.")
    label_level3_text_style: ParagraphStyle | None = Field(default=None, description="The text style used in the row of captions naming a group's summary values, at grouping depth 3.")
    label_level4_cell_style: CellStyle | None = Field(default=None, description="The cell styling for the row of captions naming a group's summary values, at grouping depth 4.")
    label_level4_text_style: ParagraphStyle | None = Field(default=None, description="The text style used in the row of captions naming a group's summary values, at grouping depth 4.")
    label_level5_cell_style: CellStyle | None = Field(default=None, description="The cell styling for the row of captions naming a group's summary values, at grouping depth 5.")
    label_level5_text_style: ParagraphStyle | None = Field(default=None, description="The text style used in the row of captions naming a group's summary values, at grouping depth 5.")
    pivot_body_summary_row_cell_style: CellStyle | None = Field(default=None, description="The cell styling for the subtotal rows in the body of a pivot table.")
    pivot_body_summary_column_cell_style: CellStyle | None = Field(default=None, description="The cell styling for the subtotal columns in the body of a pivot table.")
    pivot_header_column_summary_cell_style: CellStyle | None = Field(default=None, description="The cell styling for the header column cells that label a pivot table's subtotal rows.")


@wire(
    "com.apple.apps.content-language.stylesheet.table-style-collection.overall-style",
    version="1.0",
    fields=[
        ("name", (1, 0), "opt"),
        ("properties", (1, 0), "req"),
    ],
)
class OverallStyle(ObjectModel):
    """A table style's table-wide settings, with an optional name."""
    name: str | None = None
    properties: OverallProperties


@wire(
    "com.apple.apps.content-language.stylesheet.table-style-collection.cell-style",
    version="1.0",
    fields=[
        ("name", (1, 0), "opt"),
        ("properties", (1, 0), "req"),
    ],
)
class CellStyle(ObjectModel):
    """Cell styling for one region of a table, with an optional name."""
    name: str | None = None
    properties: CellProperties


@wire(
    "com.apple.apps.content-language.stylesheet.table-style-collection.body-stroke-style",
    version="1.0",
    fields=[
        ("name", (1, 0), "opt"),
        ("properties", (1, 0), "req"),
    ],
)
class BodyStrokeStyle(ObjectModel):
    """Gridlines and outer borders for the body of a table, with an optional name."""
    name: str | None = None
    properties: BodyStrokeProperties


@wire(
    "com.apple.apps.content-language.stylesheet.table-style-collection.header-footer-stroke-style",
    version="1.0",
    fields=[
        ("name", (1, 0), "opt"),
        ("properties", (1, 0), "req"),
    ],
)
class HeaderFooterStrokeStyle(ObjectModel):
    """Gridlines, outer border, and separator line for one header or footer region of a table, with an optional name."""
    name: str | None = None
    properties: HeaderFooterStrokeProperties


@wire(
    "com.apple.apps.content-language.stylesheet.paragraph-style",
    version="1.0",
    fields=[
        ("name", (1, 0), "opt"),
        ("properties", (1, 0), "req"),
    ],
)
class ParagraphStyle(ObjectModel):
    """A preset that the reader applies to whole paragraphs, such as a title or body style."""
    name: str | None = Field(default=None, description="The name of the style as shown in Keynote. It's absent for styles that have no name.")
    properties: ParagraphProperties = Field(description="The properties that make up the style. When a `preset_identifier` is present, the entry is only a reference and carries no property values; otherwise, this is the style's complete set of resolved properties.")


@wire(
    "com.apple.apps.content-language.stylesheet.character-style",
    version="1.0",
    fields=[
        ("name", (1, 0), "opt"),
        ("properties", (1, 0), "req"),
    ],
)
class CharacterStyle(ObjectModel):
    """A preset that the reader applies to a range of text within a paragraph."""
    name: str | None = Field(default=None, description="The name of the style as shown in Keynote. It's absent for styles that have no name.")
    properties: CharacterProperties = Field(description="The properties that make up the style. When a `preset_identifier` is present, the entry is only a reference and carries no property values; otherwise, this is the style's complete set of resolved properties.")


@wire(
    "com.apple.apps.content-language.stylesheet.list-style",
    version="1.0",
    fields=[
        ("name", (1, 0), "opt"),
        ("properties", (1, 0), "req"),
    ],
)
class ListStyle(ObjectModel):
    """A preset for bullets and numbering."""
    name: str | None = Field(default=None, description="The name of the style as shown in Keynote. It's absent for styles that have no name.")
    properties: ListProperties = Field(description="The properties that make up the style. When a `preset_identifier` is present, the entry is only a reference and carries no property values; otherwise, this is the style's complete set of resolved properties.")


@wire(
    "com.apple.apps.content-language.character-properties",
    version="1.0",
    fields=[
        ("background_color", (1, 0), "ovr"),
        ("baseline", (1, 0), "ovr"),
        ("baseline_shift", (1, 0), "ovr"),
        ("bold", (1, 0), "ovr"),
        ("capitalization", (1, 0), "ovr"),
        ("character_fill", (1, 0), "ovr"),
        ("character_fill_should_fill_container", (1, 0), "ovr"),
        ("compatibility_font_name", (1, 0), "ovr"),
        ("emphasis_mark", (1, 0), "ovr"),
        ("font_features", (1, 0), "ovr"),
        ("font_name", (1, 0), "ovr"),
        ("font_size", (1, 0), "ovr"),
        ("is_named_point_size", (1, 0), "ovr"),
        ("italic", (1, 0), "ovr"),
        ("language", (1, 0), "ovr"),
        ("ligatures", (1, 0), "ovr"),
        ("shadow", (1, 0), "ovr"),
        ("strikethrough", (1, 0), "ovr"),
        ("strikethrough_color", (1, 0), "ovr"),
        ("strikethrough_width", (1, 0), "ovr"),
        ("stroke", (1, 0), "ovr"),
        ("tracking", (1, 0), "ovr"),
        ("underline", (1, 0), "ovr"),
        ("underline_color", (1, 0), "ovr"),
        ("word_strikethrough", (1, 0), "ovr"),
        ("word_underline", (1, 0), "ovr"),
        ("writing_direction", (1, 0), "ovr"),
    ],
)
class CharacterProperties(ObjectModel):
    """The character-level properties of text.

A `preset_identifier` here is matched against the document stylesheet's character styles before the presets in `presets.json`, and an identifier that matches neither is silently ignored. An omitted property is inherited from that preset, from the enclosing style's parent chain, and, for a text run, from the paragraph style in effect; a `null` clears it instead."""
    background_color: Override[Color] = Field(default_factory=Override.not_set, description="The background color of the text.")
    baseline: Override[BaselineType] = Field(default_factory=Override.not_set, description="The superscript or subscript setting of the text.")
    baseline_shift: Override[float] = Field(default_factory=Override.not_set, description="The number of points to shift the baseline; a positive value shifts it up and a negative value shifts it down.")
    bold: Override[bool] = Field(default_factory=Override.not_set, description="Whether the text is bold.")
    capitalization: Override[CapitalizationType] = Field(default_factory=Override.not_set, description="The capitalization of the text: All Caps, Small Caps, Start Case, or Title Case.")
    character_fill: Override[Fill] = Field(default_factory=Override.not_set, description="The fill inside the characters, which can be a color, a gradient, or an image. The outline around the characters comes from `stroke` instead.")
    character_fill_should_fill_container: Override[bool] = Field(default_factory=Override.not_set, description="Whether a gradient `character_fill` is measured across the whole text container rather than across just the text it fills. It affects only a gradient fill, and the default is `false`.")
    compatibility_font_name: Override[str] = Field(default_factory=Override.not_set, description="The original font name, carried over from a PowerPoint presentation whose font was substituted, so that the name can be restored if the presentation is exported back to PowerPoint. It's absent when no substitution took place.")
    emphasis_mark: Override[str] = Field(default_factory=Override.not_set, description="The dot added to the sides of characters for emphasis in Japanese text (boten).")
    font_features: Override[list[FontFeaturesType]] = Field(default_factory=Override.not_set, description="The font features applied to the text. In Apple Advanced Typography (AAT), typographic effects are achieved through two 16-bit numbers, called a feature and a selector.")
    font_name: Override[str] = Field(default_factory=Override.not_set, description="The PostScript name of the font. Only the name is carried, not the font itself, so on a device that doesn't have the font and can't download it, the text appears in a substitute font.")
    font_size: Override[float] = Field(default_factory=Override.not_set, description="The font size, in points.")
    is_named_point_size: Override[bool] = Field(default_factory=Override.not_set, description="Whether `font_size` matches one of the named Chinese font sizes, such as 初号 for 42 points. `font_size` is a value in points either way.")
    italic: Override[bool] = Field(default_factory=Override.not_set, description="Whether the text is italic.")
    language: Override[str] = Field(default_factory=Override.not_set, description="The language ID of the text, for example, `en`, `en-GB`, or `sr-Cyrl`.")
    ligatures: Override[LigatureType] = Field(default_factory=Override.not_set, description="The ligatures to use: required, standard, or all.")
    shadow: Override[Shadow] = Field(default_factory=Override.not_set, description="The shadow applied to the characters.")
    strikethrough: Override[StrikethroughType] = Field(default_factory=Override.not_set, description="The strikethrough style of the text: single, double, or none.")
    strikethrough_color: Override[Color] = Field(default_factory=Override.not_set, description="The color of the strikethrough line or lines. When it's `null`, the line is drawn in the text's own color; whether a line appears at all comes from `strikethrough`.")
    strikethrough_width: Override[float] = Field(default_factory=Override.not_set, description="The thickness of the strikethrough line or lines, as a multiple of the font's normal line thickness rather than a length in points; `1` is the font's normal thickness.")
    stroke: Override[TextStroke] = Field(default_factory=Override.not_set, description="The stroke that outlines the characters.")
    tracking: Override[float] = Field(default_factory=Override.not_set, description="The character spacing, as a fraction of the font's em. For example, 0.20 adds about 20% extra spacing per character; a negative value tightens it.")
    underline: Override[UnderlineType] = Field(default_factory=Override.not_set, description="The underline style of the text: single, double, wavy, or none.")
    underline_color: Override[Color] = Field(default_factory=Override.not_set, description="The color of the underline. When it's `null`, the underline is drawn in the text's own color; whether an underline appears at all comes from `underline`.")
    word_strikethrough: Override[bool] = Field(default_factory=Override.not_set, description="Whether the strikethrough is drawn only through words, not through whitespace.")
    word_underline: Override[bool] = Field(default_factory=Override.not_set, description="Whether the underline is drawn only beneath words, not beneath whitespace.")
    writing_direction: Override[WritingDirectionType] = Field(default_factory=Override.not_set, description="The writing direction of the text: left to right, right to left, or natural for the content.")


class BaselineType(str, Enum):
    """The superscript or subscript setting of a text run.

A superscript or subscript run is set at a reduced size, even though `font_size` keeps the value written for it, and the shift it applies is added to `baseline_shift` rather than replacing it."""
    DEFAULT = "default"
    SUBSCRIPT = "subscript"
    SUPERSCRIPT = "superscript"


class CapitalizationType(str, Enum):
    """The way the reader alters capitalization of text when it shows it.

    all_caps — Draws every letter as a capital of the same height.
    none — Draws the text as written, with no change to its capitalization.
    small_caps — Draws every letter as a capital, using taller capitals for the letters that were already uppercase.
    start — Capitalizes the first letter of every word, including the short words such as articles that `title` leaves lowercase.
    title — Capitalizes the text as a title, applying the language-specific title-casing rules.
    """
    ALL_CAPS = "all_caps"
    NONE = "none"
    SMALL_CAPS = "small_caps"
    START = "start"
    TITLE = "title"


@wire(
    "com.apple.apps.content-language.character-properties.font-features-type",
    version="1.0",
    fields=[
        ("feature", (1, 0), "req"),
        ("selector", (1, 0), "req"),
    ],
)
class FontFeaturesType(ObjectModel):
    """A typographic feature of the font.

It's named by an Apple Advanced Typography (AAT) feature type and one of that type's settings. The feature types and their settings are listed in [Appendix F of the TrueType Reference Manual](https://developer.apple.com/fonts/TrueType-Reference-Manual/RM09/AppendixF.html)."""
    feature: int = Field(description="The identifier of the AAT font feature type, as listed in the TrueType Reference Manual, Appendix F.")
    selector: int = Field(description="The identifier of the setting to apply within the feature type named by `feature`.")


class LigatureType(str, Enum):
    """The ligatures of the font that the reader substitutes when it draws the text.

    all — Also substitutes the ligatures the font marks as optional, such as ct and st in Hoefler Text.
    required — Substitutes only the ligatures needed for correct layout, such as those in Arabic script.
    standard — Also substitutes the ligatures the font marks as standard, which typically include pairs such as fl and fi.
    """
    ALL = "all"
    REQUIRED = "required"
    STANDARD = "standard"


class StrikethroughType(str, Enum):
    """The strikethrough style of text, or no strikethrough.

This value alone decides whether a line appears; the line's color, its thickness, and whether it skips whitespace come from `strikethrough_color`, `strikethrough_width`, and `word_strikethrough`."""
    DOUBLE = "double"
    NONE = "none"
    SINGLE = "single"


class UnderlineType(str, Enum):
    """The underline style of text, or no underline.

This value alone decides whether an underline appears; the underline's color and whether it skips whitespace come from `underline_color` and `word_underline`."""
    DOUBLE = "double"
    NONE = "none"
    SINGLE = "single"
    WAVY = "wavy"


@wire_union(
    "com.apple.apps.content-language.column-metrics",
    version="1.0",
    cases=[
        ("equal", (1, 0), False),
        ("single", (1, 0), True),
        ("unequal", (1, 0), False),
    ],
)
class ColumnMetrics(TaggedUnionModel):
    """The arrangement of a text area into columns, and the width of the gutters between them."""
    equal: EqualColumnsDescription | None = Field(default=None, description="All the columns are the same width, and so are all the gutters.")
    single: Literal[True] | None = Field(default=None, description="A single column.")
    unequal: UnequalColumnsDescription | None = Field(default=None, description="Each of the column and gutter widths is specified.")

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_ColumnMetricsCase, ...]: ...

        def union_primary(self) -> _ColumnMetricsCase | None: ...

        def union_primary_name(self) -> Literal["equal", "single", "unequal"] | None: ...


@wire(
    "com.apple.apps.content-language.column-metrics.equal-columns-description",
    version="1.0",
    fields=[
        ("count", (1, 0), "req"),
        ("gutter_width", (1, 0), "opt"),
    ],
)
class EqualColumnsDescription(ObjectModel):
    """An arrangement of a text area into columns of equal width.

Only `count` and `gutter_width` are specified; each column takes an equal share of the width the gutters leave. The gutters together are clamped to 75% of the text width, so a large `gutter_width` is silently narrowed."""
    count: int = Field(ge=1, le=10, description="The number of columns.")
    gutter_width: float | None = Field(default=None, ge=0, le=75, description="The width of the gutter between adjacent columns, the same between every pair, as a percentage of the width available for text inside the container (its width less its padding). It's only meaningful when `count` is greater than `1`; the default is 5%.")


@wire(
    "com.apple.apps.content-language.column-metrics.unequal-columns-description",
    version="1.0",
    fields=[
        ("column_widths", (1, 0), "req"),
        ("gutter_widths", (1, 0), "opt"),
    ],
)
class UnequalColumnsDescription(ObjectModel):
    """An arrangement of a text area into columns of specified widths.

Each of the column and gutter widths is specified, and together they must total 100."""
    column_widths: list[float] = Field(min_length=1, max_length=10, description="The width of each column, as a percentage of the width available for text inside the container (its width less its padding). The number of columns is the length of this array, and the column widths together with the gutter widths must total 100.")
    gutter_widths: list[float] | None = Field(default=None, min_length=1, max_length=9, description="The width of the gutter following each column, as a percentage of the width available for text inside the container (its width less its padding). The array's length must be exactly one less than the number of column widths, or the content is rejected; if it's omitted, there are no gutters, which is valid only for a single column.")


@wire(
    "com.apple.apps.content-language.insets",
    version="1.0",
    fields=[
        ("top", (1, 0), "def"),
        ("bottom", (1, 0), "def"),
        ("left", (1, 0), "def"),
        ("right", (1, 0), "def"),
    ],
)
class Insets(ObjectModel):
    """Space reserved along each edge of an area, in points."""
    top: float = Field(default=0, ge=0, le=50000000, description="The top inset, in points, in the range `0` to `50000000`.")
    bottom: float = Field(default=0, ge=0, le=50000000, description="The bottom inset, in points, in the range `0` to `50000000`.")
    left: float = Field(default=0, ge=0, le=50000000, description="The left inset, in points, in the range `0` to `50000000`.")
    right: float = Field(default=0, ge=0, le=50000000, description="The right inset, in points, in the range `0` to `50000000`.")


@wire(
    "com.apple.apps.content-language.layout-properties",
    version="1.0",
    fields=[
        ("columns", (1, 0), "ovr"),
        ("continuous", (1, 0), "ovr"),
        ("margins", (1, 0), "ovr"),
        ("padding", (1, 0), "ovr"),
        ("shrink_to_fit", (1, 0), "ovr"),
        ("vertical_alignment", (1, 0), "ovr"),
        ("vertical_text", (1, 0), "ovr"),
        ("writing_direction", (1, 0), "ovr"),
    ],
)
class LayoutProperties(ObjectModel):
    """The text layout properties of a shape style or a column of text.

An omitted property is inherited from the preset named by `preset_identifier`; otherwise, it's inherited from the shape or text box style's preset or, for a column style, from the style named by `parent`. Anything still unset takes the property's built-in default, and a `null` clears it instead."""
    columns: Override[ColumnMetrics] = Field(default_factory=Override.not_set, description="The number and spacing of the columns. The default is a single column of full width.")
    continuous: Override[bool] = Field(default_factory=Override.not_set, description="Whether text using this layout continues on the page; if false, it always begins on a new page. It applies only to column layout and has no effect on shapes or text boxes.")
    margins: Override[Insets] = Field(default_factory=Override.not_set, description="The margins, in points, between the edges of the text container and the column layout inside it. They apply only to column layout; for the inset applied to any text container, see `padding`.")
    padding: Override[Insets] = Field(default_factory=Override.not_set, description="The space, in points, between the edges of the text container and the text laid out inside it, on all four edges. Unlike `margins`, which position the column layout within the container's text area, padding insets that whole text area and applies to any text container.")
    shrink_to_fit: Override[bool] = Field(default_factory=Override.not_set, description="Whether the text is scaled down to fit inside the container, to as little as 40% of the given font sizes; text that still doesn't fit at that scale overflows. The container keeps its own size. The default is `false`.")
    vertical_alignment: Override[VerticalAlignmentType] = Field(default_factory=Override.not_set, description="The vertical alignment of text within a container.")
    vertical_text: Override[bool] = Field(default_factory=Override.not_set, description="Whether the text is vertical.")
    writing_direction: Override[WritingDirectionType] = Field(default_factory=Override.not_set, description="The writing direction of the text: left to right, right to left, or natural for the content.")


@wire(
    "com.apple.apps.content-language.line-spacing-type",
    version="1.0",
    fields=[
        ("kind", (1, 0), "opt"),
        ("value", (1, 0), "req"),
    ],
)
class LineSpacingType(ObjectModel):
    """The spacing between lines of text."""
    kind: LineSpacingKindType | None = Field(default=None, strict=False, description="The kind of line spacing, which sets how `value` is interpreted: `relative` treats it as a multiple of the natural line height; `minimum`, `exact`, and `maximum` treat it as a line height in points; and `between` treats it as extra space added between lines. The default is `relative`.")
    value: float = Field(description="The amount of line spacing, interpreted according to `kind`: a multiplier for `relative` (1.0 is single-spaced, 2.0 double-spaced), otherwise a measurement in points. A negative value is meaningful only for `between`, where it tightens the space between lines.")


class LineSpacingKindType(str, Enum):
    """A kind of line spacing.

    between — `value` points of space are added between lines, in addition to the natural line height.
    exact — Lines are exactly `value` points apart.
    maximum — Lines are at most `value` points apart.
    minimum — Lines are at least `value` points apart.
    relative — `value` is a multiple of the natural line height; 1.0 is single-spaced. Shown in Keynote as Lines.
    """
    BETWEEN = "between"
    EXACT = "exact"
    MAXIMUM = "maximum"
    MINIMUM = "minimum"
    RELATIVE = "relative"


@wire_union(
    "com.apple.apps.content-language.list-label-type",
    version="1.0",
    cases=[
        ("image", (1, 0), False),
        ("none", (1, 0), True),
        ("null_image", (1, 0), True),
        ("number", (1, 0), False),
        ("string", (1, 0), False),
    ],
)
class ListLabelType(TaggedUnionModel):
    """The kind of label shown at a list level.

The `string` and `image` cases carry the label's content, size, and offset; `number` carries a numbering format and size; and `none` and `null_image` carry no value."""
    image: ListImageLabel | None = Field(default=None, description="An image label.")
    none: Literal[True] | None = Field(default=None, description="No bullet or label for this level.")
    null_image: Literal[True] | None = Field(default=None, description="An image label whose image is missing. Nothing is drawn for the level, which still counts as labeled rather than as `none`.")
    number: ListNumberLabel | None = Field(default=None, description="A number label.")
    string: ListStringLabel | None = Field(default=None, description="A text bullet.")

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_ListLabelTypeCase, ...]: ...

        def union_primary(self) -> _ListLabelTypeCase | None: ...

        def union_primary_name(self) -> Literal["image", "none", "null_image", "number", "string"] | None: ...


@wire(
    "com.apple.apps.content-language.list-label-type.list-number-label",
    version="1.0",
    fields=[
        ("number_format", (1, 0), "opt"),
        ("scale", (1, 0), "opt"),
        ("tiered", (1, 0), "opt"),
    ],
)
class ListNumberLabel(ObjectModel):
    """A numbered list label.

Its numbers can be tiered, as in 1.1 and 1.2."""
    number_format: NumberFormatType | None = Field(default=None, description="The numbering format for this level, such as numeric, Roman, or alphabetic. The default is a decimal number.")
    scale: float | None = Field(default=None, description="The label's size, as a multiple of the text size at the start of the paragraph. The default is 1.0.")
    tiered: bool | None = Field(default=None, description="Whether the numbers are tiered. The default is `false`.")


@wire(
    "com.apple.apps.content-language.list-label-type.list-string-label",
    version="1.0",
    fields=[
        ("string", (1, 0), "req"),
        ("scale", (1, 0), "opt"),
        ("offset", (1, 0), "opt"),
    ],
)
class ListStringLabel(ObjectModel):
    """A text list label, such as a bullet character or a short string."""
    string: str = Field(description="The string shown as the label.")
    scale: float | None = Field(default=None, description="The label's size, as a multiple of the text size at the start of the paragraph. The default is 1.0.")
    offset: float | None = Field(default=None, description="The vertical shift of the label from its default position, in points; a positive value raises it. The default is 0.0.")


@wire(
    "com.apple.apps.content-language.list-label-type.list-image-label",
    version="1.0",
    fields=[
        ("scale", (1, 0), "opt"),
        ("offset", (1, 0), "opt"),
        ("resource", (1, 0), "req"),
    ],
)
class ListImageLabel(ObjectModel):
    """An image bullet."""
    scale: float | None = Field(default=None, description="The height of the bullet image, as a fraction of the text height at the start of the paragraph; the image keeps its aspect ratio. The default is 1.0.")
    offset: float | None = Field(default=None, description="The vertical shift of the bullet image from its default position, in points; a positive value raises it. The default is 0.0.")
    resource: Resource = Field(description="The resource containing the image's data.")


@wire(
    "com.apple.apps.content-language.list-level-type",
    version="1.0",
    fields=[
        ("label_indent", (1, 0), "req"),
        ("text_indent", (1, 0), "req"),
        ("label", (1, 0), "req"),
    ],
)
class ListLevelType(ObjectModel):
    """One nesting level of a list style."""
    label_indent: float = Field(ge=0, description="The indent, in points, from the paragraph's leading edge to the list label for this level.")
    text_indent: float = Field(ge=0, description="The additional indent from the list label to the paragraph text for this level, as a multiple of the paragraph's font size rather than in points.")
    label: ListLabelType = Field(description="The kind of bullet or number shown at this level.")


@wire(
    "com.apple.apps.content-language.list-properties",
    version="1.0",
    fields=[
        ("font_color", (1, 0), "ovr"),
        ("font_name", (1, 0), "ovr"),
        ("writing_direction", (1, 0), "ovr"),
        ("shadow", (1, 0), "ovr"),
        ("levels", (1, 0), "ovr"),
    ],
)
class ListProperties(ObjectModel):
    """The properties of a list style.

A `preset_identifier` here is matched against the document stylesheet's list styles before the presets in `presets.json`, and an identifier that matches neither is silently ignored, so `levels` must be written here for a label to be drawn. An omitted `font_color`, `font_name`, `shadow`, or `writing_direction` follows the paragraph's text styling, and a `null` clears it instead."""
    font_color: Override[Color] = Field(default_factory=Override.not_set, description="The color applied to list labels and numbers.")
    font_name: Override[str] = Field(default_factory=Override.not_set, description="The PostScript name of the font used for list labels and numbers. Only the name is carried, not the font itself, so on a device that doesn't have the font and can't download it, the labels and numbers are drawn in a substitute font.")
    writing_direction: Override[WritingDirectionType] = Field(default_factory=Override.not_set, description="The writing direction: left to right, right to left, or natural for the content.")
    shadow: Override[Shadow] = Field(default_factory=Override.not_set, description="The shadow applied to the list label or number.")
    levels: Override[list[ListLevelType]] = Field(default_factory=Override.not_set, description="The list definition for each nesting level, with index `0` the top level. At most 9 levels are used: any beyond the ninth are ignored, and if fewer are supplied, the last one is repeated for the remaining levels.")


@wire(
    "com.apple.apps.content-language.number-format-type",
    version="1.0",
    fields=[
        ("kind", (1, 0), "opt"),
        ("upper", (1, 0), "opt"),
        ("formal", (1, 0), "opt"),
        ("format", (1, 0), "opt"),
    ],
)
class NumberFormatType(ObjectModel):
    """A format for numbers, such as those in a numbered list.

Not every combination of `kind`, `upper`, `formal`, and `format` exists; an unsupported combination falls back to a plain number followed by a period."""
    kind: NumberFormatTypeKind | None = Field(default=None, strict=False, description="The numbering system used for the label, such as Western digits, Roman numerals, Latin letters, or a Japanese, Chinese, Korean, Arabic, or Hebrew system. The default is `numeric`.")
    upper: bool | None = Field(default=None, description="Whether to use uppercase, which applies only to the `roman` and `alpha` kinds; every other kind requires `false`. The default is `false`.")
    formal: bool | None = Field(default=None, description="Whether to use the formal ideographic form, which applies only to the `japanese`, `simplified_chinese`, and `traditional_chinese` kinds; every other kind requires `false`. The default is `false`.")
    format: Format | None = Field(default=None, strict=False, description="The decoration around the number: `decimal` for a trailing period, `paren` for a trailing parenthesis, `double_paren` for enclosing parentheses, `circled` (`numeric` kind only), or `standard` (`hebrew_biblical` kind only). The default is `decimal`.")


class NumberFormatTypeKind(str, Enum):
    """A numbering system.

    alpha — Latin letters; use `upper` to choose between A and a.
    arabian — Arabic-Indic digits.
    arabian_abjad — Abjad numerals, in which Arabic letters carry numeric values.
    arabian_alpha — Arabic letters in alphabetical order.
    hebrew — Hebrew letters in alphabetical order.
    hebrew_biblical — Traditional Hebrew numerals, in which letters carry numeric values.
    hiragana — Hiragana characters in aiueo order.
    hiragana_iroha — Hiragana characters in iroha order.
    japanese — Japanese ideographic numerals; set `formal` for the formal form.
    katakana — Katakana characters in aiueo order.
    katakana_iroha — Katakana characters in iroha order.
    korean — Korean syllables in ga, na, da order.
    numeric — Western digits: 1, 2, 3.
    roman — Roman numerals; use `upper` to choose between I and i.
    simplified_chinese — Simplified Chinese ideographic numerals; set `formal` for the formal form.
    traditional_chinese — Traditional Chinese ideographic numerals; set `formal` for the formal form.
    """
    ALPHA = "alpha"
    ARABIAN = "arabian"
    ARABIAN_ABJAD = "arabian_abjad"
    ARABIAN_ALPHA = "arabian_alpha"
    HEBREW = "hebrew"
    HEBREW_BIBLICAL = "hebrew_biblical"
    HIRAGANA = "hiragana"
    HIRAGANA_IROHA = "hiragana_iroha"
    JAPANESE = "japanese"
    KATAKANA = "katakana"
    KATAKANA_IROHA = "katakana_iroha"
    KOREAN = "korean"
    NUMERIC = "numeric"
    ROMAN = "roman"
    SIMPLIFIED_CHINESE = "simplified_chinese"
    TRADITIONAL_CHINESE = "traditional_chinese"


class Format(str, Enum):
    """The decoration around a number, such as a trailing period or parentheses.

    circled — The number enclosed in a circle. Valid only with the `numeric` kind.
    decimal — The number followed by a period, as in `1.`.
    double_paren — The number enclosed in parentheses, as in `(1)`.
    paren — The number followed by a closing parenthesis, as in `1)`.
    standard — The standard form of the number for its kind, with no added decoration. Valid only with the `hebrew_biblical` kind.
    """
    CIRCLED = "circled"
    DECIMAL = "decimal"
    DOUBLE_PAREN = "double_paren"
    PAREN = "paren"
    STANDARD = "standard"


@wire(
    "com.apple.apps.content-language.offset",
    version="1.0",
    fields=[
        ("dx", (1, 0), "def"),
        ("dy", (1, 0), "def"),
    ],
)
class Offset(ObjectModel):
    """A horizontal and vertical displacement, in points."""
    dx: float = Field(default=0, description="The horizontal offset, in points.")
    dy: float = Field(default=0, description="The vertical offset, in points.")


@wire(
    "com.apple.apps.content-language.paragraph",
    version="1.0",
    fields=[
        ("style", (1, 0), "opt"),
        ("list_style", (1, 0), "opt"),
        ("list_start", (1, 0), "opt"),
        ("list_level", (1, 0), "opt"),
        ("writing_direction", (1, 0), "opt"),
        ("contents", (1, 0), "opt"),
        ("break_type", (1, 0), "opt"),
    ],
)
class Paragraph(ObjectModel):
    """A paragraph of text."""
    style: ParagraphProperties | None = Field(default=None, description="The paragraph properties for this paragraph. When `preset_identifier` is set, the paragraph inherits from a stylesheet paragraph style; otherwise, the properties are given here.")
    list_style: ListProperties | None = Field(default=None, description="The list properties for this paragraph. When `preset_identifier` is set, the paragraph inherits from a stylesheet list style; otherwise, the properties are given here. If `list_style` is absent, the paragraph keeps the list style already in effect (the preceding paragraph's, or the one the containing text starts with), so ending a list takes an explicit list style whose levels carry no label.")
    list_start: int | None = Field(default=None, description="The number at which list numbering restarts for this paragraph. If it's omitted or 0, numbering continues from the preceding list item. Values above 4294967295 are clamped.")
    list_level: int | None = Field(default=None, description="The zero-based list level of the paragraph, where `0` is the top level; if it's absent, the level is 0. The level selects which entry of the list style's `ListProperties.levels` supplies the indent and the label. Levels outside the range `0` through 8 are adjusted to the nearest supported level rather than rejected.")
    writing_direction: WritingDirectionType | None = Field(default=None, strict=False, description="The writing direction of the paragraph, used only when the paragraph style leaves the direction natural. A direction on the paragraph style takes precedence, and the document's direction applies when neither sets one.")
    contents: list[Constituent] | None = Field(default=None, description="The ordered contents of the paragraph: text runs, inline objects, and links. The break that ends the paragraph isn't included, and the property is omitted for an empty paragraph.")
    break_type: BreakType | None = Field(default=None, strict=False, description="The break that ends the paragraph. By default, paragraphs are separated by a normal paragraph break.")


@wire_union(
    "com.apple.apps.content-language.paragraph.constituent",
    version="1.0",
    cases=[
        ("hyperlink", (1, 0), False),
        ("inline_object", (1, 0), False),
        ("run", (1, 0), False),
    ],
)
class Constituent(TaggedUnionModel):
    """An element of a paragraph's contents.

Each element is a run of text, an inline object, or a link."""
    hyperlink: HyperlinkField | None = Field(default=None, description="A link.")
    inline_object: CanvasObject | None = Field(default=None, description="An inline object. \n\nAn object that can't be imported (for example, a movie the device can't play) isn't dropped on its own. In the text of a text box or shape, the whole text box or shape is removed, including all of its text; in a slide's presenter notes, such an object stops the document from loading.")
    run: TextRun | None = Field(default=None, description="A run of text in the same style.")

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_ConstituentCase, ...]: ...

        def union_primary(self) -> _ConstituentCase | None: ...

        def union_primary_name(self) -> Literal["hyperlink", "inline_object", "run"] | None: ...


@wire(
    "com.apple.apps.content-language.paragraph.hyperlink-field",
    version="1.0",
    fields=[
        ("target", (1, 0), "req"),
        ("run", (1, 0), "req"),
    ],
)
class HyperlinkField(ObjectModel):
    """A link with styled display text."""
    target: Hyperlink = Field(description="The link destination.")
    run: TextRun = Field(description="The text run shown as the link.")


class BreakType(str, Enum):
    """The break that ends a paragraph.

It decides where the following text resumes: the next line, the next column, or the next page.

    column — Column break.
    none — No terminating break; only the last paragraph of the text can lack one, and there `none` is equivalent to omitting `break_type`. On any earlier paragraph a normal paragraph break is inserted instead.
    nontopic — A paragraph break that prevents topic or list labeling.
    page — Page break.
    para — Paragraph break.
    section — Section break. Keynote has no sections: `section` is always replaced by a page break, which in Keynote only ends the paragraph. Use `para` instead.
    """
    COLUMN = "column"
    NONE = "none"
    NONTOPIC = "nontopic"
    PAGE = "page"
    PARA = "para"
    SECTION = "section"


@wire(
    "com.apple.apps.content-language.paragraph-properties",
    version="1.0",
    fields=[
        ("alignment", (1, 0), "ovr"),
        ("decimal_tab", (1, 0), "ovr"),
        ("default_tabs", (1, 0), "ovr"),
        ("fill", (1, 0), "ovr"),
        ("first_line_indent", (1, 0), "ovr"),
        ("following_style", (1, 0), "ovr"),
        ("hyphenate", (1, 0), "ovr"),
        ("list_style", (1, 0), "ovr"),
        ("keep_lines_together", (1, 0), "ovr"),
        ("keep_with_next", (1, 0), "ovr"),
        ("left_indent", (1, 0), "ovr"),
        ("line_spacing", (1, 0), "ovr"),
        ("outline_level", (1, 0), "ovr"),
        ("start_on_new_page", (1, 0), "ovr"),
        ("borders", (1, 0), "opt"),
        ("right_indent", (1, 0), "ovr"),
        ("space_after", (1, 0), "ovr"),
        ("space_before", (1, 0), "ovr"),
        ("tabs", (1, 0), "ovr"),
        ("prevent_widow", (1, 0), "ovr"),
        ("show_in_bookmarks", (1, 0), "ovr"),
        ("show_in_tocnavigator", (1, 0), "ovr"),
        ("character_properties", (1, 0), "opt"),
    ],
)
class ParagraphProperties(ObjectModel):
    """The paragraph-level properties of text.

A `preset_identifier` here is matched against the document stylesheet's paragraph styles before the presets in `presets.json`, and an identifier that matches neither is silently ignored. An omitted property is inherited from that preset and its parent presets, or from the style these properties refine, such as a table region's text style; a `null` clears it instead. `borders` and `character_properties` don't accept a `null`."""
    alignment: Override[AlignmentType] = Field(default_factory=Override.not_set, description="The horizontal alignment of the paragraph.")
    decimal_tab: Override[str] = Field(default_factory=Override.not_set, description="The character that text lines up on at a decimal tab stop, such as `.` or `,`. The default is the decimal separator of the document's language.")
    default_tabs: Override[float] = Field(default_factory=Override.not_set, description="The distance, in points, between the automatic tab stops that apply where no explicit stop from `tabs` is defined.")
    fill: Override[Color] = Field(default_factory=Override.not_set, description="The background color behind the paragraph.")
    first_line_indent: Override[float] = Field(default_factory=Override.not_set, description="The indentation, in points, of the paragraph's first line, if it differs from the rest. It's the left indent for left-to-right paragraphs and the right indent for right-to-left paragraphs, and it replaces `left_indent` on that line rather than adding to it, so a smaller value gives a hanging indent.")
    following_style: Override[str] = Field(default_factory=Override.not_set, description="The identifier or name of the paragraph style applied to the next paragraph created after this one, such as a body style following a heading. It's matched first against the identifiers of the styles in the document's stylesheet (a stylesheet entry's `preset_identifier`), and then against style names. A value matching neither is ignored.")
    hyphenate: Override[bool] = Field(default_factory=Override.not_set, description="Whether to allow long words in the paragraph to be hyphenated at line breaks. Hyphenation also requires document-wide hyphenation to be on and never happens in right-to-left paragraphs, so `false` suppresses hyphenation for the paragraph while `true` can't introduce it.")
    list_style: Override[str] = Field(default_factory=Override.not_set, description="The identifier or name of the list style that text using this paragraph style starts with, matched against list-style identifiers first, then names. A stylesheet list style's identifier is normally its `preset_identifier`. `null` means no list style, and a value matching no identifier and no name is ignored.")
    keep_lines_together: Override[bool] = Field(default_factory=Override.not_set, description="Whether to keep all of the paragraph's lines on the same page, if possible.")
    keep_with_next: Override[bool] = Field(default_factory=Override.not_set, description="Whether to keep all of the paragraph's lines on the same page as the next paragraph, if possible.")
    left_indent: Override[float] = Field(default_factory=Override.not_set, description="The indentation, in points, of the paragraph's left edge from the left edge of the text column.")
    line_spacing: Override[LineSpacingType] = Field(default_factory=Override.not_set, description="The line spacing rule and amount for the paragraph.")
    outline_level: Override[int] = Field(default_factory=Override.not_set, description="The depth of the paragraph in the document outline, where `0` is the top level. Use `-1` for body text that isn't part of the outline; values outside the range `-1` to `999` are clamped.")
    start_on_new_page: Override[bool] = Field(default_factory=Override.not_set, description="Whether the paragraph starts on a new page.")
    borders: BorderStyleType | None = Field(default=None, description="The paragraph's border or rule style.")
    right_indent: Override[float] = Field(default_factory=Override.not_set, description="The indentation, in points, of the paragraph's right edge from the right edge of the text column.")
    space_after: Override[float] = Field(default_factory=Override.not_set, description="The space after the paragraph, in points.")
    space_before: Override[float] = Field(default_factory=Override.not_set, description="The space before the paragraph, in points.")
    tabs: Override[list[TabStopType]] = Field(default_factory=Override.not_set, description="The tab stops for the paragraph.")
    prevent_widow: Override[bool] = Field(default_factory=Override.not_set, description="Whether to prevent widows and orphans (a single line that appears by itself at the bottom of a page or top of the following page).")
    show_in_bookmarks: Override[bool] = Field(default_factory=Override.not_set, description="Whether to show the paragraph in the bookmarks list.")
    show_in_tocnavigator: Override[bool] = Field(default_factory=Override.not_set, description="Whether to show the paragraph in the TOC navigator.")
    character_properties: CharacterProperties | None = Field(default=None, description="The additional character properties to apply to the paragraph.")


class AlignmentType(str, Enum):
    """The horizontal alignment of a paragraph.

    natural — In a table cell, aligns text to the leading edge and numbers to the trailing edge. Shown in Keynote as Auto-Align Table Cell.
    """
    CENTER = "center"
    JUSTIFIED = "justified"
    LEFT = "left"
    NATURAL = "natural"
    RIGHT = "right"


@wire(
    "com.apple.apps.content-language.paragraph-properties.border-style-type",
    version="1.0",
    fields=[
        ("stroke", (1, 0), "ovr"),
        ("width", (1, 0), "ovr"),
        ("offset", (1, 0), "ovr"),
        ("rounded", (1, 0), "ovr"),
        ("no_borders", (1, 0), "opt"),
        ("all_borders", (1, 0), "opt"),
        ("before", (1, 0), "opt"),
        ("after", (1, 0), "opt"),
        ("leading", (1, 0), "opt"),
        ("trailing", (1, 0), "opt"),
    ],
)
class BorderStyleType(ObjectModel):
    """The style of a paragraph's borders or rules."""
    stroke: Override[TextStroke] = Field(default_factory=Override.not_set, description="The stroke used to draw the border or rule.")
    width: Override[float] = Field(default_factory=Override.not_set, description="The length of the paragraph's rule lines as a fraction of the paragraph width, where `1` spans the full width and shorter rules are centered. Line thickness comes from `stroke` rather than from this value, and joined border lines that enclose the paragraph always span the full width.")
    offset: Override[Offset] = Field(default_factory=Override.not_set, description="The offset to the border or rule, or none.")
    rounded: Override[bool] = Field(default_factory=Override.not_set, description="Whether the border corners are rounded.")
    no_borders: bool | None = Field(default=None, description="Whether the paragraph has no border or rule lines. It takes precedence over `all_borders` and over the individual `before`, `after`, `leading`, and `trailing` flags. Only `true` has an effect: with none of the six flags `true`, border positions are inherited from the paragraph style rather than cleared.")
    all_borders: bool | None = Field(default=None, description="Whether the paragraph has a border on every side.")
    before: bool | None = Field(default=None, description="Whether the paragraph has a top rule or border.")
    after: bool | None = Field(default=None, description="Whether the paragraph has a bottom rule or border.")
    leading: bool | None = Field(default=None, description="Whether the paragraph has a leading rule or border (left for left-to-right paragraphs, right for right-to-left paragraphs).")
    trailing: bool | None = Field(default=None, description="Whether the paragraph has a trailing rule or border (right for left-to-right paragraphs, left for right-to-left paragraphs).")


@wire(
    "com.apple.apps.content-language.tab-stop-type",
    version="1.0",
    fields=[
        ("position", (1, 0), "req"),
        ("kind", (1, 0), "opt"),
        ("leader", (1, 0), "opt"),
    ],
)
class TabStopType(ObjectModel):
    """A tab stop."""
    position: float = Field(description="The position of the tab stop, in points. Use a position greater than 0; a tab stop at `0` or less is accepted but is dropped the next time the document is opened.")
    kind: TabAlignmentKindType | None = Field(default=None, strict=False, description="The alignment of the tab stop; the default is `left`.")
    leader: str | None = Field(default=None, description="The string shown in the space before the tab stop (for example, a period for a dotted leader). The default is a single space (a plain gap), so a value of `\" \"` is equivalent to omitting the property.")


class TabAlignmentKindType(str, Enum):
    """The alignment of a tab stop.

    center — Text is centered on the tab stop.
    decimal — Text is aligned so that its decimal separator lines up with the tab stop.
    left — Text begins at the tab stop, running in the paragraph's writing direction (a leading tab).
    right — Text ends at the tab stop, running in the paragraph's writing direction (a trailing tab).
    """
    CENTER = "center"
    DECIMAL = "decimal"
    LEFT = "left"
    RIGHT = "right"


@wire_union(
    "com.apple.apps.content-language.text",
    version="1.0",
    cases=[
        ("paragraphs", (1, 0), False),
        ("string", (1, 0), False),
        ("text_runs", (1, 0), False),
    ],
)
class Text(TaggedUnionModel):
    """A body of text, such as the text of a text box, a table cell, or a slide's presenter notes.

It's carried in exactly one of these forms. The text-run form is accepted when supplying text, but Keynote always writes text as paragraphs or a plain string."""
    paragraphs: list[Paragraph] | None = Field(default=None, description="An array of paragraphs of text.")
    string: str | None = Field(default=None, description="A string of Unicode text.")
    text_runs: list[TextRun] | None = Field(default=None, description="An array of runs of text.")

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_TextCase, ...]: ...

        def union_primary(self) -> _TextCase | None: ...

        def union_primary_name(self) -> Literal["paragraphs", "string", "text_runs"] | None: ...


@wire(
    "com.apple.apps.content-language.text-run",
    version="1.0",
    fields=[
        ("string", (1, 0), "req"),
        ("style", (1, 0), "opt"),
    ],
)
class TextRun(ObjectModel):
    """A run of text with a single character style."""
    string: str = Field(description="The literal text of this run, shown in the run's character style. It may be empty. A run is split wherever the character style changes, so the text of a run always has a single style.")
    style: CharacterProperties | None = Field(default=None, description="The character properties for this run. When `preset_identifier` is set, the run inherits from a stylesheet character style; otherwise, the properties are written in the run itself.")


@wire_union(
    "com.apple.apps.content-language.text-stroke",
    version="1.0",
    cases=[
        ("none", (1, 0), True),
        ("stroke", (1, 0), False),
    ],
)
class TextStroke(TaggedUnionModel):
    """A stroke for text, or a special value for no stroke."""
    none: Literal[True] | None = Field(default=None, description="No stroke.")
    stroke: Stroke | None = Field(default=None, description="A stroke, described by `Stroke`. Use `none` instead to specify no stroke at all.")

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_TextStrokeCase, ...]: ...

        def union_primary(self) -> _TextStrokeCase | None: ...

        def union_primary_name(self) -> Literal["none", "stroke"] | None: ...


class VerticalAlignmentType(str, Enum):
    """Vertical alignment of text within a container.

    bottom — Align the text to the bottom of its container.
    center — Center the text vertically in its container. Shown in Keynote as Align Middle.
    top — Align the text to the top of its container.
    """
    BOTTOM = "bottom"
    CENTER = "center"
    TOP = "top"


class WritingDirectionType(str, Enum):
    """The writing direction of the text.

    left_to_right — Lay the text out left to right.
    natural — Take the writing direction from the surrounding context: the paragraph style first, then the document. A paragraph that defers in this way carries no direction of its own.
    right_to_left — Lay the text out right to left.
    """
    LEFT_TO_RIGHT = "left_to_right"
    NATURAL = "natural"
    RIGHT_TO_LEFT = "right_to_left"


@wire_union(
    "com.apple.apps.content-language.color",
    version="1.0",
    cases=[
        ("rgba", (1, 0), False),
    ],
)
class Color(TaggedUnionModel):
    """A color that the reader uses as part of a displayed object, in one of the forms the format supports.

Every form resolves to a color that can be displayed, so a reader never has to handle one that can't be."""
    rgba: RGBA | None = Field(default=None, description="A color given as red, green, blue, and alpha components in a named RGB color space, together with an HDR headroom value.")

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_ColorCase, ...]: ...

        def union_primary(self) -> _ColorCase | None: ...

        def union_primary_name(self) -> Literal["rgba"] | None: ...


@wire(
    "com.apple.apps.content-language.color.rgba",
    version="1.1",
    fields=[
        ("red", (1, 0), "def"),
        ("green", (1, 0), "def"),
        ("blue", (1, 0), "def"),
        ("alpha", (1, 0), "def"),
        ("color_space", (1, 0), "def"),
        ("headroom", (1, 1), "def"),
    ],
)
class RGBA(ObjectModel):
    """A color in an RGB-component color space, together with its alpha and an HDR headroom value."""
    red: float = Field(default=0, ge=0, le=1, description="The red component, in the range `0` to `1`, expressed in the color space named by `color_space`.")
    green: float = Field(default=0, ge=0, le=1, description="The green component, in the range `0` to `1`, expressed in the color space named by `color_space`.")
    blue: float = Field(default=0, ge=0, le=1, description="The blue component, in the range `0` to `1`, expressed in the color space named by `color_space`.")
    alpha: float = Field(default=1, ge=0, le=1, description="The alpha (opacity) component, in the range `0` to `1`, where `0` is fully transparent and `1` is fully opaque.")
    color_space: ColorSpace = Field(default_factory=lambda: ColorSpace.SRGB, strict=False, description="The RGB color space that the red, green, and blue components are expressed in.")
    headroom: float = Field(default=1, ge=1, le=16, description="The color's own HDR headroom: how many times brighter than standard dynamic range (SDR) white it reaches. A value of `1` means an ordinary SDR color; `red`, `green`, and `blue` always describe its SDR appearance. If HDR can't be reproduced, this value is ignored and those components can be used unchanged.")


class ColorSpace(str, Enum):
    """The RGB primaries, white point, and transfer function used to map a color's red, green, and blue values to a display.

The same three numbers denote a different color in each space. Where `p3` can't be reproduced, the components are used unchanged as `srgb`, which renders a less saturated version of the intended color rather than failing.

    p3 — Display P3 color space, with a nonlinear transfer function and D65 white point.
    srgb — Standard RGB color space, with a nonlinear transfer function and D65 white point, as defined by IEC 61966-2-1.
    """
    P3 = "p3"
    SRGB = "srgb"


@wire(
    "com.apple.apps.content-language.contact-shadow",
    version="1.0",
    fields=[
        ("opacity", (1, 0), "def"),
        ("color", (1, 0), "opt"),
        ("offset", (1, 0), "def"),
        ("radius", (1, 0), "def"),
        ("height", (1, 0), "def"),
    ],
)
class ContactShadow(ObjectModel):
    """A shadow whose silhouette pools under the object's bottom edge as though the object were standing on a ground plane.

The shadow is anchored to that edge, and `height` controls how far it's foreshortened."""
    opacity: float = Field(default=1, ge=0, le=1, description="The opacity of the cast shadow, in the range `0` to `1`.")
    color: Color | None = Field(default=None, description="The color of the cast shadow. If absent, the shadow is black.")
    offset: float = Field(default=0, ge=-75, le=75, description="The vertical distance, in points, between the bottom edge of the object and the point at which the imaginary ground plane is positioned. Positive values move the shadow farther down, and negative values move it up behind the object.")
    radius: float = Field(default=28, ge=10, le=100, description="The radius (size) of the cast shadow's blur, in the range `10` to `100`.")
    height: float = Field(default=0.17364818, ge=0.08715574, le=0.57357644, description="The apparent height of the cast shadow, given as the sine of the viewing angle between the imaginary ground plane and the eye, in the range sin(5°) to sin(35°); it controls how much the contact shadow is foreshortened. The default is sin(10°).")


@wire(
    "com.apple.apps.content-language.curved-shadow",
    version="1.0",
    fields=[
        ("angle", (1, 0), "def"),
        ("opacity", (1, 0), "def"),
        ("color", (1, 0), "opt"),
        ("offset", (1, 0), "def"),
        ("radius", (1, 0), "def"),
        ("curve", (1, 0), "def"),
    ],
)
class CurvedShadow(ObjectModel):
    """A shadow whose silhouette curls away from the object, as if it were a page lifting off the surface rather than lying flat."""
    angle: float = Field(default=270, ge=0, le=360, description="The angle at which the shadow is offset from its default position, directly below the object. It's in degrees, in the range `0` to `360`, measured counterclockwise with `0` corresponding to horizontal left-to-right.")
    opacity: float = Field(default=1, ge=0, le=1, description="The opacity of the cast shadow, in the range `0` to `1`.")
    color: Color | None = Field(default=None, description="The color of the cast shadow. If absent, the shadow is black.")
    offset: float = Field(default=1, ge=-50, le=50, description="The amount by which the shadow is offset from its default position, in the direction of `angle`, in the range `-50` to `50`.")
    radius: float = Field(default=0, ge=0, le=100, description="The radius (size) of the cast shadow's blur, in the range `0` to `100`.")
    curve: float = Field(default=1, ge=-1, le=1, description="The amount by which the shadow curls away from the object, in the range `-1` to `1`. When `curve` is `0`, the shadow is cast as though the object were lying flat. Negative values of `curve` make the cast shadow appear as though the object were concave, with the left and right edges bulging toward the viewer; positive values make the cast shadow appear as though the object were convex, with the vertical center axis bulging toward the viewer.")


@wire(
    "com.apple.apps.content-language.drop-shadow",
    version="1.0",
    fields=[
        ("angle", (1, 0), "def"),
        ("opacity", (1, 0), "def"),
        ("color", (1, 0), "opt"),
        ("offset", (1, 0), "def"),
        ("radius", (1, 0), "def"),
    ],
)
class DropShadow(ObjectModel):
    """A shadow whose silhouette appears as though cast by a light source facing down toward the plane of the object.

The silhouette is blurred by `radius` and displaced `offset` points in the direction given by `angle`. It's the simplest of the three shadow kinds."""
    angle: float = Field(default=270, ge=0, le=360, description="The angle at which the shadow is offset from its default position, directly below the object. It's in degrees, in the range `0` to `360`, measured counterclockwise with `0` corresponding to horizontal left-to-right.")
    opacity: float = Field(default=1, ge=0, le=1, description="The opacity of the cast shadow, in the range `0` to `1`.")
    color: Color | None = Field(default=None, description="The color of the cast shadow. If absent, the shadow is black.")
    offset: float = Field(default=2, ge=0, le=50, description="The distance, in points, by which the shadow is offset from its default position, in the direction of `angle`, in the range `0` to `50`.")
    radius: float = Field(default=5, ge=0, le=100, description="The radius (size) of the cast shadow's blur, in the range `0` to `100`.")


@wire_union(
    "com.apple.apps.content-language.duration",
    version="1.0",
    cases=[
        ("seconds", (1, 0), False),
    ],
)
class Duration(TaggedUnionModel):
    """A length of time.

The only representation is a number of seconds."""
    seconds: float | None = Field(default=None, description="A length of time in seconds.")

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_DurationCase, ...]: ...

        def union_primary(self) -> _DurationCase | None: ...

        def union_primary_name(self) -> Literal["seconds"] | None: ...


@wire_union(
    "com.apple.apps.content-language.fill",
    version="1.0",
    cases=[
        ("color", (1, 0), False),
        ("gradient", (1, 0), False),
        ("image", (1, 0), False),
    ],
)
class Fill(TaggedUnionModel):
    """A style that fills an area with exactly one of a solid color, a gradient, or an image."""
    color: Color | None = Field(default=None, description="A solid color fill.")
    gradient: Gradient | None = Field(default=None, description="A gradient fill, either linear or radial.")
    image: ImageFill | None = Field(default=None, description="An image fill, with optional scale and tint.")

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_FillCase, ...]: ...

        def union_primary(self) -> _FillCase | None: ...

        def union_primary_name(self) -> Literal["color", "gradient", "image"] | None: ...


@wire(
    "com.apple.apps.content-language.fill.gradient",
    version="1.1",
    fields=[
        ("is_advanced", (1, 1), "def"),
        ("stops", (1, 0), "req"),
        ("opacity", (1, 0), "def"),
        ("flavor", (1, 0), "req"),
    ],
)
class Gradient(ObjectModel):
    """A fill with a continuous gradient between two or more colors."""
    is_advanced: bool = Field(default=False, description="Whether the gradient is an advanced gradient. It's independent of the linear or radial `flavor` and doesn't affect rendering.")
    stops: list[Stop] = Field(description="The color stops that define the gradient, ordered from the start of the gradient to its end. A gradient must have at least two stops. An array with fewer than two stops is padded to two on read; an empty one produces a fully transparent gradient. If a stop's `fraction` isn't greater than the previous stop's, it's shown immediately after the previous stop.")
    opacity: float = Field(default=1, ge=0, le=1, description="The opacity of the gradient, in the range `0` to `1`.")
    flavor: Flavor = Field(description="The kind of gradient, linear or radial, along with the geometry that positions it.")


@wire(
    "com.apple.apps.content-language.fill.gradient.stop",
    version="1.0",
    fields=[
        ("color", (1, 0), "req"),
        ("fraction", (1, 0), "req"),
        ("inflection", (1, 0), "def"),
    ],
)
class Stop(ObjectModel):
    """One color in the gradient, and its position along it."""
    color: Color = Field(description="The stop's color.")
    fraction: float = Field(ge=0, le=1, description="The position of the stop within the entire gradient, in the range `0` to `1`. Each stop must have its position at or after the position of the previous stop.")
    inflection: float = Field(default=0.5, ge=0, le=1, description="A position between the stop and the following stop that defines where the halfway blend of the two stops' colors falls, as a fraction of the distance between them. An inflection of 0.5 blends two stops evenly; lower values pull the blend toward the stop, and higher values toward the following stop. Has no effect on the last stop.")


@wire_union(
    "com.apple.apps.content-language.fill.gradient.flavor",
    version="1.0",
    cases=[
        ("linear", (1, 0), False),
        ("radial", (1, 0), False),
    ],
)
class Flavor(TaggedUnionModel):
    """A method for laying out a gradient's stops over the area being filled.

Each case's value gives the geometry that positions the stops."""
    linear: Linear | None = Field(default=None, description="A gradient that varies along a straight line between its stops.")
    radial: Radial | None = Field(default=None, description="A gradient that spreads outward from a center point.")

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_FlavorCase, ...]: ...

        def union_primary(self) -> _FlavorCase | None: ...

        def union_primary_name(self) -> Literal["linear", "radial"] | None: ...


@wire(
    "com.apple.apps.content-language.fill.gradient.flavor.linear",
    version="1.1",
    fields=[
        ("angle", (1, 0), "req"),
        ("start_point", (1, 1), "opt"),
        ("end_point", (1, 1), "opt"),
        ("base_natural_size", (1, 1), "opt"),
    ],
)
class Linear(ObjectModel):
    """A gradient that lays out its stops along a straight line.

`angle` alone fits the line to the filled shape's bounds, so the whole stop range is visible. `start_point`, `end_point`, and `base_natural_size` place it exactly, possibly running past those bounds; the points are in the shape's untransformed space, in points with y increasing downward, and rescale when the object's size differs from `base_natural_size`. Those three are read only together: with any of them missing, the gradient falls back to `angle` and discards the points."""
    angle: float = Field(ge=0, le=360, description="The angle in degrees at which the gradient runs, in the range `0` to `360` (exclusive) measured counterclockwise with `0` corresponding to horizontal left-to-right. Ignored if `start_point`, `end_point`, and `base_natural_size` are all present; `angle` remains the fallback for version 1.0 readers, which predate those properties.")
    start_point: Position | None = Field(default=None, description="If present, the starting point of the line along which the gradient's colors change, relative to a rectangle defined by `base_natural_size`. If it's present, it must be combined with `end_point` and `base_natural_size`; when all three are present, they take precedence over `angle`. Version 1.0 readers ignore it and render from `angle`.")
    end_point: Position | None = Field(default=None, description="If present, the end point of the line along which the gradient's colors change, relative to a rectangle defined by `base_natural_size`. If it's present, it must be combined with `start_point` and `base_natural_size`. For details, see `start_point`.")
    base_natural_size: Size | None = Field(default=None, description="If present, the size of the rectangle that `start_point` and `end_point` are relative to. When filling an area, the gradient's start and end points are transformed so that this size covers the filled area. For details, see `start_point`.")


@wire(
    "com.apple.apps.content-language.fill.gradient.flavor.radial",
    version="1.0",
    fields=[
        ("start_point", (1, 0), "req"),
        ("end_point", (1, 0), "req"),
        ("base_natural_size", (1, 0), "req"),
    ],
)
class Radial(ObjectModel):
    """A gradient that spreads its stops outward from a center point, with a second point fixing the radius and the direction of the outer edge.

Both points are in the filled shape's untransformed space, in points with y increasing downward; `base_natural_size` is the size that space was captured at, so the gradient rescales when the object's size differs from it."""
    start_point: Position = Field(description="The center point of the radial gradient, relative to a rectangle defined by `base_natural_size`.")
    end_point: Position = Field(description="A point on the outer edge of the radial gradient, relative to a rectangle defined by `base_natural_size`. Together with `start_point`, it sets the gradient's radius and direction.")
    base_natural_size: Size = Field(description="The size of the rectangle that `start_point` and `end_point` are relative to. When filling an area, the gradient's start and end points are transformed so that this size covers the filled area.")


@wire(
    "com.apple.apps.content-language.fill.image-fill",
    version="1.0",
    fields=[
        ("resource", (1, 0), "req"),
        ("technique", (1, 0), "req"),
        ("scale_percent", (1, 0), "def"),
        ("tint_color", (1, 0), "opt"),
    ],
)
class ImageFill(ObjectModel):
    """An image that the reader uses to fill an area."""
    resource: Resource = Field(description="The resource containing the image fill's data.")
    technique: Technique = Field(strict=False, description="How the image fill covers the filled area.")
    scale_percent: float = Field(default=100, ge=10, le=200, description="A scale applied to the image resource's natural size, as a percentage in the range `10` to `200`; a value of 100 shows the image at its natural size. Used only when `technique` is `natural_size` or `tile`.")
    tint_color: Color | None = Field(default=None, description="A color laid over the image, usually with an opacity less than 1. The default is none.")


class Technique(str, Enum):
    """The technique the reader uses to fit the image to the fill area.

The technique also determines whether the image keeps its aspect ratio: one technique distorts the image to the area, two preserve the ratio (cropping the overhang or leaving the area showing through), and two show the image at a size of its own.

    natural_size — Draws the image once at its own size, scaled by `Fill.ImageFill.scale_percent`, centered in the area and clipped by it, so a larger image is cropped on all four sides and a smaller one leaves the area showing around it.
    scale_to_fill — Draws the image so that it keeps its aspect ratio and completely covers the filled area, cropping what overhangs on the longer axis.
    scale_to_fit — Draws the image so that it keeps its aspect ratio and fits completely within the filled area, which shows through on the two sides where the image falls short.
    stretch — Draws the image stretched over the filled area, scaling its width and height independently and distorting it unless the area already shares the image's proportions.
    tile — Repeats the image at its own size, scaled by `Fill.ImageFill.scale_percent`, to cover the area. The first tile is placed at the filled area's top-left corner.
    """
    NATURAL_SIZE = "natural_size"
    SCALE_TO_FILL = "scale_to_fill"
    SCALE_TO_FIT = "scale_to_fit"
    STRETCH = "stretch"
    TILE = "tile"


@wire_union(
    "com.apple.apps.content-language.hyperlink",
    version="1.0",
    cases=[
        ("file", (1, 0), False),
        ("program", (1, 0), False),
        ("slide_jump", (1, 0), False),
        ("url", (1, 0), False),
    ],
)
class Hyperlink(TaggedUnionModel):
    """A clickable link attached to text.

The target is a URL, a jump to another slide in the same presentation, a file, or an opaque program action."""
    file: str | None = Field(default=None, description="A relative or absolute file path or a file URL.")
    program: str | None = Field(default=None, description="An opaque action. \n\nThe recognized value is `exit_slideshow`, which exits the slideshow. Keynote preserves unrecognized values verbatim and produces a warning on import.")
    slide_jump: SlideTarget | None = Field(default=None, description="A jump to another slide in the same presentation.")
    url: str | None = Field(default=None, description="An absolute URL with any scheme other than `file:`, such as `https://...`, `mailto:...`, `tel:+...`, or `keynote://...`.")

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_HyperlinkCase, ...]: ...

        def union_primary(self) -> _HyperlinkCase | None: ...

        def union_primary_name(self) -> Literal["file", "program", "slide_jump", "url"] | None: ...


@wire_union(
    "com.apple.apps.content-language.hyperlink.slide-target",
    version="1.0",
    cases=[
        ("by_identifier", (1, 0), False),
        ("first", (1, 0), True),
        ("last", (1, 0), True),
        ("last_viewed", (1, 0), True),
        ("next", (1, 0), True),
        ("previous", (1, 0), True),
    ],
)
class SlideTarget(TaggedUnionModel):
    """A target slide inside the same presentation, given either by identifier or by position.

The five position cases have no settings of their own, can be written as a plain string, and are the dependable choice when authoring, because they are resolved at the moment the link is followed. `by_identifier` is meaningful only against identifiers belonging to the document being read."""
    by_identifier: str | None = Field(default=None, description="References the `Slide.identifier` of a slide in the same presentation. The value is stored exactly as supplied, and reading a presentation assigns every slide a fresh identifier, so a link whose value matches no identifier in the document being read does nothing when it's followed.")
    first: Literal[True] | None = Field(default=None, description="The first slide in the presentation.")
    last: Literal[True] | None = Field(default=None, description="The last slide in the presentation.")
    last_viewed: Literal[True] | None = Field(default=None, description="The slide most recently viewed before the slide.")
    next: Literal[True] | None = Field(default=None, description="The slide immediately after the slide containing the link.")
    previous: Literal[True] | None = Field(default=None, description="The slide immediately before the slide containing the link.")

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_SlideTargetCase, ...]: ...

        def union_primary(self) -> _SlideTargetCase | None: ...

        def union_primary_name(self) -> Literal["by_identifier", "first", "last", "last_viewed", "next", "previous"] | None: ...


class LineEnd(str, Enum):
    """A decoration drawn at the end of a connection line or of a shape's open path, such as an arrowhead.

Decorations that can't be represented by one of these cases are written as `simple_arrow`.

    filled_arrow — A filled arrowhead, with a notched base. Shown in Keynote as “Filled arrow.”
    filled_circle — A filled circle. Shown in Keynote as “Filled circle.”
    filled_diamond — A filled diamond. Shown in Keynote as “Filled diamond.”
    filled_square — A filled square. Shown in Keynote as “Filled square.”
    inverted_arrow — A triangular arrowhead that points toward the center of the line instead of away from it. Shown in Keynote as “Inverted arrow.”
    line — A straight line across the end of the line, perpendicular to it. Shown in Keynote as Line.
    none — No decoration at this end of the line. Shown in Keynote as None.
    open_arrow — An open arrowhead. Shown in Keynote as “Open arrow.”
    open_circle — An open circle. Shown in Keynote as “Open circle.”
    open_square — An open square. Shown in Keynote as “Open square.”
    simple_arrow — A simple arrowhead. Shown in Keynote as “Simple arrow.”
    """
    FILLED_ARROW = "filled_arrow"
    FILLED_CIRCLE = "filled_circle"
    FILLED_DIAMOND = "filled_diamond"
    FILLED_SQUARE = "filled_square"
    INVERTED_ARROW = "inverted_arrow"
    LINE = "line"
    NONE = "none"
    OPEN_ARROW = "open_arrow"
    OPEN_CIRCLE = "open_circle"
    OPEN_SQUARE = "open_square"
    SIMPLE_ARROW = "simple_arrow"


@wire(
    "com.apple.apps.content-language.playback-options",
    version="1.0",
    fields=[
        ("volume", (1, 0), "def"),
        ("start_time", (1, 0), "opt"),
        ("end_time", (1, 0), "opt"),
        ("loop_option", (1, 0), "def"),
        ("plays_across_slides", (1, 0), "def"),
    ],
)
class PlaybackOptions(ObjectModel):
    """Options controlling playback of media."""
    volume: float = Field(default=1, ge=0, le=1, description="The audio volume for playback, where 0.0 is silent and 1.0 is full volume.")
    start_time: Duration | None = Field(default=None, description="The playback start time. If it's absent, negative, or later than the end of the media, playback starts at the beginning.")
    end_time: Duration | None = Field(default=None, description="The playback end time. If it's absent, later than the end of the media, or earlier than `start_time`, playback continues to the end of the media.")
    loop_option: LoopOption = Field(default_factory=lambda: LoopOption.NONE, strict=False, description="How playback repeats after reaching the end time.")
    plays_across_slides: bool = Field(default=False, description="Whether the media plays across slides.")


class LoopOption(str, Enum):
    """The behavior of playback when it reaches the end time.

    back_and_forth — Plays the media repeatedly forward from `start_time` to `end_time` and then backward from `end_time` to `start_time`. Not supported by all media; `none` is used instead. Shown in Keynote as Loop Back and Forth.
    none — Plays the media once through and then stops.
    repeating — Plays the media repeatedly from `start_time` to `end_time`. Shown in Keynote as Loop.
    """
    BACK_AND_FORTH = "back_and_forth"
    NONE = "none"
    REPEATING = "repeating"


@wire(
    "com.apple.apps.content-language.reflection",
    version="1.0",
    fields=[
        ("opacity", (1, 0), "def"),
        ("fade_acceleration", (1, 0), "def"),
    ],
)
class Reflection(ObjectModel):
    """A mirrored copy of the object that the reader drew directly below it on a ground plane aligned to the horizontal axis, fading out with distance.

It extends down 40% of the object's height, at most 120 points."""
    opacity: float = Field(default=1, ge=0, le=1, description="The reflection's opacity where it meets the object, in the range `0` to `1` (`0` is invisible). The reflection fades away from this opacity to zero as it extends farther down, at a rate set by `fade_acceleration`.")
    fade_acceleration: float = Field(default=1, ge=1, description="An exponent, `1` or greater, that sets how quickly the reflection fades from `opacity` to clear. A value of `1` fades linearly to 40% of the object's height (at most 120 points) when measured from the apparent ground plane, and larger values fade out more quickly.")


@wire_union(
    "com.apple.apps.content-language.shadow",
    version="1.1",
    cases=[
        ("contactShadow", (1, 0), False),
        ("curvedShadow", (1, 0), False),
        ("dropShadow", (1, 0), False),
        ("none", (1, 1), True),
    ],
)
class Shadow(TaggedUnionModel):
    """The kind of shadow cast by an object, or `none` for no shadow."""
    contactShadow: ContactShadow | None = Field(default=None, description="A contact shadow, cast by a light directly above the object.")
    curvedShadow: CurvedShadow | None = Field(default=None, description="A curved shadow, cast as though the object were curled.")
    dropShadow: DropShadow | None = Field(default=None, description="A drop shadow, cast from above the plane of the document.")
    none: Literal[True] | None = Field(default=None, description="No shadow. This case is accepted when reading but isn't written; the shadow property is omitted instead.")

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_ShadowCase, ...]: ...

        def union_primary(self) -> _ShadowCase | None: ...

        def union_primary_name(self) -> Literal["contactShadow", "curvedShadow", "dropShadow", "none"] | None: ...


@wire_union(
    "com.apple.apps.content-language.stroke",
    version="1.0",
    cases=[
        ("empty", (1, 0), True),
        ("frame", (1, 0), False),
        ("line", (1, 0), False),
    ],
)
class Stroke(TaggedUnionModel):
    """A stroke drawn along a path, such as a border around an object.

The stroke is a line or a picture frame, or `empty` for no stroke or border."""
    empty: Literal[True] | None = Field(default=None, description="No stroke or border.")
    frame: Frame | None = Field(default=None, description="A border drawn as a rectangular picture frame.")
    line: Line | None = Field(default=None, description="A stroke or border drawn as a line in one of several styles.")

    if TYPE_CHECKING:
        def union_cases(self) -> tuple[_StrokeCase, ...]: ...

        def union_primary(self) -> _StrokeCase | None: ...

        def union_primary_name(self) -> Literal["empty", "frame", "line"] | None: ...


@wire(
    "com.apple.apps.content-language.stroke.line",
    version="1.0",
    fields=[
        ("color", (1, 0), "opt"),
        ("width", (1, 0), "def"),
        ("pattern", (1, 0), "def"),
    ],
)
class Line(ObjectModel):
    """A stroke or border that the reader draws as a line in one of several styles."""
    color: Color | None = Field(default=None, description="The color of the stroke. If absent, the stroke is black.")
    width: float = Field(default=1, ge=0.25, le=100, description="The width of the stroke, in points.")
    pattern: Pattern = Field(default_factory=lambda: Pattern.SOLID, strict=False, description="The pattern of the stroke: solid, dashed, or one of several brush styles.")


class Pattern(str, Enum):
    """The pattern that the reader uses to draw a stroke: solid, one of the dash styles, or one of the brush styles.

`round_dash` also rounds the line's caps and joins, and a dashed line with round caps is written as `round_dash` regardless of its dash pattern. Without round caps, a dash pattern that doesn't match one of these cases is written as `short_dash`.

    calligraphy — A line that appears to be drawn with a calligraphy pen. Shown in Keynote as Calligraphy.
    chalk — A line that appears to be drawn with a piece of chalk pulled along a chalkboard. Shown in Keynote as Chalk.
    dry_brush — A line that appears to be painted with a dry brush on paper. Shown in Keynote as “Dry brush.”
    feathered_brush — A line that appears to be painted with a feathered brush on paper. Shown in Keynote as “Feathered brush.”
    long_dash — A dashed line with long dashes. Shown in Keynote as “Long dash.”
    medium_dash — A dashed line with medium dashes. Shown in Keynote as “Medium dash.”
    pen — A line that appears to be drawn with a pen that has uneven ink flow. Shown in Keynote as Pen.
    round_dash — A dotted line, drawn with small round dashes. Shown in Keynote as “Rounded dash.”
    short_dash — A dashed line with short dashes. Shown in Keynote as “Short dash.”
    solid — A solid line. Shown in Keynote as Solid.
    """
    CALLIGRAPHY = "calligraphy"
    CHALK = "chalk"
    DRY_BRUSH = "dry_brush"
    FEATHERED_BRUSH = "feathered_brush"
    LONG_DASH = "long_dash"
    MEDIUM_DASH = "medium_dash"
    PEN = "pen"
    ROUND_DASH = "round_dash"
    SHORT_DASH = "short_dash"
    SOLID = "solid"


@wire(
    "com.apple.apps.content-language.stroke.frame",
    version="1.0",
    fields=[
        ("name", (1, 0), "req"),
        ("scale_percent", (1, 0), "def"),
    ],
)
class Frame(ObjectModel):
    """A picture frame drawn around an object as its border."""
    name: Name = Field(strict=False, description="The name of the picture frame.")
    scale_percent: float = Field(default=100, ge=10, le=100, description="The scale applied to the picture frame artwork, as a percentage, in the range `10` to `100`. Some picture frames have an effective minimum higher than 10%, and a smaller value is raised to that minimum.")


class Name(str, Enum):
    """The name of the picture frame that Keynote uses to draw the border.

 This frame is one of the artworks that Keynote ships. Only the frame listed here can be written, so when an object has any other frame, Keynote writes it with no border. If a frame of the given name can't be found, the stroke is skipped rather than being replaced with a line, leaving the object unframed.

    photo_portfolio1 — The picture frame shown in Keynote as “Photo portfolio.”
    renaissance1 — The picture frame shown in Keynote as Renaissance.
    scrapbook2b — The picture frame shown in Keynote as Scrapbook 2.
    """
    ANTIQUE = "antique"
    CRAYON_LINE = "crayon_line"
    FORMAL_INSET = "formal_inset"
    FORMAL_SHADOW = "formal_shadow"
    GRAPH_PAPER = "graph_paper"
    HEADLINES = "headlines"
    JET_SET = "jet_set"
    PHOTO_PORTFOLIO1 = "photo_portfolio1"
    PORTFOLIO_INSET = "portfolio_inset"
    PUSHPIN = "pushpin"
    RENAISSANCE1 = "renaissance1"
    SCRAPBOOK2B = "scrapbook2b"
    STORYBOARD = "storyboard"
    VINTAGE_INSET = "vintage_inset"



# Resolve forward references between models declared in this module.
Audio.model_rebuild()
GenericCanvasObject.model_rebuild()
CanvasObject.model_rebuild()
GenericCaptionOwning.model_rebuild()
CaptionOwning.model_rebuild()
Area3DChart.model_rebuild()
AreaChart.model_rebuild()
Bar3DChart.model_rebuild()
BarChart.model_rebuild()
BarInteractiveChart.model_rebuild()
BubbleChart.model_rebuild()
BubbleInteractiveChart.model_rebuild()
GenericCategoryComparisonChart.model_rebuild()
CategoryComparisonChart.model_rebuild()
Chart.model_rebuild()
GenericChartAxisCommon.model_rebuild()
ChartAxisCommon.model_rebuild()
AxisLabelOrientation.model_rebuild()
ChartCategoryAxis.model_rebuild()
LabelSpacing.model_rebuild()
GenericChartCommon.model_rebuild()
ChartCommon.model_rebuild()
ChartColor.model_rebuild()
ChartData.model_rebuild()
ChartDataRow.model_rebuild()
ChartDataValue.model_rebuild()
GenericChartLabelFormatting.model_rebuild()
ChartLabelFormatting.model_rebuild()
ChartLegend.model_rebuild()
ChartSeries.model_rebuild()
ChartValueAxis.model_rebuild()
Column3DChart.model_rebuild()
ColumnChart.model_rebuild()
ColumnInteractiveChart.model_rebuild()
GenericCorrelationChart.model_rebuild()
CorrelationChart.model_rebuild()
DonutChart.model_rebuild()
Line3DChart.model_rebuild()
LineChart.model_rebuild()
MixedChart.model_rebuild()
Pie3DChart.model_rebuild()
PieChart.model_rebuild()
RadarChart.model_rebuild()
ScatterChart.model_rebuild()
ScatterInteractiveChart.model_rebuild()
StackedArea3DChart.model_rebuild()
StackedAreaChart.model_rebuild()
StackedBar3DChart.model_rebuild()
StackedBarChart.model_rebuild()
StackedColumn3DChart.model_rebuild()
StackedColumnChart.model_rebuild()
TwoAxisChart.model_rebuild()
ConnectionLine.model_rebuild()
LineType.model_rebuild()
End.model_rebuild()
Anchor.model_rebuild()
Magnet.model_rebuild()
Group.model_rebuild()
Image.model_rebuild()
Mask.model_rebuild()
InstantAlphaPath.model_rebuild()
Label.model_rebuild()
Movie.model_rebuild()
GenericPlaceableTitleOwning.model_rebuild()
PlaceableTitleOwning.model_rebuild()
Shape.model_rebuild()
Table.model_rebuild()
ColumnHeader.model_rebuild()
TableColumnHeaderKind.model_rebuild()
TableColumnHeaderGroupLabel.model_rebuild()
Row.model_rebuild()
TableRowKind.model_rebuild()
TableRowGroupLabel.model_rebuild()
CellProperties.model_rebuild()
Cell.model_rebuild()
UnformattedValue.model_rebuild()
Formula.model_rebuild()
IdBasedFormula.model_rebuild()
CellReference.model_rebuild()
Strokes.model_rebuild()
CellRange.model_rebuild()
RowColumnIdRange.model_rebuild()
VisualProperties.model_rebuild()
OverallProperties.model_rebuild()
BodyStrokeProperties.model_rebuild()
HeaderFooterStrokeProperties.model_rebuild()
StrokePreset.model_rebuild()
CellFormat.model_rebuild()
NumberFormat.model_rebuild()
CurrencyFormat.model_rebuild()
FractionFormat.model_rebuild()
BaseFormat.model_rebuild()
BoolFormat.model_rebuild()
DurationFormat.model_rebuild()
DateTimeFormat.model_rebuild()
Date.model_rebuild()
Predicate.model_rebuild()
Value.model_rebuild()
Reference.model_rebuild()
CustomFormat.model_rebuild()
NumberFormatData.model_rebuild()
CustomFormatCondition.model_rebuild()
ConditionalStyleSet.model_rebuild()
TableConditionalStyleSetRule.model_rebuild()
TransformationInfo.model_rebuild()
Structure.model_rebuild()
FilterSet.model_rebuild()
Filter.model_rebuild()
TableFilterSetFilterRule.model_rebuild()
Sort.model_rebuild()
TableSortRule.model_rebuild()
PivotRules.model_rebuild()
CategoryRules.model_rebuild()
Textbox.model_rebuild()
GenericTitleOwning.model_rebuild()
TitleOwning.model_rebuild()
Geometry.model_rebuild()
Path.model_rebuild()
BezierPath.model_rebuild()
Position.model_rebuild()
Rect.model_rebuild()
Size.model_rebuild()
KeynoteTheme.model_rebuild()
Presentation.model_rebuild()
Slide.model_rebuild()
SlideBackground.model_rebuild()
SlideLayout.model_rebuild()
SlideObject.model_rebuild()
PlaceholderInfo.model_rebuild()
PlaceholderDefinition.model_rebuild()
Resource.model_rebuild()
IndirectResource.model_rebuild()
Base64EncodedResource.model_rebuild()
PremiumResourceInfo.model_rebuild()
Stylesheet.model_rebuild()
ShapeStyle.model_rebuild()
ShapeProperties.model_rebuild()
MediaStyle.model_rebuild()
MediaProperties.model_rebuild()
TableStyleCollection.model_rebuild()
OverallStyle.model_rebuild()
CellStyle.model_rebuild()
BodyStrokeStyle.model_rebuild()
HeaderFooterStrokeStyle.model_rebuild()
ParagraphStyle.model_rebuild()
CharacterStyle.model_rebuild()
ListStyle.model_rebuild()
CharacterProperties.model_rebuild()
FontFeaturesType.model_rebuild()
ColumnMetrics.model_rebuild()
EqualColumnsDescription.model_rebuild()
UnequalColumnsDescription.model_rebuild()
Insets.model_rebuild()
LayoutProperties.model_rebuild()
LineSpacingType.model_rebuild()
ListLabelType.model_rebuild()
ListNumberLabel.model_rebuild()
ListStringLabel.model_rebuild()
ListImageLabel.model_rebuild()
ListLevelType.model_rebuild()
ListProperties.model_rebuild()
NumberFormatType.model_rebuild()
Offset.model_rebuild()
Paragraph.model_rebuild()
Constituent.model_rebuild()
HyperlinkField.model_rebuild()
ParagraphProperties.model_rebuild()
BorderStyleType.model_rebuild()
TabStopType.model_rebuild()
Text.model_rebuild()
TextRun.model_rebuild()
TextStroke.model_rebuild()
Color.model_rebuild()
RGBA.model_rebuild()
ContactShadow.model_rebuild()
CurvedShadow.model_rebuild()
DropShadow.model_rebuild()
Duration.model_rebuild()
Fill.model_rebuild()
Gradient.model_rebuild()
Stop.model_rebuild()
Flavor.model_rebuild()
Linear.model_rebuild()
Radial.model_rebuild()
ImageFill.model_rebuild()
Hyperlink.model_rebuild()
SlideTarget.model_rebuild()
PlaybackOptions.model_rebuild()
Reflection.model_rebuild()
Shadow.model_rebuild()
Stroke.model_rebuild()
Line.model_rebuild()
Frame.model_rebuild()


if TYPE_CHECKING:
    _CanvasObjectCase = (
        tuple[Literal["audio"], Audio]
        | tuple[Literal["chart"], Chart]
        | tuple[Literal["connectionLine"], ConnectionLine]
        | tuple[Literal["genericCanvasObject"], GenericCanvasObject]
        | tuple[Literal["group"], Group]
        | tuple[Literal["image"], Image]
        | tuple[Literal["movie"], Movie]
        | tuple[Literal["shape"], Shape]
        | tuple[Literal["table"], Table]
        | tuple[Literal["textbox"], Textbox]
    )

    _CaptionOwningCase = (
        tuple[Literal["genericCaptionOwning"], GenericCaptionOwning]
    )

    _CategoryComparisonChartCase = (
        tuple[Literal["area3Dchart"], Area3DChart]
        | tuple[Literal["areaChart"], AreaChart]
        | tuple[Literal["bar3Dchart"], Bar3DChart]
        | tuple[Literal["barChart"], BarChart]
        | tuple[Literal["barInteractiveChart"], BarInteractiveChart]
        | tuple[Literal["column3Dchart"], Column3DChart]
        | tuple[Literal["columnChart"], ColumnChart]
        | tuple[Literal["columnInteractiveChart"], ColumnInteractiveChart]
        | tuple[Literal["genericCategoryComparisonChart"], GenericCategoryComparisonChart]
        | tuple[Literal["line3Dchart"], Line3DChart]
        | tuple[Literal["lineChart"], LineChart]
        | tuple[Literal["mixedChart"], MixedChart]
        | tuple[Literal["radarChart"], RadarChart]
        | tuple[Literal["stackedArea3Dchart"], StackedArea3DChart]
        | tuple[Literal["stackedAreaChart"], StackedAreaChart]
        | tuple[Literal["stackedBar3Dchart"], StackedBar3DChart]
        | tuple[Literal["stackedBarChart"], StackedBarChart]
        | tuple[Literal["stackedColumn3Dchart"], StackedColumn3DChart]
        | tuple[Literal["stackedColumnChart"], StackedColumnChart]
        | tuple[Literal["twoAxisChart"], TwoAxisChart]
    )

    _ChartCase = (
        tuple[Literal["area"], AreaChart]
        | tuple[Literal["area_3d"], Area3DChart]
        | tuple[Literal["bar"], BarChart]
        | tuple[Literal["bar_3d"], Bar3DChart]
        | tuple[Literal["bar_interactive"], BarInteractiveChart]
        | tuple[Literal["bubble"], BubbleChart]
        | tuple[Literal["bubble_interactive"], BubbleInteractiveChart]
        | tuple[Literal["column"], ColumnChart]
        | tuple[Literal["column_3d"], Column3DChart]
        | tuple[Literal["column_interactive"], ColumnInteractiveChart]
        | tuple[Literal["donut"], DonutChart]
        | tuple[Literal["line"], LineChart]
        | tuple[Literal["line_3d"], Line3DChart]
        | tuple[Literal["mixed"], MixedChart]
        | tuple[Literal["pie"], PieChart]
        | tuple[Literal["pie_3d"], Pie3DChart]
        | tuple[Literal["radar"], RadarChart]
        | tuple[Literal["scatter"], ScatterChart]
        | tuple[Literal["scatter_interactive"], ScatterInteractiveChart]
        | tuple[Literal["stacked_area"], StackedAreaChart]
        | tuple[Literal["stacked_area_3d"], StackedArea3DChart]
        | tuple[Literal["stacked_bar"], StackedBarChart]
        | tuple[Literal["stacked_bar_3d"], StackedBar3DChart]
        | tuple[Literal["stacked_column"], StackedColumnChart]
        | tuple[Literal["stacked_column_3d"], StackedColumn3DChart]
        | tuple[Literal["two_axis"], TwoAxisChart]
    )

    _ChartAxisCommonCase = (
        tuple[Literal["chartCategoryAxis"], ChartCategoryAxis]
        | tuple[Literal["chartValueAxis"], ChartValueAxis]
        | tuple[Literal["genericChartAxisCommon"], GenericChartAxisCommon]
    )

    _AxisLabelOrientationCase = (
        tuple[Literal["custom"], float]
        | tuple[Literal["horizontal"], Literal[True]]
        | tuple[Literal["left_diagonal"], Literal[True]]
        | tuple[Literal["left_vertical"], Literal[True]]
        | tuple[Literal["parallel"], Literal[True]]
        | tuple[Literal["perpendicular"], Literal[True]]
        | tuple[Literal["right_diagonal"], Literal[True]]
        | tuple[Literal["right_vertical"], Literal[True]]
    )

    _LabelSpacingCase = (
        tuple[Literal["auto_fit"], Literal[True]]
        | tuple[Literal["custom"], int]
        | tuple[Literal["none"], Literal[True]]
        | tuple[Literal["show_all"], Literal[True]]
    )

    _ChartCommonCase = (
        tuple[Literal["area3Dchart"], Area3DChart]
        | tuple[Literal["areaChart"], AreaChart]
        | tuple[Literal["bar3Dchart"], Bar3DChart]
        | tuple[Literal["barChart"], BarChart]
        | tuple[Literal["barInteractiveChart"], BarInteractiveChart]
        | tuple[Literal["bubbleChart"], BubbleChart]
        | tuple[Literal["bubbleInteractiveChart"], BubbleInteractiveChart]
        | tuple[Literal["column3Dchart"], Column3DChart]
        | tuple[Literal["columnChart"], ColumnChart]
        | tuple[Literal["columnInteractiveChart"], ColumnInteractiveChart]
        | tuple[Literal["donutChart"], DonutChart]
        | tuple[Literal["genericChartCommon"], GenericChartCommon]
        | tuple[Literal["line3Dchart"], Line3DChart]
        | tuple[Literal["lineChart"], LineChart]
        | tuple[Literal["mixedChart"], MixedChart]
        | tuple[Literal["pie3Dchart"], Pie3DChart]
        | tuple[Literal["pieChart"], PieChart]
        | tuple[Literal["radarChart"], RadarChart]
        | tuple[Literal["scatterChart"], ScatterChart]
        | tuple[Literal["scatterInteractiveChart"], ScatterInteractiveChart]
        | tuple[Literal["stackedArea3Dchart"], StackedArea3DChart]
        | tuple[Literal["stackedAreaChart"], StackedAreaChart]
        | tuple[Literal["stackedBar3Dchart"], StackedBar3DChart]
        | tuple[Literal["stackedBarChart"], StackedBarChart]
        | tuple[Literal["stackedColumn3Dchart"], StackedColumn3DChart]
        | tuple[Literal["stackedColumnChart"], StackedColumnChart]
        | tuple[Literal["twoAxisChart"], TwoAxisChart]
    )

    _ChartDataValueCase = (
        tuple[Literal["date"], Date]
        | tuple[Literal["duration"], Duration]
        | tuple[Literal["empty"], Literal[True]]
        | tuple[Literal["number"], float]
    )

    _ChartLabelFormattingCase = (
        tuple[Literal["chartCategoryAxis"], ChartCategoryAxis]
        | tuple[Literal["chartSeries"], ChartSeries]
        | tuple[Literal["chartValueAxis"], ChartValueAxis]
        | tuple[Literal["genericChartLabelFormatting"], GenericChartLabelFormatting]
    )

    _CorrelationChartCase = (
        tuple[Literal["bubbleChart"], BubbleChart]
        | tuple[Literal["bubbleInteractiveChart"], BubbleInteractiveChart]
        | tuple[Literal["genericCorrelationChart"], GenericCorrelationChart]
        | tuple[Literal["scatterChart"], ScatterChart]
        | tuple[Literal["scatterInteractiveChart"], ScatterInteractiveChart]
    )

    _LineTypeCase = (
        tuple[Literal["corner"], Position]
        | tuple[Literal["curved"], Position]
        | tuple[Literal["straight"], Literal[True]]
    )

    _MagnetCase = (
        tuple[Literal["center"], Literal[True]]
        | tuple[Literal["east"], Literal[True]]
        | tuple[Literal["edge"], Position]
        | tuple[Literal["floating"], Position]
        | tuple[Literal["north"], Literal[True]]
        | tuple[Literal["south"], Literal[True]]
        | tuple[Literal["west"], Literal[True]]
    )

    _PlaceableTitleOwningCase = (
        tuple[Literal["genericPlaceableTitleOwning"], GenericPlaceableTitleOwning]
    )

    _TableColumnHeaderKindCase = (
        tuple[Literal["body"], Literal[True]]
        | tuple[Literal["grand_total"], Literal[True]]
        | tuple[Literal["group_label"], TableColumnHeaderGroupLabel]
        | tuple[Literal["group_subtotal"], Literal[True]]
    )

    _TableRowKindCase = (
        tuple[Literal["body"], Literal[True]]
        | tuple[Literal["grand_total"], Literal[True]]
        | tuple[Literal["group_label"], TableRowGroupLabel]
        | tuple[Literal["group_subtotal"], Literal[True]]
    )

    _UnformattedValueCase = (
        tuple[Literal["boolean"], bool]
        | tuple[Literal["date"], Date]
        | tuple[Literal["number"], float]
        | tuple[Literal["rich_text"], Text]
        | tuple[Literal["text"], str]
    )

    _FormulaCase = (
        tuple[Literal["display_string"], str]
        | tuple[Literal["id_based"], IdBasedFormula]
    )

    _CellRangeCase = (
        tuple[Literal["row_column_id_range"], RowColumnIdRange]
    )

    _ValueCase = (
        tuple[Literal["date"], Date]
        | tuple[Literal["duration"], float]
        | tuple[Literal["number"], float]
        | tuple[Literal["reference"], Reference]
        | tuple[Literal["text"], str]
    )

    _StructureCase = (
        tuple[Literal["categorized"], CategoryRules]
        | tuple[Literal["pivot"], PivotRules]
    )

    _TitleOwningCase = (
        tuple[Literal["genericTitleOwning"], GenericTitleOwning]
    )

    _PathCase = (
        tuple[Literal["bezier"], BezierPath]
    )

    _SlideBackgroundCase = (
        tuple[Literal["standard"], Fill]
    )

    _PlaceholderInfoCase = (
        tuple[Literal["defined"], PlaceholderDefinition]
        | tuple[Literal["tagged"], str]
    )

    _ResourceCase = (
        tuple[Literal["base64_encoded"], Base64EncodedResource]
        | tuple[Literal["indirect"], IndirectResource]
    )

    _ColumnMetricsCase = (
        tuple[Literal["equal"], EqualColumnsDescription]
        | tuple[Literal["single"], Literal[True]]
        | tuple[Literal["unequal"], UnequalColumnsDescription]
    )

    _ListLabelTypeCase = (
        tuple[Literal["image"], ListImageLabel]
        | tuple[Literal["none"], Literal[True]]
        | tuple[Literal["null_image"], Literal[True]]
        | tuple[Literal["number"], ListNumberLabel]
        | tuple[Literal["string"], ListStringLabel]
    )

    _ConstituentCase = (
        tuple[Literal["hyperlink"], HyperlinkField]
        | tuple[Literal["inline_object"], CanvasObject]
        | tuple[Literal["run"], TextRun]
    )

    _TextCase = (
        tuple[Literal["paragraphs"], list[Paragraph]]
        | tuple[Literal["string"], str]
        | tuple[Literal["text_runs"], list[TextRun]]
    )

    _TextStrokeCase = (
        tuple[Literal["none"], Literal[True]]
        | tuple[Literal["stroke"], Stroke]
    )

    _ColorCase = (
        tuple[Literal["rgba"], RGBA]
    )

    _DurationCase = (
        tuple[Literal["seconds"], float]
    )

    _FillCase = (
        tuple[Literal["color"], Color]
        | tuple[Literal["gradient"], Gradient]
        | tuple[Literal["image"], ImageFill]
    )

    _FlavorCase = (
        tuple[Literal["linear"], Linear]
        | tuple[Literal["radial"], Radial]
    )

    _HyperlinkCase = (
        tuple[Literal["file"], str]
        | tuple[Literal["program"], str]
        | tuple[Literal["slide_jump"], SlideTarget]
        | tuple[Literal["url"], str]
    )

    _SlideTargetCase = (
        tuple[Literal["by_identifier"], str]
        | tuple[Literal["first"], Literal[True]]
        | tuple[Literal["last"], Literal[True]]
        | tuple[Literal["last_viewed"], Literal[True]]
        | tuple[Literal["next"], Literal[True]]
        | tuple[Literal["previous"], Literal[True]]
    )

    _ShadowCase = (
        tuple[Literal["contactShadow"], ContactShadow]
        | tuple[Literal["curvedShadow"], CurvedShadow]
        | tuple[Literal["dropShadow"], DropShadow]
        | tuple[Literal["none"], Literal[True]]
    )

    _StrokeCase = (
        tuple[Literal["empty"], Literal[True]]
        | tuple[Literal["frame"], Frame]
        | tuple[Literal["line"], Line]
    )
