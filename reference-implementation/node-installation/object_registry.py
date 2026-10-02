#!/usr/bin/env python3
"""Protocol-neutral Node Core object registry."""

from __future__ import annotations
import json
import re
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

    REQUIRED_FIELDS = {
        "object_id", "object_class", "relative_path", "content_hash",
        "storage_version", "provider_type", "location_state",
        "object_state", "synchronization_state",
    }

    def register(self, metadata):
        if set(metadata) != self.REQUIRED_FIELDS:
            raise RegistryError("registry entry fields do not match canonical schema")
        object_id = metadata["object_id"]
        if not object_id or "/" in object_id or chr(92) in object_id or ".." in object_id:
            raise RegistryError("invalid object_id")
        if metadata["object_class"] == "protocol-reserved":
            raise RegistryError("protocol-reserved objects cannot be registered by Node Core")
        if not re.fullmatch(r"[a-f0-9]{64}", metadata["content_hash"]):
            raise RegistryError("content_hash must be SHA-256")
        if metadata["provider_type"] not in {"LOCAL", "DECENTRALIZED", "EXTERNAL"}:
            raise RegistryError("invalid provider_type")
        if metadata["location_state"] not in {"LOCAL_ONLY","DISTRIBUTED_ONLY","LOCAL_AND_DISTRIBUTED","SYNC_PENDING","SYNC_PROCESSING","MISSING_LOCAL","MISSING_DISTRIBUTED","CONFLICT","QUARANTINED"}:
            raise RegistryError("invalid location_state")
        if metadata["object_state"] not in {"PRESENT","MISSING","INVALID","QUARANTINED"}:
            raise RegistryError("invalid object_state")
        if metadata["synchronization_state"] not in {"NOT_SYNCHRONIZED","PROPAGATION_PENDING","PROPAGATING","THRESHOLD_NOT_REACHED","THRESHOLD_REACHED","SYNCHRONIZED","SYNC_FAILED","RETRY_WAIT","CONFLICT","QUARANTINED"}:
            raise RegistryError("invalid synchronization_state")
        self.entries[object_id] = metadata
        self.path.write_text(
            json.dumps(self.entries, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def get(self, object_id):
        if object_id not in self.entries:
            raise RegistryError("object not registered")
        return self.entries[object_id]
