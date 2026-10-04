"""Node Core security boundary and policy enforcement."""
from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class SecurityDecision:
    allowed:bool
    reason:str
class SecurityService:
    RESERVED_PREFIXES=("CPG/","Protocol/")
    def validate_path(self,path:str)->SecurityDecision:
        if not isinstance(path,str) or not path: return SecurityDecision(False,"invalid path")
        p=path.replace("\\","/")
        if p.startswith("/") or p.startswith("\\") or ".." in p.split("/"): return SecurityDecision(False,"unsafe path")
        if any(p.startswith(x) for x in self.RESERVED_PREFIXES): return SecurityDecision(False,"protocol-reserved path")
        return SecurityDecision(True,"accepted")
    def require(self,condition:bool,reason:str)->None:
        if not condition: raise PermissionError(reason)
