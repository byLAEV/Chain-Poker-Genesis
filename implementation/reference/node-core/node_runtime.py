#!/usr/bin/env python3
"""Node Core runtime lifecycle orchestration and readiness evaluation."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from storage_provider import LocalStorageProvider
from runtime_state import Readiness, Runtime, RuntimeState

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

    if manifest.get("root") != "node-storage":
        return False
    if manifest.get("required_paths") != REQUIRED_PATHS:
        return False

    required_metadata = (
        "node-storage/identity/node-identity.json",
        "node-storage/configuration/node-config.json",
        "node-storage/recovery/recovery.json",
    )
    return all((root / relative).is_file() for relative in required_metadata)


def evaluate_readiness(root: Path) -> Readiness:
    identity = _load_json(root / "node-storage/identity/node-identity.json")
    config = _load_json(root / "node-storage/configuration/node-config.json")
    recovery = _load_json(root / "node-storage/recovery/recovery.json")

    provider_ready = evaluate_provider(root)
    coherence_coherent = evaluate_coherence(root)

    return Readiness(
        identity_ready=identity.get("identity_status") == "INITIALIZED",
        configuration_ready=(
            config.get("node_core_version") is not None
            and config.get("protocol_associations") == []
            and config.get("cpg_protocol") == "NOT_INSTALLED"
        ),
        storage_ready=(root / "node-storage").is_dir(),
        provider_ready=provider_ready,
        coherence_coherent=coherence_coherent,
        recovery_ready=recovery.get("status") == "READY",
        protocol_associations_empty=config.get("protocol_associations") == [],
        cpg_not_installed=config.get("cpg_protocol") == "NOT_INSTALLED",
    )


def initialize_and_verify(root: Path) -> Runtime:
    runtime = Runtime()
    runtime.transition(RuntimeState.INITIALIZING)
    runtime.transition(RuntimeState.VERIFYING)
    runtime.transition(RuntimeState.READY, evaluate_readiness(root))
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
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("status = FAILED")
        print(f"reason = {exc}")
        return 1

    for key, value in runtime.snapshot().items():
        print(f"{key} = {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
