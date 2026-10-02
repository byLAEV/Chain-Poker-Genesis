#!/usr/bin/env python3
"""Bootstrap a protocol-neutral Chain Poker Genesis Node Core."""

from __future__ import annotations

import json
import sys
from pathlib import Path

MANIFEST_VERSION = "0.1.0"
NODE_CORE_VERSION = "0.1.0"
STORAGE_STRUCTURE_VERSION = "0.1.0"
STORAGE_MANIFEST_VERSION = "0.1.0"

REQUIRED_PATHS = [
    "node-storage",
    "node-storage/identity",
    "node-storage/cryptography",
    "node-storage/configuration",
    "node-storage/state",
    "node-storage/records",
    "node-storage/recovery",
    "node-storage/protocol",
]

def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")

def main() -> int:
    if len(sys.argv) != 2:
        fail("usage: bootstrap_node.py <target-directory>")

    target = Path(sys.argv[1]).resolve()
    target.mkdir(parents=True, exist_ok=False)

    for relative in REQUIRED_PATHS:
        (target / relative).mkdir(parents=True, exist_ok=False)

    (target / "node-storage/identity/node-identity.json").write_text(
        json.dumps(
            {
                "identity_status": "INITIALIZED",
                "identity_class": "REFERENCE_NODE_IDENTITY",
                "node_id": "NODE-REFERENCE-0001",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    (target / "node-storage/configuration/node-config.json").write_text(
        json.dumps(
            {
                "node_core_version": NODE_CORE_VERSION,
                "decentralized_storage": {
                    "status": "NOT_PROVISIONED"
                },
                "protocol_associations": [],
                "cpg_protocol": "NOT_INSTALLED",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    (target / "node-storage/state/node-state.json").write_text(
        json.dumps(
            {
                "state": "RECOVERY_READY",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    (target / "node-storage/recovery/recovery.json").write_text(
        json.dumps(
            {
                "status": "READY",
                "format_version": "0.1.0",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    storage_manifest = {
        "storage_structure_version": STORAGE_STRUCTURE_VERSION,
        "root": "node-storage",
        "required_paths": REQUIRED_PATHS,
    }

    (target / "node-storage/state/storage-manifest.json").write_text(
        json.dumps(storage_manifest, indent=2, sort_keys=True) + "\\n",
        encoding="utf-8",
    )

    manifest = {
        "manifest_version": MANIFEST_VERSION,
        "node": {
            "node_core_version": NODE_CORE_VERSION,
            "identity_status": "INITIALIZED",
        },
        "storage": {
            "storage_structure_version": STORAGE_STRUCTURE_VERSION,
            "required_paths": REQUIRED_PATHS,
            "storage_manifest_version": STORAGE_MANIFEST_VERSION,
        },
        "readiness": {
            "state": "NODE_CORE_READY",
        },
        "protocol_associations": [],
        "cpg_protocol": {
            "status": "NOT_INSTALLED",
        },
        "integrity": {
            "status": "VERIFIED",
        },
        "recovery": {
            "status": "READY",
        },
    }

    (target / "node-installation-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print("status = BOOTSTRAPPED")
    print("node_status = NODE_CORE_READY")
    print("cpg_protocol = NOT_INSTALLED")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
