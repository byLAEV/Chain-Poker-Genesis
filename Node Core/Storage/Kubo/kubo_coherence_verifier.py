#!/usr/bin/env python3
"""Local/Kubo coherence verification and Dual Storage readiness gate."""
from __future__ import annotations
from datetime import datetime, timezone
import hashlib

class KuboCoherenceError(RuntimeError): pass

class KuboCoherenceVerifier:
    """Verifies registry, local bytes, Kubo bytes and CID/content hash coherence."""

    def __init__(self, storage_manager, health_manager):
        self.storage=storage_manager
        self.health=health_manager

    def verify_all(self, *, require_healthy=True):
        health=self.health.require_healthy() if require_healthy else self.health.check()
        results=[]
        for entry in self.storage.registry.list():
            if entry.get("object_class") not in {"public","private","restricted"}:
                results.append({"object_id":entry["object_id"],"state":"SKIPPED","reason":"POLICY_EXCLUDED"})
                continue
            results.append(self._verify_one(entry))
        failures=[x for x in results if x["state"]=="FAILED"]
        synchronized=[x for x in results if x["state"]=="COHERENT"]
        ready=health.get("health_state")=="HEALTHY" and not failures and len(synchronized)>0 or (
            health.get("health_state")=="HEALTHY" and not failures and len(results)==0
        )
        return {
            "operation":"KUBO_COHERENCE_VERIFICATION",
            "verified_at":datetime.now(timezone.utc).isoformat(),
            "health":health,
            "objects_total":len(results),
            "objects_coherent":len(synchronized),
            "objects_failed":len(failures),
            "results":results,
            "coherence_state":"COHERENT" if not failures else "FAILED",
            "dual_storage_ready":ready,
        }

    def _verify_one(self, entry):
        oid=entry["object_id"]; cls=entry["object_class"]; expected=entry["content_hash"]; cid=entry.get("cid")
        if not cid or entry.get("location_state")!="LOCAL_AND_DISTRIBUTED":
            return {"object_id":oid,"state":"FAILED","reason":"MIRROR_STATE_INCOMPLETE"}
        try:
            local,_=self.storage.engine.get_local(cls,oid)
            if hashlib.sha256(local).hexdigest()!=expected:
                return {"object_id":oid,"state":"FAILED","reason":"LOCAL_HASH_MISMATCH"}
            remote=self.storage.engine.read_distributed(cid)
            if hashlib.sha256(remote).hexdigest()!=expected:
                return {"object_id":oid,"state":"FAILED","reason":"KUBO_HASH_MISMATCH"}
            if remote!=local:
                return {"object_id":oid,"state":"FAILED","reason":"LOCAL_KUBO_CONTENT_MISMATCH"}
            verification=self.storage.integrity.verify_distributed(cid,expected)
            if verification.get("verification_result")!="VALID":
                return {"object_id":oid,"state":"FAILED","reason":"DISTRIBUTED_INTEGRITY_INVALID"}
            return {"object_id":oid,"state":"COHERENT","cid":cid}
        except Exception as exc:
            return {"object_id":oid,"state":"FAILED","reason":type(exc).__name__}

class DualStorageReadiness:
    """Configuration gate; readiness is evidence-based and does not copy data."""

    def evaluate(self, coherence_report, configuration_manager=None):
        if coherence_report.get("dual_storage_ready") is not True:
            raise KuboCoherenceError("Dual Storage cannot be enabled before coherent Kubo mirror verification")
        return {
            "storage_mode":"DUAL_STORAGE",
            "state":"READY",
            "coherence_verified_at":coherence_report["verified_at"],
        }
