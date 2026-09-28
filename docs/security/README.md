# Security Architecture

## Purpose

Security is a cross-cutting architecture layer covering identity, cryptography, code integrity, authorization, protocol participation, state integrity, replay, and failure handling.

This document provides the structured security boundary while the historical security documents are being reconciled.

## Security domains

### Identity

A participant requires a cryptographic identity capable of being represented and verified by the Node.

### Communication

Peer communication must provide mechanisms for authenticating participants and validating messages.

### Code integrity

The installation and execution path must distinguish:

- source/distribution origin;
- integrity measurement;
- verification;
- compatibility;
- accreditation/authorization;
- network participation.

These are separate security claims.

### Protocol authorization

Installing Chain Poker Genesis does not by itself establish permission to participate in every protocol or table.

Authorization must be represented through explicit protocol and table permission mechanisms.

### State integrity

Protocol state transitions and ledger records must be verifiable and replayable.

### Engine integrity

An engine must be identifiable by stable metadata sufficient to determine its compatibility and historical execution requirements.

Candidate metadata includes:

- ENGINE_ID
- ENGINE_VERSION
- PROTOCOL_COMPATIBILITY
- DEPENDENCIES
- INTERFACES
- CRYPTOGRAPHIC_REQUIREMENTS
- TIME_REQUIREMENTS
- REPLAY_REQUIREMENTS
- ACCREDITATION_STATUS

These fields are candidates, not yet frozen normative schema.

## Code accreditation model

The current architecture separates code distribution from network accreditation:

    Repository / Distribution
            ↓
        Installer
            ↓
      Node / Node Manager
            ↓
    Code Measurement / Verification
            ↓
    Accreditation Request
            ↓
       Main Consensus
            ↓
    Accreditation Decision
            ↓
    Protocol Participation

The exact accreditation mechanism remains to be extracted from the historical specifications.

## Dealer security

Dealer-related security is treated as a distinct security concern because the dealer/card-dealing path affects the integrity of game execution.

The historical corpus contains dedicated dealer and dealer-security documents. Those documents must be reconciled before selecting a cryptographic construction.

No specific cryptographic primitive is assumed by this README unless confirmed by the source specifications.

## Threat model

The threat model must eventually cover at minimum:

- invalid signatures;
- forged messages;
- unauthorized protocol access;
- manipulated engine code;
- incompatible engine versions;
- conflicting table state;
- replayed messages;
- duplicated messages;
- out-of-order messages;
- participant disconnection;
- failed commitment/reveal;
- settlement failure;
- attempted state manipulation.

## Historical source

- [22.0 Security Architecture Specification](../../22.0%20Security%20Architecture%20Specification.pdf)
- [23.0 Basic Infrastructure Installation](../../23.0%20Basic%20Infrastructure%20Installation.pdf)
- [25.0 Cryptographic Defense of the Dealer](../../25.0%20Cryptographic%20Defense%20of%20the%20Dealer.pdf)

## Status

Structured security layer. Normative cryptographic algorithms and security parameters remain pending source-level audit.
