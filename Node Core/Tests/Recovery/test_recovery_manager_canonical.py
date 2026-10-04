#!/usr/bin/env python3
import tempfile
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"Recovery"))
from recovery_manager import RecoveryManager

def prepare(root):
    storage=root/"node-storage"
    (storage/"configuration").mkdir(parents=True)
    (storage/"state").mkdir(parents=True)
    (storage/"identity").mkdir(parents=True)
    (storage/"configuration/node-config.json").write_text("{}")
    (storage/"state/node-state.json").write_text("{}")
    (storage/"identity/node-identity.json").write_text("{}")

def test_recovery_state_machine():
    with tempfile.TemporaryDirectory() as d:
        root=Path(d)
        prepare(root)
        result=RecoveryManager(root).recover()
        assert result["state"]=="RECOVERED"
        assert result["status"]=="RECOVERY_READY"
        assert (root/"node-storage/recovery/node-recovery-state.json").is_file()
        journal=(root/"node-storage/recovery/node-recovery-journal.json")
        assert journal.is_file()
        again=RecoveryManager(root).recover()
        assert again["state"]=="RECOVERED"
        assert len(__import__("json").loads(journal.read_text()))==1

def test_recovery_invalid_transition_is_rejected():
    with tempfile.TemporaryDirectory() as d:
        manager = RecoveryManager(Path(d))
        invalid = (
            ("NORMAL", "RECOVERING"),
            ("RECOVERY_PENDING", "RECOVERED"),
            ("RECOVERING", "RECOVERED"),
            ("VERIFYING", "RECOVERING"),
            ("RECOVERED", "RECOVERING"),
            ("FAILED", "RECOVERED"),
        )
        for current, target in invalid:
            try:
                manager._transition(current, target)
            except RuntimeError:
                continue
            raise AssertionError(
                f"invalid recovery transition accepted: {current} -> {target}"
            )

def test_failed_recovery_is_explicit():
    with tempfile.TemporaryDirectory() as d:
        result=RecoveryManager(Path(d)).recover()
        assert result["state"]=="FAILED"
        assert result["status"]=="RECOVERY_FAILED"

if __name__=="__main__":
    test_recovery_state_machine()
    test_failed_recovery_is_explicit()
    print("Node Core Recovery tests: PASS")
