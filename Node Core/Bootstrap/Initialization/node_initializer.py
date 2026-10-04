#!/usr/bin/env python3
"""Initialize a fresh, protocol-neutral Node Core installation."""
from __future__ import annotations
import hashlib, json, os, tempfile
from pathlib import Path
from datetime import datetime, timezone

REQUIRED_DIRECTORIES=("node-storage","node-storage/configuration","node-storage/state","node-storage/recovery")
ARTIFACTS=("node-storage/configuration/node-config.json","node-storage/state/node-state.json")

class InitializationError(Exception): pass

def sha256_file(path: Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
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
    target=Path(target).resolve(); target.mkdir(parents=True,exist_ok=True)
    for relative in REQUIRED_DIRECTORIES: (target/relative).mkdir(parents=True,exist_ok=True)
    config=target/ARTIFACTS[0]; state=target/ARTIFACTS[1]
    if not config.exists():
        atomic_write_json(config,{"node_core_version":node_core_version,"installation_state":"INITIALIZED","protocol_associations":[]})
    if not state.exists():
        atomic_write_json(state,{"state":"INITIALIZED","initialized_at":datetime.now(timezone.utc).isoformat()})
    manifest=write_integrity_manifest(target)
    return {"state":"INITIALIZED","target":str(target),"integrity":manifest}