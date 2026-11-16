# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


def extend_path(path: str, key: str) -> str:
    return key if not path else f"{path}.{key}"
