# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from enum import Enum


class DocumentPackageErrorKind(str, Enum):
    """The defect that a document package error reports.

    Test ``kind`` to tell the defects apart. The message is often the text that
    ``zipfile`` raised. Every member is a defect in the bytes. A caller that skips any
    ``DocumentPackageError`` therefore stays correct for a member added later. A limit
    of the reader raises :class:`DocumentVersionError` instead.

    ``str(kind)`` isn't the member's value. Interpolate ``kind.value`` to get the text.
    """

    MALFORMED_ARCHIVE = "malformed_archive"
    """A ZIP archive that Python fails to read, such as a truncated or encrypted one, or
    one with a checksum that doesn't match."""
    MALFORMED_JSON = "malformed_json"
    """A payload file that isn't valid JSON.

    The payload file is ``main.json``. A bad manifest is defaulted instead."""
    MALFORMED_PRESETS = "malformed_presets"
    """A presets file that isn't a JSON array, a preset without properties, or a preset
    cycle that the payload actually reaches.

    The presets file is ``presets.json``, and a preset's properties are its
    ``properties`` key."""
    MISSING_MAIN_FILE = "missing_main_file"
    """A package without a payload file.

    The payload file is ``main.json``."""
    NOT_A_PACKAGE = "not_a_package"
    """A file or stream that isn't a ZIP archive, or a path that isn't a regular file,
    such as a directory."""


class DocumentError(Exception):
    """The library can't read the input far enough to validate it.

    Each subclass tells a batch caller what to do with the input:

    - :class:`DocumentPackageError` means the data is wrong. Skip the file.
    - :class:`DocumentVersionError` means the library is too old for the data. Stop the
      run and upgrade.

    Catch this base class only to report that the input couldn't be read.

    A payload that parses but doesn't match the models raises neither subclass. Because
    the mismatch can equally mean that the models are behind the exporter, it raises
    ``pydantic.ValidationError``. A caller's mistakes raise built-in exceptions.

    Pydantic wraps only a ``ValueError`` or an ``AssertionError`` that a validator
    raises, so a ``DocumentError`` raised inside a validator reaches the caller of
    ``model_validate`` unwrapped.
    """


class DocumentPackageError(DocumentError):
    """The document's bytes are invalid, and no Keynote export produces bytes like them.

    Args:
        kind: The defect, also the ``kind`` attribute.
        message: The text that ``str(error)`` returns.
    """

    def __init__(self, kind: DocumentPackageErrorKind, message: str) -> None:
        super().__init__(kind, message)
        self.kind = kind

    def __str__(self) -> str:
        message: str = self.args[1]
        return message


class DocumentVersionError(DocumentError):
    """An error that means this library is too old to read the document.

    The document can still be valid.

    The library raises this error when the package or any object declares a newer major
    version. Lenient decoding instead skips a value with a newer major version that a
    preset supplies for an optional or defaulted field, and leaves the field unset.

    The class itself names the cause, and the error has no ``kind``. This is the one
    failure with a certain fix, which its message names.
    """
