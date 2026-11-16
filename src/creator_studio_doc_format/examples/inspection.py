# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0

"""Print a presentation's text, then replace it with lorem ipsum of the same length.

A real document can hold thousands of models, so printing a whole subtree floods the
output. A depth-limited `rich.pretty.pprint(model, ...)` of the top levels, with
truncated lists and strings, shows more than text, such as geometry and presets. The
library doesn't depend on `rich`, so install it separately to try this.
`model_dump` output is harder to read because every model includes its
`type_identifier` and `version`.

`iterate_models` descends through lists, groups, and unions on its own, so the code
names only the leaf model types. Both passes iterate over each slide rather than
`doc.presentation`, which also reaches the theme's layouts and their placeholder text.
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from creator_studio_doc_format.core import (
    HyperlinkField,
    KeyxDocument,
    SlideObject,
    Text,
    TextRun,
)
from creator_studio_doc_format.core import (
    SlideObjectPlaceholderInfoPlaceholderDefinitionKind as PlaceholderKind,
)
from creator_studio_doc_format.navigation import IteratedModel, iterate_models

logger = logging.getLogger(__name__)

FIXTURES = Path(__file__).parent / "fixtures"

LOREM = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam fermentum "
    "vestibulum est. Cras rhoncus. Pellentesque habitant morbi tristique senectus "
    "et netus et malesuada fames ac turpis egestas. Sed quis tortor. Donec non "
    "ipsum. Mauris condimentum, odio nec porta tristique, ante neque malesuada "
    "massa, in dignissim eros velit at tellus. Donec et risus in ligula eleifend "
    "consectetur. Donec volutpat eleifend augue. Integer gravida sodales leo. Nunc "
    "vehicula neque ac erat. Vivamus non nisl. Fusce ac magna. Suspendisse euismod "
    "libero eget mauris."
)


def lorem_of_length(n: int) -> str:
    """Returns lorem ipsum text, repeated and cut to exactly ``n`` characters."""
    if n <= 0:
        return ""
    repeats = n // len(LOREM) + 1
    return (LOREM * repeats)[:n]


def _in_protected_subtree(item: IteratedModel) -> bool:
    """Returns a Boolean value that indicates whether the item is inside a locked slide
    object or a title placeholder.
    """
    for a in item.ancestors:
        if not isinstance(a, SlideObject):
            continue
        if a.is_locked:
            return True
        pi = a.placeholder_info
        if (
            pi is not None
            and pi.defined is not None
            and pi.defined.kind == PlaceholderKind.TITLE
        ):
            return True
    return False


def print_texts(doc: KeyxDocument) -> None:
    """Logs every primary text string without changing the document.

    Skips the display text of hyperlinks.
    """
    for slide in doc.presentation.slides:
        for item in iterate_models(slide):
            model = item.model
            if isinstance(model, TextRun) and any(
                isinstance(a, HyperlinkField) for a in item.ancestors
            ):
                continue
            if isinstance(model, (TextRun, Text)) and model.string:
                logger.info("  %r", model.string)


def replace_texts(doc: KeyxDocument) -> None:
    """Replaces each slide's text with lorem ipsum, in place.

    Locked objects and title placeholders keep their text.
    """
    for slide in doc.presentation.slides:
        for item in iterate_models(slide):
            if _in_protected_subtree(item):
                continue
            model = item.model
            if isinstance(model, TextRun) or (
                isinstance(model, Text) and model.string is not None
            ):
                model.string = lorem_of_length(len(model.string))


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    parser = argparse.ArgumentParser(description=__doc__.partition("\n")[0])
    parser.add_argument("input", type=Path, nargs="?", default=FIXTURES / "sample.keyx")
    parser.add_argument(
        "output", type=Path, nargs="?", default=Path("tmp/replaced.keyx")
    )
    args = parser.parse_args()

    doc = KeyxDocument.open(args.input)
    logger.info("Before:")
    print_texts(doc)
    replace_texts(doc)
    logger.info("After:")
    print_texts(doc)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(args.output)
    logger.info("Wrote %s", args.output)


if __name__ == "__main__":
    main()
