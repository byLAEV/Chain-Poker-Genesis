#!/usr/bin/env python3
"""Minimal, protocol-neutral Node Core storage policy engine."""

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


def _policy(where, who, when, how_long, sync, placement, visibility,
            persistence, encryption, pin, replicate, delete, retention):
    return {
        "where": where,
        "who": who,
        "when": when,
        "how_long": how_long,
        "sync": sync,
        "placement": placement,
        "visibility": visibility,
        "persistence": persistence,
        "encryption": encryption,
        "pin": pin,
        "replicate": replicate,
        "delete": delete,
        "retention": retention,
    }


_DEFAULTS = {
    "TEMPORARY": _policy(
        "NODE_LOCAL", "NODE_LOCAL", "IMMEDIATE", "TEMPORARY",
        "DISABLED", "LOCAL_ONLY", "LOCAL", "TEMPORARY",
        "POLICY_DEFINED", "DISABLED", "DISABLED", "POLICY_DEFINED", "TEMPORARY",
    ),
    "LOCAL_PUBLIC": _policy(
        "NODE_LOCAL", "NODE_LOCAL", "IMMEDIATE", "PERSISTENT",
        "DISABLED", "LOCAL_ONLY", "PUBLIC_LOCAL", "PERSISTENT",
        "POLICY_DEFINED", "DISABLED", "DISABLED", "POLICY_DEFINED", "PERSISTENT",
    ),
    "LOCAL_PRIVATE": _policy(
        "NODE_LOCAL", "NODE_LOCAL", "IMMEDIATE", "PERSISTENT",
        "DISABLED", "LOCAL_ONLY", "PRIVATE", "PERSISTENT",
        "REQUIRED", "DISABLED", "LOCAL_ONLY", "POLICY_DEFINED", "PERSISTENT",
    ),
    "LOCAL_RESTRICTED": _policy(
        "NODE_LOCAL", "AUTHORIZED_ONLY", "IMMEDIATE", "PERSISTENT",
        "DISABLED", "LOCAL_ONLY", "RESTRICTED", "PERSISTENT",
        "REQUIRED", "DISABLED", "LOCAL_ONLY", "POLICY_DEFINED", "PERSISTENT",
    ),
    "LOCAL_PERSONAL": _policy(
        "NODE_LOCAL", "LOCAL_IDENTITY", "IMMEDIATE", "PERSISTENT",
        "DISABLED", "LOCAL_ONLY", "PERSONAL", "PERSISTENT",
        "POLICY_DEFINED", "DISABLED", "LOCAL_ONLY", "POLICY_DEFINED", "PERSISTENT",
    ),
}


class StoragePolicyEngine:
    """Resolve the canonical minimum policy for a storage class."""

    SUPPORTED_CLASSES = frozenset(_DEFAULTS)

    def evaluate(self, storage_class: str, overrides: dict | None = None) -> StoragePolicy:
        if storage_class not in self.SUPPORTED_CLASSES:
            raise StoragePolicyError(f"unsupported storage class: {storage_class}")

        values = dict(_DEFAULTS[storage_class])
        if overrides:
            unknown = set(overrides) - set(values)
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
