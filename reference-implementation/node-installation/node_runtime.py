#!/usr/bin/env python3
"""Node Core runtime lifecycle orchestration and readiness evaluation."""

from __future__ import annotations
import json
import sys
from pathlib import Path
from runtime_state import Readiness, Runtime, RuntimeState


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate_readiness(root: Path) -> Readiness:
    identity = _load_json(root / "node-storage/identity/node-identity.json")
    config = _load_json(root / "node-storage/configuration/node-config.json")
    recovery = _load_json(root / "node-storage/recovery/recovery.json")
    return Readiness(
        identity_ready=identity.get("identity_status") == "INITIALIZED",
        configuration_ready=(
            config.get("node_core_version") is not None
            and config.get("protocol_associations") == []
            and config.get("cpg_protocol") == "NOT_INSTALLED"
        ),
        storage_ready=(root / "node-storage").is_dir(),
        provider_ready=True,
        coherence_coherent=True,
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
    runtime = initialize_and_verify(root)
    for key, value in runtime.snapshot().items():
        print(f"{key} = {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
