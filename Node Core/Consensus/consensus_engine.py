"""Protocol-neutral deterministic consensus infrastructure."""
from __future__ import annotations
import hashlib,json
class ConsensusEngine:
    VERSION="1.0"
    def canonical(self,value): return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
    def state_hash(self,state): return hashlib.sha256(self.canonical(state)).hexdigest()
    def validate_transition(self,previous,current): return isinstance(previous,dict) and isinstance(current,dict) and "state" in current
    def accept(self,previous,current):
        if not self.validate_transition(previous,current): raise ValueError("invalid consensus transition")
        return {"accepted":True,"previous_hash":self.state_hash(previous),"state_hash":self.state_hash(current)}
