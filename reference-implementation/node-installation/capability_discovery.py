#!/usr/bin/env python3
"""Minimum protocol-neutral FN-025 capability discovery."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

CAPABILITY_SCHEMA_VERSION = "1"
BASE_CAPABILITIES = frozenset(
    {
        "identity.node",
        "network.peer",
        "storage.local",
        "storage.distributed",
    }
)

@dataclass(frozen=True)
class CapabilityEvidence:
    node_id: str
    node_instance_id: str
    schema_version: str
    capabilities: tuple[str, ...]

    def snapshot(self) -> dict[str, object]:
        return {
            "node_id": self.node_id,
            "node_instance_id": self.node_instance_id,
            "schema_version": self.schema_version,
            "capabilities": list(self.capabilities),
        }

class CapabilityDiscovery:
    def __init__(self, node_id: str, node_instance_id: str) -> None:
        if not node_id or not node_instance_id:
            raise ValueError("node_id and node_instance_id are required")
        self.node_id = node_id
        self.node_instance_id = node_instance_id

    def describe(self, capabilities: Iterable[str]) -> CapabilityEvidence:
        normalized = tuple(sorted(set(capabilities)))
        if any(not capability or "." not in capability for capability in normalized):
            raise ValueError("capabilities must use explicit dotted identifiers")
        return CapabilityEvidence(
            node_id=self.node_id,
            node_instance_id=self.node_instance_id,
            schema_version=CAPABILITY_SCHEMA_VERSION,
            capabilities=normalized,
        )

    def discover_base(self) -> CapabilityEvidence:
        return self.describe(BASE_CAPABILITIES)