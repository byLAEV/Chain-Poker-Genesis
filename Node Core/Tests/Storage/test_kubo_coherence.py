from pathlib import Path
from tempfile import TemporaryDirectory
import sys
BASE=Path(__file__).resolve().parents[2]/"Storage";sys.path += [str(BASE),str(BASE/"Kubo")]
from kubo_coherence_verifier import KuboCoherenceVerifier,DualStorageReadiness
from storage_manager import StorageManager

class FakeHealth:
    def require_healthy(self): return {"health_state":"HEALTHY","peer_id":"peer","version":"0.43.1"}
    def check(self): return self.require_healthy()

def test_coherence_gate():
    with TemporaryDirectory() as root:
        from test_storage_complete import FakeKubo
        m=StorageManager(root,kubo=FakeKubo())
        m.put("public","coherent",b"hello",mirror=True)
        report=KuboCoherenceVerifier(m,FakeHealth()).verify_all()
        assert report["coherence_state"]=="COHERENT"
        assert report["dual_storage_ready"] is True
        assert DualStorageReadiness().evaluate(report)["state"]=="READY"

def test_coherence_detects_remote_mismatch():
    with TemporaryDirectory() as root:
        from test_storage_complete import FakeKubo
        m=StorageManager(root,kubo=FakeKubo())
        m.put("public","mismatch",b"hello",mirror=True)
        entry=m.registry.get("mismatch")
        # Replace the provider's content with different bytes under the same CID.
        m.engine.kubo.objects[entry["cid"]]=b"tampered"
        report=KuboCoherenceVerifier(m,FakeHealth()).verify_all()
        assert report["dual_storage_ready"] is False
        assert report["objects_failed"]==1

def test_empty_storage_can_be_ready_after_healthy_check():
    with TemporaryDirectory() as root:
        from test_storage_complete import FakeKubo
        m=StorageManager(root,kubo=FakeKubo())
        report=KuboCoherenceVerifier(m,FakeHealth()).verify_all()
        assert report["dual_storage_ready"] is True
