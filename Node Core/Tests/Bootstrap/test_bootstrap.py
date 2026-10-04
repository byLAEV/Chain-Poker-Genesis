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

    # Missing required path must fail closed.
    missing_root=p/"missing-path-check"
    b.bootstrap(missing_root)
    (missing_root/"node-storage/recovery").rmdir()
    try: b.verify(missing_root)
    except BootstrapVerificationError: pass
    else: raise AssertionError("missing required bootstrap path was accepted")

    # Malformed required metadata must fail closed.
    malformed_root=p/"malformed-metadata-check"
    b.bootstrap(malformed_root)
    malformed_cfg=malformed_root/"node-storage/configuration/node-config.json"
    malformed_cfg.write_text("{not-json",encoding="utf-8")
    try: b.verify(malformed_root)
    except BootstrapVerificationError: pass
    else: raise AssertionError("malformed bootstrap metadata was accepted")

    # Protocol-isolation violation must fail closed before readiness can be accepted.
    isolation_root=p/"protocol-isolation-check"
    b.bootstrap(isolation_root)
    isolation_cfg=isolation_root/"node-storage/configuration/node-config.json"
    isolation_cfg.write_text(
        isolation_cfg.read_text(encoding="utf-8").replace(
            '"protocol_associations": []',
            '"protocol_associations": ["cpg"]'
        ),
        encoding="utf-8"
    )
    try: b.verify(isolation_root)
    except BootstrapVerificationError: pass
    else: raise AssertionError("protocol isolation violation was accepted")

print("Node Core Bootstrap integration tests: PASS")