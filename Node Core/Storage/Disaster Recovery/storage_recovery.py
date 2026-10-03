#!/usr/bin/env python3
"""Verified decentralized-to-local recovery."""
from __future__ import annotations
from storage_engine import sha256

class RecoveryError(Exception):
    pass

class StorageRecovery:
    def __init__(self, engine, registry, integrity):
        self.engine = engine
        self.registry = registry
        self.integrity = integrity

    def recover(self, object_id):
        entry = self.registry.get(object_id)
        cid = entry.get("cid")
        if not cid:
            raise RecoveryError("no decentralized recovery source available")
        if not self.engine.kubo:
            raise RecoveryError("decentralized provider unavailable")
        try:
            data = self.engine.read_distributed(cid)
        except Exception as exc:
            raise RecoveryError("decentralized provider unavailable") from exc
        if sha256(data) != entry["content_hash"]:
            raise RecoveryError("recovery source failed integrity verification")
        metadata = self.engine.local.put(entry["object_class"], object_id, data)
        metadata.update({
            "cid": cid,
            "provider_type": "DECENTRALIZED",
            "location_state": "LOCAL_AND_DISTRIBUTED",
            "synchronization_state": "SYNCHRONIZED",
            "recovery_state": "RECOVERED",
            "encryption_state": entry.get("encryption_state", "PLAINTEXT"),
        })
        for key in ("policy_version", "distribution_allowed",
                    "encryption_required_for_distribution"):
            if key in entry:
                metadata[key] = entry[key]
        saved = self.registry.upsert(metadata)
        return data, saved
