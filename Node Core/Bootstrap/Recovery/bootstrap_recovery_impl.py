#!/usr/bin/env python3
"""Idempotent, fail-closed recovery for incomplete Node Core bootstrap."""
from __future__ import annotations
from pathlib import Path
import json
import sys

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "Initialization"))
sys.path.insert(0, str(BASE / "Verification"))

from node_initializer import initialize, atomic_write_json, write_integrity_manifest
from bootstrap_verifier import verify


def recover(target: Path, node_core_version: str = "1.0.0"):
    target = Path(target).resolve()
    manifest = target / "node-installation-manifest.json"

    # A missing installation may be safely rebuilt. An existing but malformed
    # manifest is corruption and must fail closed without rewriting evidence.
    if not target.exists():
        initialize(target, node_core_version)
    elif not manifest.exists():
        initialize(target, node_core_version)
    else:
        try:
            json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(
                "bootstrap recovery refused: existing installation manifest is corrupt"
            ) from exc

    atomic_write_json(target / "node-storage/state/node-state.json", {
        "state": "NODE_CORE_READY",
        "recovered": True
    })
    atomic_write_json(target / "node-storage/recovery/recovery.json", {
        "status": "READY",
        "format_version": "1.0.0",
        "last_operation": "RECOVERY"
    })

    data = json.loads(manifest.read_text(encoding="utf-8"))
    data["recovery"] = {"status": "READY"}
    data["integrity"] = {"status": "VERIFIED"}
    atomic_write_json(manifest, data)

    write_integrity_manifest(target)
    verify(target)
    return {"state": "RECOVERY_READY"}
