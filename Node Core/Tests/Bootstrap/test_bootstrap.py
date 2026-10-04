#!/usr/bin/env python3
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import json

BASE=Path(__file__).resolve().parents[2]/"Bootstrap"
sys.path.insert(0,str(BASE))
sys.path.insert(0,str(BASE/"Installer"))
from bootstrap import Bootstrap
from Installer.bootstrap_node import BootstrapInstallationError, install
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

    missing_root=p/"missing-path-check"
    b.bootstrap(missing_root)
    (missing_root/"node-storage/recovery").rmdir()
    try: b.verify(missing_root)
    except BootstrapVerificationError: pass
    else: raise AssertionError("missing required bootstrap path was accepted")

    malformed_root=p/"malformed-metadata-check"
    b.bootstrap(malformed_root)
    malformed_cfg=malformed_root/"node-storage/configuration/node-config.json"
    malformed_cfg.write_text("{not-json",encoding="utf-8")
    try: b.verify(malformed_root)
    except BootstrapVerificationError: pass
    else: raise AssertionError("malformed bootstrap metadata was accepted")

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

with TemporaryDirectory() as root:
    target=Path(root)/"installer"
    result=install(target)
    assert result["status"]=="VERIFIED"
    assert result["environment"]["status"]=="VALIDATED"
    assert result["existing_installation"]["status"]=="NO_EXISTING_INSTALLATION"
    assert result["node_status"]=="NODE_CORE_READY"
    assert result["cpg_protocol"]=="NOT_INSTALLED"
    assert result["protocol_associations"]==[]

    repeat=install(target)
    assert repeat["status"]=="VERIFIED"
    assert repeat["existing_installation"]["status"]=="VALID_EXISTING_INSTALLATION"

    conflict=Path(root)/"conflict"
    conflict.mkdir()
    (conflict/"node-installation-manifest.json").write_text(json.dumps({
        "node":{"status":"BROKEN"},
        "readiness":{"state":"FAILED"},
        "protocol_associations":["example.protocol"],
        "cpg_protocol":{"status":"NOT_INSTALLED"}
    }),encoding="utf-8")
    try:
        install(conflict)
    except BootstrapInstallationError: pass
    else: raise AssertionError("conflicting installation was overwritten")

print("Node Core Bootstrap integration and installer contract tests: PASS")
