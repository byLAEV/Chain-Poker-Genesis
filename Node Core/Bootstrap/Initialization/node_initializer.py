#!/usr/bin/env python3
"""Initialize a fresh, protocol-neutral Node Core installation."""
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone

REQUIRED_DIRECTORIES = ("node-storage","node-storage/configuration","node-storage/state","node-storage/recovery")

class InitializationError(Exception): pass

def initialize(target: Path, node_core_version: str = "1.0.0"):
    target = Path(target).resolve()
    target.mkdir(parents=True, exist_ok=True)
    for relative in REQUIRED_DIRECTORIES:
        (target / relative).mkdir(parents=True, exist_ok=True)
    config = target / "node-storage/configuration/node-config.json"
    state = target / "node-storage/state/node-state.json"
    if not config.exists():
        config.write_text(json.dumps({"node_core_version":node_core_version,"installation_state":"INITIALIZED","protocol_associations":[]},indent=2,sort_keys=True)+"\n",encoding="utf-8")
    if not state.exists():
        state.write_text(json.dumps({"state":"INITIALIZED","initialized_at":datetime.now(timezone.utc).isoformat()},indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return {"state":"INITIALIZED","target":str(target)}
