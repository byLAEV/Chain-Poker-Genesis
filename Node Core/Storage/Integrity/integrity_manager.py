#!/usr/bin/env python3
"""Content integrity verification for local and distributed storage copies."""

from __future__ import annotations
from datetime import datetime, timezone

class IntegrityManager:
    VALID = "VALID"
    MISMATCH = "MISMATCH"
    CORRUPTED = "CORRUPTED"
    QUARANTINED = "QUARANTINED"

    def __init__(self, engine):
        self.engine = engine

    def verify(self, object_class, object_id, expected_hash):
        checked_at = datetime.now(timezone.utc).isoformat()
        try:
            data, metadata = self.engine.get(object_class, object_id)
            actual = metadata.get("content_hash")
            result = self.VALID if actual == expected_hash else self.MISMATCH
            return {
                "object_id": object_id, "expected_hash": expected_hash,
                "actual_hash": actual, "verification_time": checked_at,
                "verification_source": metadata.get("read_source", "LOCAL"),
                "verification_result": result,
            }
        except Exception as exc:
            return {
                "object_id": object_id, "expected_hash": expected_hash,
                "actual_hash": None, "verification_time": checked_at,
                "verification_source": "UNAVAILABLE",
                "verification_result": self.CORRUPTED,
                "error": type(exc).__name__,
            }

    def verify_distributed(self, cid, expected_hash):
        if not self.engine.kubo:
            return {"verification_result": "UNAVAILABLE"}
        try:
            actual = __import__("hashlib").sha256(self.engine.kubo.get(cid)).hexdigest()
            return {"expected_hash": expected_hash, "actual_hash": actual,
                    "verification_result": self.VALID if actual == expected_hash else self.MISMATCH}
        except Exception as exc:
            return {"expected_hash": expected_hash, "actual_hash": None,
                    "verification_result": self.CORRUPTED, "error": type(exc).__name__}
