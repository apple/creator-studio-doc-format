# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0

# [iterate]
from creator_studio_doc_format.core import KeyxDocument, Text, TextRun
from creator_studio_doc_format.navigation import iterate_models

doc = KeyxDocument.open("presentation.keyx")
# Per slide, because the presentation also holds placeholder text from
# slide layouts.
for number, slide in enumerate(doc.presentation.slides, start=1):
    for item in iterate_models(slide):
        if isinstance(item.model, (TextRun, Text)) and item.model.string:
            print(number, repr(item.model.string))
# [/iterate]

# [captions]
from creator_studio_doc_format.core import Image

for number, slide in enumerate(doc.presentation.slides, start=1):
    for item in iterate_models(slide):
        if not (isinstance(item.model, (TextRun, Text)) and item.model.string):
            continue

        if any(isinstance(ancestor, Image) for ancestor in item.ancestors):
            print(number, repr(item.model.string))
# [/captions]

# [lazy]
with KeyxDocument.open_lazy("big-presentation.keyx") as big:
    print(len(big.presentation.slides))  # This reads no resource.
    photo = big.resources["sample_photo.jpg"]  # This reads only that file.
# [/lazy]
