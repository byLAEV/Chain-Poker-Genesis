"""Deterministic Node Core time reference service."""
from __future__ import annotations
import time
from dataclasses import dataclass
@dataclass(frozen=True)
class TimeRecord:
    sequence:int
    timestamp:int
    previous_hash:str|None
class TimeService:
    def __init__(self)->None: self.sequence=0; self.previous_hash=None
    def now(self)->int: return int(time.time())
    def record(self,timestamp:int|None=None)->TimeRecord:
        import hashlib, json
        ts=self.now() if timestamp is None else timestamp
        body={"sequence":self.sequence,"timestamp":ts,"previous_hash":self.previous_hash}
        digest=hashlib.sha256(json.dumps(body,sort_keys=True,separators=(",",":")).encode()).hexdigest()
        self.sequence+=1; self.previous_hash=digest
        return TimeRecord(body["sequence"],ts,digest)
