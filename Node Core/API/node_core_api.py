"""Minimal programmatic Node Core API facade."""
from __future__ import annotations
class NodeCoreAPI:
    def __init__(self,manager=None,storage=None):
        self.manager=manager; self.storage=storage
    def health(self)->dict: return {"service":"Node Core API","status":"READY"}
    def node_status(self)->dict: return self.manager.snapshot() if self.manager else {"state":"UNKNOWN"}
    def read(self,object_id:str): return self.storage.read(object_id) if self.storage else None
