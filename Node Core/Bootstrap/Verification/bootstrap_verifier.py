#!/usr/bin/env python3
"""Verify Node Core bootstrap invariants and artifact integrity."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
class BootstrapVerificationError(Exception): pass
REQUIRED=("node-storage","node-storage/identity","node-storage/cryptography","node-storage/configuration","node-storage/state","node-storage/records","node-storage/recovery","node-storage/protocol")
ARTIFACTS=("node-storage/identity/node-identity.json","node-storage/configuration/node-config.json","node-storage/state/node-state.json","node-storage/recovery/recovery.json","node-storage/state/storage-manifest.json","node-installation-manifest.json")

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
        identity=json.loads((target/ARTIFACTS[0]).read_text(encoding="utf-8"))
        config=json.loads((target/ARTIFACTS[1]).read_text(encoding="utf-8"))
        state=json.loads((target/ARTIFACTS[2]).read_text(encoding="utf-8"))
        recovery=json.loads((target/ARTIFACTS[3]).read_text(encoding="utf-8"))
        storage=json.loads((target/ARTIFACTS[4]).read_text(encoding="utf-8"))
        installation=json.loads((target/ARTIFACTS[5]).read_text(encoding="utf-8"))
        integrity=json.loads((target/"node-storage/state/bootstrap-integrity.json").read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as exc:
        raise BootstrapVerificationError("bootstrap metadata is invalid") from exc
    if identity.get("identity_status")!="INITIALIZED": raise BootstrapVerificationError("identity is not initialized")
    if config.get("protocol_associations")!=[] or config.get("cpg_protocol")!="NOT_INSTALLED": raise BootstrapVerificationError("protocol isolation invariant failed")
    if state.get("state")!="NODE_CORE_READY": raise BootstrapVerificationError("invalid bootstrap state")
    if recovery.get("status")!="READY": raise BootstrapVerificationError("recovery is not ready")
    if storage.get("root")!="node-storage" or storage.get("required_paths")!=list(REQUIRED): raise BootstrapVerificationError("storage structure mismatch")
    if installation.get("node",{}).get("status")!="READY": raise BootstrapVerificationError("installation manifest is not READY")
    if installation.get("readiness",{}).get("state")!="NODE_CORE_READY": raise BootstrapVerificationError("installation readiness mismatch")
    if installation.get("protocol_associations")!=[] or installation.get("cpg_protocol",{}).get("status")!="NOT_INSTALLED": raise BootstrapVerificationError("installation protocol isolation failed")
    if integrity.get("algorithm")!="SHA-256": raise BootstrapVerificationError("unsupported integrity algorithm")
    expected=integrity.get("artifacts",{})
    for relative in ARTIFACTS:
        if expected.get(relative)!=sha256_file(target/relative):
            raise BootstrapVerificationError(f"bootstrap artifact integrity failure: {relative}")
    return {"status":"VERIFIED","state":state["state"],"integrity":"VERIFIED"}
