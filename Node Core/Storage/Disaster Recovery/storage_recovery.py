#!/usr/bin/env python3
"""Protocol-neutral local storage recovery from a verified decentralized copy."""

from __future__ import annotations

from storage_engine import StorageError, sha256

class RecoveryError(Exception): pass

class StorageRecovery:
    def __init__(self, engine, registry, integrity):
        self.engine = engine
        self.registry = registry
        self.integrity = integrity

    def recover(self, object_id):
        entry = self.registry.get(object_id)
        if not entry.get("cid") or not self.engine.kubo:
            raise RecoveryError("no decentralized recovery source available")
        try:
            data = self.engine.kubo.get(entry["cid"])
        except Exception as exc:
            raise RecoveryError("decentralized provider unavailable") from exc
        if sha256(data) != entry["content_hash"]:
            raise RecoveryError("recovery source failed integrity verification")
        metadata = self.engine.local.put(entry["object_class"], object_id, data)
        metadata.update({
            "cid": entry["cid"],
            "provider_type": "DECENTRALIZED",
            "location_state": "LOCAL_AND_DISTRIBUTED",
            "synchronization_state": "SYNCHRONIZED",
            "recovery_state": "RECOVERED",
            "encryption_state": entry.get("encryption_state", "PLAINTEXT"),
        })
        self.engine._write_registry(metadata)
        self.registry.upsert(metadata)
        return metadata
