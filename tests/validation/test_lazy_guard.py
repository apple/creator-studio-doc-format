# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


from creator_studio_doc_format.core.package import _ZipBackend
from creator_studio_doc_format.validation import validate_document

from .builders import doc_with_indirect_image


def test_validate_document_reads_no_resource_bytes_when_lazy(
    tmp_path, monkeypatch
) -> None:
    doc = doc_with_indirect_image("present.png")
    doc.resources["present.png"] = b"\x89PNG\r\n\x1a\n"
    path = tmp_path / "d.keyx"
    doc.save(path)

    reads: list[str] = []
    orig = _ZipBackend.read
    monkeypatch.setattr(
        _ZipBackend,
        "read",
        lambda self, name: (reads.append(name), orig(self, name))[1],
    )

    from creator_studio_doc_format.core import KeyxDocument

    with KeyxDocument.open_lazy(path) as lazy:
        validate_document(lazy)
        assert reads == []
