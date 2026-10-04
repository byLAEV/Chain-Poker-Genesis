# Node Core Cryptographic Test Vector Format

**Status:** Normative format v1.0
**Scope:** Portable cryptographic conformance vectors

## 1. Required fields
Each vector identifies id, profile, operation, inputs, expected result, and result class. Optional fields include description, version, negative_case, and failure.

## 2. Encoding
Vector files use UTF-8 JSON under the Canonical Serialization Profile. Binary values use lowercase hexadecimal unless another profile explicitly specifies otherwise.

## 3. Result classes
Allowed classes are PASS, REJECT, and ERROR. Negative vectors MUST identify the expected rejection or failure condition.

## 4. Required families
Vectors are required for SHA-256, canonical serialization, canonical hashing, Ed25519 signing and verification, altered payload, invalid signature, malformed key, CSPRNG failure, AEAD, and Merkle construction. AEAD and Merkle vectors become mandatory when their profiles are accepted.

## 5. Independence
Expected results for deterministic operations MUST be independently reviewed or generated from an independent reference and MUST NOT be derived solely from the implementation under test.

**Closure criterion:** format accepted and initial deterministic vectors defined; remaining families are pending until their profiles close.
