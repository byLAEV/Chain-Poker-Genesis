from pathlib import Path
from tempfile import TemporaryDirectory
import sys
BASE=Path(__file__).resolve().parents[2]/"Storage"/"Kubo";sys.path.insert(0,str(BASE))
from kubo_process_manager import KuboProcessManager,KuboProcessError
from kubo_health_manager import KuboHealthManager

def test_process_stale_pid_cleared():
    with TemporaryDirectory() as root:
        from kubo_paths import KuboPathManager
        paths=KuboPathManager(root).paths("v0.43.1")
        paths.runtime.mkdir(parents=True)
        (paths.runtime/"kubo.pid").write_text("999999999\n")
        assert KuboProcessManager(paths).is_running() is False
        assert not (paths.runtime/"kubo.pid").exists()

def test_process_requires_repository():
    with TemporaryDirectory() as root:
        from kubo_paths import KuboPathManager
        paths=KuboPathManager(root).paths("v0.43.1")
        try: KuboProcessManager(paths).start("/bin/sh",version="v0.43.1")
        except KuboProcessError: pass
        else: raise AssertionError("daemon start allowed without repository")

def test_health_success(monkeypatch):
    manager=KuboHealthManager()
    responses={"/api/v0/id":{"ID":"peer-test"},"/api/v0/version":{"Version":"0.43.1"}}
    monkeypatch.setattr(manager,"_post",lambda path:responses[path])
    result=manager.require_healthy()
    assert result["health_state"]=="HEALTHY"
    assert result["peer_id"]=="peer-test"
