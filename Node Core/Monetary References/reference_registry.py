#!/usr/bin/env python3
"""Protocol-neutral registry for Node Core monetary references."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

BASE = Path(__file__).resolve().parent
MANIFEST = BASE / "MONETARY-REFERENCE-MANIFEST.json"


class MonetaryReferenceRegistry:
    """Read-only runtime view of the Node Core monetary reference manifest."""

    def __init__(self, manifest: Path = MANIFEST) -> None:
        self.manifest = manifest
        self.data: dict[str, Any] = json.loads(manifest.read_text(encoding="utf-8"))

    def get(self, reference_id: str) -> dict[str, Any]:
        for reference in self.data["references"]:
            if reference["id"] == reference_id:
                return dict(reference)
        raise KeyError(reference_id)

    def all(self) -> tuple[dict[str, Any], ...]:
        return tuple(dict(reference) for reference in self.data["references"])

    def settlement_execution_enabled(self) -> bool:
        return bool(self.data["settlement_execution"])

    def custody_enabled(self) -> bool:
        return bool(self.data["custody"])
