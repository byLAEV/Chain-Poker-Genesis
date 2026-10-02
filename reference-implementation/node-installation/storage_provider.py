#!/usr/bin/env python3
"""Provider-neutral storage boundary for Node Core."""

from __future__ import annotations

from storage_manager import StorageManager, StorageError

class StorageProvider:
    provider_type = 'ABSTRACT'

    def put(self, object_class, object_id, value):
        raise NotImplementedError

    def get(self, object_class, object_id):
        raise NotImplementedError

    def exists(self, object_class, object_id):
        raise NotImplementedError

    def verify(self, object_class, object_id, expected_hash):
        raise NotImplementedError

class LocalStorageProvider(StorageProvider):
    provider_type = 'LOCAL'

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

    def verify(self, object_class, object_id, expected_hash):
        return self.manager.verify(object_class, object_id, expected_hash)

    def status(self):
        return {'provider_type': 'LOCAL', 'status': 'READY'}