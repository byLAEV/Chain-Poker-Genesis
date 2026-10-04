# Node Core Cryptography

**Status:** IMPLEMENTED_PARTIAL / AEAD_VERIFIED / RECONCILED
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

Authenticated encryption (AEAD) is a required boundary in the formal profile. The normative production profile is `Core/ENCRYPTION-AEAD-PROFILE-v1.0.md`, which fixes AES-256-GCM, nonce/container parameters, HKDF-SHA-256 when explicitly required, and fail-closed authentication behavior. Implementation and independent vectors are VERIFIED by Node Core CI Run #605 on commit `815fa46cb8499a17dd1ea3fce9489628513ae967`.

Merkle construction is implemented as the normative deterministic Merkle profile `Core/MERKLE-PROFILE-v1.0.md`, with domain-separated SHA-256 leaves/parents, odd-node promotion, empty-tree handling and ordered proof verification. Independent conformance vectors are executed by `Tests/Cryptography/test_merkle.py`.

This component does not define CPG consensus, player state, table state, ledger rules, settlement, rake or protocol-specific cryptography.

The Cryptography component remains **PARTIAL** because Merkle and production cryptographic-security review remain open. The AEAD boundary itself is **IMPLEMENTED_VERIFIED**.
