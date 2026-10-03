#!/usr/bin/env python3
"""Protocol-neutral orchestration boundary for Node Core Storage."""

from __future__ import annotations
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "Storage Policy"))
sys.path.insert(0, str(ROOT / "Object Registry"))
sys.path.insert(0, str(ROOT / "Integrity"))
sys.path.insert(0, str(ROOT / "Disaster Recovery"))

from storage_engine import StorageEngine, StorageError
from storage_policy import StoragePolicy
from object_registry import ObjectRegistry, RegistryError
from integrity_manager import IntegrityManager
from storage_recovery import StorageRecovery

class StorageManager:
    """Single high-level entry point for storage lifecycle operations."""

    def __init__(self, node_root, *, kubo=None):
        self.node_root = Path(node_root).resolve()
        self.engine = StorageEngine(self.node_root, kubo=kubo)
        self.policy = StoragePolicy()
        self.registry = ObjectRegistry(self.node_root)
        self.integrity = IntegrityManager(self.engine)
        self.recovery = StorageRecovery(self.engine, self.registry, self.integrity)

    def put(self, object_class, object_id, data, *, mirror=True, encrypted=False):
        rule = self.policy.validate_write(object_class, mirror=mirror, encrypted=encrypted)
        metadata = self.engine.put(object_class, object_id, data, mirror=mirror, encrypted=encrypted)
        metadata.update(rule)
        self.registry.upsert(metadata)
        return metadata

    def get(self, object_class, object_id):
        return self.engine.get(object_class, object_id)

    def update(self, object_class, object_id, data, *, mirror=True, encrypted=False):
        if not self.engine.exists(object_class, object_id):
            raise StorageError("object not found")
        return self.put(object_class, object_id, data, mirror=mirror, encrypted=encrypted)

    def delete(self, object_class, object_id):
        self.policy.validate_delete(object_class)
        deleted = self.engine.delete(object_class, object_id)
        if deleted:
            self.registry.remove(object_id)
        return deleted

    def locate(self, object_id):
        return self.registry.get(object_id)

    def verify(self, object_class, object_id):
        entry = self.registry.get(object_id)
        return self.integrity.verify(object_class, object_id, entry["content_hash"])

    def synchronize(self, object_id):
        entry = self.registry.get(object_id)
        return self.engine.synchronize(
            entry["object_class"], object_id, encrypted=entry.get("encryption_state") == "ENCRYPTED"
        )

    def recover(self, object_id):
        return self.recovery.recover(object_id)

    def status(self):
        return {
            "storage_version": self.engine.version,
            "policy_version": self.policy.version,
            "registered_objects": len(self.registry.list()),
            "engine": self.engine.status(),
        }
