# Node Core OpenPGP Test Plan v1.0

## Purpose

Verify the OpenPGP provider boundary without coupling tests to CPG poker state.

## Required vectors

1. Generate a key pair.
2. Parse public and private keys.
3. Encrypt and decrypt text.
4. Encrypt and decrypt binary data.
5. Sign and verify an inline signed message.
6. Create and verify a detached signature.
7. Reject a signature made with a different key.
8. Reject altered ciphertext.
9. Reject an incorrect private-key passphrase.
10. Confirm private key material is not persisted by the provider.
11. Confirm provider operations are deterministic with respect to supplied inputs except for intentionally randomized cryptographic operations.
12. Confirm the provider remains independent of CPG protocol state.

## Security requirements

- Test fixtures MUST use dedicated test keys.
- Production private keys MUST NOT be committed to the repository.
- Passphrases MUST NOT be committed.
- Test output MUST NOT expose private-key material.
- Upstream OpenPGP.js security updates MUST be evaluated before dependency upgrades.

## Upstream reference

The provider targets OpenPGP.js v6.3.2. The upstream project exposes generation, parsing, encryption, decryption, signing and verification APIs used by this adapter.

## Status

**Plan established. Runtime execution requires a Node Core build/test environment.**
