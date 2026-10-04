# Node Core Bootstrap Specification

**Project:** Chain Poker Genesis by LAEV  
**Layer:** Generic Node Core  
**Status:** Active implementation baseline  
**Version:** 0.1.0

## 1. Objective

Define a deterministic bootstrap procedure for a new node before any protocol is installed or associated.

## 2. Required Artifacts

A successful bootstrap creates:

- node identity metadata;
- node configuration;
- node state;
- canonical storage namespace;
- cryptographic metadata boundary;
- recovery metadata;
- installation manifest.

## 3. Bootstrap Procedure

### 3.1 Create workspace

The installer receives a clean target directory.

### 3.2 Validate environment

The reference implementation requires:

- a supported Python 3 runtime;
- writable target storage;
- no pre-existing conflicting manifest.

No CPG package is downloaded or installed.

### 3.3 Initialize identity

The reference bootstrap initializes identity metadata only. It does not generate production cryptographic keys or claim production identity conformance.

The bootstrap records:

`identity/status = INITIALIZED`

without claiming production key-management conformance.

### 3.4 Initialize storage

Create exactly the canonical logical namespace defined by the Node Core Installation Baseline.

### 3.5 Initialize state

Create node lifecycle state with:

`NODE_CORE_READY`

### 3.6 Initialize recovery metadata

Create an empty recovery record describing:

- recovery format version;
- last valid bootstrap state;
- recovery readiness.

### 3.7 Create installation manifest

The manifest references the node-core and storage versions and declares:

`protocol_associations = []`

and:

`cpg_protocol.status = NOT_INSTALLED`

### 3.8 Verify

The verifier checks:

- required directories;
- manifest structure;
- node readiness;
- CPG absence;
- manifest consistency.

## 4. Protocol Isolation

Protocol isolation is an installation invariant.

The bootstrap process must not:

- download CPG artifacts;
- import CPG engine code;
- create CPG ledger records;
- create CPG table state;
- establish CPG protocol membership.

The reserved `node-storage/protocol/` directory is an empty namespace boundary only.

## 5. State Model

```text
UNINITIALIZED
      |
      v
ENVIRONMENT_VALIDATED
      |
      v
IDENTITY_INITIALIZED
      |
      v
STORAGE_INITIALIZED
      |
      v
STORAGE_STRUCTURE_VERIFIED
      |
      v
INTEGRITY_VERIFIED
      |
      v
RECOVERY_READY
      |
      v
NODE_CORE_READY
```

Failure states are terminal for the current installation attempt and must be reported explicitly.

## 6. Deterministic Installation Result

The verifier returns a canonical result:

```json
{
  "status": "VERIFIED",
  "node_status": "NODE_CORE_READY",
  "cpg_protocol": "NOT_INSTALLED"
}
```

The exact canonical serialization is established by the reference verifier for this baseline and may later be superseded by the CPG-wide serialization specification.

## 7. Provider Boundary

IPFS/Kubo and other decentralized storage providers are represented through a provider boundary.

The Node Core baseline does not silently install a provider binary.

A provider may later transition from:

`NOT_PROVISIONED`

to:

`READY`

through a dedicated provider installation specification.

This preserves the distinction between installing the node substrate and installing a protocol.
