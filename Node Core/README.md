# Node Core

## Purpose

This directory contains the canonical implementation of the **Node Core** for Chain Poker Genesis.

Node Core defines the node-level infrastructure required to participate in the **Red de Nodos by LAEV** independently of any specific application protocol.

## Architectural Boundary

Node Core is not the CPG Protocol. It provides the foundational node runtime and services over which protocols may be installed and executed.

```text
Red de Nodos by LAEV
        │
        ▼
    Node Core
        │
        ├── Cryptographic identity
        ├── Node runtime
        ├── Storage interfaces
        ├── Synchronization foundations
        ├── Integrity and recovery
        └── Protocol installation boundary
                │
                ▼
          CPG Protocol
```

## Scope

The canonical Node Core may contain node identity, runtime and lifecycle, local storage interfaces, synchronization foundations, integrity verification, recovery mechanisms, protocol installation/execution boundaries, network interfaces and deterministic node-level services.

## Non-Scope

Node Core must not contain CPG-specific poker rules, table state, table consensus, player seating, table wallet lifecycle, settlement/rake, CPG ledger semantics or table-viewer protocol logic. Those belong to **CPG Protocol** when protocol-specific.

## Design Principle

Node Core should remain usable as a node foundation without requiring Chain Poker Genesis to be installed.

## Historical Source

Previous implementation material is preserved under `Main Temporal/`. It is a source for audit, normalization and canonicalization, not automatically the final implementation.

## Repository Relationship

```text
Chain-Poker-Genesis/
├── Node Core/          ← node infrastructure
├── CPG Protocol/       ← CPG protocol implementation
├── Main Temporal/      ← preserved historical material
├── .github/            ← repository automation
└── .devcontainer/      ← development environment
```

## Status

**Canonical architectural directory — implementation in progress.**
