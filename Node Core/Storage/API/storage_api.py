#!/usr/bin/env python3
"""Programmatic API boundary for Node Core Storage.

The API delegates to StorageManager and contains no independent persistence logic.
"""

from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "Storage Manager"))
from storage_manager import StorageManager

class StorageAPI:
    def __init__(self, node_root, *, kubo=None):
        self.manager = StorageManager(node_root, kubo=kubo)

    def create(self, object_class, object_id, data, *, mirror=True, encrypted=False):
        return self.manager.put(object_class, object_id, data, mirror=mirror, encrypted=encrypted)

    def read(self, object_class, object_id):
        return self.manager.get(object_class, object_id)

    def update(self, object_class, object_id, data, *, mirror=True, encrypted=False):
        return self.manager.update(object_class, object_id, data, mirror=mirror, encrypted=encrypted)

    def delete(self, object_class, object_id):
        return self.manager.delete(object_class, object_id)

    def locate(self, object_id):
        return self.manager.locate(object_id)

    def verify(self, object_class, object_id):
        return self.manager.verify(object_class, object_id)

    def synchronize(self, object_id):
        return self.manager.synchronize(object_id)

    def recover(self, object_id):
        return self.manager.recover(object_id)

    def status(self):
        return self.manager.status()
