# Node Core Formal Cryptographic Profile

**Status:** Normative profile v1.0  
**Scope:** Node Core cryptographic primitives and verification boundary

## 1. Purpose
Define the minimum deterministic cryptographic profile required by Node Core without binding CPG protocol semantics.

## 2. Required primitives
- SHA-256 for content hashing and integrity identifiers.
- Ed25519 for Node Core digital signatures.
- CSPRNG for cryptographic randomness.
- UTF-8 encoded canonical byte input for all defined operations.

## 3. Canonical serialization
JSON used for signed or hashed protocol objects MUST use:
- UTF-8;
- deterministic key ordering;
- no insignificant whitespace;
- explicit escaping;
- no floating-point values where canonical exactness is required.

The canonical serialization algorithm MUST be implemented and covered by test vectors before production signing is enabled.

## 4. Hashing
`SHA-256(input_bytes)` is the canonical content-hash operation.

Hexadecimal representation is lowercase when represented as text.

## 5. Digital signatures
Ed25519 is the baseline signature algorithm.

Verification MUST be performed over the exact canonical serialized byte sequence.

Node Core MUST distinguish:
- public key;
- signature;
- signed payload;
- key identifier;
- verification result.

## 6. Encryption
Node Core requires an authenticated-encryption boundary but does not treat encryption as a substitute for identity or signatures.

The production AEAD algorithm, nonce construction, key derivation, and key lifecycle MUST be fixed by a separate encryption profile before normative encryption implementation.

## 7. Merkle
Merkle construction is reserved for a separate deterministic Merkle specification. Node Core MUST NOT silently define tree padding, odd-node handling, domain separation, or leaf serialization beyond the hash primitive.

## 8. Key custody
Private keys MUST NOT be embedded in protocol state or manifests. Key custody is external to the cryptographic verification record.

## 9. Test vectors
Before declaring Cryptography Core production-ready, the repository MUST contain vectors for:
- SHA-256;
- canonical serialization;
- Ed25519 signing/verification;
- invalid signature;
- altered payload;
- malformed key;
- randomness failure handling;
- AEAD once its profile is fixed;
- Merkle construction once its specification is fixed.

## 10. Security invariants
- Never log private key material.
- Never treat an unverified signature as valid.
- Never silently downgrade algorithms.
- Never reinterpret bytes during verification.
- Fail closed on malformed cryptographic inputs.

## 11. CPG boundary
This profile defines infrastructure primitives only. It does not define CPG consensus, poker randomness, table state, settlement, or ledger cryptography.

## 12. Normative subordinate profiles
The following v1.0 profiles are part of the Cryptography Core contract closure:
- CANONICAL-SERIALIZATION-PROFILE-v1.0.md
- CRYPTO-TEST-VECTOR-FORMAT-v1.0.md
- CSPRNG-FAILURE-CONTRACT-v1.0.md
- KEY-LIFECYCLE-BOUNDARY-v1.0.md
- ENCRYPTION-AEAD-PROFILE-v1.0.md
- MERKLE-PROFILE-v1.0.md
- PRODUCTION-CRYPTOGRAPHIC-SECURITY-REQUIREMENTS-v1.0.md

These profiles close the previously open normative boundaries. Implementation and verification remain separate subsequent phases.
