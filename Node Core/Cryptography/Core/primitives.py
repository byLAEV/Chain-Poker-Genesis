"""Protocol-neutral Node Core cryptographic primitives."""
from __future__ import annotations
import hashlib, hmac, secrets
def sha256(data: bytes) -> str: return hashlib.sha256(data).hexdigest()
def sha256_bytes(data: bytes) -> bytes: return hashlib.sha256(data).digest()
def random_bytes(size: int = 32) -> bytes: return secrets.token_bytes(size)
def hmac_sha256(key: bytes, data: bytes) -> str: return hmac.new(key,data,hashlib.sha256).hexdigest()
def merkle_root(items: list[bytes]) -> str:
    if not items: return sha256(b"")
    level=[sha256_bytes(x) for x in items]
    while len(level)>1:
        if len(level)%2: level.append(level[-1])
        level=[hashlib.sha256(level[i]+level[i+1]).digest() for i in range(0,len(level),2)]
    return level[0].hex()
