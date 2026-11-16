..
    Copyright © 2026 Apple Inc.

    Licensed under Apache License v2.0. For more information, see LICENSE.
    SPDX-License-Identifier: Apache-2.0

Validating a document
=====================

Check a document against the format's rules as you open, edit, and save it, so that
Keynote opens it as you wrote it.

The format places rules on every document, from the type of each field to the slides that
links point to. The library checks those rules when you open a document and as you edit its models. It
also checks them before you save, when you pass ``validate_document`` to ``save``.

Opening a document checks the file, and a failure raises an error that says why.
Constructing or changing a model checks that model immediately. Passed to ``save`` as a
hook, ``validate_document`` checks the whole document before ``save`` writes it,
including items added to a list in place and references across the document.

The format defines each type in a
:formatref:`JSON Schema <downloading-the-schema-for-keynote-interchange-format>`. Any
JSON Schema validator can check a file against it, one file at a time. Unlike that check,
``validate_document`` covers the values that a document's presets supply and the
references between its files.

.. _validation-errors:

Handle errors from opening a document
-------------------------------------

When opening a document fails, the error it raises says why. A
:class:`~creator_studio_doc_format.core.DocumentVersionError` means the file needs a newer
version of the library.

The following example reports each error:

.. literalinclude:: ../snippets/validation.py
   :language: python
   :start-after: # [errors]
   :end-before: # [/errors]

.. _models-validation:

Catch errors as you edit
------------------------

When you construct a :term:`model`, it validates types, required fields, and
constraints, such as ``slides`` needing at least one entry. Types are strict. A field
typed :class:`~creator_studio_doc_format.core.Text` doesn't accept a value of type ``str``.

A model checks again whenever you set a field. Both checks raise
|pydantic_error|_ at the statement responsible:

.. code-block:: python

   Slide(depth="deep")  # Raises `pydantic.ValidationError`.
   slide.depth = "deep"  # Raises the same error at the assignment.

A model doesn't check an item added to one of its lists in place, such as with
``slides.append``. :func:`~creator_studio_doc_format.validation.validate_document` does.

Validate the document before you save
-------------------------------------

Pass ``validate_document`` in the ``pre_save_hooks`` argument of every
:meth:`save <creator_studio_doc_format.core.Package.save>`.
Without it, an edit that breaks the format's rules reaches the saved file unnoticed. One
example is deleting a slide that a link points to. ``save`` calls each function in its
``pre_save_hooks`` parameter with the document and the JSON it's about to write.

The following example validates a document before saving it as a new file:

.. literalinclude:: ../snippets/validation.py
   :language: python
   :start-after: # [validate]
   :end-before: # [/validate]

.. seealso::

   - :doc:`../api/errors`
   - :authoring:`Validate what you write <Validate-what-you-write>`
