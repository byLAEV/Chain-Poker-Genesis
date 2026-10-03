#!/usr/bin/env python3
"""Protocol-neutral Node Core recovery coordinator."""
from __future__ import annotations
import json
from pathlib import Path
from .recovery_state import RecoveryRecord

class RecoveryManager:
    version="1.1.0"
    def __init__(self, root):
        self.root=Path(root).resolve()
        self.recovery_dir=self.root/"node-storage/recovery"
        self.state_file=self.recovery_dir/"node-recovery-state.json"
    def inspect(self):
        storage=self.root/"node-storage"
        return {
            "environment":self.root.is_dir(),
            "storage":storage.is_dir(),
            "configuration":(storage/"configuration/node-config.json").is_file(),
            "state":(storage/"state/node-state.json").is_file(),
            "recovery":self.recovery_dir.is_dir(),
            "identity":(storage/"identity/node-identity.json").is_file(),
        }
    def recover(self):
        self.recovery_dir.mkdir(parents=True,exist_ok=True)
        checks=self.inspect()
        if not checks["environment"] or not checks["storage"]:
            return self._record("RECOVERY_FAILED",checks)
        if not checks["configuration"] or not checks["state"]:
            return self._record("RECOVERY_INCOMPLETE",checks)
        return self._record("RECOVERY_READY",checks)
    def _record(self,status,details):
        record={"status":status,"details":details}
        self.state_file.write_text(json.dumps(record,indent=2,sort_keys=True)+"\n",encoding="utf-8")
        return record
