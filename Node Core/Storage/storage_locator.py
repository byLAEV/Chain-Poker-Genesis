#!/usr/bin/env python3
"""Canonical logical-to-physical Node Core storage locator."""

from __future__ import annotations
import sys
from pathlib import Path

_STORAGE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_STORAGE_DIR / "Object Registry"))
sys.path.insert(0, str(_STORAGE_DIR / "Providers"))

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
        if entry.get("location_state") not in {
            "LOCAL_ONLY", "LOCAL_AND_DISTRIBUTED", "DISTRIBUTED_ONLY",
            "SYNC_PENDING", "SYNC_PROCESSING", "MISSING_LOCAL",
            "MISSING_DISTRIBUTED", "CONFLICT", "QUARANTINED",
        }:
            raise StorageLocatorError("invalid location state")
        return {
            "object_id": object_id,
            "logical_path": entry["relative_path"],
            "location": entry["location"],
            "storage_class": entry["storage_class"],
            "state": entry["state"],
            "version": entry["version"],
            "provider_type": entry["provider_type"],
            "cid": entry.get("cid"),
            "location_state": entry["location_state"],
        }
