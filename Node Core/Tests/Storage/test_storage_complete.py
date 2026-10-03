#!/usr/bin/env python3
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

STORAGE = Path(__file__).resolve().parents[2] / "Storage"
sys.path.insert(0, str(STORAGE))
sys.path.insert(0, str(STORAGE / "Storage Manager"))
sys.path.insert(0, str(STORAGE / "Storage Policy"))
from storage_manager import StorageManager
from storage_policy import StoragePolicy, StoragePolicyError
from storage_engine import StorageError
from synchronization_manager import SynchronizationManager

def test_local_crud():
    with TemporaryDirectory() as root:
        manager = StorageManager(root)
        meta = manager.put("public", "object-a", b"hello", mirror=False)
        assert meta["location_state"] == "LOCAL_ONLY"
        data, _ = manager.get("public", "object-a")
        assert data == b"hello"
        assert manager.verify("public", "object-a")["verification_result"] == "VALID"
        assert manager.delete("public", "object-a") is True

def test_policy():
    policy = StoragePolicy()
    try:
        policy.validate_write("private", mirror=True, encrypted=False)
        raise AssertionError("private distribution must require encryption")
    except StoragePolicyError:
        pass
    policy.validate_write("private", mirror=True, encrypted=True)

def test_path_traversal():
    with TemporaryDirectory() as root:
        manager = StorageManager(root)
        try:
            manager.put("public", "../escape", b"x", mirror=False)
            raise AssertionError("path traversal was accepted")
        except StorageError:
            pass

def test_sync_state_machine():
    sync = SynchronizationManager()
    assert sync.transition("LOCAL_ONLY", "SYNC_PENDING") == "SYNC_PENDING"
    assert sync.transition("SYNC_PENDING", "SYNC_PROCESSING") == "SYNC_PROCESSING"
    assert sync.transition("SYNC_PROCESSING", "SYNCHRONIZED") == "SYNCHRONIZED"

if __name__ == "__main__":
    test_local_crud(); test_policy(); test_path_traversal(); test_sync_state_machine()
    print("Storage complete integration tests: PASS")
