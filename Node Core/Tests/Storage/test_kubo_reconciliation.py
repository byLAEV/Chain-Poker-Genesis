from pathlib import Path
from tempfile import TemporaryDirectory
import sys
BASE=Path(__file__).resolve().parents[2]/"Storage"; sys.path += [str(BASE), str(BASE/"Kubo")]
from storage_manager import StorageManager
from kubo_reconciliation_manager import KuboReconciliationManager

class Healthy:
    def require_healthy(self): return {"health_state":"HEALTHY","peer_id":"peer","version":"0.43.1"}
    def check(self): return self.require_healthy()

def make():
    from test_storage_complete import FakeKubo
    with TemporaryDirectory() as root:
        m=StorageManager(root,kubo=FakeKubo())
        yield m

def test_reconcile_coherent():
    for m in make():
        m.put("public","a",b"hello",mirror=True)
        r=KuboReconciliationManager(m,Healthy()).reconcile()
        assert r["state"]=="COHERENT"
        assert r["objects_coherent"]==1

def test_reconcile_recovers_missing_local():
    for m in make():
        m.put("public","a",b"hello",mirror=True)
        m.engine.delete_local("public","a")
        r=KuboReconciliationManager(m,Healthy()).reconcile()
        assert r["objects_repaired"]==1
        assert m.engine.exists_local("public","a")

def test_reconcile_does_not_blindly_overwrite_divergence():
    for m in make():
        m.put("public","a",b"hello",mirror=True)
        entry=m.registry.get("a")
        m.engine.local.put("public","a",b"local-different")
        m.engine.kubo.objects[entry["cid"]]=b"remote-different"
        r=KuboReconciliationManager(m,Healthy()).reconcile()
        assert r["objects_conflict"]==1
        assert m.engine.get_local("public","a")[0]==b"local-different"
