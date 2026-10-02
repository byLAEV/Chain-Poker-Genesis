#!/usr/bin/env python3
"""Canonical logical-to-physical Node Core storage locator."""

from __future__ import annotations

from object_registry import ObjectRegistry, RegistryError
from storage_provider import LocalStorageProvider

class StorageLocatorError(Exception):
    pass

class StorageLocator:
    def __init__(self, node_root):
        self.registry = ObjectRegistry(node_root)
        self.provider = LocalStorageProvider(node_root)

    def locate(self, object_id):
        try:
            entry = self.registry.get(object_id)
        except RegistryError as exc:
            raise StorageLocatorError(str(exc)) from exc

        if entry.get("provider_type") != self.provider.provider_type:
            raise StorageLocatorError("unsupported provider for current Node Core baseline")

        if entry.get("location_state") not in {
            "LOCAL_ONLY", "LOCAL_AND_DISTRIBUTED", "DISTRIBUTED_ONLY",
            "SYNC_PENDING", "SYNC_PROCESSING", "MISSING_LOCAL",
            "MISSING_DISTRIBUTED", "CONFLICT", "QUARANTINED",
        }:
            raise StorageLocatorError("invalid location state")

        return {
            "object_id": object_id,
            "logical_path": entry["relative_path"],
            "provider_type": entry["provider_type"],
            "location_state": entry["location_state"],
        }
