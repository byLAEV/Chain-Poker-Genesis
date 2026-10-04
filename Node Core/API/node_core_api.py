"""Minimal protocol-neutral Node Core API facade.

The canonical API contract defines the surface; the manifest defines
implementation availability. This facade must not claim readiness it cannot
establish.
"""
from __future__ import annotations


class NodeCoreAPI:
    def __init__(self, manager=None, storage=None):
        self.manager = manager
        self.storage = storage

    def health(self) -> dict:
        if self.manager is None:
            return {"service": "Node Core API", "status": "UNKNOWN"}
        try:
            state = self.manager.snapshot().get("state", "UNKNOWN")
        except (AttributeError, TypeError):
            state = "UNKNOWN"
        return {"service": "Node Core API", "status": "READY" if state in {"READY", "RUNNING", "NODE_CORE_READY"} else state}

    def node_status(self) -> dict:
        return self.manager.snapshot() if self.manager else {"state": "UNKNOWN"}

    def read(self, object_id: str):
        if not isinstance(object_id, str) or not object_id:
            raise ValueError("object_id must be a non-empty string")
        if self.storage is None:
            return None
        return self.storage.read(object_id)
