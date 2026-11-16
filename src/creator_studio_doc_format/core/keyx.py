# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0

"""Keynote ``.keyx`` documents, a ``Package`` with a ``Presentation`` root model."""

from __future__ import annotations

from typing import ClassVar

from .models import Presentation
from .package import Package


class KeyxDocument(Package[Presentation]):
    """A document that holds a presentation with its presets, manifest, and resources.

    Opening, saving, and closing are inherited from :class:`Package`. For more
    information, see :meth:`Package.open`, :meth:`Package.open_lazy`,
    :meth:`Package.save`, and :meth:`Package.close`.

    Args:
        payload: The presentation, written to ``main.json``.
        presets: The presets, written to ``presets.json``.
        manifest: The manifest, written to ``manifest.json``.
        resources: The ``Data/`` resources, as a map from filename to bytes.

    Attributes:
        payload_model: :class:`Presentation`, the model that ``main.json`` is validated
            against.
    """

    payload_model: ClassVar[type[Presentation]] = Presentation

    @property
    def presentation(self) -> Presentation:
        """The document's presentation, decoded from the main JSON file.

        ``presentation`` and ``payload`` return the same object.
        """
        return self.payload
