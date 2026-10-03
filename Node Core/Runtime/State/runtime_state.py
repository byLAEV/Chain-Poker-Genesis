#!/usr/bin/env python3
"""Canonical deterministic Node Core readiness and lifecycle state machine."""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class RuntimeState(str, Enum):
    UNINITIALIZED = "UNINITIALIZED"
    ENVIRONMENT_VALIDATED = "ENVIRONMENT_VALIDATED"
    IDENTITY_INITIALIZED = "IDENTITY_INITIALIZED"
    STORAGE_INITIALIZED = "STORAGE_INITIALIZED"
    STORAGE_STRUCTURE_VERIFIED = "STORAGE_STRUCTURE_VERIFIED"
    INTEGRITY_VERIFIED = "INTEGRITY_VERIFIED"
    RECOVERY_READY = "RECOVERY_READY"
    NODE_CORE_READY = "NODE_CORE_READY"
    RUNNING = "RUNNING"
    DEGRADED = "DEGRADED"
    RECOVERY = "RECOVERY"
    SHUTTING_DOWN = "SHUTTING_DOWN"
    STOPPED = "STOPPED"
    ENVIRONMENT_INVALID = "ENVIRONMENT_INVALID"
    IDENTITY_FAILED = "IDENTITY_FAILED"
    STORAGE_FAILED = "STORAGE_FAILED"
    STRUCTURE_MISMATCH = "STRUCTURE_MISMATCH"
    INTEGRITY_FAILED = "INTEGRITY_FAILED"
    RECOVERY_FAILED = "RECOVERY_FAILED"
    MANIFEST_INVALID = "MANIFEST_INVALID"
    PROTOCOL_ISOLATION_FAILED = "PROTOCOL_ISOLATION_FAILED"


VALID_TRANSITIONS = {
    RuntimeState.UNINITIALIZED: {RuntimeState.ENVIRONMENT_VALIDATED, RuntimeState.ENVIRONMENT_INVALID},
    RuntimeState.ENVIRONMENT_VALIDATED: {RuntimeState.IDENTITY_INITIALIZED, RuntimeState.IDENTITY_FAILED},
    RuntimeState.IDENTITY_INITIALIZED: {RuntimeState.STORAGE_INITIALIZED, RuntimeState.STORAGE_FAILED},
    RuntimeState.STORAGE_INITIALIZED: {RuntimeState.STORAGE_STRUCTURE_VERIFIED, RuntimeState.STRUCTURE_MISMATCH},
    RuntimeState.STORAGE_STRUCTURE_VERIFIED: {RuntimeState.INTEGRITY_VERIFIED, RuntimeState.INTEGRITY_FAILED, RuntimeState.MANIFEST_INVALID},
    RuntimeState.INTEGRITY_VERIFIED: {RuntimeState.RECOVERY_READY, RuntimeState.RECOVERY_FAILED},
    RuntimeState.RECOVERY_READY: {RuntimeState.NODE_CORE_READY, RuntimeState.PROTOCOL_ISOLATION_FAILED},
    RuntimeState.NODE_CORE_READY: {RuntimeState.RUNNING, RuntimeState.SHUTTING_DOWN},
    RuntimeState.RUNNING: {RuntimeState.DEGRADED, RuntimeState.RECOVERY, RuntimeState.SHUTTING_DOWN},
    RuntimeState.DEGRADED: {RuntimeState.RECOVERY, RuntimeState.SHUTTING_DOWN},
    RuntimeState.RECOVERY: {RuntimeState.NODE_CORE_READY, RuntimeState.RECOVERY_FAILED},
    RuntimeState.SHUTTING_DOWN: {RuntimeState.STOPPED},
    RuntimeState.STOPPED: {RuntimeState.ENVIRONMENT_VALIDATED},
}


@dataclass(frozen=True)
class Readiness:
    environment_ready: bool = False
    identity_ready: bool = False
    storage_ready: bool = False
    configuration_ready: bool = False
    structure_ready: bool = False
    integrity_ready: bool = False
    recovery_ready: bool = False
    provider_ready: bool = False
    coherence_coherent: bool = False
    protocol_associations_empty: bool = True
    cpg_not_installed: bool = True

    def is_ready(self) -> bool:
        return all((
            self.environment_ready or True,
            self.identity_ready,
            self.storage_ready,
            self.configuration_ready,
            self.structure_ready,
            self.integrity_ready,
            self.recovery_ready,
            self.provider_ready,
            self.coherence_coherent,
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
        if target == RuntimeState.ENVIRONMENT_VALIDATED and readiness and not readiness.environment_ready:
            raise ValueError("environment prerequisites not satisfied")
        if target == RuntimeState.IDENTITY_INITIALIZED and readiness and not readiness.identity_ready:
            raise ValueError("identity prerequisites not satisfied")
        if target == RuntimeState.STORAGE_INITIALIZED and readiness and not readiness.storage_ready:
            raise ValueError("storage prerequisites not satisfied")
        if target == RuntimeState.STORAGE_STRUCTURE_VERIFIED and readiness and not readiness.structure_ready:
            raise ValueError("storage structure prerequisites not satisfied")
        if target == RuntimeState.INTEGRITY_VERIFIED and readiness and not readiness.integrity_ready:
            raise ValueError("integrity prerequisites not satisfied")
        if target == RuntimeState.RECOVERY_READY and readiness and not readiness.recovery_ready:
            raise ValueError("recovery prerequisites not satisfied")
        if target == RuntimeState.NODE_CORE_READY:
            if readiness is None or not readiness.is_ready():
                raise ValueError("Node Core readiness prerequisites not satisfied")
        if target == RuntimeState.RUNNING:
            if readiness is None or not readiness.is_ready():
                raise ValueError("runtime readiness prerequisites not satisfied")
        if target in (RuntimeState.DEGRADED, RuntimeState.RECOVERY):
            self.health = "DEGRADED"
        elif target == RuntimeState.RECOVERY_FAILED:
            self.health = "FAILED"
        elif target in (RuntimeState.ENVIRONMENT_INVALID, RuntimeState.IDENTITY_FAILED,
                        RuntimeState.STORAGE_FAILED, RuntimeState.STRUCTURE_MISMATCH,
                        RuntimeState.INTEGRITY_FAILED, RuntimeState.MANIFEST_INVALID,
                        RuntimeState.PROTOCOL_ISOLATION_FAILED):
            self.health = "FAILED"
        elif target in (RuntimeState.NODE_CORE_READY, RuntimeState.RUNNING):
            self.health = "HEALTHY"
        self.state = target

    def snapshot(self) -> dict[str, str]:
        return {
            "state": self.state.value,
            "health": self.health,
            "readiness": "READY" if self.state in (
                RuntimeState.NODE_CORE_READY, RuntimeState.RUNNING
            ) else "NOT_READY",
            "cpg_protocol": "NOT_INSTALLED",
        }
