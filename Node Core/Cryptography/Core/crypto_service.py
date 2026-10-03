"""Node Core cryptography service boundary."""
from __future__ import annotations
import hashlib
from .primitives import sha256, hmac_sha256, merkle_root, random_bytes
class CryptoService:
    algorithm="SHA-256"
    def hash(self,data:bytes)->str: return sha256(data)
    def hmac(self,key:bytes,data:bytes)->str: return hmac_sha256(key,data)
    def merkle(self,items:list[bytes])->str: return merkle_root(items)
    def random(self,size:int=32)->bytes: return random_bytes(size)
    def derive_key(self,material:bytes)->bytes: return hashlib.sha256(b"NodeCore-Key-v1:"+material).digest()
