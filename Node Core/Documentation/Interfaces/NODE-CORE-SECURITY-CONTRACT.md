# Node Core Security Contract

**Status:** CANONICAL  
**Version:** 1.0.0  
**Scope:** Protocol-neutral executable security boundary

## 1. Purpose

Security Service enforces Node Core security boundaries and fail-closed policy checks. It does not replace Identity, Cryptography, Storage, Runtime, Network or Protocol Interface.

## 2. Canonical security boundaries

Security governs:

- identity boundary;
- credential boundary;
- configuration boundary;
- storage/path boundary;
- runtime/process boundary;
- engine boundary;
- protocol boundary;
- network boundary;
- recovery boundary;
- audit boundary.

## 3. Required baseline controls

The reference security boundary MUST enforce:

- least privilege;
- fail-closed validation;
- path traversal prevention;
- protocol-reserved path protection;
- sensitive-data non-disclosure;
- explicit trust configuration;
- authorization for protected operations;
- protocol isolation.

## 4. Path policy

The Node Core Security Service MUST reject:

- absolute paths;
- path traversal components;
- protocol-reserved prefixes.

The reference reserved prefixes are:

`CPG/`
`Protocol/`

Acceptance of a path does not grant permission to perform the operation.

## 5. Authorization

Protected operations MUST fail closed when their authorization condition is false.

Security Service MUST NOT silently elevate privileges.

## 6. Cryptographic boundary

Security Service does not define cryptographic algorithms.

Algorithm selection, hashing, signatures, encryption/decryption and key operations belong to the Cryptography contract.

Private-key custody/signing authority remains outside ordinary Node Core Security Service unless explicitly authorized by a credential profile.

## 7. Protocol isolation

Security Service MUST reject Node Core operations that attempt to bypass the Protocol Interface or directly modify protocol-reserved state.

Security MUST NOT implement CPG consensus, ledger, poker rules, Table Wallet, settlement or rake.

## 8. Failure behavior

Malformed or unauthorized security-sensitive operations MUST fail closed.

No security check may return success when its required condition is false.

## 9. Implementation status

The security manifest declares:

`IMPLEMENTED_PARTIAL`

Currently implemented baseline controls:

- path policy;
- permission guard;
- external key custody boundary.

Not yet implemented:

- security audit log;
- secure configuration enforcement.

This contract therefore defines the canonical boundary without claiming full Security implementation.

## 10. Verification

Canonical Security tests MUST verify:

1. path traversal rejection;
2. protocol-reserved path rejection;
3. safe path acceptance;
4. authorization failure;
5. authorization success;
6. no private-key exposure;
7. protocol isolation;
8. implementation availability remains consistent with the manifest.
