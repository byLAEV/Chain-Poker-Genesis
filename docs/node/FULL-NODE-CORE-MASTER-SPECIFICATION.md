# Full Node Core Master Specification

**Project:** Chain Poker Genesis by LAEV  
**Author:** Lerry Alexander Elizondo Villalobos — LAEV / byLAEV  
**Status:** Architectural master specification  
**Scope:** Full autonomous Node Core / Red de Nodos substrate before CPG Protocol association  

## 1. Purpose

This document freezes the scope of the **Full Node Core** so that implementation is driven by the repository's architecture rather than by incremental assumptions.

The Full Node Core is the autonomous substrate on which higher-level protocols, including Chain Poker Genesis, may later operate.

The Full Node Core must be operational before CPG Protocol association.

## 2. Architectural Boundary

```text
FULL NODE CORE
│
├── Node Identity
├── Cryptographic Core / Key References
├── Configuration
├── Local Storage
├── Decentralized Storage (IPFS/Kubo)
├── Storage Manager
├── Storage Policy Engine
├── Object Registry
├── Storage Locator
├── Storage Manifest
├── Synchronization Engine
├── Durable Operation Queue / Retry
├── Recovery / Integrity
├── Runtime Lifecycle
├── Health / Readiness
├── Node Networking Substrate
├── Capability Discovery
├── Propagation / Peer Evidence
└── Proof of Functions / Node Evidence
        │
        ▼
PROTOCOL ASSOCIATION BOUNDARY
        │
        ▼
CHAIN POKER GENESIS PROTOCOL CORE
```

The CPG Dedicated Ledger, poker semantics, protocol consensus, settlement, and protocol-specific state do not belong to the Full Node Core.

## 3. Storage Domains

The Full Node Core has two logical storage domains:

1. **Local Node Storage** — directly controlled persistent storage.
2. **Decentralized Node Storage** — initially represented through IPFS/Kubo.

The domains share a canonical logical namespace but may use different physical implementations.

## 4. Bootstrap Contract

The mandatory installation order is:

```text
INSTALLATION
→ ENVIRONMENT VALIDATION
→ NODE IDENTITY INITIALIZATION
→ CANONICAL STORAGE STRUCTURE
→ LOCAL STORAGE INITIALIZATION
→ IPFS/KUBO INITIALIZATION
→ STRUCTURAL VERIFICATION
→ STORAGE MANIFEST GENERATION
→ LOCAL/IPFS SYNCHRONIZATION
→ CROSS-STORAGE VERIFICATION
→ RECOVERY / INTEGRITY VERIFICATION
→ NETWORK / CAPABILITY READINESS
→ PROOF OF FUNCTIONS
→ NODE READY
→ CPG ASSOCIATION ALLOWED
```

No protocol association is permitted before `NODE READY`.

## 5. Canonical Storage Structure

The protocol-controlled logical namespace begins with:

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

The same logical structure must be representable in the local and IPFS/Kubo domains.

## 6. Storage Management

All higher-level components must use the Storage API / Storage Manager boundary.

The Storage Manager coordinates object creation, retrieval, update, deletion, classification, verification, synchronization preparation, recovery, and quarantine.

The Storage Policy Engine determines placement and behavior. Storage implementation details must not leak into higher-level protocols.

## 7. Object and Manifest Integrity

Each managed object must have separable identifiers for:

- logical object identity;
- operation identity;
- version;
- content hash;
- CID where decentralized storage is used.

The canonical storage manifest is the deterministic reference for the controlled storage structure.

## 8. Synchronization

Synchronization is a distinct subsystem and is not equivalent to storage, distribution, replication, or publication.

At minimum, synchronization must detect:

- synced state;
- local-ahead state;
- IPFS-ahead state;
- divergence;
- structure mismatch;
- version mismatch;
- invalid state;
- retryable failure;
- terminal failure.

The synchronization implementation must be durable and recoverable.

## 9. Recovery and Integrity

The Node Core must preserve local integrity when IPFS or network services are unavailable.

Recovery must be based on durable metadata, manifests, operation records, integrity checks, and reconciliation rather than directory movement alone.

## 10. Networking and Capability Discovery

The Full Node Core includes a protocol-neutral networking substrate and capability-discovery boundary.

Networking must remain independent of CPG semantics.

Capability evidence must describe whether the node can perform the required Node Core functions without implying CPG membership.

## 11. Proof of Functions

The Full Node Core must eventually produce machine-verifiable evidence for the functions that determine `NODE READY`, including storage, integrity, synchronization, recovery, networking/capability readiness, and protocol-boundary isolation.

PoF is evidence of Node readiness; it is not CPG consensus.

## 12. Explicit Non-Goals

The Full Node Core does not install or activate:

- CPG Protocol Core;
- CPG Dedicated Ledger;
- poker tables/hands/events;
- protocol consensus;
- settlement coordination;
- protocol-specific distribution policy;
- CPG membership.

## 13. Completion Gate

`FULL_NODE_CORE_COMPLETE` may only be declared when every mandatory requirement in the Full Node Core Gap Matrix is:

- implemented;
- automatically tested;
- CI verified;
- reconciled to its source specification;
- and compatible with the CPG isolation boundary.

Any `DOCUMENTED_NOT_EXECUTED`, `CONFLICT_OR_SCOPE_GAP`, or `UNRESOLVED` mandatory item blocks completion.

## 14. Source Authority

This master specification consolidates the repository's Node architecture, dual-storage bootstrap specification, storage infrastructure specification, installation-engine specification, Node Core verification artifacts, and related Node documentation.

Historical source documents remain authoritative for unresolved historical requirements until explicitly reconciled.

---

**Master invariant:** The Node provides the autonomous substrate. The protocol provides semantics. The ledger belongs to the protocol. CPG association occurs only after the Node Core has independently reached a verified ready state.
