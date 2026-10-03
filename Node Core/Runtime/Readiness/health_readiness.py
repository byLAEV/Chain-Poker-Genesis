#!/usr/bin/env python3
"""Objective Node Core health and readiness evaluation."""

from __future__ import annotations
import sys
from dataclasses import dataclass
from pathlib import Path

_RUNTIME_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_RUNTIME_DIR))

from node_runtime import evaluate_coherence, evaluate_provider, evaluate_readiness

@dataclass(frozen=True)
class HealthReport:
    identity_ready: bool
    configuration_ready: bool
    storage_ready: bool
    provider_ready: bool
    coherence_coherent: bool
    recovery_ready: bool
    protocol_isolated: bool
    synchronization: str
    cpg_protocol: str

    @property
    def healthy(self) -> bool:
        return all((self.identity_ready, self.configuration_ready, self.storage_ready, self.structure_ready, self.integrity_ready,
                    self.provider_ready, self.coherence_coherent, self.recovery_ready,
                    self.protocol_isolated))

    @property
    def ready(self) -> bool:
        return self.healthy and self.cpg_protocol == "NOT_INSTALLED"

    def snapshot(self) -> dict[str, str]:
        return {
            "health": "HEALTHY" if self.healthy else "FAILED",
            "readiness": "NODE_CORE_READY" if self.ready else "NOT_READY",
            "synchronization": self.synchronization,
            "cpg_protocol": self.cpg_protocol,
        }

def evaluate_health(root: Path) -> HealthReport:
    readiness = evaluate_readiness(root)
    isolated = readiness.protocol_associations_empty and readiness.cpg_not_installed
    return HealthReport(
        identity_ready=readiness.identity_ready,
        configuration_ready=readiness.configuration_ready,
        storage_ready=readiness.storage_ready,
        provider_ready=evaluate_provider(root),
        coherence_coherent=evaluate_coherence(root),
        recovery_ready=readiness.recovery_ready,
        protocol_isolated=isolated,
        synchronization="NOT_EVALUATED",
        cpg_protocol="NOT_INSTALLED" if readiness.cpg_not_installed else "INVALID",
    )

def main() -> int:
    if len(sys.argv) != 2:
        print("usage: health_readiness.py <node-directory>")
        return 2
    report = evaluate_health(Path(sys.argv[1]).resolve())
    for key, value in report.snapshot().items():
        print(f"{key} = {value}")
    return 0 if report.ready else 1

if __name__ == "__main__":
    raise SystemExit(main())
