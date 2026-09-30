# Developer Specifications and Manuals

This directory contains the technical specifications and developer manuals for the **Chain Poker Genesis by LAEV** repository and the infrastructure layers that support it.

## Base structure

```text
docs/
└── developer-specifications/
    ├── README.md
    ├── node-infrastructure/
    │   └── Unified Specification — Red de Nodos by LAEV — V1.7.md
    ├── storage/
    │   └── README.md
    ├── identity/
    ├── synchronization/
    ├── consensus/
    ├── recovery/
    ├── security/
    ├── engines/
    ├── APIs/
    ├── testing/
    └── integration/
```

## Architectural separation

```text
RED DE NODOS BY LAEV
        │
        ├── Node Infrastructure
        │   ├── Identity
        │   ├── Storage
        │   ├── State Manifest
        │   ├── Synchronization
        │   ├── Propagation
        │   ├── Proof of Functions
        │   ├── Backup / Recovery
        │   └── State Anchoring
        │
        ├── Consensus / Coordination
        │
        ▼
CHAIN POKER GENESIS
        ├── Poker Engines
        ├── Wallet Engines
        ├── Settlement Engines
        └── Application Components
```

The infrastructure specifications of the Red de Nodos by LAEV remain independent from Chain Poker Genesis. Higher-level protocols and engines consume these capabilities through defined APIs and contracts.

## Documentation directories

- `node-infrastructure/` — unified Red de Nodos infrastructure specification, including identity, storage, manifests, synchronization, propagation, Proof of Functions, backup/recovery, reconciliation, auditing, and state anchoring.
- `storage/` — local storage, metadata, policies, synchronization, recovery, and Kubo/IPFS integration.
- `identity/` — node cryptographic identity.
- `synchronization/` — synchronization and distribution.
- `consensus/` — coordination and consensus between nodes.
- `recovery/` — recovery, continuity, and backups.
- `security/` — cross-cutting security.
- `engines/` — specifications for installable engines.
- `APIs/` — interface contracts between layers.
- `testing/` — tests and acceptance criteria.
- `integration/` — integration between infrastructure, engines, and applications.

## Node Infrastructure Specification

The current unified infrastructure specification is:

**Red de Nodos by LAEV — Unified Specification of Storage, Identity, Reputation, Backup, Recovery, Propagation and State Anchoring Infrastructure — Version 1.7**

It formally includes **Proof of Functions (PoF)** and the initial five-node **Genesis Proof of Functions** model.

PoF remains separate from Proof of Work, consensus, synchronization, backup, recovery, external anchoring, and application validity.

## Status

This structure is the documentation baseline for developing formal specifications before implementing each component.
