# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


def claim_unique(seen: dict[str, str], key: str, path: str, field: str) -> None:
    if (existing_path := seen.get(key)) is not None:
        raise ValueError(
            f"`{field}` {key!r} is a duplicate (at {path}). The first is at "
            f"{existing_path}."
        )
    seen[key] = path
