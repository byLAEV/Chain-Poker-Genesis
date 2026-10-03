#!/usr/bin/env python3
"""Node Core recovery integration."""

from __future__ import annotations
import sys
from pathlib import Path

_RUNTIME_DIR = Path(__file__).resolve().parent.parent / "Runtime"
sys.path.insert(0, str(_RUNTIME_DIR))

from node_runtime import evaluate_readiness
from runtime_state import Runtime, RuntimeState

class RecoveryManager:
    def __init__(self, root: Path):
        self.root = root.resolve()

    def recover(self, runtime: Runtime) -> Runtime:
        if runtime.state not in (RuntimeState.RUNNING, RuntimeState.DEGRADED):
            raise ValueError(f"recovery requires RUNNING or DEGRADED, got {runtime.state.value}")
        runtime.transition(RuntimeState.RECOVERY)
        readiness = evaluate_readiness(self.root)
        if readiness.is_ready():
            runtime.transition(RuntimeState.NODE_CORE_READY, readiness)
            return runtime
        runtime.transition(RuntimeState.RECOVERY_FAILED)
        raise RuntimeError("Node Core recovery prerequisites are not satisfied")
