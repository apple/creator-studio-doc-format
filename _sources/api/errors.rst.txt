..
    Copyright © 2026 Apple Inc.

    Licensed under Apache License v2.0. For more information, see LICENSE.
    SPDX-License-Identifier: Apache-2.0

Errors
======

Handle the exceptions that opening or saving a document raises.

Opening a document raises these exceptions when the file is corrupt or too new.
:meth:`~creator_studio_doc_format.core.Package.save` can raise
:class:`~creator_studio_doc_format.core.DocumentPackageError` and
:class:`~creator_studio_doc_format.core.DocumentVersionError` too.

DocumentPackageError
--------------------

.. autoclass:: creator_studio_doc_format.core.DocumentPackageError
   :show-inheritance:

DocumentPackageErrorKind
~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: creator_studio_doc_format.core.DocumentPackageErrorKind
   :members:
   :undoc-members:

DocumentVersionError
--------------------

.. autoclass:: creator_studio_doc_format.core.DocumentVersionError
   :show-inheritance:

DocumentError
-------------

.. autoclass:: creator_studio_doc_format.core.DocumentError

.. seealso:: Learn how to catch them in
   :ref:`Handle errors from opening a document <validation-errors>`.
