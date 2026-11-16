# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0

"""Python bindings for the Keynote Interchange Format (``.keyx``)."""

import logging
from importlib.metadata import packages_distributions, version

logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__: list[str] = []


def __getattr__(name: str) -> str:
    if name != "__version__":
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    dists = packages_distributions().get(__name__)
    return version(dists[0]) if dists else "unknown"
