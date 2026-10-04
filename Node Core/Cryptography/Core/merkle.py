"""Deterministic protocol-neutral Node Core Merkle implementation.

Conforms to MERKLE-PROFILE-v1.0: SHA-256, domain-separated leaves/parents,
odd-node promotion, empty-tree root, and ordered proof verification.
"""
from __future__ import annotations
import hashlib
from dataclasses import dataclass
from typing import Sequence

LEAF_TAG=b"\x00"
PARENT_TAG=b"\x01"
EMPTY_TAG=b"\x02"
HASH_SIZE=32

def _h(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()

def leaf(data: bytes) -> bytes:
    if not isinstance(data,(bytes,bytearray,memoryview)):
        raise TypeError("leaf data must be bytes")
    return _h(LEAF_TAG+bytes(data))

def parent(left: bytes,right: bytes) -> bytes:
    if len(left)!=HASH_SIZE or len(right)!=HASH_SIZE:
        raise ValueError("Merkle child hash must be 32 bytes")
    return _h(PARENT_TAG+left+right)

def root(leaves: Sequence[bytes]) -> bytes:
    if not leaves:
        return _h(EMPTY_TAG)
    level=[bytes(x) for x in leaves]
    if any(len(x)!=HASH_SIZE for x in level):
        raise ValueError("Merkle leaves must be 32-byte hashes")
    while len(level)>1:
        nxt=[]
        for i in range(0,len(level),2):
            if i+1==len(level):
                nxt.append(level[i])
            else:
                nxt.append(parent(level[i],level[i+1]))
        level=nxt
    return level[0]

@dataclass(frozen=True)
class MerkleProof:
    siblings: tuple[bytes,...]
    directions: tuple[str,...]
    def __post_init__(self):
        if len(self.siblings)!=len(self.directions):
            raise ValueError("proof siblings and directions must have equal length")
        if any(len(x)!=HASH_SIZE for x in self.siblings):
            raise ValueError("proof sibling hash must be 32 bytes")
        if any(x not in {"L","R"} for x in self.directions):
            raise ValueError("proof directions must be L or R")

def build_proof(leaves: Sequence[bytes], index: int) -> MerkleProof:
    if not 0<=index<len(leaves):
        raise IndexError("Merkle leaf index out of range")
    level=[bytes(x) for x in leaves]
    if any(len(x)!=HASH_SIZE for x in level):
        raise ValueError("Merkle leaves must be 32-byte hashes")
    siblings=[]; directions=[]; i=index
    while len(level)>1:
        if i%2==0:
            if i+1<len(level):
                siblings.append(level[i+1]); directions.append("R")
        else:
            siblings.append(level[i-1]); directions.append("L")
        nxt=[]
        for j in range(0,len(level),2):
            nxt.append(level[j] if j+1==len(level) else parent(level[j],level[j+1]))
        level=nxt; i//=2
    return MerkleProof(tuple(siblings),tuple(directions))

def verify_proof(leaf_hash: bytes, proof: MerkleProof, expected_root: bytes) -> bool:
    if len(leaf_hash)!=HASH_SIZE or len(expected_root)!=HASH_SIZE:
        return False
    try:
        current=bytes(leaf_hash)
        for sibling,direction in zip(proof.siblings,proof.directions):
            current=parent(current,sibling) if direction=="R" else parent(sibling,current)
        return current==expected_root
    except (TypeError,ValueError):
        return False

__all__=["leaf","parent","root","MerkleProof","build_proof","verify_proof"]
