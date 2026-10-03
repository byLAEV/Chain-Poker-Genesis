# Node Core

## Overview

**Node Core** is the foundational, protocol-agnostic node infrastructure of the **Red de Nodos by LAEV** within the Chain Poker Genesis repository.

It defines the components and boundaries required for a node to exist, initialize, identify itself, operate, communicate, store and verify information, execute node-level services, and provide a controlled interface through which independent protocols may be installed and executed.

Node Core is infrastructure first. It is **not the CPG Protocol** and does not contain application-specific poker logic.

## Architectural Position

\`\`\`text
Red de Nodos by LAEV
        │
        ▼
    Node Core
        │
        ├── Bootstrap
        ├── Identity
        ├── Node Manager
        ├── Configuration
        ├── Runtime
        ├── Engine Runtime
        ├── Cryptography
        ├── Consensus
        ├── Time
        ├── Storage
        ├── Network
        ├── Security
        ├── API
        ├── CLI
        ├── Tests
        └── Protocol Interface
                │
                ▼
        Independent Protocols
                │
                ▼
          CPG Protocol
\`\`\`

The protocol boundary is intentional: Node Core provides the node infrastructure; a protocol uses that infrastructure without redefining the node itself.

## Architectural Boundary

### Node Core provides

Node Core may define and implement node-level infrastructure for:

- node bootstrap and initialization;
- node identity and cryptographic identity management;
- node lifecycle and runtime;
- configuration and operational state;
- engine loading and execution at the node level;
- cryptographic primitives and cryptographic services;
- node-level consensus foundations;
- deterministic time services;
- local and decentralized storage interfaces;
- network communication foundations;
- integrity, security and recovery mechanisms;
- command-line and API interfaces;
- protocol installation and execution boundaries;
- node-level testing and verification.

### Node Core does not define

The following are outside the Node Core boundary when they are protocol-specific:

- poker rules;
- Texas Hold'em / NLHE game logic;
- table state;
- player seating;
- table consensus;
- table wallet lifecycle;
- settlement;
- rake;
- CPG ledger semantics;
- CPG-specific reputation rules;
- CPG-specific viewer logic;
- poker-specific protocol state machines.

Those concerns belong to the **CPG Protocol** or to their respective protocol-level components.

## Core Principle

> **Node Core must remain usable as node infrastructure without requiring Chain Poker Genesis protocol logic.**

A node may provide infrastructure for multiple protocols while each protocol maintains its own rules, state, engines, manifests and execution semantics.

## Node Lifecycle

The intended architectural lifecycle is:

\`\`\`text
Bootstrap
    │
    ▼
Initialization
    │
    ▼
Cryptographic Identity
    │
    ▼
Configuration
    │
    ▼
Node Runtime
    │
    ├── Network
    ├── Storage
    ├── Cryptography
    ├── Time
    ├── Security
    └── Node-level Engines
    │
    ▼
Protocol Interface
    │
    ▼
Protocol Installation / Execution
\`\`\`

The exact implementation of each stage remains subject to the implementation and verification work of the corresponding component.

## Core Components

The current Node Core structure establishes the following architectural areas:

| Component | Architectural responsibility |
|---|---|
| \`Bootstrap/\` | Node installation, initialization, verification and recovery foundations. |
| \`Identity/\` | Cryptographic node identity and identity management. |
| \`Node Manager/\` | Node-level management and coordination. |
| \`Configuration/\` | Node configuration and operational parameters. |
| \`Runtime/\` | Core node lifecycle and runtime services. |
| \`Engine Runtime/\` | Loading, controlling and executing node-level engines. |
| \`Cryptography/\` | Cryptographic primitives and services required by the node. |
| \`Consensus/\` | Node-level consensus foundations, independent of application-specific consensus. |
| \`Time/\` | Deterministic and node-level time services. |
| \`Storage/\` | Storage interfaces and node-level storage foundations. |
| \`Network/\` | Network communication and node connectivity foundations. |
| \`Security/\` | Node security, integrity and protection mechanisms. |
| \`API/\` | Programmatic interface to Node Core services. |
| \`CLI/\` | Command-line interface for node operations. |
| \`Protocol Interface/\` | Controlled boundary between Node Core and external protocols. |
| \`Tests/\` | Verification and validation of Node Core behavior. |
| \`Documentation/\` | Node Core technical and architectural documentation. |

These directories establish the current structural architecture. Their presence does not by itself imply that every component is fully implemented.

## Protocol Interface

\`Protocol Interface/\` is a critical architectural boundary.

A protocol should not need to become part of the Node Core implementation merely because it runs on a node.

The interface is intended to provide a controlled mechanism for:

1. identifying a protocol;
2. validating protocol compatibility;
3. installing or loading protocol components;
4. providing required Node Core services;
5. executing protocol-defined engines;
6. maintaining separation between node state and protocol state;
7. preventing protocol-specific logic from becoming embedded in Node Core.

For Chain Poker Genesis:

\`\`\`text
Node Core
    │
    │ infrastructure
    ▼
Protocol Interface
    │
    │ protocol boundary
    ▼
CPG Protocol
\`\`\`

## Cryptographic Boundary

Node Core provides cryptographic infrastructure required by the node.

This may include:

- hashing;
- encryption and decryption services;
- signature verification;
- key-related interfaces;
- integrity verification;
- cryptographic identity support;
- Merkle-related primitives where required by node infrastructure.

Private keys and protocol-specific custody models must not be assumed to belong to Node Core simply because cryptographic services exist here.

Cryptography is infrastructure; custody and transaction semantics belong to the component or protocol that defines them.

## Storage Boundary

Node Core provides storage interfaces and foundations required for node operation.

Storage architecture must remain distinguishable from protocol-specific data semantics.

\`\`\`text
Node Core Storage
        │
        ├── node infrastructure
        ├── local storage interfaces
        ├── decentralized storage interfaces
        └── integrity / recovery foundations
                    │
                    ▼
             Protocol Storage
                    │
                    └── protocol-defined data
\`\`\`

The existence of storage within Node Core does not mean that Node Core owns the ledger or state model of CPG.

## Consensus Boundary

Node Core may provide consensus infrastructure required at the node level.

This must remain separate from application-specific consensus.

\`\`\`text
Node-level consensus
        ≠
CPG table consensus
        ≠
CPG protocol state agreement
\`\`\`

The CPG Protocol may use Node Core capabilities while retaining responsibility for its own protocol-specific consensus rules.

## Manifest

\`NODE-CORE-MANIFEST.json\` is the structural manifest for this directory.

Its current definition identifies Node Core as:

- protocol-agnostic node infrastructure;
- an independent Node Core layer;
- having no direct protocol dependency;
- a structural layer within the repository.

The manifest and this README should remain consistent. If the architecture changes, both should be reviewed together.

## Relationship to Chain Poker Genesis

The repository separates infrastructure from protocol implementation:

\`\`\`text
Chain-Poker-Genesis/
│
├── Node Core/
│   └── Node infrastructure
│
├── CPG Protocol/
│   └── Chain Poker Genesis protocol
│
├── Main Temporal/
│   └── Historical / preserved material
│
├── .github/
│   └── Repository automation
│
└── .devcontainer/
    └── Development environment
\`\`\`

The CPG Protocol is therefore a protocol operating on the node infrastructure rather than the definition of the node itself.

## Historical Material

Historical implementation material may be preserved under \`Main Temporal/\`.

Historical material is retained for:

- audit;
- comparison;
- recovery of design decisions;
- normalization;
- canonicalization;
- implementation reference.

Historical code or documentation must not automatically be treated as the canonical Node Core implementation.

## Implementation Status

**Status: Structural definition / implementation in progress**

The current directory establishes the intended Node Core architecture and component boundaries.

Structural presence must not be interpreted as functional completion.

Implementation should proceed through explicit review, normalization, canonicalization, verification and testing of each component.

## Design Rule

The central architectural rule of Node Core is:

> **Node Core provides the node. Protocols provide their protocols.**

Chain Poker Genesis may use Node Core, but CPG-specific rules and state must remain outside the Node Core boundary unless a future architectural decision explicitly reclassifies a component as node infrastructure.

## Repository Ownership

This Node Core architecture is part of the Chain Poker Genesis project by **LAEV**.
