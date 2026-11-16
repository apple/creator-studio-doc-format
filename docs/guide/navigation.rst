..
    Copyright © 2026 Apple Inc.

    Licensed under Apache License v2.0. For more information, see LICENSE.
    SPDX-License-Identifier: Apache-2.0

Navigating a document efficiently
=================================

Find the models you need without reading the whole document.

A document can hold thousands of :term:`models <model>`, because even a short
presentation carries its theme's layouts and styles. The right tool depends on what you
already know about the document.

Find specific models
--------------------

When you know the kind of model you want but not where it is, search the model tree.
:func:`~creator_studio_doc_format.navigation.iterate_models` takes any model, such as a
presentation or a single slide. It yields that model, then every model nested inside
it, in pre-order.

A common use case is searching a document's text. The following example prints the
text of every :class:`~creator_studio_doc_format.core.Text` and
:class:`~creator_studio_doc_format.core.TextRun` model on each slide:

.. literalinclude:: ../snippets/navigation.py
   :language: python
   :start-after: # [iterate]
   :end-before: # [/iterate]

For ``creator_studio_doc_format/examples/fixtures/Tidal_en.keyx``, the output starts with:

.. code-block:: text

   1 'A theme built for testing, not for sale'
   2 'Example Company'
   2 ' · Confidential'
   3 '#'
   7 'Photo caption sample'
   8 'Testing is the ultimate confidence.'
   8 'A. Synthetic Author'
   11 'Second line'

Each item that ``iterate_models`` yields is an
:class:`~creator_studio_doc_format.navigation.IteratedModel`, which holds the model
together with where it sits in the tree. An item's ``ancestors`` lists the models that
enclose it, starting from the outermost. Its ``path`` names the fields that lead to it.

The following example finds the caption text inside an
:class:`~creator_studio_doc_format.core.Image`:

.. literalinclude:: ../snippets/navigation.py
   :language: python
   :start-after: # [captions]
   :end-before: # [/captions]

For ``creator_studio_doc_format/examples/fixtures/Tidal_en.keyx``, it prints
``7 'Photo caption sample'``.

Explore an unfamiliar document
------------------------------

When you don't yet know what a document contains, print only part of its tree.
Limiting the depth and length is a quick way to see its structure. Lower the limits
until the output fits, then descend into the branch you want and raise them again.

This library doesn't depend on ``rich``, so install it separately with ``pip install rich``.
The following example
uses ``rich`` to print the top levels of the presentation's tree:

.. code-block:: python

   from rich.pretty import pretty_repr

   print(
       pretty_repr(
           doc.presentation,
           max_depth=3,  # Stays out of the deeply nested style models.
           max_length=8,  # Truncates long contents lists.
           max_string=80,  # Keeps one slide's body text from filling the screen.
       )
   )

.. _read-resources-lazily:

Read resources only when you need them
--------------------------------------

:meth:`~creator_studio_doc_format.core.Package.open` reads every resource into
memory, so a document with many images or movies opens slowly.
:meth:`~creator_studio_doc_format.core.Package.open_lazy` reads a resource's bytes
only when you first access them, so the same document opens as fast as its JSON:

.. literalinclude:: ../snippets/navigation.py
   :language: python
   :start-after: # [lazy]
   :end-before: # [/lazy]

The document keeps the file open until the ``with`` block ends. Read the resources you
need inside the block. ``save`` and ``doc.resources.items()`` read every resource, so call
them inside the block too. Editing models and running ``validate_document`` read no
resources.
