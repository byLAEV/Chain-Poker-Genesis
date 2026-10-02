#!/usr/bin/env python3
"""End-to-end Node Core installation validation."""

from __future__ import annotations
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from health_readiness import evaluate_health
from node_runtime import evaluate_readiness, initialize_and_verify
from recovery_manager import RecoveryManager
from runtime_state import RuntimeState

def run(command: list[str]) -> None:
    subprocess.run(command, check=True)

def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "node"
        run([sys.executable, "bootstrap_node.py", str(root)])
        run([sys.executable, "verify_node_installation.py", str(root)])
        run([sys.executable, "verify_storage_coherence.py", str(root)])

        runtime = initialize_and_verify(root)
        assert runtime.state == RuntimeState.READY

        health = evaluate_health(root)
        assert health.healthy and health.ready

        readiness = evaluate_readiness(root)
        runtime.transition(RuntimeState.RUNNING, readiness)
        runtime.transition(RuntimeState.DEGRADED)
        RecoveryManager(root).recover(runtime)
        assert runtime.state == RuntimeState.READY

        manifest = json.loads((root / "node-installation-manifest.json").read_text(encoding="utf-8"))
        config = json.loads((root / "node-storage/configuration/node-config.json").read_text(encoding="utf-8"))
        assert manifest["protocol_associations"] == []
        assert manifest["cpg_protocol"]["status"] == "NOT_INSTALLED"
        assert config["protocol_associations"] == []
        assert config["cpg_protocol"] == "NOT_INSTALLED"

        print("e2e_status = PASS")
        print("node_core = READY")
        print("health = HEALTHY")
        print("recovery = VERIFIED")
        print("cpg_protocol = NOT_INSTALLED")
        return 0

if __name__ == "__main__":
    raise SystemExit(main())
