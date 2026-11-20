..
    Copyright © 2026 Apple Inc.

    Licensed under Apache License v2.0. For more information, see LICENSE.
    SPDX-License-Identifier: Apache-2.0

Presentation
============

Build the presentation at a document's root, and every model it contains.

.. autopydantic_model:: creator_studio_doc_format.core.Presentation

.. The theme nests each toctree's entries under the heading it sits in, so each group
   holds its own hidden toctree to give the sidebar the same groups.

Slides and placement
--------------------

:doc:`slides`
    Build slides from the layouts a theme provides, and set the information a slide keeps
    about each object on it.

:doc:`canvas`
    Place objects on a slide, in a group, or inline in a paragraph, and set the properties
    they share.

:doc:`positions`
    Position an object and set how much room it reserves, in points.

.. toctree::
   :hidden:

   slides
   canvas
   positions

.. _api-content:

Slide content
-------------

:doc:`text`
    Add bodies of text and the containers that hold them, and set their paragraph and
    character properties.

:doc:`lists`
    Define bulleted and numbered list styles, their nesting levels, and the text, number, or
    image label each level shows.

:doc:`links`
    Attach links to text that open a URL or a file, jump to another slide, or exit the
    slideshow.

:doc:`shapes`
    Draw paths with a fill and a stroke, and connect objects with lines.

:doc:`tables/index`
    Add tables of cells, and arrange a text area in columns.

:doc:`charts/index`
    Add column, pie, scatter, and other charts to a slide.

:doc:`media`
    Add images, movies, and audio, and control how they play.

:doc:`resources`
    Refer to the data that media, image fills, and image bullets use.

.. toctree::
   :hidden:

   text
   lists
   links
   shapes
   tables/index
   charts/index
   media
   resources

Styles and appearance
---------------------

:doc:`styling`
    Apply a theme and the named styles that a presentation's objects and text refer to.

:doc:`fills`
    Fill an area with a solid color, a gradient, or an image.

:doc:`colors`
    Specify the colors that displayed objects use.

:doc:`shadows`
    Add shadows and reflections around an object.

:doc:`numbers`
    Format numbers, such as those in a numbered list.

:doc:`titles`
    Add a title or caption to an object and set its properties.

.. toctree::
   :hidden:

   styling
   fills
   colors
   shadows
   numbers
   titles

Common types
------------

:doc:`common_types`
    Describe groups of objects, sizes, labels, and dates with types that many others use.

.. toctree::
   :hidden:

   common_types
