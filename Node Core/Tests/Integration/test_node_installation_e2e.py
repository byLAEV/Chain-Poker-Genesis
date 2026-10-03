#!/usr/bin/env python3
"""End-to-end Node Core installation validation."""

from __future__ import annotations
import json
import subprocess
import sys
import tempfile
from pathlib import Path

NODE_CORE = Path(__file__).resolve().parents[2]
BOOTSTRAP = NODE_CORE / "Bootstrap/Installer/bootstrap_node.py"
VERIFY = NODE_CORE / "Tools/Validation/verify_node_installation.py"
COHERENCE = NODE_CORE / "Tools/Validation/verify_storage_coherence.py"
RUNTIME = NODE_CORE / "Runtime"
RECOVERY = NODE_CORE / "Recovery"

sys.path.insert(0, str(RUNTIME))
sys.path.insert(0, str(RECOVERY))

from health_readiness import evaluate_health
from node_runtime import evaluate_readiness, initialize_and_verify
from recovery_manager import RecoveryManager
from runtime_state import RuntimeState, VALID_TRANSITIONS


def run(command: list[str]) -> None:
    subprocess.run(command, check=True, cwd=NODE_CORE)


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "node"
        run([sys.executable, str(BOOTSTRAP), str(root)])
        run([sys.executable, str(VERIFY), str(root)])
        run([sys.executable, str(COHERENCE), str(root)])

        readiness = evaluate_readiness(root)
        runtime = initialize_and_verify(root)
        assert runtime.state == RuntimeState.NODE_CORE_READY
        assert readiness.environment_ready
        assert readiness.identity_ready
        assert readiness.storage_ready
        assert readiness.structure_ready
        assert readiness.integrity_ready
        assert readiness.recovery_ready
        assert readiness.protocol_associations_empty
        assert readiness.cpg_not_installed

        expected = [
            RuntimeState.UNINITIALIZED,
            RuntimeState.ENVIRONMENT_VALIDATED,
            RuntimeState.IDENTITY_INITIALIZED,
            RuntimeState.STORAGE_INITIALIZED,
            RuntimeState.STORAGE_STRUCTURE_VERIFIED,
            RuntimeState.INTEGRITY_VERIFIED,
            RuntimeState.RECOVERY_READY,
            RuntimeState.NODE_CORE_READY,
        ]
        for source, target in zip(expected, expected[1:]):
            assert target in VALID_TRANSITIONS[source]

        health = evaluate_health(root)
        assert health.healthy and health.ready

        runtime.transition(RuntimeState.RUNNING, readiness)
        runtime.transition(RuntimeState.DEGRADED)
        RecoveryManager(root).recover(runtime)
        assert runtime.state == RuntimeState.NODE_CORE_READY
        runtime.transition(RuntimeState.SHUTTING_DOWN)
        runtime.transition(RuntimeState.STOPPED)
        assert runtime.state == RuntimeState.STOPPED

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
