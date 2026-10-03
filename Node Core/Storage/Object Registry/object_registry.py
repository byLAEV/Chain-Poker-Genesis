#!/usr/bin/env python3
"""Canonical protocol-neutral Node Core Storage object registry."""

from __future__ import annotations
import json
import os
import re
import tempfile
from pathlib import Path

REGISTRY_PATH = "node-storage/state/object-registry.json"

class RegistryError(Exception):
    pass

class ObjectRegistry:
    REQUIRED_FIELDS = {
        "object_id", "object_class", "relative_path", "content_hash",
        "storage_version", "provider_type", "location_state",
        "object_state", "synchronization_state",
    }
    LOCATION_STATES = {
        "LOCAL_ONLY","LOCAL_AND_DISTRIBUTED","DISTRIBUTED_ONLY",
        "SYNC_PENDING","SYNC_PROCESSING","MISSING_LOCAL",
        "MISSING_DISTRIBUTED","CONFLICT","QUARANTINED",
    }
    SYNC_STATES = {
        "NOT_SYNCHRONIZED","PROPAGATION_PENDING","PROPAGATING",
        "SYNCHRONIZED","SYNC_FAILED","RETRY_WAIT","CONFLICT","QUARANTINED",
    }

    def __init__(self, node_root):
        self.node_root = Path(node_root).resolve()
        self.path = self.node_root / REGISTRY_PATH
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.exists():
            try:
                self.entries = json.loads(self.path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise RegistryError("invalid object registry") from exc
        else:
            self.entries = {}

    @staticmethod
    def _valid_id(value):
        return bool(value) and "/" not in value and chr(92) not in value and ".." not in value

    @classmethod
    def validate(cls, metadata):
        if not cls._valid_id(metadata.get("object_id")):
            raise RegistryError("invalid object_id")
        if metadata.get("object_class") == "protocol-reserved":
            raise RegistryError("protocol-reserved objects cannot be registered by Node Core")
        if not re.fullmatch(r"[a-f0-9]{64}", metadata.get("content_hash", "")):
            raise RegistryError("content_hash must be SHA-256")
        if metadata.get("provider_type") not in {"LOCAL","DECENTRALIZED","EXTERNAL"}:
            raise RegistryError("invalid provider_type")
        if metadata.get("location_state") not in cls.LOCATION_STATES:
            raise RegistryError("invalid location_state")
        if metadata.get("synchronization_state") not in cls.SYNC_STATES:
            raise RegistryError("invalid synchronization_state")
        if metadata.get("object_state") not in {"PRESENT","MISSING","INVALID","QUARANTINED"}:
            raise RegistryError("invalid object_state")
        return True

    def upsert(self, metadata):
        self.validate(metadata)
        self.entries[metadata["object_id"]] = dict(metadata)
        self._save()
        return self.entries[metadata["object_id"]]

    register = upsert

    def get(self, object_id):
        try:
            return self.entries[object_id]
        except KeyError as exc:
            raise RegistryError("object not registered") from exc

    def list(self):
        return list(self.entries.values())

    def remove(self, object_id):
        self.entries.pop(object_id, None)
        self._save()

    def _save(self):
        fd, tmp = tempfile.mkstemp(prefix=".object-registry.", dir=self.path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(self.entries, handle, indent=2, sort_keys=True)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp, self.path)
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)
