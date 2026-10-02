#!/usr/bin/env python3
"""Verify a protocol-neutral Node Core installation."""

from __future__ import annotations

import json
import sys
from pathlib import Path

MANIFEST = "node-installation-manifest.json"

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

def fail(message: str) -> int:
    print(f"status = FAILED")
    print(f"reason = {message}")
    return 1

def main() -> int:
    if len(sys.argv) != 2:
        return fail("usage: verify_node_installation.py <node-directory>")

    root = Path(sys.argv[1]).resolve()
    manifest_path = root / MANIFEST

    if not root.is_dir():
        return fail("node directory missing")
    if not manifest_path.is_file():
        return fail("installation manifest missing")

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return fail(f"invalid manifest: {exc}")

    for relative in REQUIRED_PATHS:
        if not (root / relative).is_dir():
            return fail(f"required path missing: {relative}")

    if manifest.get("readiness", {}).get("state") != "NODE_CORE_READY":
        return fail("node is not NODE_CORE_READY")

    if manifest.get("protocol_associations") != []:
        return fail("protocol association list is not empty")

    if manifest.get("cpg_protocol", {}).get("status") != "NOT_INSTALLED":
        return fail("CPG protocol isolation invariant failed")

    storage_manifest_path = root / "node-storage/state/storage-manifest.json"
    if not storage_manifest_path.is_file():
        return fail("storage manifest missing")
    try:
        storage_manifest = json.loads(storage_manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return fail(f"invalid storage manifest: {exc}")
    if storage_manifest.get("root") != "node-storage":
        return fail("invalid storage manifest root")
    if storage_manifest.get("required_paths") != REQUIRED_PATHS:
        return fail("storage manifest required paths mismatch")

    if manifest.get("cpg_protocol", {}).get("status") != "NOT_INSTALLED":
        return fail("CPG protocol isolation invariant failed")

    if manifest.get("integrity", {}).get("status") != "VERIFIED":
        return fail("integrity status is not VERIFIED")

    if manifest.get("recovery", {}).get("status") != "READY":
        return fail("recovery status is not READY")

    identity_path = root / "node-storage/identity/node-identity.json"
    config_path = root / "node-storage/configuration/node-config.json"
    recovery_path = root / "node-storage/recovery/recovery.json"
    for path in (identity_path, config_path, recovery_path):
        if not path.is_file():
            return fail(f"required metadata missing: {path.relative_to(root)}")
    try:
        identity = json.loads(identity_path.read_text(encoding="utf-8"))
        config = json.loads(config_path.read_text(encoding="utf-8"))
        recovery = json.loads(recovery_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return fail(f"invalid node metadata: {exc}")
    if identity.get("identity_status") != "INITIALIZED":
        return fail("identity is not initialized")
    if config.get("protocol_associations") != []:
        return fail("node configuration contains protocol associations")
    if config.get("cpg_protocol") != "NOT_INSTALLED":
        return fail("node configuration activates CPG")
    if recovery.get("status") != "READY":
        return fail("recovery metadata is not READY")

    print("status = VERIFIED")
    print("node_status = NODE_CORE_READY")
    print("cpg_protocol = NOT_INSTALLED")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
