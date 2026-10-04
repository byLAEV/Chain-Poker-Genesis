# Node Core Installation Baseline

**Project:** Chain Poker Genesis by LAEV  
**Layer:** Node Core  
**Status:** SUPPORTING / RECONCILED  
**Version:** 0.1.0  
**Protocol installation:** Explicitly excluded

## 1. Purpose

This document defines the implementation boundary for installing and bootstrapping a **protocol-neutral Node Core**.

The immediate objective is to make a machine capable of becoming a valid operational node substrate **without installing, activating, or executing Chain Poker Genesis**.

The Node Core exists before protocol association.

## 2. Hard Boundary

The installation phase covered here MUST NOT install or activate:

- Chain Poker Genesis Protocol Core;
- CPG poker rules;
- CPG table logic;
- CPG dealer logic;
- CPG settlement;
- CPG consensus;
- CPG Dedicated Ledger;
- CPG-specific P2P behavior;
- CPG-specific wallets;
- CPG-specific gameplay engines.

A successful installation must therefore be able to demonstrate:

`NODE_CORE_READY` while:

`CPG_PROTOCOL = NOT_INSTALLED`

## 3. Installation Layers

The baseline is divided into:

1. Installer Runtime
2. Environment Validation
3. Node Identity
4. Node Cryptographic Boundary
5. Node Configuration
6. Local Storage
7. Decentralized Storage Interface
8. Storage Synchronization Boundary
9. Integrity Verification
10. Recovery Metadata
11. Node Lifecycle
12. Readiness Verification

The baseline does not require a specific operating system, database, cloud provider, or protocol implementation.

## 4. Canonical Node Storage Namespace

The initial logical namespace is:

```text
node-storage/
├── identity/
├── cryptography/
├── configuration/
├── state/
├── records/
├── recovery/
└── protocol/
```

The `protocol/` directory exists as a reserved namespace boundary. Its presence does **not** mean that a protocol is installed.

The baseline installer must create an empty protocol namespace and record that no protocol association exists.

## 5. Installation Sequence

```text
UNINITIALIZED
      ↓
ENVIRONMENT_VALIDATED
      ↓
IDENTITY_INITIALIZED
      ↓
STORAGE_INITIALIZED
      ↓
STORAGE_STRUCTURE_VERIFIED
      ↓
INTEGRITY_VERIFIED
      ↓
RECOVERY_READY
      ↓
NODE_CORE_READY
```

Decentralized storage providers may be attached through a later provider adapter. Provider-specific installation is not part of the protocol layer.

## 6. Node Installation Manifest

Every successful bootstrap must produce a machine-readable node installation manifest containing at minimum:

- installation version;
- node identity reference;
- node-core version;
- storage-structure version;
- readiness state;
- protocol association list;
- CPG protocol status;
- canonical storage paths;
- integrity status;
- recovery status.

For an unassociated node:

```json
{
  "protocol_associations": [],
  "cpg_protocol": {
    "status": "NOT_INSTALLED"
  }
}
```

## 7. Readiness Levels

The baseline recognizes three levels:

### NODE_BOOTSTRAPPED

Local bootstrap completed and canonical structure exists.

### NODE_STORAGE_READY

Local storage and configured decentralized storage domains have passed their verification boundary.

### NODE_CORE_READY

The node has a valid identity, configuration, canonical storage substrate, integrity metadata, recovery metadata, and no protocol has been installed or associated.

A provider-dependent service may remain `NOT_PROVISIONED` until a compatible provider adapter is explicitly installed.

## 8. Integrity Boundary

The installation layer records integrity facts but does not silently invent a protocol trust root.

The following mechanisms remain separate specifications:

- signing authority;
- trust-anchor provisioning;
- key rotation;
- revocation;
- anti-rollback;
- remote-node authentication.

The installer must clearly report whether a value is:

- verified;
- not provisioned;
- unavailable;
- failed.

## 9. Failure Principle

A failed installation MUST NOT be reported as ready.

The verifier must fail closed for malformed manifests, missing required paths, invalid readiness state, or accidental CPG activation.

## 10. Acceptance Criteria

The Node Core Installation Baseline is satisfied when the reference bootstrap can:

1. create a clean node workspace;
2. create the canonical storage namespace;
3. create node configuration and identity metadata;
4. create recovery metadata;
5. produce a canonical installation manifest;
6. verify the manifest;
7. prove that CPG is not installed or associated;
8. report a deterministic readiness result.

## 11. Non-Goals

This baseline does not implement:

- poker;
- CPG consensus;
- CPG settlement;
- CPG ledger semantics;
- CPG networking;
- production distributed storage;
- production key management;
- protocol interoperability.

Those belong to later layers.

**Author:** Lerry Alexander Elizondo Villalobos — LAEV / byLAEV
