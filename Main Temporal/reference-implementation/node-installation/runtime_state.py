#!/usr/bin/env python3
"""Deterministic Node Core runtime state machine."""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class RuntimeState(str, Enum):
    UNINITIALIZED = "UNINITIALIZED"
    INITIALIZING = "INITIALIZING"
    VERIFYING = "VERIFYING"
    READY = "READY"
    RUNNING = "RUNNING"
    DEGRADED = "DEGRADED"
    RECOVERY = "RECOVERY"
    SHUTTING_DOWN = "SHUTTING_DOWN"
    STOPPED = "STOPPED"
    INITIALIZATION_FAILED = "INITIALIZATION_FAILED"
    VERIFICATION_FAILED = "VERIFICATION_FAILED"
    RECOVERY_FAILED = "RECOVERY_FAILED"


VALID_TRANSITIONS = {
    RuntimeState.UNINITIALIZED: {RuntimeState.INITIALIZING},
    RuntimeState.INITIALIZING: {RuntimeState.VERIFYING, RuntimeState.INITIALIZATION_FAILED},
    RuntimeState.VERIFYING: {RuntimeState.READY, RuntimeState.VERIFICATION_FAILED},
    RuntimeState.READY: {RuntimeState.RUNNING, RuntimeState.SHUTTING_DOWN},
    RuntimeState.RUNNING: {RuntimeState.DEGRADED, RuntimeState.RECOVERY, RuntimeState.SHUTTING_DOWN},
    RuntimeState.DEGRADED: {RuntimeState.RECOVERY, RuntimeState.SHUTTING_DOWN},
    RuntimeState.RECOVERY: {RuntimeState.READY, RuntimeState.RECOVERY_FAILED},
    RuntimeState.SHUTTING_DOWN: {RuntimeState.STOPPED},
    RuntimeState.STOPPED: {RuntimeState.INITIALIZING},
    RuntimeState.INITIALIZATION_FAILED: {RuntimeState.INITIALIZING},
    RuntimeState.VERIFICATION_FAILED: {RuntimeState.INITIALIZING},
    RuntimeState.RECOVERY_FAILED: {RuntimeState.INITIALIZING},
}


@dataclass(frozen=True)
class Readiness:
    identity_ready: bool
    configuration_ready: bool
    storage_ready: bool
    provider_ready: bool
    coherence_coherent: bool
    recovery_ready: bool
    protocol_associations_empty: bool = True
    cpg_not_installed: bool = True

    def is_ready(self) -> bool:
        return all((
            self.identity_ready,
            self.configuration_ready,
            self.storage_ready,
            self.provider_ready,
            self.coherence_coherent,
            self.recovery_ready,
            self.protocol_associations_empty,
            self.cpg_not_installed,
        ))


@dataclass
class Runtime:
    state: RuntimeState = RuntimeState.UNINITIALIZED
    health: str = "HEALTHY"

    def transition(self, target: RuntimeState, readiness: Readiness | None = None) -> None:
        if target not in VALID_TRANSITIONS.get(self.state, set()):
            raise ValueError(f"invalid runtime transition: {self.state.value} -> {target.value}")
        if target in (RuntimeState.READY, RuntimeState.RUNNING):
            if readiness is None or not readiness.is_ready():
                raise ValueError(f"readiness prerequisites not satisfied for {target.value}")
        if target in (RuntimeState.DEGRADED, RuntimeState.RECOVERY):
            self.health = "DEGRADED"
        elif target == RuntimeState.RECOVERY_FAILED:
            self.health = "FAILED"
        elif target in (RuntimeState.READY, RuntimeState.RUNNING):
            self.health = "HEALTHY"
        self.state = target

    def snapshot(self) -> dict[str, str]:
        return {
            "state": self.state.value,
            "health": self.health,
            "readiness": "READY" if self.state in (RuntimeState.READY, RuntimeState.RUNNING) else "NOT_READY",
            "cpg_protocol": "NOT_INSTALLED",
        }
