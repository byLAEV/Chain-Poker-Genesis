#!/usr/bin/env python3
"""Tests for the Node Core runtime lifecycle."""

from __future__ import annotations
import subprocess
import sys
import tempfile
from pathlib import Path

from node_runtime import evaluate_readiness, initialize_and_verify
from runtime_state import Readiness, Runtime, RuntimeState


def test_valid_lifecycle() -> None:
    runtime = Runtime()
    runtime.transition(RuntimeState.INITIALIZING)
    runtime.transition(RuntimeState.VERIFYING)
    ready = Readiness(True, True, True, True, True, True)
    runtime.transition(RuntimeState.READY, ready)
    runtime.transition(RuntimeState.RUNNING, ready)
    runtime.transition(RuntimeState.DEGRADED)
    runtime.transition(RuntimeState.RECOVERY)
    runtime.transition(RuntimeState.READY, ready)
    runtime.transition(RuntimeState.SHUTTING_DOWN)
    runtime.transition(RuntimeState.STOPPED)
    assert runtime.snapshot()["cpg_protocol"] == "NOT_INSTALLED"


def test_invalid_transition() -> None:
    runtime = Runtime()
    try:
        runtime.transition(RuntimeState.RUNNING)
    except ValueError:
        pass
    else:
        raise AssertionError("invalid transition was accepted")


def test_running_requires_readiness() -> None:
    runtime = Runtime()
    runtime.transition(RuntimeState.INITIALIZING)
    runtime.transition(RuntimeState.VERIFYING)
    incomplete = Readiness(True, True, True, False, True, True)
    try:
        runtime.transition(RuntimeState.READY, incomplete)
    except ValueError:
        pass
    else:
        raise AssertionError("incomplete readiness was accepted")


def test_clean_node_reaches_ready_without_cpg() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "node"
        subprocess.run([sys.executable, "bootstrap_node.py", str(root)], check=True)
        runtime = initialize_and_verify(root)
        assert runtime.state == RuntimeState.READY
        assert runtime.snapshot()["cpg_protocol"] == "NOT_INSTALLED"
        assert evaluate_readiness(root).is_ready()


if __name__ == "__main__":
    test_valid_lifecycle()
    test_invalid_transition()
    test_running_requires_readiness()
    test_clean_node_reaches_ready_without_cpg()
    print("runtime lifecycle tests: PASS")
