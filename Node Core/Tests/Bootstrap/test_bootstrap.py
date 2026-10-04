#!/usr/bin/env python3
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
BASE=Path(__file__).resolve().parents[2]/"Bootstrap"; sys.path.insert(0,str(BASE))
from bootstrap import Bootstrap
from Verification.bootstrap_verifier import BootstrapVerificationError

with TemporaryDirectory() as root:
    b=Bootstrap(); p=Path(root)
    result=b.bootstrap(root)
    assert result["verification"]["integrity"]=="VERIFIED"
    assert (p/"node-storage/state/bootstrap-integrity.json").exists()
    original=(p/"node-storage/configuration/node-config.json").read_bytes()
    b.initialize(root)
    assert (p/"node-storage/configuration/node-config.json").read_bytes()==original
    recovery_target=p/"recovery-target"
    assert b.recover(recovery_target)["state"]=="RECOVERY_READY"
    assert b.recover(recovery_target)["state"]=="RECOVERY_READY"
    cfg=p/"node-storage/configuration/node-config.json"
    cfg.write_text(cfg.read_text(encoding="utf-8")+"corruption",encoding="utf-8")
    try: b.verify(root)
    except BootstrapVerificationError: pass
    else: raise AssertionError("corrupted bootstrap artifact was accepted")
print("Node Core Bootstrap integration tests: PASS")