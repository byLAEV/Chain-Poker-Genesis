# Node Core Bootstrap Contract

**Status:** CANONICAL
**Version:** 1.0.0
**Scope:** Fixed, protocol-neutral Node Core installation boundary

## 1. Purpose

Bootstrap creates and verifies the minimum Node Core substrate required before any protocol is installed or associated.

## 2. Canonical sequence

`UNINITIALIZED → ENVIRONMENT_VALIDATED → IDENTITY_INITIALIZED → STORAGE_INITIALIZED → STORAGE_STRUCTURE_VERIFIED → INTEGRITY_VERIFIED → RECOVERY_READY → NODE_CORE_READY`

The reference installer may execute these internally, but the resulting installation MUST satisfy the final invariants.

## 3. Installation invariants

A successful bootstrap MUST produce:

- identity metadata with no private-key generation claim;
- canonical Node Core storage namespace;
- validated configuration;
- node state;
- recovery metadata;
- installation manifest;
- integrity metadata.

The final state is `NODE_CORE_READY`.

## 4. Protocol isolation

A fresh bootstrap MUST produce:

`protocol_associations = []`

and:

`cpg_protocol.status = NOT_INSTALLED`

Bootstrap MUST NOT download, import, activate or execute CPG engines, consensus, ledger, poker rules, Table Wallet or settlement.

## 5. Boundaries

Bootstrap may initialize metadata for Identity, Configuration, Storage and Recovery.

It MUST NOT become the authority for:

- cryptographic private-key custody;
- protocol installation;
- protocol activation;
- protocol consensus;
- network synchronization;
- Runtime lifecycle after bootstrap completion.

## 6. Fixed installer

Bootstrap is a fixed installation substrate. Protocol engines are independently versioned and installed through Protocol Interface.

Bootstrap MUST NOT silently update itself or installed protocol engines.

## 7. Failure behavior

Missing required paths, malformed metadata, integrity mismatch, invalid configuration or protocol-isolation violation MUST fail closed.

A failed bootstrap MUST NOT be reported as `NODE_CORE_READY`.

## 8. Recovery

Recovery MUST be idempotent.

Repeating recovery against the same valid target MUST preserve the canonical installation invariants.

Recovery completion restores `NODE_CORE_READY`; the recovery operation may be reported separately as `RECOVERY_READY`.

## 9. Repeatability

Running initialization against an already valid installation MUST NOT silently overwrite existing canonical configuration, identity or state metadata.

## 10. Provider boundary

Bootstrap establishes the local provider baseline only. External decentralized-storage providers are not silently installed.

## 11. Verification

Canonical tests MUST verify:

1. clean bootstrap;
2. canonical paths;
3. identity metadata boundary;
4. configuration isolation;
5. CPG absence;
6. installation manifest;
7. integrity verification;
8. corrupted-artifact failure;
9. idempotent initialization;
10. repeatable recovery.
