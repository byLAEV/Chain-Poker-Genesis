#!/usr/bin/env python3
"""Recover incomplete Node Core bootstrap."""
from __future__ import annotations
import json
from pathlib import Path

def recover(target: Path, node_core_version: str = "1.0.0"):
    target=Path(target).resolve()
    for relative in ("node-storage","node-storage/configuration","node-storage/state","node-storage/recovery"):
        (target/relative).mkdir(parents=True,exist_ok=True)
    state=target/"node-storage/state/node-state.json"
    payload={"state":"RECOVERY_READY","node_core_version":node_core_version}
    state.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return payload
