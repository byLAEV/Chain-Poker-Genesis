"""Node Core cryptography service boundary."""
from __future__ import annotations
from pathlib import Path
import importlib.util, sys
_SPEC=importlib.util.spec_from_file_location("node_core_crypto_primitives",Path(__file__).resolve().parent/"primitives.py")
_PRIM=importlib.util.module_from_spec(_SPEC); assert _SPEC and _SPEC.loader; sys.modules[_SPEC.name]=_PRIM; _SPEC.loader.exec_module(_PRIM)
class CryptoService:
    algorithm="SHA-256"
    def hash(self,data:bytes)->str: return _PRIM.sha256(data)
    def hmac(self,key:bytes,data:bytes)->str: return _PRIM.hmac_sha256(key,data)
    def merkle(self,items:list[bytes])->str: return _PRIM.merkle_root(items)
    def random(self,size:int=32)->bytes: return _PRIM.random_bytes(size)
    def derive_key(self,material:bytes)->bytes: return self.hash(b"NodeCore-Key-v1:"+material).encode()[:32]
