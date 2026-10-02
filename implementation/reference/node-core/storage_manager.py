#!/usr/bin/env python3
"""Protocol-neutral Node Core Storage Manager."""

from __future__ import annotations
import hashlib
import json
from pathlib import Path

STORAGE_VERSION = "0.1.0"

CLASS_DIRS = {
    "identity": "identity",
    "cryptography": "cryptography",
    "configuration": "configuration",
    "state": "state",
    "record": "records",
    "recovery": "recovery",
    "protocol-reserved": "protocol",
}

class StorageError(Exception):
    pass

class StorageManager:
    def __init__(self, node_root):
        self.node_root = Path(node_root).resolve()
        self.storage_root = (self.node_root / "node-storage").resolve()
        if not self.storage_root.is_dir():
            raise StorageError("node storage root does not exist")

    def _canonical_path(self, object_class, object_id):
        if object_class not in CLASS_DIRS:
            raise StorageError("unsupported object class")
        if not object_id or "/" in object_id or chr(92) in object_id or ".." in object_id:
            raise StorageError("invalid object id")
        if object_class == "protocol-reserved":
            raise StorageError("protocol-reserved storage is not writable by Node Core")
        path = (self.storage_root / CLASS_DIRS[object_class] / (object_id + ".json")).resolve()
        if self.storage_root not in path.parents:
            raise StorageError("object path escapes storage root")
        return path

    @staticmethod
    def _hash(data):
        return hashlib.sha256(data).hexdigest()

    def put_json(self, object_class, object_id, value):
        path = self._canonical_path(object_class, object_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")
        path.write_bytes(data)
        return {
            "object_id": object_id,
            "object_class": object_class,
            "relative_path": path.relative_to(self.node_root).as_posix(),
            "content_hash": self._hash(data),
            "content_encoding": "utf-8",
            "storage_version": STORAGE_VERSION
        }

    def get_json(self, object_class, object_id):
        path = self._canonical_path(object_class, object_id)
        if not path.is_file():
            raise StorageError("object not found")
        data = path.read_bytes()
        metadata = {
            "object_id": object_id,
            "object_class": object_class,
            "relative_path": path.relative_to(self.node_root).as_posix(),
            "content_hash": self._hash(data),
            "content_encoding": "utf-8",
            "storage_version": STORAGE_VERSION
        }
        return json.loads(data.decode("utf-8")), metadata

    def verify(self, object_class, object_id, expected_hash):
        _, metadata = self.get_json(object_class, object_id)
        return metadata["content_hash"] == expected_hash
