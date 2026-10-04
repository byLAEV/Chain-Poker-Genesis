#!/usr/bin/env python3
"""Kubo provider failure detection and controlled recovery."""
from __future__ import annotations

class KuboRecoveryManager:
    """Keeps local storage usable while Kubo is degraded, then reconciles before READY."""

    def __init__(self, process_manager, health_manager, storage_manager, coherence_verifier,
                 reconciliation_manager, provider_state=None):
        self.process = process_manager
        self.health = health_manager
        self.storage = storage_manager
        self.coherence = coherence_verifier
        self.reconciliation = reconciliation_manager
        self.state = provider_state

    def observe(self):
        result = self.health.check()
        if result.get("health_state") == "HEALTHY":
            if self.state:
                self.state.transition(health_state="HEALTHY", lifecycle_state="HEALTHY")
            return {"provider_state":"HEALTHY","health":result,"local_fallback":False}
        if self.state:
            self.state.transition(
                health_state="UNHEALTHY",
                lifecycle_state="DEGRADED",
                synchronization_state="DEGRADED",
            )
        return {
            "provider_state":"DEGRADED",
            "health":result,
            "local_fallback":True,
            "reason":result.get("reason","Kubo unavailable"),
        }

    def recover(self, executable, *, version, max_attempts=1):
        last=None
        for _ in range(max_attempts):
            try:
                if not self.process.is_running():
                    if self.state:
                        self.state.transition(lifecycle_state="STARTING", health_state="UNHEALTHY")
                    self.process.start(executable, version=version)

                health=self.health.require_healthy()
                if self.state:
                    self.state.transition(
                        lifecycle_state="HEALTHY",
                        health_state="HEALTHY",
                        synchronization_state="INITIAL_SYNC_PENDING",
                    )

                reconciliation=self.reconciliation.reconcile()
                if reconciliation["state"] == "CONFLICT":
                    raise RuntimeError("Kubo recovery stopped: reconciliation conflict")
                if reconciliation["state"] == "FAILED":
                    raise RuntimeError("Kubo recovery stopped: reconciliation failure")

                coherence=self.coherence.verify_all()
                if not coherence["dual_storage_ready"]:
                    raise RuntimeError("Kubo recovery stopped: coherence gate not satisfied")

                if self.state:
                    self.state.transition(
                        lifecycle_state="READY",
                        health_state="HEALTHY",
                        synchronization_state="SYNCHRONIZED",
                    )
                return {
                    "provider_state":"READY",
                    "health":health,
                    "reconciliation":reconciliation,
                    "coherence":coherence,
                }
            except Exception as exc:
                last=exc
                if self.state:
                    self.state.transition(
                        lifecycle_state="DEGRADED",
                        health_state="UNHEALTHY",
                        synchronization_state="DEGRADED",
                    )
        raise RuntimeError("Kubo recovery failed") from last
