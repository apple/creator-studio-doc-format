..
    Copyright © 2026 Apple Inc.

    Licensed under Apache License v2.0. For more information, see LICENSE.
    SPDX-License-Identifier: Apache-2.0

Authoring from a theme
======================

Build a styled document from a theme's slide layouts, and style new models using its
presets.

A theme already provides the design. Its slide layouts set type, color, geometry, and
spacing, and its presets define styles that new models can reuse. In Keynote, export a
presentation that uses the theme. Every document you build from that file starts with the
theme's slide layouts and presets. The functions in
:mod:`creator_studio_doc_format.authoring` fill in the placeholders of those slide layouts.

Explore a theme's slide layouts
-------------------------------

:func:`~creator_studio_doc_format.authoring.summarize_slide_layouts` reports every slide
layout by name, with the placeholders you can set in it:

.. literalinclude:: ../snippets/authoring.py
   :language: python
   :start-after: # [summarize]
   :end-before: # [/summarize]

For ``creator_studio_doc_format/examples/fixtures/Tidal_en.keyx``, part of the output
is:

.. code-block:: text

   Title ['TITLE', 'Subtitle']
   Title & Bullets ['TITLE', 'BODY', 'Presentation Name', 'SLIDE_NUMBER']
   Title, Bullets & Photo ['TITLE', 'BODY', 'Media']
   Quote ['Text', 'Text-1']
   Blank []

Each placeholder that ``summarize_slide_layouts`` returns is a
:class:`~creator_studio_doc_format.authoring.LayoutPlaceholderSummary`. The following
example prints the ones from the ``"Title & Bullets"`` layout:

.. code-block:: pycon

   >>> from pprint import pprint
   >>> for placeholder in summarize_slide_layouts(theme)["Title & Bullets"]:
   ...     pprint(placeholder)
   LayoutPlaceholderSummary(name='TITLE',
                            object_case='shape',
                            prompt='Title Text',
                            tag=None)
   LayoutPlaceholderSummary(name='BODY',
                            object_case='shape',
                            prompt='Body Level One',
                            tag=None)
   LayoutPlaceholderSummary(name='Presentation Name',
                            object_case='shape',
                            prompt='Example Company',
                            tag='Presentation Name')
   LayoutPlaceholderSummary(name='SLIDE_NUMBER',
                            object_case='shape',
                            prompt=None,
                            tag=None)

Each summary tells you how to fill in the placeholder:

``name``
   Identifies the placeholder within its layout. You pass it to the function that fills
   the placeholder.

``object_case``
   Names the kind of object the placeholder holds. An ``"image"`` placeholder takes an
   image, and a text placeholder takes text. For example, the ``"Title, Bullets & Photo"`` layout has an
   image placeholder named ``"Media"``. Keynote exports an object the format has no
   type for, such as a live video, as an image placeholder holding a picture of it.
   :func:`~creator_studio_doc_format.authoring.set_slide_placeholder_image` replaces that
   picture with yours.

``prompt``
   Holds the placeholder text Keynote shows, such as ``"Title Text"``. It's ``None``
   when the placeholder has no text, as for ``"SLIDE_NUMBER"``.

``tag``
   Holds a label that the theme's designer gives a custom placeholder, such as
   ``"Presentation Name"``. It's ``None`` for a predefined placeholder such as
   ``"TITLE"``. A tagged placeholder's ``name`` is its tag.

.. _create-a-slide-from-a-layout:

Create a slide from a layout
----------------------------

:func:`~creator_studio_doc_format.authoring.slide_from_layout` creates a slide the way
Keynote does when you choose that layout, and returns it for you to add to the
document:

.. literalinclude:: ../snippets/authoring.py
   :language: python
   :start-after: # [slide-from-layout]
   :end-before: # [/slide-from-layout]

Set the placeholders
--------------------

Which function you use depends on the placeholder's ``object_case``:

:func:`~creator_studio_doc_format.authoring.set_slide_placeholder_text`
   Fills a text placeholder, which has an ``object_case`` of ``"shape"`` or
   ``"textbox"``. It takes a string for one paragraph or a list of strings for several.
   Each paragraph gets the placeholder's text style.

:func:`~creator_studio_doc_format.authoring.set_slide_placeholder_image`
   Fills an ``"image"`` placeholder by pointing its image at a :term:`resource`. It
   doesn't store the image's bytes. :ref:`Add them to the resource store <add-media>`
   first.

.. important::

   ``slide_from_layout`` empties only the ``"TITLE"`` and ``"BODY"`` placeholders. As in
   Keynote, a tagged placeholder keeps its sample text and an image placeholder keeps
   its sample photo until you replace them.

The following example sets a slide's text:

.. literalinclude:: ../snippets/authoring.py
   :language: python
   :start-after: # [set-slide-placeholder-text]
   :end-before: # [/set-slide-placeholder-text]

The following example adds an image's bytes, then sets the image:

.. literalinclude:: ../snippets/authoring.py
   :language: python
   :start-after: # [set-slide-placeholder-image]
   :end-before: # [/set-slide-placeholder-image]

Build a document from the layouts
---------------------------------

The following example replaces a themed document's slides with ones that use its
layouts, and saves the result as a new file:

.. literalinclude:: ../snippets/authoring.py
   :language: python
   :start-after: # [together]
   :end-before: # [/together]

Style new models using presets
------------------------------

When no layout fits, style the models you create using the theme's presets. A theme
stores its style and appearance as :term:`presets <preset>`, such as the paragraph style
for body text. You can :ref:`apply one <apply-a-preset>` to a :term:`model`. To see what a
preset provides, resolve it with
:class:`~creator_studio_doc_format.core.PresetRegistry`.

The following example finds the theme's Body style and prints the font and size it
provides:

.. literalinclude:: ../snippets/authoring.py
   :language: python
   :start-after: # [presets]
   :end-before: # [/presets]

A style property that a preset can supply is often an
:class:`~creator_studio_doc_format.core.Override` field. An ``Override`` keeps an omitted
property apart from an explicit ``null``.

.. important::

   Assigning ``None`` to an ``Override`` field clears it. For example,
   ``shape.shadow = None`` removes a shadow that the shape's preset gives it. On a field
   that isn't an ``Override``, such as
   :attr:`Shape.fill <creator_studio_doc_format.core.Shape.fill>`, ``None`` omits the
   property.

The ``get()`` method of an ``Override`` returns ``None`` both for an omitted property and
for a ``null``. To tell them apart, read ``is_not_set`` or ``is_cleared``.
