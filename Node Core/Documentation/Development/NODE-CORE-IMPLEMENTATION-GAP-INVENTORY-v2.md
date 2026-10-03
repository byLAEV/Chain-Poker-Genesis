# Node Core Implementation Gap Inventory v2

**Project:** Chain Poker Genesis by LAEV  
**Scope:** Node Core only  
**Baseline:** Implementation baseline verified by GitHub Actions Run #37  
**Verified commit:** `ab81b793c328778c870bde6fcb5192d7fad318b7`

## Status model

- **IMPLEMENTED + VERIFIED** — executable behavior is present and covered by the current verification gate.
- **IMPLEMENTED / PARTIAL** — executable behavior exists, but coverage or operational scope remains incomplete.
- **SPECIFICATION / SCHEMA ONLY** — requirements or schemas exist without a complete executable implementation.
- **STRUCTURAL ONLY** — directory structure exists primarily through placeholders.
- **BLOCKED BY SPECIFICATION** — normative decisions must be resolved before implementation should proceed.

## Current inventory

| Subsystem | Evidence at baseline | State | Next action |
|---|---|---|---|
| Bootstrap / Installer | executable bootstrap + CI/E2E verification | IMPLEMENTED + VERIFIED | preserve baseline; expand negative cases |
| Configuration | schemas + generated node configuration + readiness validation | IMPLEMENTED / PARTIAL | connect full configuration policy to runtime |
| Identity | executable offline Identity Core + canonical schema + lifecycle/tamper tests; production integration remains open | IMPLEMENTED / PARTIAL | integrate credential adapters, binding, persistence, propagation and recovery |
| Cryptography Core | core specification; implementation directories remain placeholders | BLOCKED BY SPECIFICATION | freeze cryptographic profile before normative implementation |
| Storage Manager | executable manager + tests + coherence validation | IMPLEMENTED / PARTIAL | expand failure and fallback coverage |
| Object Registry | executable registry + tests | IMPLEMENTED / PARTIAL | expand integrity/schema edge cases |
| Storage Provider | local provider + tests; external provider not provisioned | IMPLEMENTED / PARTIAL | define distributed-provider contract and test fallback |
| Storage Locator | executable locator + tests | IMPLEMENTED / PARTIAL | complete all location-state cases |
| Runtime | executable lifecycle + readiness state model + E2E | IMPLEMENTED + VERIFIED | add transition-negative coverage |
| Health / Readiness | executable health evaluator + E2E verification | IMPLEMENTED + VERIFIED | expand failure-state coverage |
| Recovery | executable recovery manager + E2E verification | IMPLEMENTED / PARTIAL | add interruption/corruption scenarios |
| Network / Synchronization | executable peer registry, TCP reference transport, message framing, hello handshake, propagation boundary, synchronization state + tests | IMPLEMENTED / PARTIAL | integrate authenticated production provider, decentralized discovery, and live synchronization verification |
| Protocol Interface | protocol installation boundary + schema + E2E isolation | IMPLEMENTED + VERIFIED | expand rejection/compatibility cases |
| Node Manager | structural directories/documentation | STRUCTURAL ONLY | define manager contract and implement |
| API | structural API directories | STRUCTURAL ONLY | define Node Core API contract |
| CLI | structural CLI directories | STRUCTURAL ONLY | define operational command contract |
| Security | structural security directories/specification | STRUCTURAL ONLY | define executable security boundary |
| Time | structural time directories/specification | STRUCTURAL ONLY | define executable Node Core time service contract |
| Consensus | structural consensus directories | STRUCTURAL ONLY | keep protocol/table consensus outside Node Core baseline unless infrastructure contract requires otherwise |
| Engine Runtime | structural runtime directories + related tests/specifications | IMPLEMENTED / PARTIAL | reconcile engine lifecycle boundary with canonical runtime |
| Release / Integrity | release-integrity implementation + validation | IMPLEMENTED / PARTIAL | integrate release verification into CI |
| Tests / Test Vectors | automated tests + test-vector inventory | IMPLEMENTED / PARTIAL | increase negative, mutation, and cross-component coverage |

## Verified baseline boundary

The following are now verified invariants:

```
NODE_CORE_READY
protocol_associations = []
cpg_protocol = NOT_INSTALLED
synchronization = NOT_EVALUATED
```

The Node Core bootstrap does not install or activate CPG.

## Remaining architectural blockers

### 1. Cryptography

The repository does not yet contain a normative cryptographic profile sufficient for production implementation.

Before implementing normative cryptographic primitives, define:

1. Formal Cryptographic Profile.
2. Canonical Serialization Specification.
3. Merkle Tree Specification.
4. Cryptographic Test Vector Suite.
5. Key-management and verification boundaries.

### 2. Identity

The current identity layer establishes metadata and documents the cryptographic connection boundary, but does not constitute a complete production identity engine.

The implementation must distinguish:

- credential acquisition;
- identity derivation;
- identity validation;
- node registration;
- node activation;
- recovery.

Unspecified hardware-wallet or derivation behavior must not be invented as an implicit protocol rule.

### 3. Distributed storage

The current baseline proves the local storage provider boundary. It does not prove live decentralized provider operation or synchronization.

Those remain separate from the Node Core readiness gate.

## Recommended implementation sequence

1. Preserve the current Node Core implementation baseline.
2. Expand negative-path tests for Bootstrap, Configuration, Runtime, Health, Recovery, and Protocol Interface.
3. Complete Storage fallback/coherence verification.
4. Define Node Manager contract.
5. Define CLI contract.
6. Define Security boundary.
7. Define Time service contract.
8. Resolve the Formal Cryptographic Profile.
9. Resolve the formal Identity profile.
10. Implement cryptographic and identity components against those normative specifications.
11. Implement live network synchronization only after its boundary is formally defined.
12. Re-run the complete Node Core verification gate after each architectural milestone.

## Completion rule

A subsystem is not complete merely because its directory, README, schema, or placeholder exists.

Completion requires, where applicable:

- executable behavior;
- deterministic acceptance criteria;
- automated tests;
- negative-path coverage;
- verification evidence tied to a repository commit.

**Author:** Lerry Alexander Elizondo Villalobos — LAEV / byLAEV
