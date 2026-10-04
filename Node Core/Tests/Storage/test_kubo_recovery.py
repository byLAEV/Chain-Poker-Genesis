from pathlib import Path
from tempfile import TemporaryDirectory
import sys
BASE=Path(__file__).resolve().parents[2]/"Storage"; sys.path += [str(BASE),str(BASE/"Kubo")]
from kubo_recovery_manager import KuboRecoveryManager

class Process:
    def __init__(self): self.running=False
    def is_running(self): return self.running
    def start(self, executable, *, version): self.running=True

class Health:
    def __init__(self, ok=True): self.ok=ok
    def check(self): return {"health_state":"HEALTHY"} if self.ok else {"health_state":"UNHEALTHY","reason":"offline"}
    def require_healthy(self):
        if not self.ok: raise RuntimeError("offline")
        return {"health_state":"HEALTHY","peer_id":"peer","version":"0.43.1"}

class State:
    def __init__(self): self.events=[]
    def transition(self, **kwargs): self.events.append(kwargs)

class Recon:
    def reconcile(self): return {"state":"COHERENT"}

class Coh:
    def verify_all(self): return {"dual_storage_ready":True}

def test_recovery_restarts_then_reconciles_before_ready():
    p=Process(); s=State()
    r=KuboRecoveryManager(p,Health(),object(),Coh(),Recon(),s).recover("/bin/ipfs",version="0.43.1")
    assert r["provider_state"]=="READY"
    assert any(e.get("lifecycle_state")=="STARTING" for e in s.events)
    assert any(e.get("lifecycle_state")=="READY" for e in s.events)

def test_observe_degraded_allows_local_fallback():
    s=State()
    result=KuboRecoveryManager(Process(),Health(ok=False),object(),Coh(),Recon(),s).observe()
    assert result["provider_state"]=="DEGRADED"
    assert result["local_fallback"] is True
    assert any(e.get("lifecycle_state")=="DEGRADED" for e in s.events)

def test_conflict_does_not_restore_ready():
    class BadRecon:
        def reconcile(self): return {"state":"CONFLICT"}
    try:
        KuboRecoveryManager(Process(),Health(),object(),Coh(),BadRecon(),State()).recover("/bin/ipfs",version="0.43.1")
    except RuntimeError: pass
    else: raise AssertionError("conflict allowed READY")
