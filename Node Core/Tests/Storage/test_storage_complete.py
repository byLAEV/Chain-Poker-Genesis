#!/usr/bin/env python3
"""Executable integration tests for the Node Core Storage subsystem."""
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

STORAGE = Path(__file__).resolve().parents[2] / "Storage"
sys.path.insert(0, str(STORAGE))
sys.path.insert(0, str(STORAGE / "Storage Manager"))
sys.path.insert(0, str(STORAGE / "Storage Policy"))
sys.path.insert(0, str(STORAGE / "Synchronization"))

from storage_manager import StorageManager
from storage_policy import StoragePolicy, StoragePolicyError
from storage_engine import StorageError
from synchronization_manager import SynchronizationManager

class FakeKubo:
    def __init__(self):
        self.objects = {}
        self.pins = set()

    def status(self):
        return {"provider_type": "DECENTRALIZED", "status": "READY"}

    def add(self, data, *, pin=True):
        import hashlib
        cid = "bafy" + hashlib.sha256(data).hexdigest()[:32]
        self.objects[cid] = bytes(data)
        if pin:
            self.pins.add(cid)
        return cid

    def get(self, cid):
        if cid not in self.objects:
            raise RuntimeError("missing CID")
        return self.objects[cid]

    def verify(self, cid, expected_hash):
        import hashlib
        return hashlib.sha256(self.get(cid)).hexdigest() == expected_hash

    def unpin(self, cid):
        self.pins.discard(cid)
        return True


class FailingKubo(FakeKubo):
    def get(self, cid):
        raise RuntimeError("Kubo unavailable")

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

def test_kubo_mirror_and_preferred_read():
    with TemporaryDirectory() as root:
        kubo = FakeKubo()
        manager = StorageManager(root, kubo=kubo)
        meta = manager.put("public", "object-b", b"distributed", mirror=True)
        assert meta["location_state"] == "LOCAL_AND_DISTRIBUTED"
        assert meta["synchronization_state"] == "SYNCHRONIZED"
        data, read_meta = manager.get("public", "object-b")
        assert data == b"distributed"
        assert read_meta["read_source"] == "KUBO_IPFS"

def test_local_fallback():
    with TemporaryDirectory() as root:
        kubo = FakeKubo()
        manager = StorageManager(root, kubo=kubo)
        manager.put("public", "object-c", b"fallback", mirror=True)
        kubo.objects.clear()
        data, read_meta = manager.get("public", "object-c")
        assert data == b"fallback"
        assert read_meta["read_source"] == "LOCAL_FALLBACK"


def test_kubo_unavailable_local_fallback():
    with TemporaryDirectory() as root:
        kubo = FailingKubo()
        manager = StorageManager(root, kubo=kubo)
        manager.put("public", "object-kubo-down", b"fallback-on-provider-failure", mirror=True)
        data, read_meta = manager.get("public", "object-kubo-down")
        assert data == b"fallback-on-provider-failure"
        assert read_meta["read_source"] == "LOCAL_FALLBACK"

def test_disaster_recovery():
    with TemporaryDirectory() as root:
        kubo = FakeKubo()
        manager = StorageManager(root, kubo=kubo)
        manager.put("public", "object-d", b"recover-me", mirror=True)
        manager.engine.delete_local("public", "object-d")
        assert not manager.engine.exists_local("public", "object-d")
        data, metadata = manager.get("public", "object-d")
        assert data == b"recover-me"
        assert metadata["recovery_state"] == "RECOVERED"
        assert manager.engine.exists_local("public", "object-d")

def test_sync_state_machine():
    sync = SynchronizationManager()
    assert sync.transition("LOCAL_ONLY", "SYNC_PENDING") == "SYNC_PENDING"
    assert sync.transition("SYNC_PENDING", "SYNC_PROCESSING") == "SYNC_PROCESSING"
    assert sync.transition("SYNC_PROCESSING", "SYNCHRONIZED") == "SYNCHRONIZED"

if __name__ == "__main__":
    test_local_crud()
    test_policy()
    test_path_traversal()
    test_kubo_mirror_and_preferred_read()
    test_local_fallback()
    test_kubo_unavailable_local_fallback()
    test_disaster_recovery()
    test_sync_state_machine()
    print("Node Core Storage integration tests: PASS")
