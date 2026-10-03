#!/usr/bin/env python3
"""Integrity verification boundary for Node Core Storage."""
from __future__ import annotations
from datetime import datetime, timezone
import hashlib

class IntegrityManager:
    VALID = "VALID"
    MISMATCH = "MISMATCH"
    CORRUPTED = "CORRUPTED"
    UNAVAILABLE = "UNAVAILABLE"

    def __init__(self, engine):
        self.engine = engine

    def verify(self, object_class, object_id, expected_hash):
        checked_at = datetime.now(timezone.utc).isoformat()
        try:
            data, metadata = self.engine.get_local(object_class, object_id)
            actual = hashlib.sha256(data).hexdigest()
            return {
                "object_id": object_id,
                "expected_hash": expected_hash,
                "actual_hash": actual,
                "verification_time": checked_at,
                "verification_source": "LOCAL",
                "verification_result": self.VALID if actual == expected_hash else self.MISMATCH,
            }
        except Exception as exc:
            return {
                "object_id": object_id,
                "expected_hash": expected_hash,
                "actual_hash": None,
                "verification_time": checked_at,
                "verification_source": "LOCAL",
                "verification_result": self.CORRUPTED,
                "error": type(exc).__name__,
            }

    def verify_distributed(self, cid, expected_hash):
        checked_at = datetime.now(timezone.utc).isoformat()
        try:
            actual = hashlib.sha256(self.engine.read_distributed(cid)).hexdigest()
            return {
                "expected_hash": expected_hash,
                "actual_hash": actual,
                "verification_time": checked_at,
                "verification_source": "KUBO_IPFS",
                "verification_result": self.VALID if actual == expected_hash else self.MISMATCH,
            }
        except Exception as exc:
            return {
                "expected_hash": expected_hash,
                "actual_hash": None,
                "verification_time": checked_at,
                "verification_source": "KUBO_IPFS",
                "verification_result": self.UNAVAILABLE,
                "error": type(exc).__name__,
            }
