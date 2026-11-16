# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0

# [errors]
from pydantic import ValidationError

from creator_studio_doc_format.core import (
    DocumentPackageError,
    DocumentPackageErrorKind,
    DocumentVersionError,
    KeyxDocument,
)

path = "not-a-presentation.keyx"
try:
    doc = KeyxDocument.open(path)
except DocumentVersionError:
    print(f"{path} needs a newer version of the library.")
except DocumentPackageError as exc:
    # Branch on `kind`. The message text varies.
    if exc.kind is DocumentPackageErrorKind.NOT_A_PACKAGE:
        print(f"{path} isn't a document.")
    else:
        print(f"{path} is corrupt ({exc.kind.value}).")
except ValidationError:
    print(f"{path} doesn't match this library's models.")
except OSError as exc:
    print(f"Can't read {path}: {exc.strerror}.")
# [/errors]

# [validate]
from creator_studio_doc_format.validation import validate_document

doc = KeyxDocument.open("presentation.keyx")

# Writes nothing if the document is invalid.
doc.save("out.keyx", pre_save_hooks=[validate_document])
# [/validate]
