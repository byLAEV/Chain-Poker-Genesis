#!/usr/bin/env python3
"""Minimal, protocol-neutral Node Core storage policy engine.

This layer decides storage treatment; it does not perform synchronization,
replication, encryption, publication, or deletion. Those actions remain
separate infrastructure concerns until their specifications are reconciled.
"""

from __future__ import annotations

from dataclasses import dataclass


class StoragePolicyError(ValueError):
    pass


@dataclass(frozen=True)
class StoragePolicy:
    storage_class: str
    where: str
    who: str
    when: str
    how_long: str
    sync: str
    placement: str
    visibility: str
    persistence: str
    encryption: str
    pin: str
    replicate: str
    delete: str
    retention: str


_DEFAULTS = {
    "TEMPORARY": {
        "where": "NODE_LOCAL",
        "who": "NODE_LOCAL",
        "when": "IMMEDIATE",
        "how_long": "TEMPORARY",
        "where": "NODE_LOCAL",
        "who": "NODE_LOCAL",
        "when": "IMMEDIATE",
        "how_long": "PERSISTENT",
        "where": "NODE_LOCAL",
        "who": "NODE_LOCAL",
        "when": "IMMEDIATE",
        "how_long": "PERSISTENT",
        "where": "NODE_LOCAL",
        "who": "AUTHORIZED_ONLY",
        "when": "IMMEDIATE",
        "how_long": "PERSISTENT",
        "where": "NODE_LOCAL",
        "who": "LOCAL_IDENTITY",
        "when": "IMMEDIATE",
        "how_long": "PERSISTENT",
        "sync": "DISABLED",
        "placement": "LOCAL_ONLY",
        "visibility": "LOCAL",
        "persistence": "TEMPORARY",
        "encryption": "POLICY_DEFINED",
        "pin": "DISABLED",
        "replicate": "DISABLED",
        "delete": "POLICY_DEFINED",
        "retention": "TEMPORARY",
    },
    "LOCAL_PUBLIC": {
        "sync": "DISABLED",
        "placement": "LOCAL_ONLY",
        "visibility": "PUBLIC_LOCAL",
        "persistence": "PERSISTENT",
        "encryption": "POLICY_DEFINED",
        "pin": "DISABLED",
        "replicate": "DISABLED",
        "delete": "POLICY_DEFINED",
        "retention": "PERSISTENT",
    },
    "LOCAL_PRIVATE": {
        "sync": "DISABLED",
        "placement": "LOCAL_ONLY",
        "visibility": "PRIVATE",
        "persistence": "PERSISTENT",
        "encryption": "REQUIRED",
        "pin": "DISABLED",
        "replicate": "LOCAL_ONLY",
        "delete": "POLICY_DEFINED",
        "retention": "PERSISTENT",
    },
    "LOCAL_RESTRICTED": {
        "sync": "DISABLED",
        "placement": "LOCAL_ONLY",
        "visibility": "RESTRICTED",
        "persistence": "PERSISTENT",
        "encryption": "REQUIRED",
        "pin": "DISABLED",
        "replicate": "LOCAL_ONLY",
        "delete": "POLICY_DEFINED",
        "retention": "PERSISTENT",
    },
    "LOCAL_PERSONAL": {
        "sync": "DISABLED",
        "placement": "LOCAL_ONLY",
        "visibility": "PERSONAL",
        "persistence": "PERSISTENT",
        "encryption": "POLICY_DEFINED",
        "pin": "DISABLED",
        "replicate": "LOCAL_ONLY",
        "delete": "POLICY_DEFINED",
        "retention": "PERSISTENT",
    },
}


class StoragePolicyEngine:
    """Resolve the canonical minimum policy for a storage class."""

    SUPPORTED_CLASSES = frozenset(_DEFAULTS)

    def evaluate(self, storage_class: str, overrides: dict | None = None) -> StoragePolicy:
        if storage_class not in self.SUPPORTED_CLASSES:
            raise StoragePolicyError(f"unsupported storage class: {storage_class}")

        values = dict(_DEFAULTS[storage_class])
        if overrides:
            allowed = set(values)
            unknown = set(overrides) - allowed
            if unknown:
                raise StoragePolicyError(
                    f"unsupported policy fields: {', '.join(sorted(unknown))}"
                )
            values.update(overrides)

        if values["sync"] not in {"ENABLED", "DISABLED"}:
            raise StoragePolicyError("sync must be ENABLED or DISABLED")

        if values["sync"] == "DISABLED" and values["placement"] != "LOCAL_ONLY":
            raise StoragePolicyError(
                "synchronization-disabled policy must use LOCAL_ONLY placement"
            )

        return StoragePolicy(storage_class=storage_class, **values)
