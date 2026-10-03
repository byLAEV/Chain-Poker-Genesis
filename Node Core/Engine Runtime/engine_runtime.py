"""Protocol-neutral engine runtime."""
from __future__ import annotations
from dataclasses import dataclass,field
@dataclass
class EngineRecord:
    name:str
    version:str
    state:str="REGISTERED"
@dataclass
class EngineRuntime:
    engines:dict[str,EngineRecord]=field(default_factory=dict)
    def register(self,name:str,version:str)->EngineRecord:
        if not name or not version: raise ValueError("engine name and version required")
        record=EngineRecord(name,version); self.engines[name]=record; return record
    def start(self,name:str)->None:
        self.engines[name].state="ACTIVE"
    def stop(self,name:str)->None:
        self.engines[name].state="STOPPED"
    def snapshot(self): return {k:vars(v).copy() for k,v in self.engines.items()}
