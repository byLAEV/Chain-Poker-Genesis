#!/usr/bin/env python3
"""Node Core runtime lifecycle orchestration and readiness evaluation."""

from __future__ import annotations

import json
import sys
from pathlib import Path

_RUNTIME_DIR = Path(__file__).resolve().parent
_STORAGE_DIR = _RUNTIME_DIR.parent / "Storage"
sys.path.insert(0, str(_RUNTIME_DIR))
sys.path.insert(0, str(_RUNTIME_DIR / "State"))
sys.path.insert(0, str(_STORAGE_DIR / "Providers"))
sys.path.insert(0, str(_STORAGE_DIR / "Storage Manager"))

from storage_provider import LocalStorageProvider
from runtime_state import Readiness, Runtime, RuntimeState
sys.path.insert(0, str(_RUNTIME_DIR.parent / "Configuration"))
from configuration_manager import ConfigurationError, validate_configuration

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


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate_provider(root: Path) -> bool:
    try:
        return LocalStorageProvider(root).status().get("status") == "READY"
    except (OSError, ValueError):
        return False


def evaluate_coherence(root: Path) -> bool:
    if not root.is_dir():
        return False
    for relative in REQUIRED_PATHS:
        if not (root / relative).is_dir():
            return False
    manifest_path = root / "node-storage/state/storage-manifest.json"
    if not manifest_path.is_file():
        return False
    try:
        manifest = _load_json(manifest_path)
    except (OSError, json.JSONDecodeError):
        return False
    return (
        manifest.get("root") == "node-storage"
        and manifest.get("required_paths") == REQUIRED_PATHS
        and all((root / p).is_file() for p in (
            "node-storage/identity/node-identity.json",
            "node-storage/configuration/node-config.json",
            "node-storage/recovery/recovery.json",
        ))
    )


def evaluate_readiness(root: Path) -> Readiness:
    identity = _load_json(root / "node-storage/identity/node-identity.json")
    config = _load_json(root / "node-storage/configuration/node-config.json")
    recovery = _load_json(root / "node-storage/recovery/recovery.json")
    installation = _load_json(root / "node-installation-manifest.json")
    config=validate_configuration(config, fresh_node=True)
    return Readiness(
        environment_ready=root.is_dir(),
        identity_ready=identity.get("identity_status") == "INITIALIZED",
        storage_ready=(root / "node-storage").is_dir(),
        configuration_ready=all(key in config for key in ("node_core_version", "decentralized_storage", "protocol_associations", "cpg_protocol")),
        structure_ready=evaluate_coherence(root),
        integrity_ready=installation.get("integrity", {}).get("status") == "VERIFIED",
        recovery_ready=recovery.get("status") == "READY",
        provider_ready=evaluate_provider(root),
        coherence_coherent=evaluate_coherence(root),
        protocol_associations_empty=config.get("protocol_associations") == [],
        cpg_not_installed=config.get("cpg_protocol") == "NOT_INSTALLED",
    )


def initialize_and_verify(root: Path) -> Runtime:
    readiness = evaluate_readiness(root)
    runtime = Runtime()
    runtime.transition(RuntimeState.ENVIRONMENT_VALIDATED, readiness)
    runtime.transition(RuntimeState.IDENTITY_INITIALIZED, readiness)
    runtime.transition(RuntimeState.STORAGE_INITIALIZED, readiness)
    runtime.transition(RuntimeState.STORAGE_STRUCTURE_VERIFIED, readiness)
    runtime.transition(RuntimeState.INTEGRITY_VERIFIED, readiness)
    runtime.transition(RuntimeState.RECOVERY_READY, readiness)
    runtime.transition(RuntimeState.NODE_CORE_READY, readiness)
    return runtime


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: node_runtime.py <node-directory>")
        return 2
    root = Path(sys.argv[1]).resolve()
    if not root.is_dir():
        print("status = FAILED")
        print("reason = node directory missing")
        return 1
    try:
        runtime = initialize_and_verify(root)
    except (OSError, ValueError, json.JSONDecodeError, ConfigurationError) as exc:
        print("status = FAILED")
        print(f"reason = {exc}")
        return 1
    for key, value in runtime.snapshot().items():
        print(f"{key} = {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
