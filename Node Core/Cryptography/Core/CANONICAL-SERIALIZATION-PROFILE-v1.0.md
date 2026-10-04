# Node Core Canonical Serialization Profile

**Status:** Normative profile v1.0
**Scope:** Deterministic serialization of protocol objects consumed by Node Core cryptographic operations

## 1. Authority
This profile defines the canonical byte representation used before hashing, signing, commitments, authenticated encryption, or Merkle leaf construction.

## 2. Format
Canonical objects use JSON encoded as UTF-8. Object keys are ordered lexicographically. Insignificant whitespace is prohibited. Arrays preserve order. Unsupported values are rejected.

Floating-point numbers are prohibited. NaN, Infinity, and negative Infinity are rejected. Integers are preserved exactly. JSON escaping follows the JSON standard.

## 3. Cryptographic boundary
canonicalize(object) produces the UTF-8 byte sequence of the canonical JSON representation. Cryptographic operations over structured protocol objects MUST consume these bytes.

## 4. Failure semantics
Malformed objects, unsupported types, floating-point values, non-finite numbers, and serialization failures MUST fail closed. No silent coercion is permitted.

## 5. Required vectors
Vectors MUST cover key ordering, nested objects, array ordering, Unicode, escaping, integer preservation, floating-point rejection, non-finite rejection, unsupported types, and exact expected bytes.

## 6. Compatibility
Changes to ordering, escaping, numeric policy, encoding, or whitespace rules require a new profile version and an explicit compatibility decision.

**Closure criterion:** profile accepted, reference vectors committed, and implementation passes the vectors.
