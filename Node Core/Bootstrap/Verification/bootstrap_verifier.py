#!/usr/bin/env python3
"""Verify Node Core bootstrap invariants."""
from __future__ import annotations
import json
from pathlib import Path

class BootstrapVerificationError(Exception): pass
REQUIRED=("node-storage","node-storage/configuration","node-storage/state","node-storage/recovery")

def verify(target: Path):
    target=Path(target).resolve()
    missing=[p for p in REQUIRED if not (target/p).exists()]
    if missing: raise BootstrapVerificationError("missing bootstrap paths: "+", ".join(missing))
    try:
        config=json.loads((target/"node-storage/configuration/node-config.json").read_text(encoding="utf-8"))
        state=json.loads((target/"node-storage/state/node-state.json").read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as exc:
        raise BootstrapVerificationError("bootstrap metadata is invalid") from exc
    if not config.get("node_core_version"): raise BootstrapVerificationError("node_core_version is missing")
    if state.get("state") not in {"INITIALIZED","READY","RECOVERY_READY"}:
        raise BootstrapVerificationError("invalid bootstrap state")
    return {"status":"VERIFIED","state":state["state"]}
