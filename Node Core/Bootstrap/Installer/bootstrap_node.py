#!/usr/bin/env python3
"""Fixed Node Core Bootstrap installer.

The installer is a fixed substrate boundary. It performs an explicit
environment preflight, rejects conflicting existing installations, then
initializes and verifies the Node Core without installing protocols.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

BASE=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(BASE/"Initialization"))
sys.path.insert(0,str(BASE/"Verification"))
from node_initializer import initialize
from bootstrap_verifier import verify


class BootstrapInstallationError(RuntimeError):
    pass


def validate_environment(target: Path) -> dict:
    target=Path(target).resolve()
    if sys.version_info < (3, 9):
        raise BootstrapInstallationError("Python 3.9 or newer is required")
    if target.exists() and not target.is_dir():
        raise BootstrapInstallationError("installation target exists and is not a directory")
    probe = target if target.exists() else target.parent
    if not probe.exists() or not probe.is_dir():
        raise BootstrapInstallationError("installation target parent does not exist")
    if not os.access(probe, os.R_OK | os.W_OK | os.X_OK):
        raise BootstrapInstallationError("installation target is not accessible for read/write")
    if target.exists() and not os.access(target, os.R_OK | os.W_OK | os.X_OK):
        raise BootstrapInstallationError("installation target is not accessible for read/write")
    return {
        "status": "VALIDATED",
        "python": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "target": str(target),
    }


def preflight_existing_installation(target: Path) -> dict:
    target=Path(target).resolve()
    manifest=target/"node-installation-manifest.json"
    if not manifest.exists():
        return {"status":"NO_EXISTING_INSTALLATION"}
    try:
        data=json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BootstrapInstallationError(
            "existing installation manifest is invalid; refusing to overwrite"
        ) from exc
    if (
        data.get("node",{}).get("status")=="READY"
        and data.get("readiness",{}).get("state")=="NODE_CORE_READY"
        and data.get("protocol_associations")==[]
        and data.get("cpg_protocol",{}).get("status")=="NOT_INSTALLED"
    ):
        return {"status":"VALID_EXISTING_INSTALLATION"}
    raise BootstrapInstallationError(
        "conflicting or non-canonical existing Node Core installation; refusing to overwrite"
    )


def install(target):
    target=Path(target).resolve()
    environment=validate_environment(target)
    existing=preflight_existing_installation(target)
    result=initialize(target)
    verification=verify(target)
    return {
        "status":"VERIFIED",
        "environment":environment,
        "existing_installation":existing,
        "installation":result,
        "verification":verification,
        "node_status":verification["state"],
        "cpg_protocol": "NOT_INSTALLED",
        "protocol_associations": [],
    }


if __name__=="__main__":
    if len(sys.argv)!=2:
        raise SystemExit("usage: bootstrap_node.py <target-directory>")
    try:
        result=install(sys.argv[1])
    except BootstrapInstallationError as exc:
        print(json.dumps({
            "status":"FAILED",
            "error":{"type":"BOOTSTRAP_INSTALLATION_ERROR","message":str(exc)}
        },sort_keys=True))
        raise SystemExit(1)
    print(json.dumps(result,sort_keys=True))
