#!/usr/bin/env python3
"""Provider-neutral storage contract and local provider."""

from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from storage_engine import LocalStore, StorageError

class StorageProvider:
    provider_type = "ABSTRACT"

    def put(self, object_class, object_id, data): raise NotImplementedError
    def get(self, object_class, object_id): raise NotImplementedError
    def exists(self, object_class, object_id): raise NotImplementedError
    def delete(self, object_class, object_id): raise NotImplementedError
    def verify(self, object_class, object_id, expected_hash): raise NotImplementedError
    def status(self): raise NotImplementedError
    def capabilities(self): return set()

class LocalStorageProvider(StorageProvider):
    provider_type = "LOCAL"

    def __init__(self, node_root):
        self.store = LocalStore(node_root)

    def put(self, object_class, object_id, data):
        return self.store.put(object_class, object_id, data)

    def get(self, object_class, object_id):
        return self.store.get(object_class, object_id)

    def exists(self, object_class, object_id):
        try:
            self.store.get(object_class, object_id)
            return True
        except StorageError:
            return False

    def delete(self, object_class, object_id):
        return self.store.delete(object_class, object_id)

    def verify(self, object_class, object_id, expected_hash):
        return self.store.verify(object_class, object_id, expected_hash)

    def status(self):
        return {"provider_type": self.provider_type, "status": "READY"}

    def capabilities(self):
        return {"put", "get", "delete", "exists", "verify", "atomic_write"}
