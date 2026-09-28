# Chain Poker Genesis Protocol

## Purpose

This document defines the architectural boundary of Chain Poker Genesis as a protocol executed by participating nodes.

The protocol is distinct from generic node infrastructure, the Node Manager, and any particular application or interface.

## Foundational identity

The historical source **0.0 CHAIN POKER GENESIS — Digital Poker Protocol** establishes the foundational distinction between Chain Poker Genesis and a conventional poker application.

Chain Poker Genesis is defined at protocol level: a set of rules, principles, structures, and interaction boundaries from which multiple compatible implementations, applications, or interfaces may be built.

Therefore:

```
Protocol
  ↓
Compatible implementations
  ↓
Applications / interfaces
```

An implementation may change without automatically changing the identity of the protocol, provided it remains compatible with the published specification.

## System position

```
Node Network
    ↓
Main Consensus
    ↓
Chain Poker Genesis Protocol
    ↓
Protocol Engines
    ↓
Table State / Table Consensus
    ↓
Settlement / Ledger Records
```

## Protocol responsibilities

The protocol layer is responsible for the rules and state transitions that define a Chain Poker Genesis execution.

This includes, subject to detailed specification audit:

- protocol access;
- table lifecycle;
- participant permissions;
- game state;
- engine coordination;
- card/dealing processes;
- commitment and reveal;
- betting/state transitions;
- table conflict handling;
- hand resolution;
- monetary settlement;
- protocol-specific ledger events;
- deterministic replay.

## Protocol vs. application

A poker application normally packages an interface and execution environment for users.

The protocol is the lower-level specification that defines the interoperable behavior expected from compatible implementations.

The protocol therefore does not require one particular:

- user interface;
- application;
- hosting provider;
- programming language;
- implementation;
- vendor.

The exact requirements for protocol compatibility must be established by the normative technical specifications.

## Engines

The protocol is decomposed into engines rather than treated as one monolithic implementation.

The historical corpus contains separate documents covering areas including installation, table creation, table joining, table wallet, commitment/reveal, card dealing, dealer behavior, poker rules, permissions, conflict resolution, disconnection management, settlement, governance, adoption, documentation, and other protocol services.

The exact engine boundaries will be frozen only after cross-document audit.

## Protocol stability and engine evolution

The current architecture follows the principle:

> The protocol should remain stable while the system grows through independently evolving engines.

Consequently, protocol compatibility must be evaluated against engine versions and dependencies rather than assuming that every system change constitutes a new protocol version.

See [Engine Evolution](../architecture/ENGINE-EVOLUTION.md).

## Consensus

Two distinct consensus scopes are currently recognized:

### Main consensus

Consensus among participating network identities/nodes.

### Table consensus

Consensus among participants in a specific poker table.

These scopes must not be conflated. The exact algorithms, thresholds, escalation rules, and evidence requirements remain pending formal extraction from the historical specifications.

## Ledger boundary

Settlement changes protocol state. The Ledger records and verifies the resulting protocol history/state.

```
Protocol State Machine
        ↓
Settlement State Transition
        ↓
Ledger Record
        ↓
Verification / Replay
```

The Ledger is not automatically equivalent to consensus.

## Determinism

A valid implementation must define sufficient information to reproduce a historical hand, including the relevant engine versions and protocol state.

Where deterministic replay cannot be defined, the specification must identify the missing information explicitly.

## Error classification

The architecture reserves explicit documentation for:

- ERR_SPECIFICATION_GAP
- ERR_PROTOCOL_CONFLICT
- ERR_NON_DETERMINISTIC_BEHAVIOR
- ERR_IMPLEMENTATION_BLOCKER

These are documentation/engineering classifications until their normative semantics are formally specified.

## Historical sources

- [0.0 CHAIN POKER GENESIS — Digital Poker Protocol](../../0.0%20CHAIN%20POKER%20GENESIS__by%20LAEV__Digital%20Poker%20Protocol__.pdf)
- [Historical audit of source 0.0](../history/00.0-CHAIN-POKER-GENESIS-DIGITAL-POKER-PROTOCOL.md)
- [CHAIN POKER GENESIS by LAEV](../../CHAIN%20POKER%20GENESIS%20by%20LAEV.pdf)
- [34.0 Formal Specification of Engine Evolution](../../34.0%20Formal%20Specification%20of%20Engine%20Evolution.pdf)

## Status

Working structured specification. The foundational protocol/application distinction is extracted from source 0.0. Normative technical details remain under historical-document audit.
