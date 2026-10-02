# Installation and Dual-Storage Bootstrap Specification

**Chain Poker Genesis by LAEV**  
**Status:** Architectural specification  
**Version:** 1.0  
**Scope:** Local Node Storage + IPFS/Kubo Node Storage

## 1. Purpose

This specification defines the bootstrap relationship between the local storage domain of a Genesis Player Node and its IPFS/Kubo storage domain.

The design intentionally establishes the same canonical directory structure in both storage domains **before storage placement and distribution policies are configured**.

The objective is to make the storage system:

- structurally predictable;
- easier to inspect;
- easier to validate;
- resistant to ambiguous read/write placement;
- easier to diagnose when a storage state is incorrect;
- extensible for future implementations;
- compatible with later distribution and replication policies.

The principle is:

> **First establish the canonical structure. Then synchronize the two storage domains. Only after successful synchronization may storage placement and distribution rules be configured.**

## 2. Architectural Principle

The local storage and IPFS/Kubo storage domains are treated as two implementations of the same **Canonical Node Storage Structure**.

Conceptually:

`Canonical Storage Structure
        ↓
Local Storage Domain
        ↕
Synchronization / Verification
        ↕
IPFS/Kubo Storage Domain
        ↓
Storage Configuration
        ↓
Placement / Distribution / Replication`

The two domains must expose the same protocol-defined logical structure.

### Important distinction

“Exactly equal” refers to the **protocol-managed logical structure and its semantics**.

It does not require the internal physical database, blockstore, datastore, cache, lock files, or implementation-specific directories used internally by Kubo to be identical to the local filesystem.

Kubo's internal implementation remains an implementation detail.

The protocol-controlled storage namespace is canonical.

## 3. Canonical Storage Tree

The initial logical structure is:

```
node-storage/
├── identity/
├── cryptography/
├── configuration/
├── state/
├── records/
├── recovery/
└── protocol/
```

This structure is a protocol-level model.

Individual subdirectories may later contain additional canonical descendants, but new protocol-controlled paths must be introduced through a versioned storage specification.

## 4. Installation Order

The required bootstrap sequence is:

```
INSTALLATION
     ↓
CREATE CANONICAL STRUCTURE
     ↓
INITIALIZE LOCAL STORAGE
     ↓
INITIALIZE IPFS/KUBO STORAGE
     ↓
STRUCTURAL VERIFICATION
     ↓
CONTENT / MANIFEST SYNCHRONIZATION
     ↓
CROSS-STORAGE VERIFICATION
     ↓
STORAGE READY
     ↓
CONFIGURE PLACEMENT
     ↓
CONFIGURE DISTRIBUTION / REPLICATION
```

Configuration must not be used to compensate for an incomplete or inconsistent base structure.

## 5. Local Installation

During installation, the node creates the canonical local storage structure.

The installer must verify:

1. all required canonical directories exist;
2. no required directory is missing;
3. required directory names match the canonical specification;
4. required hierarchy is correct;
5. storage metadata identifies the applicable storage-structure version;
6. the resulting structure can be deterministically represented for verification.

The installer must distinguish:

- required protocol directories;
- optional implementation directories;
- implementation-private directories.

Implementation-private directories must not silently become protocol storage locations.

## 6. IPFS/Kubo Initialization

When the node's IPFS/Kubo storage domain is initialized, the protocol-controlled logical storage structure must be instantiated there as well.

The IPFS/Kubo domain must therefore expose an equivalent canonical namespace:

```
node-storage/
├── identity/
├── cryptography/
├── configuration/
├── state/
├── records/
├── recovery/
└── protocol/
```

The implementation may represent this namespace using IPFS directories, UnixFS objects, manifests, CIDs, or another compatible mechanism.

The representation must preserve the canonical hierarchy and semantics.

## 7. Structural Equality

For bootstrap purposes, the two storage domains are considered structurally synchronized only when:

- the canonical root exists in both domains;
- the storage-structure version matches;
- every required path exists in both domains;
- path types are compatible;
- canonical metadata is compatible;
- no required path is missing;
- no protocol-defined path is mapped to an incompatible location.

A successful directory creation alone is therefore insufficient.

## 8. Canonical Storage Manifest

The bootstrap process should maintain a canonical storage manifest describing the protocol-controlled structure.

Conceptually:

```
Storage Manifest
├── storage_structure_version
├── root_identifier
├── required_paths
├── path_types
├── semantic_classes
├── canonicalization_version
└── manifest_hash
```

The manifest provides a deterministic reference against which both storage domains can be checked.

The exact serialization and hashing mechanism must be defined by the canonical serialization and cryptographic specifications.

## 9. Synchronization Before Configuration

The two storage domains must reach a verified bootstrap state before the node is allowed to configure storage placement.

This creates a deliberate boundary:

**Bootstrap Structure**
→ **Synchronization**
→ **Verification**
→ **Configuration**

The node must not begin assigning records to local-only, IPFS-only, or dual-storage locations before this boundary is satisfied.

