"""Append-only local identity evidence store."""
from __future__ import annotations
import json
from pathlib import Path
class IdentityStore:
    def __init__(self,root:Path): self.root=Path(root); self.root.mkdir(parents=True,exist_ok=True)
    def put(self,name:str,record:dict)->Path:
        if not name or "/" in name or "\\" in name or ".." in name: raise ValueError("invalid identity record name")
        target=self.root/(name+".json")
        if target.exists(): raise FileExistsError("identity record already exists")
        target.write_text(json.dumps(record,sort_keys=True,separators=(",",":"),ensure_ascii=False),encoding="utf-8")
        return target
    def get(self,name:str)->dict:
        if not name or "/" in name or "\\" in name or ".." in name: raise ValueError("invalid identity record name")
        target=self.root/(name+".json")
        return json.loads(target.read_text(encoding="utf-8"))
