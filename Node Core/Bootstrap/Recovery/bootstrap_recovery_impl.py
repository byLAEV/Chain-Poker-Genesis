#!/usr/bin/env python3
"""Idempotent recovery for incomplete Node Core bootstrap."""
from __future__ import annotations
from pathlib import Path
import sys
BASE=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(BASE/"Initialization")); sys.path.insert(0,str(BASE/"Verification"))
from node_initializer import initialize,atomic_write_json,sha256_file,ARTIFACTS,REQUIRED_DIRECTORIES,write_integrity_manifest
from bootstrap_verifier import verify

def recover(target: Path,node_core_version: str="1.0.0"):
    target=Path(target).resolve()
    for relative in REQUIRED_DIRECTORIES: (target/relative).mkdir(parents=True,exist_ok=True)
    config=target/ARTIFACTS[0]; state=target/ARTIFACTS[1]
    if not config.exists() or not state.exists():
        initialize(target,node_core_version)
    payload={"state":"RECOVERY_READY","node_core_version":node_core_version}
    atomic_write_json(state,payload)
    write_integrity_manifest(target)
    verify(target)
    return payload