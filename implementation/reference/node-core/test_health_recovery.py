#!/usr/bin/env python3
"""Tests for health/readiness and recovery integration."""

from __future__ import annotations
import subprocess
import sys
import tempfile
from pathlib import Path
from health_readiness import evaluate_health
from node_runtime import evaluate_readiness
from recovery_manager import RecoveryManager
from runtime_state import Runtime, RuntimeState

def bootstrap(root: Path) -> None:
    subprocess.run([sys.executable, "bootstrap_node.py", str(root)], check=True)

def test_health_ready() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "node"
        bootstrap(root)
        report = evaluate_health(root)
        assert report.healthy and report.ready
        assert report.cpg_protocol == "NOT_INSTALLED"

def test_health_detects_configuration_failure() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "node"
        bootstrap(root)
        config = root / "node-storage/configuration/node-config.json"
        config.write_text(
            '{"node_core_version":"0.1.0","protocol_associations":["chain-poker-genesis"],"cpg_protocol":"NOT_INSTALLED"}\n',
            encoding="utf-8",
        )
        report = evaluate_health(root)
        assert not report.healthy
        assert not report.ready

def test_recovery_returns_to_ready() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "node"
        bootstrap(root)
        readiness = evaluate_readiness(root)
        runtime = Runtime()
        runtime.transition(RuntimeState.INITIALIZING)
        runtime.transition(RuntimeState.VERIFYING)
        runtime.transition(RuntimeState.READY, readiness)
        runtime.transition(RuntimeState.RUNNING, readiness)
        runtime.transition(RuntimeState.DEGRADED)
        RecoveryManager(root).recover(runtime)
        assert runtime.state == RuntimeState.READY
        assert runtime.health == "HEALTHY"

if __name__ == "__main__":
    test_health_ready()
    test_health_detects_configuration_failure()
    test_recovery_returns_to_ready()
    print("health/recovery tests: PASS")
