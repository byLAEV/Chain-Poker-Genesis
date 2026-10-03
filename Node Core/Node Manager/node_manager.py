"""Node Core Manager reference implementation."""
from __future__ import annotations
from dataclasses import dataclass,field
@dataclass
class NodeStatus:
    state:str="UNINITIALIZED"
    protocols:list[str]=field(default_factory=list)
    engines:list[str]=field(default_factory=list)
class NodeManager:
    def __init__(self): self.status=NodeStatus()
    def initialize(self)->NodeStatus:
        if self.status.state!="UNINITIALIZED": raise RuntimeError("node already initialized")
        self.status.state="INITIALIZED"; return self.status
    def activate(self)->NodeStatus:
        if self.status.state!="INITIALIZED": raise RuntimeError("node must be initialized")
        self.status.state="ACTIVE"; return self.status
    def register_engine(self,name:str)->None:
        if self.status.state!="ACTIVE": raise RuntimeError("node must be active")
        if name not in self.status.engines: self.status.engines.append(name)
    def install_protocol(self,name:str)->None:
        if not name or name=="Node Core": raise ValueError("invalid protocol")
        if name not in self.status.protocols: self.status.protocols.append(name)
    def snapshot(self): return {"state":self.status.state,"protocols":list(self.status.protocols),"engines":list(self.status.engines)}
