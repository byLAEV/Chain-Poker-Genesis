#!/usr/bin/env python3
"""Verify Node Core bootstrap invariants and artifact integrity."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
class BootstrapVerificationError(Exception): pass
REQUIRED=("node-storage","node-storage/configuration","node-storage/state","node-storage/recovery")
ARTIFACTS=("node-storage/configuration/node-config.json","node-storage/state/node-state.json")

def sha256_file(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def verify(target: Path):
    target=Path(target).resolve()
    missing=[p for p in REQUIRED if not (target/p).is_dir()]
    if missing: raise BootstrapVerificationError("missing bootstrap paths: "+", ".join(missing))
    try:
        config=json.loads((target/ARTIFACTS[0]).read_text(encoding="utf-8"))
        state=json.loads((target/ARTIFACTS[1]).read_text(encoding="utf-8"))
        integrity=json.loads((target/"node-storage/state/bootstrap-integrity.json").read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as exc:
        raise BootstrapVerificationError("bootstrap metadata is invalid") from exc
    if not config.get("node_core_version"): raise BootstrapVerificationError("node_core_version is missing")
    if state.get("state") not in {"INITIALIZED","READY","RECOVERY_READY"}: raise BootstrapVerificationError("invalid bootstrap state")
    if integrity.get("algorithm")!="SHA-256": raise BootstrapVerificationError("unsupported integrity algorithm")
    expected=integrity.get("artifacts",{})
    for relative in ARTIFACTS:
        if expected.get(relative)!=sha256_file(target/relative):
            raise BootstrapVerificationError(f"bootstrap artifact integrity failure: {relative}")
    return {"status":"VERIFIED","state":state["state"],"integrity":"VERIFIED"}