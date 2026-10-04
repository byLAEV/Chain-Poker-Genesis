# Node Core Deterministic Merkle Profile

**Status:** Normative profile v1.0

## 1. Hash primitive
SHA-256 is the underlying hash function.

## 2. Domain separation
Leaf tag is byte 00. Parent tag is byte 01. Empty-tree tag is byte 02.

## 3. Leaf
For canonical serialized bytes B, leaf equals SHA-256 of leaf tag concatenated with B. Structured leaves MUST use the Canonical Serialization Profile.

## 4. Parent
For ordered child hashes L and R, parent equals SHA-256 of parent tag concatenated with L and R. Left/right order is significant and child hashes MUST NOT be sorted.

## 5. Odd nodes
An odd final node is promoted unchanged to the next level. It MUST NOT be duplicated.

## 6. Empty and single-leaf trees
Empty root equals SHA-256 of the empty-tree tag. A single-leaf root equals that leaf hash.

## 7. Proofs
A proof contains ordered sibling hashes and one left/right direction bit per level. Verification reconstructs the root using the exact parent rule.

## 8. Failure
Malformed proof lengths, invalid hash lengths, invalid direction data, and root mismatch MUST fail closed.

**Closure criterion:** profile accepted, independently generated root/proof vectors committed, and implementation passes them.
