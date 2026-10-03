#!/usr/bin/env python3
"""Protocol-neutral Node Core runtime manager."""
from __future__ import annotations
from pathlib import Path
from .State.runtime_state import Runtime, RuntimeState, Readiness

class RuntimeManager:
    version="1.1.0"
    def __init__(self, node_root):
        self.root=Path(node_root).resolve()
        self.runtime=Runtime()

    def readiness(self):
        storage=self.root/"node-storage"
        config=storage/"configuration/node-config.json"
        state=storage/"state/node-state.json"
        recovery=storage/"recovery"
        identity=storage/"identity"
        return Readiness(
            environment_ready=self.root.is_dir(),
            identity_ready=identity.is_dir() and any(identity.iterdir()),
            storage_ready=storage.is_dir(),
            configuration_ready=config.is_file(),
            structure_ready=all((storage/p).is_dir() for p in ("configuration","state","recovery")),
            integrity_ready=state.is_file(),
            recovery_ready=recovery.is_dir(),
            provider_ready=True,
            coherence_coherent=True,
            protocol_associations_empty=(self._config(config).get("protocol_associations",[])==[] if config.is_file() else False),
            cpg_not_installed=(self._config(config).get("cpg_protocol") in (None,"NOT_INSTALLED") if config.is_file() else False),
        )

    @staticmethod
    def _config(path):
        try:
            import json
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError,ValueError):
            return {}

    def start(self):
        r=self.readiness()
        self.runtime.transition(RuntimeState.ENVIRONMENT_VALIDATED,r)
        if not r.identity_ready:
            raise RuntimeError("Node identity must be provisioned before runtime start")
        self.runtime.transition(RuntimeState.IDENTITY_INITIALIZED,r)
        self.runtime.transition(RuntimeState.STORAGE_INITIALIZED,r)
        self.runtime.transition(RuntimeState.STORAGE_STRUCTURE_VERIFIED,r)
        self.runtime.transition(RuntimeState.INTEGRITY_VERIFIED,r)
        self.runtime.transition(RuntimeState.RECOVERY_READY,r)
        self.runtime.transition(RuntimeState.NODE_CORE_READY,r)
        self.runtime.transition(RuntimeState.RUNNING,r)
        return self.runtime.snapshot()

    def stop(self):
        if self.runtime.state in (RuntimeState.RUNNING,RuntimeState.DEGRADED):
            self.runtime.transition(RuntimeState.SHUTTING_DOWN)
            self.runtime.transition(RuntimeState.STOPPED)
        return self.runtime.snapshot()
