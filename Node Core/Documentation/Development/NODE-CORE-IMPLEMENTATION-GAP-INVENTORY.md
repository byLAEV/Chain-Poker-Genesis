# Node Core Implementation Gap Inventory

**Baseline:** 2026-10-02
**Scope:** Node Core only
**Method:** repository evidence, executable files, schemas, specifications, and tests.

## Status model
- **IMPLEMENTED + VERIFIED** — executable behavior has corresponding verification evidence.
- **IMPLEMENTED / PARTIAL** — executable code exists, but one or more required behaviors remain incomplete or insufficiently verified.
- **SPECIFICATION / SCHEMA ONLY** — requirements exist but no production implementation is present.
- **STRUCTURAL ONLY** — directory exists primarily through placeholders.
- **BLOCKED BY SPECIFICATION** — implementation must wait for an unresolved normative decision.

## Current inventory

| Subsystem | Repository evidence | Current state | Next action |
|---|---|---|---|
| Bootstrap / Installer | bootstrap implementation + schemas + integration tests | IMPLEMENTED / PARTIAL | complete CI/E2E gate |
| Identity | cryptographic-connection specification + identity schema; no complete engine implementation | SPECIFICATION / SCHEMA ONLY | define formal identity profile and implement |
| Cryptography Core | architectural specification only; no complete engine | BLOCKED BY SPECIFICATION | freeze cryptographic profile before normative implementation |
| Storage Manager | implementation + tests + specification | IMPLEMENTED / PARTIAL | expand failure/fallback verification |
| Object Registry | implementation + tests + specification | IMPLEMENTED / PARTIAL | verify schema/integrity edge cases |
| Storage Provider | local provider implementation + tests | IMPLEMENTED / PARTIAL | establish distributed-provider contract and fallback tests |
| Storage Locator | implementation + tests + specification | IMPLEMENTED / PARTIAL | complete all location-state cases |
| Runtime | lifecycle implementation + tests + specification | IMPLEMENTED / PARTIAL | align every transition with readiness model |
| Health / Readiness | implementation + tests + specification | IMPLEMENTED / PARTIAL | integrate into final operational gate |
| Recovery | implementation + specification | IMPLEMENTED / PARTIAL | add interruption/corruption recovery tests |
| Network / Synchronization | executable peer registry, TCP reference transport, message framing, hello handshake, propagation boundary, synchronization state + tests | IMPLEMENTED / PARTIAL | integrate authenticated production provider, decentralized discovery, and live synchronization verification |
| Protocol Interface | installation boundary implementation + schema + specification | IMPLEMENTED / PARTIAL | verify rejection/isolation cases |
| Configuration | schemas and manifest validation | IMPLEMENTED / PARTIAL | connect validation to complete runtime configuration |
| Node Manager | structural directory / documentation evidence | STRUCTURAL ONLY | define contract and implement |
| API | structural directory / documentation evidence | STRUCTURAL ONLY | define required Node Core API surface |
| CLI | structural directory / documentation evidence | STRUCTURAL ONLY | define operational command contract and implement |
| Security | structural directory / documentation evidence | STRUCTURAL ONLY | define Node Core security boundary |
| Time | structural directory / documentation evidence | STRUCTURAL ONLY | define required Node Core time service contract |
| Consensus | structural directory / documentation evidence | STRUCTURAL ONLY | keep CPG/table consensus outside baseline unless Node Core contract explicitly requires infrastructure only |
| Engine Runtime | runtime tests/specification exist | IMPLEMENTED / PARTIAL | reconcile with canonical Runtime boundary |
| Release / Integrity | implementation + integrity specification | IMPLEMENTED / PARTIAL | integrate release verification into CI |
| Tests / Test Vectors | substantial test/vector inventory | IMPLEMENTED / PARTIAL | increase negative and cross-component coverage |

## Architectural blockers

### Cryptography
The current Cryptographic Core specification explicitly leaves the cryptographic profile open. A normative production implementation must not silently choose algorithms, encodings, derivation rules, or Merkle semantics.

Required before normative cryptographic implementation:
1. Formal Cryptographic Profile.
2. Canonical Serialization Specification.
3. Merkle Tree Specification.
4. Cryptographic Test Vector Suite.

### Identity
The historical Cryptographic Connection specification documents multiple credential paths but explicitly leaves hardware-wallet protocol, validation algorithms, secure local storage, derivation policy, and recovery details unspecified.

Identity implementation must therefore separate credential acquisition, identity derivation, identity validation, and node activation, and must not invent unspecified protocol behavior.

## Immediate execution order
1. Finish current GitHub Actions E2E/final-audit gate.
2. Reconcile Runtime implementation with the canonical readiness state model.
3. Close Bootstrap/Configuration installation verification.
4. Expand Storage negative/fallback tests.
5. Define Node Manager contract.
6. Define CLI contract.
7. Define Security boundary.
8. Resolve the Formal Cryptographic Profile before implementing normative cryptographic primitives.
9. Resolve the formal Identity profile and implement the Cryptographic Connection Engine.\n10. Network implementation baseline: peer registry, transport framing, hello handshake, propagation and network-state observation are now executable.\n11. Integrate authenticated production transport and decentralized discovery only after the provider/security contract is frozen.
12. Integrate all completed components into the Local Readiness Gate.

## Completion rule
A subsystem cannot be marked complete because its directory, README, schema, or placeholder exists. Completion requires executable behavior where applicable, applicable automated tests, and verification evidence tied to a repository commit.