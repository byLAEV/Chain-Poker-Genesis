# Node Core Cryptography — External Authentication & OpenPGP References

This directory contains external repositories selected as implementation references for cryptographic login, challenge-response authentication, OpenPGP/GPG signing, signature verification, and identity association.

## Intended research model

The references are used to study and compare:

1. cryptographic challenge / response;
2. proof of possession of a private key without transferring the private key;
3. OpenPGP/GPG signing and verification;
4. mapping a verified key/fingerprint to a Node Core identity;
5. signing a Node Core record;
6. account or node association;
7. hardware-backed OpenPGP authentication.

## Important boundary

These repositories are REFERENCE ONLY.

They are not automatically part of the Node Core implementation and their semantics do not become CPG protocol rules.

The target Node Core flow to evaluate is:

CHALLENGE
→ SIGN WITH EXTERNAL KEY
→ VERIFY SIGNATURE
→ RESOLVE KEY / FINGERPRINT
→ ASSOCIATE WITH NODE IDENTITY
→ CREATE VERIFIED IDENTITY BINDING
→ AUTHORIZE OPERATION

For record signing:

RECORD
→ CANONICALIZE
→ HASH / DIGEST
→ EXTERNAL SIGNATURE
→ VERIFY
→ STORE SIGNATURE EVIDENCE

Private keys must remain outside the Node Core process unless an explicitly defined secure provider boundary permits hardware-backed signing.

## License and provenance

Do not copy third-party source code into Node Core until its license, copyright requirements, dependencies and compatibility have been reviewed.
