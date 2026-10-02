#!/usr/bin/env python3
"""Minimal protocol-neutral Node Core replication policy engine."""

from __future__ import annotations

from dataclasses import dataclass


class ReplicationPolicyError(ValueError):
    pass


@dataclass(frozen=True)
class ReplicationPolicy:
    replication_policy: str
    minimum_copies: int
    external_service: bool
    local_required: bool


class ReplicationPolicyEngine:
    """Resolve explicit replication intent without performing replication."""

    SUPPORTED_POLICIES = frozenset(
        {"LOCAL_ONLY", "MULTI_NODE", "EXTERNAL_PINNING"}
    )

    def evaluate(self, replication_policy: str) -> ReplicationPolicy:
        if replication_policy not in self.SUPPORTED_POLICIES:
            raise ReplicationPolicyError(
                f"unsupported replication policy: {replication_policy}"
            )

        if replication_policy == "LOCAL_ONLY":
            return ReplicationPolicy(replication_policy, 1, False, True)

        if replication_policy == "MULTI_NODE":
            return ReplicationPolicy(replication_policy, 2, False, True)

        return ReplicationPolicy(replication_policy, 2, True, True)
