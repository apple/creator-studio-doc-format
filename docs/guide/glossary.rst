..
    Copyright © 2026 Apple Inc.

    Licensed under Apache License v2.0. For more information, see LICENSE.
    SPDX-License-Identifier: Apache-2.0

Glossary
========

Look up the terms that the guide and the API use in a specific sense.

File format
-----------

.. glossary::

   document
      A ``.keyx`` file as a whole, which is the presentation together with its
      :term:`presets <preset>`, :term:`manifest`, and :term:`resources <resource>`. It's
      a ZIP archive with these entries:

      ``main.json``
         The presentation, which is its slides and everything on them.

      ``presets.json``
         The presets.

      ``manifest.json``
         The manifest.

      ``Data/``
         The resources that the document keeps as files.

      For more information, see
      :structure:`Explore the files in a document <Explore-the-files-in-a-document>`.

      People who use Keynote call the whole file a presentation. In this library, that
      file is a document. Its presentation is the part that holds the slides. A
      :class:`~creator_studio_doc_format.core.KeyxDocument` holds a document in memory,
      and reads and writes its ZIP archive.

   reader
      A program that opens a document, such as Keynote. The format's documentation and
      the API reference describe each value by what a reader does with it.

   property
      A key-value pair in a JSON object, such as ``"width": 1024`` in a size.

   identifier
      The name other JSON objects use to refer to one, such as a preset. It's unique
      across the whole document. For more information, see
      :authoring:`Write unique object identifiers <Write-unique-object-identifiers>`.

   preset
      A reusable, named set of properties that JSON objects in ``main.json`` adopt and
      inherit. A preset can hold any property of the object that adopts it, including a
      property that isn't visual, such as whether a paragraph's lines stay together. For
      more information, see
      :structure:`Style objects with presets <Style-objects-with-presets>`.

   resource
      Binary data that a JSON object references. The document keeps it as its own file or
      embeds it in the JSON. The bytes of an image or a movie are a resource. For more
      information, see :doc:`../api/resources` and
      :structure:`Store media as resources <Store-media-as-resources>`.

   manifest
      The part of a document that declares its ``package_version``, which is the version
      of the format that the document uses. For more information,
      see :authoring:`Declare versions <Declare-versions>`.

   version
      A number in major.minor form, such as ``1.0``, that the format uses for backward
      and forward compatibility. Each type has one, and a JSON object can declare which
      version of its type it follows. A document's package version, which the
      :term:`manifest` writes as ``package_version``, is the version of the format as a
      whole. For more information, see
      :structure:`Distinguish the two kinds of version <Distinguish-the-two-kinds-of-version>`.

Library
-------

.. glossary::

   model
      A Python object that represents a JSON object in the document. It's an instance of
      a Pydantic model class, such as :class:`~creator_studio_doc_format.core.Slide` or
      :class:`~creator_studio_doc_format.core.Text`, and its fields mirror the JSON
      object's properties.

   union
      A model for a property that holds exactly one of several values, such as a
      :class:`~creator_studio_doc_format.core.CanvasObject`, which holds a text box, a
      shape, or another object. Each possible value is an optional field, called a
      *case*, and you set exactly one. For more information, see
      :class:`~creator_studio_doc_format.core.TaggedUnionModel` and
      :structure:`Recognize values that take one of several forms
      <Recognize-values-that-take-one-of-several-forms>`.

Keynote
-------

:doc:`authoring` shows how these work together, and
:structure:`Base slides on a theme and its layouts <Base-slides-on-a-theme-and-its-layouts>`
shows how a document stores them.

.. glossary::

   theme
      The predesigned look a presentation builds on. You choose it by name, such as ``"White"``. It
      provides the presentation's slide layouts and default styles.
      :attr:`Presentation.theme
      <creator_studio_doc_format.core.Presentation.theme>` names it, and can
      carry slide layouts that replace the theme's own.

   slide layout
      One of a theme's predesigned slides, which a slide builds on through
      :attr:`Slide.layout <creator_studio_doc_format.core.Slide.layout>`. It
      provides the slide's placeholders and background. Also called a *layout*.

   placeholder
      An object that marks where content goes on a slide, such as the title or body
      text.
