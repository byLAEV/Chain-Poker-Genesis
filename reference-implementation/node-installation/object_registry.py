#!/usr/bin/env python3
"""Protocol-neutral Node Core object registry."""

from __future__ import annotations
import json
from pathlib import Path

REGISTRY_PATH = "node-storage/state/object-registry.json"

class RegistryError(Exception):
    pass

class ObjectRegistry:
    def __init__(self, node_root):
        self.node_root = Path(node_root).resolve()
        self.path = self.node_root / REGISTRY_PATH
        if not self.path.parent.is_dir():
            raise RegistryError("registry storage does not exist")
        if self.path.exists():
            try:
                self.entries = json.loads(self.path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise RegistryError("invalid object registry") from exc
        else:
            self.entries = {}

    def register(self, metadata):
        object_id = metadata.get("object_id")
        if not object_id:
            raise RegistryError("object_id missing")
        if metadata.get("object_class") == "protocol-reserved":
            raise RegistryError("protocol-reserved objects cannot be registered by Node Core")
        self.entries[object_id] = metadata
        self.path.write_text(
            json.dumps(self.entries, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def get(self, object_id):
        if object_id not in self.entries:
            raise RegistryError("object not registered")
        return self.entries[object_id]
