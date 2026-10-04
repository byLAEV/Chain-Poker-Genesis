#!/usr/bin/env python3
"""Protocol-neutral Node Core recovery coordinator."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from recovery_state import RecoveryRecord

class RecoveryManager:
    version = "1.2.0"
    STATES = {
        "NORMAL",
        "FAILURE_DETECTED",
        "RECOVERY_PENDING",
        "RECOVERING",
        "VERIFYING",
        "RECOVERED",
        "FAILED",
    }
    TRANSITIONS = {
        "NORMAL": {"FAILURE_DETECTED"},
        "FAILURE_DETECTED": {"RECOVERY_PENDING", "FAILED"},
        "RECOVERY_PENDING": {"RECOVERING", "FAILED"},
        "RECOVERING": {"VERIFYING", "FAILED"},
        "VERIFYING": {"RECOVERED", "FAILED"},
        "RECOVERED": {"FAILURE_DETECTED"},
        "FAILED": {"FAILURE_DETECTED"},
    }

    def __init__(self, root):
        self.root = Path(root).resolve()
        self.recovery_dir = self.root / "node-storage/recovery"
        self.state_file = self.recovery_dir / "node-recovery-state.json"
        self.journal_file = self.recovery_dir / "node-recovery-journal.json"

    def inspect(self):
        storage = self.root / "node-storage"
        return {
            "environment": self.root.is_dir(),
            "storage": storage.is_dir(),
            "configuration": (storage / "configuration/node-config.json").is_file(),
            "state": (storage / "state/node-state.json").is_file(),
            "recovery": self.recovery_dir.is_dir(),
            "identity": (storage / "identity/node-identity.json").is_file(),
        }

    def recover(self):
        self.recovery_dir.mkdir(parents=True, exist_ok=True)
        checks = self.inspect()

        # A complete, previously recovered installation is not silently rewritten.
        existing = self._load_latest()
        if existing and existing.get("state") == "RECOVERED" and all(
            checks.get(key, False) for key in ("environment", "storage", "configuration", "state")
        ):
            return existing

        current = existing.get("state", "NORMAL") if existing else "NORMAL"
        current = self._transition(current, "FAILURE_DETECTED")
        current = self._transition(current, "RECOVERY_PENDING")

        required = ("environment", "storage", "configuration", "state")
        if not all(checks.get(key, False) for key in required):
            return self._finish("FAILED", checks, "required recovery prerequisites are missing")

        current = self._transition(current, "RECOVERING")
        # Generic Node Core Recovery does not invent a protocol-specific restoration source.
        current = self._transition(current, "VERIFYING")
        verification = self.inspect()
        if not all(verification.get(key, False) for key in required):
            return self._finish("FAILED", verification, "post-recovery verification failed")

        return self._finish("RECOVERED", verification, "recovery prerequisites verified")

    def _transition(self, current, target):
        if target not in self.TRANSITIONS.get(current, set()):
            raise RuntimeError(f"invalid recovery transition: {current} -> {target}")
        return target

    def _finish(self, state, details, message):
        now = datetime.now(timezone.utc).isoformat()
        record = RecoveryRecord(
            operation="NODE_CORE_RECOVERY",
            status="RECOVERY_READY" if state == "RECOVERED" else "RECOVERY_FAILED",
            started_at=now,
            completed_at=now,
            details={
                "state": state,
                "message": message,
                "checks": details,
            },
        )
        payload = {
            "status": record.status,
            "state": state,
            "operation": record.operation,
            "started_at": record.started_at,
            "completed_at": record.completed_at,
            "details": record.details,
        }
        self._append_journal(payload)
        self.state_file.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return payload

    def _load_latest(self):
        if not self.state_file.is_file():
            return None
        try:
            return json.loads(self.state_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None

    def _append_journal(self, payload):
        entries = []
        if self.journal_file.is_file():
            try:
                entries = json.loads(self.journal_file.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                raise RuntimeError("recovery journal is invalid")
        if not isinstance(entries, list):
            raise RuntimeError("recovery journal must be a list")
        entries.append(payload)
        self.journal_file.write_text(
            json.dumps(entries, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
