# Node Core — Zero-Knowledge Verification

## Purpose

This directory defines the Node Core boundary for zero-knowledge proof verification.

Zero-knowledge verification is implemented here as an **identity / verification capability of Node Core**, not as a poker engine and not as a CPG-specific protocol implementation.

## Architectural position

```text
Node Core
  │
  └── Identity
       │
       └── Verification
            │
            └── Zero-Knowledge
                 ├── adapter contract
                 ├── proof-system adapters
                 ├── public-input validation
                 └── deterministic verification result
```

The component is intentionally placed below `Identity/Verification/` because a zero-knowledge proof is evidence used to establish a requested property. The proof system itself is a cryptographic mechanism; the meaning of the property remains owned by the requesting protocol.

## Boundary

Node Core SHALL provide:

- a stable ZK verifier interface;
- proof envelope validation;
- public-input validation;
- verification-key selection and integrity checks;
- deterministic verification results;
- replay/context checks where required by the Node Core verification contract;
- error classification;
- test and reference integration boundaries.

Node Core SHALL NOT define:

- poker rules;
- Texas Hold'em state;
- card dealing semantics;
- table state;
- player seating;
- table consensus;
- settlement or rake;
- CPG-specific proof statements.

Those concerns belong to the protocol using Node Core.

## Reference integration

The initial technical reference is:

- Repository: `candrea-rares/Decentralized-Zero-Knowledge-Poker`
- Branch: `main`
- Pinned commit: `c6ca40add20945615eb1442c9ef41cf2c03e82d5`
- Proof family described by the reference: Groth16 / Circom
- Reference primitives described by the repository: elliptic-curve ElGamal, multi-party shuffle/re-encryption and Poseidon-based commitments.

The reference repository contains poker-specific circuits. Those circuits are therefore treated as **external research/reference material**, not as canonical Node Core implementation.

No source code from that repository is copied here.

## Adapter rule

The adapter MUST remain proof-system-neutral at the Node Core contract level.

A future implementation may provide adapters for:

- Groth16;
- another approved SNARK/STARK system;
- another proof system selected through a formal architecture decision.

The selected proof system MUST NOT be hard-coded into the identity semantics.

## Current status

**Status: verification boundary established; reference integration recorded; production verifier implementation pending selected proof-system contract and approved test vectors.**
