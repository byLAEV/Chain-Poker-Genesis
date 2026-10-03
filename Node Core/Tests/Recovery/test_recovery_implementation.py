#!/usr/bin/env python3
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
BASE=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(BASE))
from Recovery.recovery_manager import RecoveryManager

def main():
    with TemporaryDirectory() as d:
        root=Path(d); s=root/"node-storage"
        (s/"configuration").mkdir(parents=True); (s/"state").mkdir(); (s/"recovery").mkdir()
        (s/"configuration/node-config.json").write_text("{}")
        (s/"state/node-state.json").write_text("{}")
        result=RecoveryManager(root).recover()
        assert result["status"]=="RECOVERY_READY"
        assert (s/"recovery/node-recovery-state.json").exists()
    with TemporaryDirectory() as d:
        result=RecoveryManager(Path(d)).recover()
        assert result["status"]=="RECOVERY_FAILED"
    print("Node Core Recovery implementation tests: PASS")
if __name__=="__main__": main()
