# Node Core — OpenPGP Cryptography Provider

## Purpose

This directory contains the Node Core integration boundary for OpenPGP cryptographic operations.

OpenPGP is treated as a **cryptographic protocol/provider**, not as the identity model of Node Core and not as a CPG protocol engine.

## Architectural position

```text
Node Core
└── Cryptography
    ├── Core
    ├── Encryption
    ├── Decryption
    ├── Digital Signatures
    ├── Verification
    └── OpenPGP
        ├── Key Management
        ├── Encryption / Decryption Adapter
        ├── Signature Adapter
        └── Verification Adapter
```

The OpenPGP provider implements reusable cryptographic capabilities that other Node Core components may request through their defined interfaces.

## Upstream implementation

Canonical upstream project:

- Repository: `openpgpjs/openpgpjs`
- Release: `v6.3.2`
- License: LGPL-3.0-or-later
- Protocol: OpenPGP, implementing RFC 9580

The upstream implementation is consumed as a dependency. Its source is **not copied into Chain Poker Genesis**.

## Supported Node Core capabilities

The provider boundary covers:

- OpenPGP key parsing and generation;
- public/private key handling;
- encryption;
- decryption;
- digital signatures;
- signature verification;
- armored and binary OpenPGP message handling;
- cryptographic key metadata required by the provider;
- deterministic error classification at the Node Core boundary.

## Security boundary

Private keys MUST remain outside protocol state and MUST NOT be placed in CPG ledgers, table state, manifests, or public event records.

The provider may operate on externally supplied private-key material, but custody and persistence remain controlled by the Node Core key-management boundary and the storage/security policy.

## Non-goals

OpenPGP does not become:

- the CPG consensus algorithm;
- the CPG ledger encryption format by assumption;
- the player identity model by assumption;
- the table wallet;
- a replacement for the Node Core cryptographic primitives;
- a poker-specific cryptographic engine.

## Current integration status

**Provider boundary: established.**

**Pinned upstream dependency: established.**

**Production runtime wiring: pending Node Core runtime/package build integration and cryptographic test vectors.**
