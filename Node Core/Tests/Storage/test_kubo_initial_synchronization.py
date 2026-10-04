from pathlib import Path
from tempfile import TemporaryDirectory
import sys
BASE=Path(__file__).resolve().parents[2]/"Storage"
sys.path += [str(BASE),str(BASE/"Storage Manager"),str(BASE/"Synchronization"),str(BASE/"Kubo")]
from storage_manager import StorageManager
from kubo_initial_synchronizer import KuboInitialSynchronizer

class FakeHealth:
    def require_healthy(self): return {"health_state":"HEALTHY","peer_id":"peer-test","version":"0.43.1"}
    def check(self): return self.require_healthy()

def test_initial_sync_uses_registry_and_verifies_kubo():
    with TemporaryDirectory() as root:
        from test_storage_complete import FakeKubo
        manager=StorageManager(root,kubo=FakeKubo())
        manager.put("public","sync-a",b"hello",mirror=False)
        result=KuboInitialSynchronizer(manager,FakeHealth()).synchronize_all()
        assert result["sync_state"]=="SYNCHRONIZED"
        assert result["objects_synchronized"]==1
        entry=manager.registry.get("sync-a")
        assert entry["location_state"]=="LOCAL_AND_DISTRIBUTED"
        assert entry["synchronization_state"]=="SYNCHRONIZED"

def test_initial_sync_excludes_non_distributable_classes():
    with TemporaryDirectory() as root:
        from test_storage_complete import FakeKubo
        manager=StorageManager(root,kubo=FakeKubo())
        manager.put("temporary","temp-a",b"temporary",mirror=False)
        result=KuboInitialSynchronizer(manager,FakeHealth()).synchronize_all()
        assert result["objects_skipped"]==1
        assert result["objects_failed"]==0

def test_initial_sync_fails_on_local_corruption():
    with TemporaryDirectory() as root:
        from test_storage_complete import FakeKubo
        manager=StorageManager(root,kubo=FakeKubo())
        manager.put("public","bad-a",b"correct",mirror=False)
        path=manager.engine.local._path("public","bad-a")
        path.write_bytes(b"tampered")
        result=KuboInitialSynchronizer(manager,FakeHealth()).synchronize_all()
        assert result["objects_failed"]==1
