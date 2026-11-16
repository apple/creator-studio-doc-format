# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


import re
from pathlib import Path

import pytest

import creator_studio_doc_format

_PYPROJECT = Path(__file__).parent.parent / "pyproject.toml"


def test_version_matches_pyproject() -> None:
    declared = re.search(r'^version = "([^"]+)"', _PYPROJECT.read_text(), re.MULTILINE)
    assert declared
    assert creator_studio_doc_format.__version__ == declared[1]


def test_unknown_attribute_still_raises() -> None:
    with pytest.raises(AttributeError):
        creator_studio_doc_format.nope  # noqa: B018
