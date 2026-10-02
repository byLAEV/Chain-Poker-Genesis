# Node

## Purpose

The Node is the operational and networking environment through which a participant can communicate with a decentralized network and execute a selected protocol.

Chain Poker Genesis must not be treated as synonymous with the Node.

## Boundary

    Individual
        ↓
    Node Manager
        ↓
    Node
        ├── Identity
        ├── Networking
        ├── Synchronization
        ├── Storage
        ├── Verification
        ├── Recovery
        └── Protocol Interface
                 ↓
           Selected Protocol
                 ↓
          Chain Poker Genesis

## Responsibilities

The generic Node boundary is expected to provide:

- cryptographic identity integration;
- peer-to-peer networking;
- network discovery;
- synchronization;
- persistence/storage services;
- verification services;
- recovery mechanisms;
- protocol execution interfaces;
- access to generic cryptographic services;
- access to network time services where required.

These responsibilities are intentionally separated from CPG-specific game logic.

## What does not belong to the generic Node

The generic Node must not implicitly contain:

- poker rules;
- table accounting semantics;
- CPG settlement rules;
- CPG table consensus;
- CPG-specific ledger semantics;
- a mandatory CPG wallet;
- CPG-specific engine implementations.

Those belong to the selected protocol or to protocol-defined interfaces.

## Node Manager relationship

The Node Manager is the control plane above the Node.

It may:

- configure the Node;
- manage identity;
- connect to networks;
- select protocols;
- install or manage engines;
- select compatible engine versions;
- request code verification/accreditation;
- inspect state;
- manage table participation;
- access historical/replay functions.

The Node Manager does not replace the Node's protocol-execution responsibilities.

## Protocol interface

The Node exposes a boundary through which a selected protocol can use generic network capabilities.

The interface must eventually define:

- message transport;
- peer identity;
- verification;
- synchronization;
- persistence;
- recovery;
- time;
- cryptographic services;
- protocol lifecycle;
- error reporting.

Exact interface schemas remain subject to historical-document audit.

## Security boundary

Node security must distinguish:

1. identity authenticity;
2. code integrity;
3. compatibility;
4. accreditation/authorization;
5. network participation.

A valid installation is not automatically equivalent to authorized participation.

## Historical reproducibility

The Node architecture must support execution and replay of historical protocol activity using the exact engine versions required by the recorded execution.

## Status

This is the structured architecture layer. Exact requirements are still being reconciled against the historical infrastructure and security PDFs.


## Current Implementation Baseline

The repository now defines an executable **Node Core Installation Baseline** that intentionally stops before protocol installation.

See:

- [Node Core Installation Baseline](INSTALLATION-BASELINE.md)
- [Node Core Bootstrap Specification](NODE-CORE-BOOTSTRAP-SPECIFICATION.md)
- [Node Readiness State Model](NODE-READINESS-STATE-MODEL.md)
- [Node Installation Manifest Schema](node-installation-manifest.schema.json)
- [Node Installation Test Vector](test-vectors/NODE-INSTALL-0001.json)
- [Node Installation Reference Implementation](../../reference-implementation/node-installation/README.md)

The acceptance boundary is:

`NODE_CORE_READY + CPG_PROTOCOL = NOT_INSTALLED + PROTOCOL_ASSOCIATIONS = []`

The installation workflow is validated automatically by GitHub Actions.


## Historical source

- [23.0 Basic Infrastructure Installation](../../23.0%20Basic%20Infrastructure%20Installation.pdf)
- [22.0 Security Architecture Specification](../../22.0%20Security%20Architecture%20Specification.pdf)
- [0.0 CHAIN POKER GENESIS — Digital Poker Protocol](../../0.0%20CHAIN%20POKER%20GENESIS__by%20LAEV__Digital%20Poker%20Protocol__.pdf)
