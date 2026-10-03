# Node Core — USB Hardware Wallet Approval Signer

## Purpose

This component provides the Node Core boundary for an external HD hardware wallet connected through USB and used as an approval/signing element.

The hardware wallet is an **external signing authority**. Node Core does not own, persist, export, derive, or reconstruct the hardware wallet's private keys.

## Architectural position

```text
Node Core
└── Cryptography
    └── Hardware Wallet
        └── USB
            ├── Device Discovery
            ├── Device Identity
            ├── Approval Request
            ├── User Confirmation
            ├── Signature Transport
            └── Signature Verification
```

## Reference implementation

Primary generic Bitcoin hardware-wallet interface reference:

- Repository: `bitcoin-core/HWI`
- URL: https://github.com/bitcoin-core/HWI
- License: MIT
- Purpose: standard interface between software and hardware wallets without requiring application code to implement each device-specific driver.

HWI is Bitcoin-oriented. Therefore Node Core adopts its **hardware-wallet transport and signing boundary as a reference**, not as the definition of CPG approval semantics.

## Approval model

The correct flow is:

```text
Protocol / Node Core
      │
      │ approval request
      ▼
USB Hardware Wallet Adapter
      │
      │ display / user confirmation
      ▼
Hardware Wallet
      │
      │ signature
      ▼
USB Adapter
      │
      ▼
Node Core Verification
      │
      ▼
Protocol acceptance
```

A valid signature does not by itself authorize an operation. The requesting protocol determines what the signature authorizes and under which policy.

## Security boundary

The following MUST remain outside Node Core persistent storage:

- seed phrase;
- master private key;
- child private keys;
- exported private-key material;
- PIN/passphrase secrets.

Node Core MAY retain:

- public key / extended public key when required;
- device identifier;
- derivation-path metadata;
- signer capability metadata;
- approval request identifiers;
- signatures;
- verification results;
- audit references that do not expose secrets.

## HD wallet relationship

HD derivation remains a property of the external signing device. Node Core may request a public derivation result or a signature for a specific derivation path, but it MUST NOT recreate the device's private-key derivation internally merely to emulate the device.

## Current implementation status

- Hardware-wallet boundary: defined
- USB signer location: defined
- HWI reference: pinned conceptually as external reference
- Private-key custody boundary: defined
- Approval-signature flow: defined
- Production USB transport adapter: pending runtime implementation and device test vectors
