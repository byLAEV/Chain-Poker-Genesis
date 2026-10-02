# CPG Protocol

## Purpose

This directory contains the canonical implementation of the **Chain Poker Genesis (CPG) Protocol**.

CPG Protocol is installed and executed over the **Node Core**. It defines protocol-specific state, rules, engines and execution required for Chain Poker Genesis.

## Architectural Position

```text
Red de Nodos by LAEV
        │
        ▼
    Node Core
        │
        ▼
   CPG Protocol
        │
        ├── CPG protocol state
        ├── CPG ledger
        ├── consensus
        ├── cryptographic protocol services
        ├── reputation
        ├── time
        ├── poker / table rules
        ├── table lifecycle
        └── settlement
```

## Scope

This directory is intended for CPG-specific implementation including protocol initialization, protocol state, the dedicated CPG ledger, consensus, cryptographic protocol operations, reputation, protocol time, poker and table rules, player/seat state, table lifecycle, settlement, table-wallet protocol logic, table-viewer integration and CPG-specific manifests/execution models.

## Architectural Boundary

Generic node identity, storage interfaces and node runtime belong to **Node Core**. CPG-specific ledger state, consensus and table state belong here.

## Ledger Boundary

A node does not require a dedicated CPG ledger merely to exist as a node. The **CPG Protocol** introduces and manages the protocol-specific ledger required by Chain Poker Genesis.

## Cryptography Boundary

CPG Protocol may use cryptographic capabilities exposed by Node Core and define CPG-specific cryptographic operations. Private signing keys must not be embedded in the protocol implementation.

## Historical Source

Previous CPG material is preserved under `Main Temporal/`. Historical files should be audited and normalized before being promoted into this canonical directory.

## Development Rule

Every component added here should answer: **Is this behavior specific to the Chain Poker Genesis protocol?** If not, placement in Node Core or another repository-level component must be evaluated.

## Status

**Canonical architectural directory — implementation in progress.**
