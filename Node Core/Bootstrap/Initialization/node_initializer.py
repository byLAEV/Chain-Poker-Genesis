#!/usr/bin/env python3
"""Fixed Node Core Bootstrap initializer."""
from __future__ import annotations
import hashlib, json, os, tempfile
from pathlib import Path
from datetime import datetime, timezone

REQUIRED_DIRECTORIES=(
    "node-storage","node-storage/identity","node-storage/cryptography",
    "node-storage/configuration","node-storage/state","node-storage/records",
    "node-storage/recovery","node-storage/protocol","node-storage/network"
)
ARTIFACTS=(
    "node-storage/identity/node-identity.json",
    "node-storage/configuration/node-config.json",
    "node-storage/state/node-state.json",
    "node-storage/recovery/recovery.json",
    "node-storage/state/storage-manifest.json",
    "node-storage/network/network-state.json",
    "node-installation-manifest.json",
)
STORAGE_PATHS=list(REQUIRED_DIRECTORIES)

class InitializationError(Exception):
    pass

def sha256_file(path: Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def atomic_write_json(path: Path,payload: dict)->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    data=json.dumps(payload,indent=2,sort_keys=True)+"\n"
    fd,tmp=tempfile.mkstemp(prefix=f".{path.name}.",suffix=".tmp",dir=str(path.parent))
    try:
        with os.fdopen(fd,"w",encoding="utf-8") as f:
            f.write(data); f.flush(); os.fsync(f.fileno())
        os.replace(tmp,path)
        dir_fd=os.open(path.parent,os.O_RDONLY)
        try: os.fsync(dir_fd)
        finally: os.close(dir_fd)
    except Exception:
        try: os.unlink(tmp)
        except FileNotFoundError: pass
        raise

def write_integrity_manifest(target: Path)->dict:
    manifest={"algorithm":"SHA-256","artifacts":{p:sha256_file(target/p) for p in ARTIFACTS}}
    atomic_write_json(target/"node-storage/state/bootstrap-integrity.json",manifest)
    return manifest

def initialize(target: Path,node_core_version: str="1.0.0"):
    target=Path(target).resolve()
    target.mkdir(parents=True,exist_ok=True)
    for relative in REQUIRED_DIRECTORIES:
        (target/relative).mkdir(parents=True,exist_ok=True)

    identity=target/"node-storage/identity/node-identity.json"
    config=target/"node-storage/configuration/node-config.json"
    state=target/"node-storage/state/node-state.json"
    recovery=target/"node-storage/recovery/recovery.json"
    storage=target/"node-storage/state/storage-manifest.json"
    network_state=target/"node-storage/network/network-state.json"
    installation=target/"node-installation-manifest.json"

    if not identity.exists():
        atomic_write_json(identity,{"identity_status":"INITIALIZED","key_material":"EXTERNAL_OR_SEPARATE_CRYPTOGRAPHY"})
    if not config.exists():
        atomic_write_json(config,{
            "node_core_version":node_core_version,
            "decentralized_storage":{"status":"NOT_PROVISIONED"},
            "protocol_associations":[],
            "cpg_protocol":"NOT_INSTALLED",
            "network":{"minimum_protocol_nodes":5}
        })
    if not state.exists():
        atomic_write_json(state,{"state":"NODE_CORE_READY","initialized_at":datetime.now(timezone.utc).isoformat()})
    if not recovery.exists():
        atomic_write_json(recovery,{"status":"READY","format_version":"1.0.0"})
    if not storage.exists():
        atomic_write_json(storage,{
            "root":"node-storage",
            "storage_structure_version":"1.0.0",
            "required_paths":STORAGE_PATHS
        })
    if not network_state.exists():
        atomic_write_json(network_state,{
            "connection_status":"SEARCHING_FOR_CONNECTIONS",
            "connected_nodes":0,
            "minimum_protocol_nodes":5,
            "protocol_readiness":"NOT_READY"
        })
    if not installation.exists():
        atomic_write_json(installation,{
            "manifest_version":"1.1.0",
            "node":{"node_core_version":node_core_version,"status":"READY"},
            "storage":{"storage_structure_version":"1.0.0","required_paths":STORAGE_PATHS,"storage_manifest_version":"1.0.0"},
            "readiness":{"state":"NODE_CORE_READY"},
            "network":{"connection_status":"SEARCHING_FOR_CONNECTIONS","connected_nodes":0,"minimum_protocol_nodes":5,"protocol_readiness":"NOT_READY"},
            "provider":{"type":"LOCAL","status":"READY"},
            "coherence":{"status":"COHERENT"},
            "synchronization":{"state":"NOT_EVALUATED"},
            "recovery":{"status":"READY"},
            "integrity":{"status":"VERIFIED"},
            "protocol_associations":[],
            "cpg_protocol":{"status":"NOT_INSTALLED"}
        })
    integrity=write_integrity_manifest(target)
    return {"state":"NODE_CORE_READY","target":str(target),"integrity":integrity}
