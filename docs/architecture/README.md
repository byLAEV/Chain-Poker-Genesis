# Chain Poker Genesis — Architecture

## Purpose

This document establishes the first structured architecture layer for Chain Poker Genesis by LAEV. It is derived from the historical design corpus preserved in the repository and is intended to become the navigation point for the implementation architecture.

The original PDF documents remain historical source material. This Markdown layer is not a replacement for those documents; it organizes the concepts into explicit system boundaries, interfaces, and dependencies.

## Architectural boundary

    Individual
        ↓
    Node Manager
        ↓
    Cryptographic Identity
        ↓
    Node / Decentralized Network
        ↓
    Selected Protocol
        ↓
    Chain Poker Genesis
        ↓
    Protocol Engines

## Primary layers

### Node

The node represents the operational/network participant. It provides generic network capabilities required to communicate, verify, synchronize, persist, recover, and execute protocol interfaces.

### Node Manager

The Node Manager is the control plane used to configure and operate a node. It is responsible for selecting protocols, managing engines and versions, observing node state, initiating verification/accreditation procedures, and managing protocol participation.

### Protocol

The protocol defines the rules and state transitions that constitute Chain Poker Genesis. The protocol consumes services exposed by the node rather than redefining the entire node architecture.

### Engines

Protocol functionality is decomposed into engines. Engines may evolve independently while the protocol's historical reproducibility is preserved.

### Ledger

The CPG Ledger is a protocol-specific subsystem for recording, verifying, and replaying protocol history and relevant state. It is not assumed to be a generic requirement of every node.

### Security

Security crosses all layers. Cryptographic identity, code verification, authorization, state integrity, engine compatibility, replay, and protocol participation must be specified at their respective boundaries.

## Core architectural principles

1. Node and protocol are separate architectural objects.
2. Node Manager is a control plane, not an identity and not the protocol.
3. Chain Poker Genesis is one protocol that can use a collection of engines.
4. Engines are independently evolvable components.
5. Historical protocol execution must remain reproducible.
6. The CPG Ledger is protocol-specific and must not be confused with generic node storage.
7. Main network consensus and table-level consensus are distinct concerns.
8. Interfaces must be explicit before implementation dependencies are fixed.
9. Cryptographic and time services should be consumed through defined interfaces.
10. Ambiguities discovered during specification or simulation must be recorded rather than silently resolved.

## Consensus boundary

    Node Network
        ↓
    Main Consensus
        ↓
    Chain Poker Genesis
        ↓
    Table Consensus

The exact algorithms and thresholds remain specification questions until verified against the historical documents.

## Documentation status

| Area | Status |
|---|---|
| Historical PDF preservation | Established |
| PDF mapping | Established |
| High-level architecture | Structured working layer |
| Normative extraction from every PDF | In progress |
| Machine-readable schemas | Not yet frozen |
| Reference implementation | Not started |
| Deterministic simulation | Planned |

## Historical sources

- [0.0 CHAIN POKER GENESIS — Digital Poker Protocol](../../0.0%20CHAIN%20POKER%20GENESIS__by%20LAEV__Digital%20Poker%20Protocol__.pdf)
- [CHAIN POKER GENESIS by LAEV](../../CHAIN%20POKER%20GENESIS%20by%20LAEV.pdf)
- [23.0 Basic Infrastructure Installation](../../23.0%20Basic%20Infrastructure%20Installation.pdf)
- [22.0 Security Architecture Specification](../../22.0%20Security%20Architecture%20Specification.pdf)
- [34.0 Formal Specification of Engine Evolution](../../34.0%20Formal%20Specification%20of%20Engine%20Evolution.pdf)

## Next refinement

This document becomes normative only after the historical PDFs are text-audited and cross-referenced. Conflicts, duplicated concepts, missing interfaces, and unresolved requirements must be recorded in the architecture audit rather than silently normalized.
