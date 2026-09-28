# Engine Evolution

## Purpose

This document structures the engine-evolution model of Chain Poker Genesis.

The central architectural principle is:

> The system grows through engines while preserving the protocol's ability to reproduce historical executions.

## Protocol and engine relationship

The protocol defines the stable execution environment and rules.

Engines provide independently evolving capabilities within that protocol.

    Stable Protocol
          ↓
    Engine Contracts
          ↓
    Engine Versions
          ↓
    Protocol Execution
          ↓
    Historical Record
          ↓
    Deterministic Replay

## Historical execution

A historical hand must not depend only on the current implementation.

A record must identify the engine versions and relevant protocol state required to reproduce the execution.

This prevents future engine evolution from destroying historical reproducibility.

## Compatibility

The repository should use explicit engine compatibility states rather than prematurely importing versioning concepts from unrelated protocol families.

Current candidate states:

- COMPATIBLE
- INCOMPATIBLE
- UPGRADE_REQUIRED
- VERSION_REQUIRED
- REPLAY_REQUIRED
- ACCREDITATION_REQUIRED
- UNSUPPORTED

These states are working terminology until the historical specification establishes the final vocabulary.

## Engine identity

An engine should eventually have stable machine-readable identity and compatibility metadata.

Candidate fields:

- ENGINE_ID
- ENGINE_VERSION
- PROTOCOL_COMPATIBILITY
- DEPENDENCIES
- INTERFACES
- REQUIRED_CAPABILITIES
- CRYPTOGRAPHIC_REQUIREMENTS
- TIME_REQUIREMENTS
- REPLAY_REQUIREMENTS
- ACCREDITATION_STATUS

The final schema must be derived from the formal engine-evolution specification rather than assumed from this working document.

## Evolution process

A future engine release should be evaluated through:

1. specification;
2. interface compatibility;
3. dependency validation;
4. security requirements;
5. deterministic behavior;
6. replay compatibility;
7. accreditation requirements;
8. simulation;
9. tests;
10. implementation.

## Failure classification

If engine evolution exposes an unresolved architectural condition, it must be recorded explicitly as one of:

- ERR_SPECIFICATION_GAP
- ERR_PROTOCOL_CONFLICT
- ERR_NON_DETERMINISTIC_BEHAVIOR
- ERR_IMPLEMENTATION_BLOCKER

## Historical source

- [34.0 Formal Specification of Engine Evolution](../../34.0%20Formal%20Specification%20of%20Engine%20Evolution.pdf)
- [0.0 CHAIN POKER GENESIS — Digital Poker Protocol](../../0.0%20CHAIN%20POKER%20GENESIS__by%20LAEV__Digital%20Poker%20Protocol__.pdf)

## Status

Working structured document pending complete source-level reconciliation.
