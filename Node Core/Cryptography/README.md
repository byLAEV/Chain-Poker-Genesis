# Node Core Cryptography

**Status:** IMPLEMENTED_PARTIAL / RECONCILED
**Version:** 1.2.0

This module is the protocol-neutral cryptographic execution boundary for Node Core.

## Implemented profile operations

- deterministic UTF-8 canonical serialization;
- SHA-256 hashing and canonical-object hashing;
- cryptographically secure random bytes;
- constant-time byte comparison;
- Ed25519 keypair generation;
- Ed25519 signing and verification;
- fail-closed malformed signature/key handling.

Private keys are accepted only as operation inputs and are not persisted by this module.

## Explicitly deferred

Authenticated encryption (AEAD) is a required boundary in the formal profile, but its production algorithm, nonce construction, key derivation and key lifecycle are not yet fixed by a separate encryption profile.

Merkle construction is intentionally not implemented as a normative primitive. A separate deterministic Merkle specification is required before tree behavior is fixed.

This component does not define CPG consensus, player state, table state, ledger rules, settlement, rake or protocol-specific cryptography.

The implementation remains **PARTIAL** until the AEAD profile and its test vectors are fixed and implemented.
