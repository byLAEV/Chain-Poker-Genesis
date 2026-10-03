#!/usr/bin/env python3
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
BASE=Path(__file__).resolve().parents[2]/"Bootstrap"
sys.path.insert(0,str(BASE))
from bootstrap import Bootstrap

with TemporaryDirectory() as root:
    bootstrap=Bootstrap()
    result=bootstrap.bootstrap(root)
    assert result["verification"]["status"]=="VERIFIED"
    assert (Path(root)/"node-storage/configuration/node-config.json").exists()
    assert (Path(root)/"node-storage/state/node-state.json").exists()
    assert not (Path(root)/"node-storage/identity/node-identity.json").exists()
    recovered=bootstrap.recover(Path(root)/"recovery-target")
    assert recovered["state"]=="RECOVERY_READY"
print("Node Core Bootstrap integration tests: PASS")
