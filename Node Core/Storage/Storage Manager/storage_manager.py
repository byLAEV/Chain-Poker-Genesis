#!/usr/bin/env python3
"""Protocol-neutral high-level Node Core Storage Manager."""
from __future__ import annotations

import sys
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
for subdir in ("Storage Policy", "Object Registry", "Integrity", "Disaster Recovery", "Synchronization"):
    sys.path.insert(0, str(ROOT / subdir))

from storage_engine import StorageEngine, StorageError, sha256
from storage_policy import StoragePolicy
from object_registry import ObjectRegistry
from integrity_manager import IntegrityManager
from storage_recovery import StorageRecovery
from synchronization_manager import SynchronizationManager

class StorageManager:
    def __init__(self, node_root, *, kubo=None):
        self.node_root = Path(node_root).resolve()
        self.engine = StorageEngine(self.node_root, kubo=kubo)
        self.policy = StoragePolicy()
        self.registry = ObjectRegistry(self.node_root)
        self.integrity = IntegrityManager(self.engine)
        self.synchronization = SynchronizationManager()
        self.recovery = StorageRecovery(self.engine, self.registry, self.integrity)

    def create(self, object_class, object_id, data, *, mirror=True, encrypted=False):
        policy = self.policy.validate_write(object_class, mirror=mirror, encrypted=encrypted)
        metadata = self.engine.put_local(object_class, object_id, data)
        if encrypted:
            metadata["encryption_state"] = "ENCRYPTED"

        if mirror:
            try:
                cid = self.engine.mirror(data)
                metadata.update({
                    "provider_type": "DECENTRALIZED",
                    "location_state": "LOCAL_AND_DISTRIBUTED",
                    "synchronization_state": "SYNCHRONIZED",
                    "cid": cid,
                })
            except Exception as exc:
                metadata.update({
                    "provider_type": "LOCAL",
                    "location_state": "SYNC_PENDING",
                    "synchronization_state": "SYNC_FAILED",
                    "sync_error": type(exc).__name__,
                })

        metadata.update(policy)
        return self.registry.upsert(metadata)

    put = create
    write = create

    def put_json(self, object_class, object_id, value, *, mirror=True, encrypted=False):
        data = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return self.create(object_class, object_id, data, mirror=mirror, encrypted=encrypted)

    def exists(self, object_class, object_id):
        try:
            entry = self.registry.get(object_id)
            return entry.get("object_class") == object_class and self.engine.exists_local(object_class, object_id)
        except Exception:
            return False

    def get(self, object_class, object_id):
        entry = self.registry.get(object_id)
        if entry["object_class"] != object_class:
            raise StorageError("object class does not match registry entry")

        cid = entry.get("cid")
        if cid and self.engine.kubo:
            try:
                data = self.engine.read_distributed(cid)
                if sha256(data) == entry["content_hash"]:
                    return data, {**entry, "read_source": "KUBO_IPFS"}
            except Exception:
                pass

        try:
            data, metadata = self.engine.get_local(object_class, object_id)
        except StorageError:
            if cid:
                return self.recovery.recover(object_id)
            raise

        if sha256(data) != entry["content_hash"]:
            raise StorageError("local content integrity mismatch")
        return data, {**entry, "read_source": "LOCAL_FALLBACK" if cid else "LOCAL"}

    def update(self, object_class, object_id, data, *, mirror=True, encrypted=False):
        existing = self.registry.get(object_id)
        if existing.get("object_class") != object_class:
            raise StorageError("object class does not match registry entry")
        metadata = self.create(object_class, object_id, data, mirror=mirror, encrypted=encrypted)
        metadata["version"] = int(existing.get("version", 1)) + 1
        metadata["created_at"] = existing["created_at"]
        from datetime import datetime, timezone
        metadata["updated_at"] = datetime.now(timezone.utc).isoformat()
        return self.registry.upsert(metadata)

    def delete(self, object_class, object_id):
        self.policy.validate_delete(object_class)
        entry = self.registry.get(object_id)
        if entry.get("cid") and self.engine.kubo:
            try:
                self.engine.kubo.unpin(entry["cid"])
            except Exception:
                pass
        deleted = self.engine.delete_local(object_class, object_id)
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
        if not self.engine.exists_local(entry["object_class"], object_id):
            raise StorageError("cannot synchronize missing local object")
        try:
            self.synchronization.transition(entry["location_state"], "SYNC_PROCESSING")
        except ValueError:
            pass
        try:
            data, local_metadata = self.engine.get_local(entry["object_class"], object_id)
            if sha256(data) != entry["content_hash"]:
                raise StorageError("local content integrity mismatch")
            if entry["object_class"] in {"private", "restricted"} and entry.get("encryption_state") != "ENCRYPTED":
                raise StorageError("private/restricted distribution requires encrypted bytes")
            cid = self.engine.mirror(data)
            entry.update(local_metadata)
            entry.update({
                "provider_type": "DECENTRALIZED",
                "location_state": "LOCAL_AND_DISTRIBUTED",
                "synchronization_state": "SYNCHRONIZED",
                "cid": cid,
                "encryption_state": entry.get("encryption_state", "PLAINTEXT"),
            })
            return self.registry.upsert(entry)
        except Exception as exc:
            entry.update({
                "location_state": "SYNC_PENDING",
                "synchronization_state": "SYNC_FAILED",
                "sync_error": type(exc).__name__,
            })
            self.registry.upsert(entry)
            raise

    def recover(self, object_id):
        return self.recovery.recover(object_id)

    def status(self):
        return {
            "storage_version": self.engine.version,
            "policy_version": self.policy.version,
            "registered_objects": len(self.registry.list()),
            "engine": self.engine.status(),
        }
