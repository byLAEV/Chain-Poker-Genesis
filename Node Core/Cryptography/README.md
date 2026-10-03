# Node Core Cryptography

**Status:** IMPLEMENTED
**Version:** 1.1.0

This module is the protocol-neutral cryptographic execution boundary for Node Core.

Implemented core operations:
- canonical serialization for deterministic cryptographic inputs;
- SHA-256 hashing;
- canonical-object hashing;
- cryptographically secure random bytes;
- constant-time byte comparison;
- Ed25519 keypair generation;
- Ed25519 signing and verification.

Private keys are accepted only as operation inputs and are not persisted by this module.

Cryptography does not define CPG consensus, player state, table state, ledger rules, settlement, or rake.

External cryptographic systems such as GPG/OpenPGP, hardware wallets, secp256k1 libraries, and libsodium remain provider/reference boundaries until an explicit adapter is implemented and tested.
