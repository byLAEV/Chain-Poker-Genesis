from pathlib import Path
import sys
BASE=Path(__file__).resolve().parents[2]/"Runtime"; sys.path.insert(0,str(BASE))
from runtime_manager import RuntimeManager
from State.runtime_state import RuntimeState

class Unhealthy:
    def check(self): return {"health_state":"UNHEALTHY","reason":"kubo offline"}

def test_running_node_degrades_without_stopping_local_runtime():
    manager=RuntimeManager(Path.cwd())
    manager.runtime.state=RuntimeState.RUNNING
    result=manager.observe_storage_provider(Unhealthy())
    assert result["provider_state"]=="DEGRADED"
    assert result["local_fallback"] is True
    assert manager.runtime.state==RuntimeState.DEGRADED
