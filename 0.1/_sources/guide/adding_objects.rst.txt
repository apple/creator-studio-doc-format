..
    Copyright © 2026 Apple Inc.

    Licensed under Apache License v2.0. For more information, see LICENSE.
    SPDX-License-Identifier: Apache-2.0

Adding content to a slide
=========================

Add text, shapes, images, tables, and charts to a slide, and connect them with lines.

Most content sets its position and size in its own
:class:`~creator_studio_doc_format.core.Geometry`. Wrap the content in a
:class:`~creator_studio_doc_format.core.CanvasObject`, which has one field for each kind
of content, such as ``textbox`` or ``shape``. The ``CanvasObject`` goes inside a
:class:`~creator_studio_doc_format.core.SlideObject` in the slide's ``contents``.

The text example shows how to wrap content in a ``CanvasObject`` and a ``SlideObject``.
The examples after it build only the object.

.. _set-one-case:

Set one case of a union
-----------------------

``CanvasObject``, :class:`~creator_studio_doc_format.core.Fill`,
:class:`~creator_studio_doc_format.core.Color`, :class:`~creator_studio_doc_format.core.Stroke`,
:class:`~creator_studio_doc_format.core.Path`, and other unions hold one of several kinds of value,
called cases. Each case is an optional field. Set the one field for the case you want.
Two examples below each set one case: ``CanvasObject(textbox=...)`` in the text example
and ``Path(bezier=...)`` in the shape example.

The following example builds a solid fill and a stroke with no line:

.. literalinclude:: ../snippets/adding_objects.py
   :language: python
   :start-after: # [union]
   :end-before: # [/union]

A union with no case set raises ``pydantic.ValidationError``. However, a union with two
cases set raises nothing, and an app that opens the document uses only one of them.
:class:`TaggedUnionModel <creator_studio_doc_format.core.TaggedUnionModel>` describes the
full contract, and :structure:`Recognize values that take one of several forms
<Recognize-values-that-take-one-of-several-forms>` shows how a document writes a union.

.. _add-text:

Add text
--------

The ``text`` field of a
:class:`~creator_studio_doc_format.core.Textbox` or a
:class:`~creator_studio_doc_format.core.Shape` holds a
:class:`~creator_studio_doc_format.core.Text`, which holds one of three cases:

``string``
   Plain text.

``text_runs``
   A list of :class:`~creator_studio_doc_format.core.TextRun`, for text with a style
   that changes within a line.

``paragraphs``
   A list of :class:`~creator_studio_doc_format.core.Paragraph`, for several lines,
   alignment, or a list.

Use the simplest case that holds your text:

.. literalinclude:: ../snippets/adding_objects.py
   :language: python
   :start-after: # [text]
   :end-before: # [/text]

.. _draw-a-shape:

Add a shape
-----------

A shape's outline is
:attr:`Shape.path <creator_studio_doc_format.core.Shape.path>`, which holds a ``Path``.
The ``bezier`` case of a ``Path`` holds SVG path data.
:attr:`BezierPath.space <creator_studio_doc_format.core.BezierPath.space>` sets
the path's coordinate space, which Keynote stretches over the shape's ``geometry``. To
move, resize, or rotate a shape, change ``geometry`` rather than the path.

The simplest space is a unit box, where the path's numbers are fractions of the shape:

.. literalinclude:: ../snippets/adding_objects.py
   :language: python
   :start-after: # [shape]
   :end-before: # [/shape]

.. _add-media:

Add an image
------------

An :class:`~creator_studio_doc_format.core.Image` refers to its bytes through a
:class:`~creator_studio_doc_format.core.Resource`. Most images use an
:class:`~creator_studio_doc_format.core.IndirectResource`, which names a file in
``doc.resources``. That store works like a dictionary of filenames to bytes:

.. literalinclude:: ../snippets/adding_objects.py
   :language: python
   :start-after: # [image]
   :end-before: # [/image]

``unique_filename`` returns a name no file in the document uses yet, such as
``"cover 2.png"`` when the document already has a ``cover.png``. ``identifier`` names the
file that holds the bytes, and ``filename`` is the name Keynote shows. Without
``identifier``, ``filename`` names the file too. A
:class:`~creator_studio_doc_format.core.Movie` or
:class:`~creator_studio_doc_format.core.Audio` object refers to its file the same way.

.. _add-a-table:

Add a table
-----------

A :class:`~creator_studio_doc_format.core.Table` states its size in
``number_of_rows`` and ``number_of_columns``. The counts must match the rows in ``content``
and the entries in ``column_headers``. Every row also needs one cell for each column
header. Adding a
:class:`~creator_studio_doc_format.core.Row` doesn't update ``number_of_rows``.

.. important::

   ``value`` is the cell's formatted display string. A number, date, or Boolean cell
   needs a typed ``unformatted_value``. Without one, Keynote treats the cell as text. A
   text cell can omit it.

The following example builds a table of two rows and two columns:

.. literalinclude:: ../snippets/adding_objects.py
   :language: python
   :start-after: # [table]
   :end-before: # [/table]

.. _add-a-chart:

Add a chart
-----------

Keynote offers :doc:`more than 20 kinds of charts <../api/presentation/charts/kinds>`.
All of them take their data in the same grid, a
:class:`~creator_studio_doc_format.core.ChartData`. Its ``plot_direction``
sets whether the grid's rows or its columns become the series:

.. literalinclude:: ../snippets/adding_objects.py
   :language: python
   :start-after: # [chart]
   :end-before: # [/chart]

.. _connect-objects:

Add a connection line
---------------------

A :class:`~creator_studio_doc_format.core.ConnectionLine` takes its position from its
two ends, each an :class:`~creator_studio_doc_format.core.End`. An end attaches to an
object through its ``anchor``, which names the object by
:attr:`Anchor.object_id <creator_studio_doc_format.core.Anchor.object_id>`. The
object must be in the same list of objects as the line, such as the slide's
``contents``.

Wrap a line as ``CanvasObject(connectionLine=...)``. ``connectionLine`` and
``genericCanvasObject`` are the two camelCase fields of ``CanvasObject``. The rest are
lowercase.

.. warning::

   Every end needs an ``end_point``, even one that ``anchor`` attaches. Omitting it
   drops the whole line. For an attached end, use the object's center.

An end with no ``anchor`` stays at its ``end_point``. The following example attaches the
arrow's head to the oval from the shape example and leaves its tail unattached:

.. literalinclude:: ../snippets/adding_objects.py
   :language: python
   :start-after: # [connection-line]
   :end-before: # [/connection-line]

.. _apply-a-preset:

Style content with a preset
---------------------------

A :term:`preset` lets content share one set of properties, which keeps styling
consistent and the document compact.

The following example defines a body preset and a title preset that builds on it, then
applies each to a run of text:

.. literalinclude:: ../snippets/adding_objects.py
   :language: python
   :start-after: # [preset]
   :end-before: # [/preset]

.. seealso::

   - :ref:`Slide content <api-content>`, the API reference's page for each kind of content
   - :doc:`../api/resources`, which holds the bytes an image refers to
   - ``creator_studio_doc_format/examples/``, a runnable script for each kind of slide
     content
