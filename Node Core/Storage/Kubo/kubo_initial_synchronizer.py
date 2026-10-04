#!/usr/bin/env python3
"""Initial local-to-Kubo synchronization coordinator."""
from __future__ import annotations
from datetime import datetime, timezone
import hashlib

class KuboInitialSyncError(RuntimeError): pass

class KuboInitialSynchronizer:
    """Uses the canonical StorageManager registry/policy/integrity boundaries."""

    def __init__(self, storage_manager, health_manager):
        self.storage = storage_manager
        self.health = health_manager

    def synchronize_all(self, *, include_classes=("public","private","restricted"), require_healthy=True):
        if require_healthy:
            health=self.health.require_healthy()
        else:
            health=self.health.check()
        results=[]
        for entry in self.storage.registry.list():
            object_class=entry.get("object_class")
            if object_class not in include_classes:
                results.append(self._skip(entry,"POLICY_EXCLUDED"))
                continue
            results.append(self._sync_one(entry))
        failures=[r for r in results if r["state"]=="FAILED"]
        return {
            "operation":"INITIAL_LOCAL_TO_KUBO",
            "started_at":datetime.now(timezone.utc).isoformat(),
            "health":health,
            "objects_total":len(results),
            "objects_synchronized":sum(r["state"]=="SYNCHRONIZED" for r in results),
            "objects_skipped":sum(r["state"]=="SKIPPED" for r in results),
            "objects_failed":len(failures),
            "results":results,
            "sync_state":"FAILED" if failures else "SYNCHRONIZED",
        }

    def _sync_one(self, entry):
        object_id=entry["object_id"]; cls=entry["object_class"]
        try:
            if entry.get("cid"):
                verification=self.storage.integrity.verify_distributed(entry["cid"],entry["content_hash"])
                if verification["verification_result"]=="VALID":
                    return {"object_id":object_id,"state":"SYNCHRONIZED","cid":entry["cid"],"source":"KUBO_EXISTING"}
            data,_=self.storage.engine.get_local(cls,object_id)
            if hashlib.sha256(data).hexdigest()!=entry["content_hash"]:
                return {"object_id":object_id,"state":"FAILED","reason":"LOCAL_INTEGRITY_MISMATCH"}
            cid=self.storage.engine.mirror(data)
            if not self.storage.engine.verify_distributed(cid,entry["content_hash"]):
                return {"object_id":object_id,"state":"FAILED","reason":"KUBO_INTEGRITY_MISMATCH"}
            entry.update({
                "provider_type":"DECENTRALIZED",
                "location_state":"LOCAL_AND_DISTRIBUTED",
                "synchronization_state":"SYNCHRONIZED",
                "cid":cid,
                "updated_at":datetime.now(timezone.utc).isoformat(),
            })
            self.storage.registry.upsert(entry)
            return {"object_id":object_id,"state":"SYNCHRONIZED","cid":cid,"source":"LOCAL"}
        except Exception as exc:
            entry.update({"location_state":"SYNC_PENDING","synchronization_state":"SYNC_FAILED","sync_error":type(exc).__name__})
            self.storage.registry.upsert(entry)
            return {"object_id":object_id,"state":"FAILED","reason":type(exc).__name__}

    @staticmethod
    def _skip(entry, reason):
        return {"object_id":entry["object_id"],"state":"SKIPPED","reason":reason}
