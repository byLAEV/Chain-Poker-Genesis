# Node Core GPG Signing Specification v1.0

## 1. Scope

Defines how Node Core may use GnuPG keys as an external approval-signature provider.

## 2. Canonical signing flow

```text
Object
  ↓
Canonical serialization
  ↓
Digest / signing payload
  ↓
Approval request
  ↓
GnuPG external signer
  ↓
Detached signature
  ↓
Node Core verification
```

## 3. Required binding

An approval signature SHOULD be bound to:

- protocol identifier;
- protocol version;
- operation identifier;
- request identifier;
- canonical payload digest;
- signer fingerprint;
- creation time where required;
- expiration where required;
- domain/context identifier.

## 4. Verification

Node Core MUST verify:

1. signature syntax;
2. cryptographic validity;
3. signer fingerprint;
4. expected public key;
5. canonical payload digest;
6. operation/request binding;
7. expiration/replay policy where applicable.

## 5. Key custody

Private keys remain outside Node Core. A GPG agent or hardware-backed smartcard integration may perform the private-key operation without exposing the private key to Node Core.

## 6. Protocol neutrality

GPG does not decide consensus, seating, settlement, rake, poker rules, or ledger acceptance. It only supplies cryptographic evidence.

## 7. Relationship with OpenPGP.js

OpenPGP.js and GnuPG are alternative OpenPGP providers. Node Core SHALL expose one provider-neutral cryptographic contract rather than allowing either provider to define identity semantics.
