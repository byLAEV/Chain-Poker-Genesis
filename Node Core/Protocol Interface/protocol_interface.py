"""Protocol-neutral Node Core protocol interface."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass(frozen=True)
class ProtocolDescriptor:
    protocol_id:str
    version:str
    engine_id:str
    manifest_hash:str
    capabilities:tuple[str,...]=()
    metadata:dict=field(default_factory=dict)

@dataclass
class ProtocolRecord:
    descriptor:ProtocolDescriptor
    state:str="DISCOVERED"
    registered_at:str=field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class ProtocolInterface:
    STATES={"DISCOVERED","COMPATIBLE","REGISTERED","INSTALLED","ACTIVE","SUSPENDED","REMOVED"}
    def __init__(self): self._records={}
    def discover(self,descriptor): self._records[descriptor.protocol_id]=ProtocolRecord(descriptor); return self._records[descriptor.protocol_id]
    def check_compatibility(self,protocol_id, node_capabilities=()):
        r=self._records[protocol_id]
        ok=set(r.descriptor.capabilities).issubset(set(node_capabilities))
        r.state="COMPATIBLE" if ok else "DISCOVERED"
        return ok
    def register(self,protocol_id):
        r=self._records[protocol_id]; r.state="REGISTERED"; return r
    def install(self,protocol_id):
        r=self._records[protocol_id]
        if r.state!="REGISTERED": raise RuntimeError("protocol must be registered before installation")
        r.state="INSTALLED"; return r
    def activate(self,protocol_id):
        r=self._records[protocol_id]
        if r.state!="INSTALLED": raise RuntimeError("protocol must be installed before activation")
        r.state="ACTIVE"; return r
    def suspend(self,protocol_id): self._records[protocol_id].state="SUSPENDED"; return self._records[protocol_id]
    def remove(self,protocol_id): self._records[protocol_id].state="REMOVED"; return self._records[protocol_id]
    def get(self,protocol_id): return self._records[protocol_id]
    def all(self): return tuple(self._records.values())
