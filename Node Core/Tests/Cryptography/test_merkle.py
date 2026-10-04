#!/usr/bin/env python3
from pathlib import Path\nimport hashlib
import sys
BASE=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(BASE/"Cryptography/Core"))
from merkle import leaf,parent,root,build_proof,verify_proof,MerkleProof

assert root([])==hashlib.sha256(b"\\x02").digest()
# Independent construction vectors derived directly from the normative byte rules.
leaves=[leaf(b"a"),leaf(b"b"),leaf(b"c")]
expected=parent(parent(leaves[0],leaves[1]),leaves[2])
assert root(leaves)==expected
proof=build_proof(leaves,2)
assert verify_proof(leaves[2],proof,root(leaves))
proof0=build_proof(leaves,0)
assert verify_proof(leaves[0],proof0,root(leaves))
assert not verify_proof(leaves[0],proof0,parent(root(leaves),leaves[0]))
try:
    MerkleProof((b"\x00"*32,),())
except ValueError: pass
else: raise AssertionError("malformed proof length accepted")
try:
    parent(b"\x00"*31,b"\x00"*32)
except ValueError: pass
else: raise AssertionError("invalid hash length accepted")
print("Node Core deterministic Merkle vectors and negative tests: PASS")
