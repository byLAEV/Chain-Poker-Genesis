#!/usr/bin/env python3
"""Evidence-based continuous local/Kubo reconciliation."""
from __future__ import annotations
from datetime import datetime, timezone
import hashlib

class ReconciliationError(RuntimeError):
    pass

class KuboReconciliationManager:
    """Reconciles registered mirrors without blind overwrite."""

    DISTRIBUTABLE = {"public", "private", "restricted"}

    def __init__(self, storage_manager, health_manager):
        self.storage = storage_manager
        self.health = health_manager

    def reconcile(self, *, require_healthy=True):
        health = self.health.require_healthy() if require_healthy else self.health.check()
        results = [self._reconcile_entry(e) for e in self.storage.registry.list()]
        conflicts = [r for r in results if r["state"] == "CONFLICT"]
        failures = [r for r in results if r["state"] == "FAILED"]
        return {
            "operation": "KUBO_CONTINUOUS_RECONCILIATION",
            "reconciled_at": datetime.now(timezone.utc).isoformat(),
            "health": health,
            "objects_total": len(results),
            "objects_coherent": sum(r["state"] == "COHERENT" for r in results),
            "objects_repaired": sum(r["state"] == "REPAIRED" for r in results),
            "objects_conflict": len(conflicts),
            "objects_failed": len(failures),
            "results": results,
            "state": "CONFLICT" if conflicts else ("FAILED" if failures else "COHERENT"),
        }

    def _reconcile_entry(self, entry):
        oid = entry["object_id"]
        cls = entry["object_class"]
        if cls not in self.DISTRIBUTABLE:
            return {"object_id": oid, "state": "SKIPPED", "reason": "POLICY_EXCLUDED"}
        cid = entry.get("cid")
        if not cid:
            return {"object_id": oid, "state": "FAILED", "reason": "CID_MISSING"}

        local = None
        local_error = None
        try:
            local, _ = self.storage.engine.get_local(cls, oid)
        except Exception as exc:
            local_error = type(exc).__name__

        remote = None
        remote_error = None
        try:
            remote = self.storage.engine.read_distributed(cid)
        except Exception as exc:
            remote_error = type(exc).__name__

        expected = entry["content_hash"]
        local_valid = local is not None and hashlib.sha256(local).hexdigest() == expected
        remote_valid = remote is not None and hashlib.sha256(remote).hexdigest() == expected

        if local_valid and remote_valid:
            if local != remote:
                return self._mark_conflict(entry, "CONTENT_DIVERGENCE")
            self._mark_coherent(entry)
            return {"object_id": oid, "state": "COHERENT", "cid": cid}

        if not local_valid and remote_valid:
            # Safe recovery direction: Kubo -> local only when the registry hash validates.
            try:
                self.storage.recover(oid)
                return {"object_id": oid, "state": "REPAIRED", "direction": "KUBO_TO_LOCAL", "cid": cid}
            except Exception as exc:
                return {"object_id": oid, "state": "FAILED", "reason": type(exc).__name__}

        if local_valid and not remote_valid:
            # Safe mirror direction: local -> Kubo, never overwrite a valid divergent remote object.
            try:
                new_cid = self.storage.engine.mirror(local)
                if new_cid != cid:
                    return self._mark_conflict(entry, "CID_CHANGED_OR_REMOTE_UNAVAILABLE")
                return self._mark_coherent(entry)
            except Exception as exc:
                return {"object_id": oid, "state": "FAILED", "reason": type(exc).__name__}

        return self._mark_conflict(entry, "BOTH_SIDES_INVALID_OR_UNAVAILABLE",
                                   details={"local_error": local_error, "remote_error": remote_error})

    def _mark_coherent(self, entry):
        entry.update({
            "location_state": "LOCAL_AND_DISTRIBUTED",
            "synchronization_state": "SYNCHRONIZED",
            "reconciliation_state": "COHERENT",
            "reconciled_at": datetime.now(timezone.utc).isoformat(),
        })
        self.storage.registry.upsert(entry)
        return {"object_id": entry["object_id"], "state": "COHERENT", "cid": entry.get("cid")}

    def _mark_conflict(self, entry, reason, details=None):
        entry.update({
            "synchronization_state": "CONFLICT",
            "reconciliation_state": "CONFLICT",
            "conflict_reason": reason,
            "conflict_detected_at": datetime.now(timezone.utc).isoformat(),
        })
        self.storage.registry.upsert(entry)
        result = {"object_id": entry["object_id"], "state": "CONFLICT", "reason": reason}
        if details:
            result["details"] = details
        return result