## 10. Read/Write Placement

After synchronization, the protocol may define placement policies such as:

| Storage policy | Local | IPFS/Kubo |
|---|---:|---:|
| Local-only | Yes | No |
| Distributed-only | No | Yes |
| Dual-storage | Yes | Yes |
| Replicated | Yes | Yes / additional nodes |
| Temporary | Policy-defined | Policy-defined |
| Reconstructible | Policy-defined | Policy-defined |
| Non-reconstructible | Policy-defined | Policy-defined |

The table is a policy model, not a default allocation.

The important rule is that placement decisions operate **inside an already synchronized canonical structure**.

## 11. Read and Write Safety

A future implementation must not decide read/write destinations solely from physical filesystem availability.

Each protocol-controlled record should have an explicit storage-placement classification.

Conceptually:

```
Record
  ↓
Storage Class
  ↓
Placement Policy
  ↓
Local / IPFS / Dual / Replicated
```

This prevents different components from independently deciding where the same record belongs.

The storage system should therefore have one authoritative placement decision for each record class.

## 12. Conflict Prevention

The dual-storage model is specifically intended to reduce future read/write ambiguity.

Potential conflicts include:

- a record existing locally but not in IPFS;
- a record existing in IPFS but not locally;
- different versions of the same record;
- different manifests;
- different storage-structure versions;
- simultaneous writes to both domains;
- stale replicas;
- incompatible serialization;
- an implementation writing outside its authorized storage class.

These conditions must be detectable.

The system should therefore distinguish at minimum:

- **SYNCED**
- **LOCAL_AHEAD**
- **IPFS_AHEAD**
- **DIVERGED**
- **STRUCTURE_MISMATCH**
- **VERSION_MISMATCH**
- **INVALID**

Exact transition rules belong to the future storage synchronization state machine.

## 13. Storage Is Not the Ledger

The existence of the canonical storage structure does not make every stored object part of the Chain Poker Genesis Dedicated Ledger.

The architecture must preserve the distinction:

**Storage**
= where protocol data is physically or logically represented.

**Dedicated Ledger**
= the protocol-owned record/history system defined by the CPG Protocol Core.

**Distribution Policy**
= rules determining where particular data is stored, replicated, or reconstructed.

A ledger record may use the storage system, but generic node storage must not automatically become the Dedicated Ledger.

## 14. Relationship to Node Core

The local and IPFS/Kubo storage bootstrap belongs to the Node Core infrastructure layer.

The Node Core establishes the node's storage substrate.

The CPG Protocol Core may subsequently use that substrate for protocol-specific resources, including the Dedicated Ledger.

Therefore:

```
Node Core
├── Local Storage
├── IPFS/Kubo Storage
├── Storage Synchronization
├── Storage Integrity / Recovery
└── Storage Configuration Boundary
        ↓
CPG Protocol Core
├── Protocol State
├── Tables
├── Hands
├── Events
└── Dedicated Ledger
```

## 15. Why the Structure Is Established Before Policy

The order is intentional.

If storage placement is configured before a canonical structure exists, different implementations may independently create different paths or interpretations.

If the structure is established first, then later questions become explicit:

- what data goes where;
- what is read locally;
- what is read from IPFS;
- what is written to both;
- what is replicated;
- what is temporary;
- what is reconstructible;
- what requires stronger persistence;
- what belongs to the Dedicated Ledger.

This turns storage configuration into a policy problem rather than a filesystem-discovery problem.

## 16. Future Implementation Requirements

Before production implementation, the following should be specified:

- canonical path registry;
- storage manifest schema;
- canonical serialization;
- manifest hashing;
- storage synchronization state machine;
- record placement schema;
- read policy;
- write policy;
- conflict detection;
- conflict resolution;
- atomicity requirements;
- recovery behavior;
- rollback;
- replication;
- retention;
- garbage collection;
- encryption boundaries;
- access-control boundaries;
- IPFS pinning policy;
- CID/version handling;
- offline behavior;
- storage migration;
- compatibility between storage-structure versions.

These items must be specified independently rather than inferred from the directory structure.

## 17. Bootstrap Acceptance Condition

A node may transition from **BOOTSTRAP** to **STORAGE_READY** only when:

1. the canonical local structure exists;
2. the canonical IPFS/Kubo structure exists;
3. both structures conform to the same storage-structure version;
4. required paths have been verified;
5. canonical metadata is compatible;
6. the synchronization check succeeds;
7. no unresolved structural divergence exists.

Only after this condition is satisfied may storage placement and distribution policies be activated.

## 18. Core Principle

The architectural rule established by this specification is:

> **The node first creates the same canonical storage structure in both storage domains, verifies that both domains represent that structure consistently, and only then determines how individual data classes are read, written, replicated, or distributed.**

This ordering is intentional future-proofing for implementations that may otherwise introduce storage conflicts or ambiguous ownership.

---

© 2026 Lerry Alexander Elizondo Villalobos (LAEV).  
Chain Poker Genesis by LAEV.
