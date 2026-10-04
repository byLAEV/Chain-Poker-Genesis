# Node Core Authenticated Encryption Profile

**Status:** Normative profile v1.0

## 1. Algorithm
The baseline AEAD algorithm is AES-256-GCM.

## 2. Parameters
Key size is 32 bytes. Nonce size is 12 bytes. Authentication tag size is 16 bytes. Plaintext and associated data are byte sequences subject to implementation limits.

## 3. Nonce
A nonce MUST be unique for every encryption performed with the same key. Nonce reuse is a protocol failure. Core MUST NOT derive a nonce silently from plaintext, timestamp, process state, or key material.

## 4. Container
The canonical ciphertext container is version, algorithm identifier, nonce, ciphertext, and tag. Version is 1. The algorithm identifier is the profile's unambiguous AES-256-GCM identifier.

## 5. Derivation
When derivation is explicitly required, HKDF-SHA-256 is the approved derivation primitive with explicit salt and profile-defined context. Long-term key lifecycle remains external.

## 6. Failure
Authentication failure MUST return a generic failure and MUST NOT expose unauthenticated plaintext. Malformed parameters MUST fail closed.

## 7. Vectors
Vectors MUST cover known plaintext, AAD, empty plaintext, modified ciphertext, modified tag, modified AAD, wrong key, nonce-reuse detection at the calling boundary, and malformed containers.

**Closure criterion:** profile accepted, independent AES-256-GCM vectors committed, and implementation conforms without plaintext exposure on authentication failure.
