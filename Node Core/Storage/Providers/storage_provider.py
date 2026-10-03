#!/usr/bin/env python3
"""Provider-neutral storage boundary for Node Core."""

from __future__ import annotations
import sys
from pathlib import Path

_STORAGE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_STORAGE_DIR / "Storage Manager"))

from storage_manager import StorageManager, StorageError

class StorageProvider:
    provider_type = "ABSTRACT"

    def put(self, object_class, object_id, value):
        raise NotImplementedError
    def get(self, object_class, object_id):
        raise NotImplementedError
    def exists(self, object_class, object_id):
        raise NotImplementedError
    def delete(self, object_class, object_id):
        raise NotImplementedError
    def verify(self, object_class, object_id, expected_hash):
        raise NotImplementedError
    def describe(self, object_class, object_id):
        raise NotImplementedError
    def status(self):
        raise NotImplementedError

class LocalStorageProvider(StorageProvider):
    provider_type = "LOCAL"

    def __init__(self, node_root):
        self.manager = StorageManager(node_root)

    def put(self, object_class, object_id, value):
        return self.manager.put_json(object_class, object_id, value)
    def get(self, object_class, object_id):
        return self.manager.get_json(object_class, object_id)
    def exists(self, object_class, object_id):
        try:
            self.manager.get_json(object_class, object_id)
            return True
        except StorageError:
            return False
    def delete(self, object_class, object_id):
        path = self.manager._canonical_path(object_class, object_id)
        if not path.is_file():
            return False
        path.unlink()
        return True
    def verify(self, object_class, object_id, expected_hash):
        return self.manager.verify(object_class, object_id, expected_hash)
    def describe(self, object_class, object_id):
        _, metadata = self.manager.get_json(object_class, object_id)
        return {"provider_type": self.provider_type, **metadata}
    def status(self):
        return {"provider_type": self.provider_type, "status": "READY"}
