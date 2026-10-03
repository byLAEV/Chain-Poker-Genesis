# Node Core — GPG Provider

## Purpose

This directory defines the Node Core integration boundary for GnuPG (GPG) keys and operations.

GPG is treated as an external cryptographic provider. Node Core may request key discovery, signing, verification, encryption, and decryption through a controlled adapter, but Node Core does not become the custodian of private GPG keys.

## Official references

- GnuPG: `gpg/gnupg`
- GPGME: `gpg/gpgme`

GnuPG is the complete OpenPGP implementation. GPGME is the application-facing C API for GnuPG and exposes high-level encryption, decryption, signing, signature verification, and key management.

## Architectural position

```text
Node Core
└── Cryptography
    └── GPG
        ├── provider contract
        ├── GnuPG adapter
        ├── GPGME integration boundary
        ├── key discovery
        ├── signing
        ├── verification
        ├── encryption
        └── decryption
```

## Private-key rule

Private GPG keys MUST remain under the external GnuPG key-management boundary.

Node Core MUST NOT:

- copy private keys into the repository;
- persist private keys in the Node Core ledger;
- expose private-key material through protocol APIs;
- treat the GPG keyring as a CPG wallet;
- embed passphrases in configuration;
- silently export private keys.

Node Core works with public-key metadata, fingerprints, signatures, canonical payloads, and verification results.

## Approval-signature use

GPG can be used as an approval signer for protocol operations:

```text
Protocol request
      ↓
Node Core canonical payload
      ↓
GPG approval request
      ↓
External GnuPG key / agent / smartcard boundary
      ↓
Detached signature
      ↓
Node Core verification
      ↓
Protocol acceptance
```

The signature proves authorization. It does not itself decide whether the protocol operation is valid.

## Important distinction from OpenPGP.js

OpenPGP.js already exists in Node Core as a JavaScript OpenPGP provider. This GPG component is a separate provider boundary for systems where the operating-system GnuPG stack, gpg-agent, smartcard, or external GPG key infrastructure is the required trust boundary.

The two providers MUST NOT create competing identity semantics.

## Status

**Architecture integrated. Production runtime adapter and hardware-backed GPG validation remain pending.**
