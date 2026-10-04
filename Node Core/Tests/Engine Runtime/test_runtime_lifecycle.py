#!/usr/bin/env python3
"""Canonical Node Core Runtime lifecycle tests."""

from __future__ import annotations
import tempfile
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE / "Bootstrap/Installer"))
sys.path.insert(0, str(BASE / "Runtime"))
sys.path.insert(0, str(BASE / "Runtime/State"))

from bootstrap_node import bootstrap_node
from node_runtime import evaluate_readiness, initialize_and_verify
from runtime_state import Readiness, Runtime, RuntimeState


def test_valid_lifecycle() -> None:
    runtime = Runtime()
    ready = Readiness(
        True, True, True, True, True, True, True, True, True, True, True
    )
    runtime.transition(RuntimeState.ENVIRONMENT_VALIDATED, ready)
    runtime.transition(RuntimeState.IDENTITY_INITIALIZED, ready)
    runtime.transition(RuntimeState.STORAGE_INITIALIZED, ready)
    runtime.transition(RuntimeState.STORAGE_STRUCTURE_VERIFIED, ready)
    runtime.transition(RuntimeState.INTEGRITY_VERIFIED, ready)
    runtime.transition(RuntimeState.RECOVERY_READY, ready)
    runtime.transition(RuntimeState.NODE_CORE_READY, ready)
    runtime.transition(RuntimeState.RUNNING, ready)
    runtime.transition(RuntimeState.DEGRADED)
    runtime.transition(RuntimeState.RECOVERY)
    runtime.transition(RuntimeState.NODE_CORE_READY, ready)
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
    incomplete = Readiness(True, True, True, False, True, True)
    runtime.transition(RuntimeState.ENVIRONMENT_VALIDATED, incomplete)
    try:
        runtime.transition(RuntimeState.IDENTITY_INITIALIZED, incomplete)
        runtime.transition(RuntimeState.STORAGE_INITIALIZED, incomplete)
        runtime.transition(RuntimeState.STORAGE_STRUCTURE_VERIFIED, incomplete)
        runtime.transition(RuntimeState.INTEGRITY_VERIFIED, incomplete)
        runtime.transition(RuntimeState.RECOVERY_READY, incomplete)
        runtime.transition(RuntimeState.NODE_CORE_READY, incomplete)
    except ValueError:
        return
    raise AssertionError("incomplete readiness was accepted")


def test_clean_node_reaches_ready_without_cpg() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "node"
        bootstrap_node(root)
        runtime = initialize_and_verify(root)
        assert runtime.state == RuntimeState.NODE_CORE_READY
        assert runtime.snapshot()["cpg_protocol"] == "NOT_INSTALLED"
        assert evaluate_readiness(root).is_ready()


if __name__ == "__main__":
    test_valid_lifecycle()
    test_invalid_transition()
    test_running_requires_readiness()
    test_clean_node_reaches_ready_without_cpg()
    print("runtime lifecycle tests: PASS")
