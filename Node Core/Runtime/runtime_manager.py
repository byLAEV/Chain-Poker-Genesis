#!/usr/bin/env python3
"""Protocol-neutral Node Core runtime manager.

RuntimeManager is an orchestration facade over the canonical Runtime state
machine and readiness evaluator. It does not define a second lifecycle.
"""
from __future__ import annotations
from pathlib import Path
import sys

_RUNTIME_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_RUNTIME_DIR))
from node_runtime import evaluate_readiness
from State.runtime_state import Runtime, RuntimeState

class RuntimeManager:
    version = "1.1.0"

    def __init__(self, node_root):
        self.root = Path(node_root).resolve()
        self.runtime = Runtime()

    def readiness(self):
        try:
            return evaluate_readiness(self.root)
        except (OSError, ValueError, TypeError, KeyError, FileNotFoundError):
            from State.runtime_state import Readiness
            return Readiness()

    def start(self):
        readiness = self.readiness()
        self.runtime.transition(RuntimeState.ENVIRONMENT_VALIDATED, readiness)
        self.runtime.transition(RuntimeState.IDENTITY_INITIALIZED, readiness)
        self.runtime.transition(RuntimeState.STORAGE_INITIALIZED, readiness)
        self.runtime.transition(RuntimeState.STORAGE_STRUCTURE_VERIFIED, readiness)
        self.runtime.transition(RuntimeState.INTEGRITY_VERIFIED, readiness)
        self.runtime.transition(RuntimeState.RECOVERY_READY, readiness)
        self.runtime.transition(RuntimeState.NODE_CORE_READY, readiness)
        self.runtime.transition(RuntimeState.RUNNING, readiness)
        return self.runtime.snapshot()

    def observe_storage_provider(self, health_manager):
        """Observe an external storage provider without redefining Node Core readiness."""
        result = health_manager.check()
        if result.get("health_state") != "HEALTHY":
            if self.runtime.state == RuntimeState.RUNNING:
                self.runtime.transition(RuntimeState.DEGRADED)
            return {"runtime_state": self.runtime.state.value, "provider_state": "DEGRADED",
                    "local_fallback": True, "health": result}
        return {"runtime_state": self.runtime.state.value, "provider_state": "HEALTHY",
                "local_fallback": False, "health": result}

    def complete_recovery_to_ready(self, readiness):
        """Complete canonical recovery and stop at NODE_CORE_READY."""
        if self.runtime.state == RuntimeState.DEGRADED:
            self.runtime.transition(RuntimeState.RECOVERY)
        if self.runtime.state == RuntimeState.RECOVERY:
            self.runtime.transition(RuntimeState.NODE_CORE_READY, readiness)
        return self.runtime.snapshot()

    def complete_storage_provider_recovery(self, readiness):
        """Return from provider recovery only after canonical Node Core readiness passes."""
        if self.runtime.state == RuntimeState.RUNNING:
            return self.runtime.snapshot()
        if self.runtime.state == RuntimeState.DEGRADED:
            self.runtime.transition(RuntimeState.RECOVERY)
        if self.runtime.state == RuntimeState.RECOVERY:
            self.runtime.transition(RuntimeState.NODE_CORE_READY, readiness)
            self.runtime.transition(RuntimeState.RUNNING, readiness)
        return self.runtime.snapshot()

    def stop(self):
        if self.runtime.state in (RuntimeState.NODE_CORE_READY, RuntimeState.RUNNING, RuntimeState.DEGRADED):
            self.runtime.transition(RuntimeState.SHUTTING_DOWN)
            self.runtime.transition(RuntimeState.STOPPED)
        return self.runtime.snapshot()
