# Node Core Implementation Gap Inventory v2

**Project:** Chain Poker Genesis by LAEV  
**Scope:** Node Core only  
**Baseline:** Node Core lifecycle baseline verified by GitHub Actions Run #631  
**Verified commit:** `4a0a2dd694d38f7f5cfe1ce00ff1ead0467274b3`

## Status model

- **IMPLEMENTED + VERIFIED** — executable behavior is present and covered by the current verification gate.
- **IMPLEMENTED / PARTIAL** — executable behavior exists, but coverage or operational scope remains incomplete.
- **SPECIFICATION / SCHEMA ONLY** — requirements or schemas exist without a complete executable implementation.
- **STRUCTURAL ONLY** — directory structure exists primarily through placeholders.
- **BLOCKED BY SPECIFICATION** — normative decisions must be resolved before implementation should proceed.

## Current inventory

| Subsystem | Evidence at current baseline | State | Next action |
|---|---|---|---|
| Bootstrap / Installer | executable bootstrap + structural audit + compilation + verification + installation manifest + E2E + final audit | IMPLEMENTED + VERIFIED | expand negative cases |
| Configuration | canonical contract + schema + Configuration Manager + readiness integration + tests + CI | IMPLEMENTED / PARTIAL | complete broader policy/negative-path coverage |
| Identity | executable Identity Core + canonical profile + lifecycle/tamper tests + CI; production trust/registration remains open | IMPLEMENTED / PARTIAL | complete credential adapters, registration, persistence, propagation and recovery |
| Cryptography Core | executable core primitives/service + canonical profile + crypto tests + CI; AEAD boundary and vectors are IMPLEMENTED_VERIFIED; Merkle and production security remain open | IMPLEMENTED / PARTIAL | complete Merkle specification/vectors and production security review |
| Storage | executable local storage, registry, locator, synchronization/recovery boundaries + provider-failure fallback test + CI; live Kubo operation remains environment-dependent | IMPLEMENTED / PARTIAL | live-provider evidence and broader reconciliation/failure matrix |
| Runtime | canonical lifecycle + readiness implementation + cross-component lifecycle + full Node lifecycle + invalid-transition matrix + final audit; GitHub Actions Runs #631/#634 | IMPLEMENTED + VERIFIED | broaden mutation/environmental coverage where justified |
| Health / Readiness | executable evaluator + installation/E2E verification + final audit | IMPLEMENTED + VERIFIED | expand failure-state coverage |
| Recovery | executable recovery manager + recovery tests + cross-component/full lifecycle coverage + invalid-transition matrix + final audit; GitHub Actions Runs #631/#635 | IMPLEMENTED / PARTIAL | expand interruption/corruption/reconciliation scenarios |
| Network / Synchronization | executable peer registry, reference transport, framing, handshake, envelopes, propagation and synchronization state + tests + CI | IMPLEMENTED / PARTIAL | authenticated production transport, decentralized discovery and live synchronization |
| Protocol Interface | executable catalog/download/package verification/installation boundary + E2E isolation + manifest-tamper and compatibility/lifecycle negative tests + CI | IMPLEMENTED / PARTIAL | complete persistent administrative/install lifecycle and broader compatibility cases |
| Node Manager | canonical contract + executable manager + lifecycle integration + contract tests + GitHub Actions Run #631 | IMPLEMENTED / PARTIAL | complete broader management surface |
| API | canonical API contract + executable facade + API tests + CI | IMPLEMENTED / PARTIAL | expand service/command surface |
| CLI | canonical CLI contract + executable command subset + CLI tests + CI | IMPLEMENTED / PARTIAL | expand operational command catalog |
| Security | canonical security contract + executable security service + contract tests + CI | IMPLEMENTED / PARTIAL | audit logging and secure-configuration enforcement |
| Time | canonical time contract + executable service + contract tests + CI | IMPLEMENTED / PARTIAL | expand synchronization/reference-status coverage |
| Consensus Infrastructure | protocol-neutral boundary only; CPG consensus remains protocol-specific and excluded from generic Node Core authority | OUT OF SCOPE | keep CPG consensus in CPG Protocol Core |
| Engine Runtime | canonical contract + executable shared runtime + contract tests + CI | IMPLEMENTED / PARTIAL | complete sandbox/resource controls |
| Release / Integrity | executable validation and manifest authority + CI final audit | IMPLEMENTED / PARTIAL | expand release verification evidence |
| Tests / Test Vectors | automated verification, integration, E2E, cross-component lifecycle, full Node lifecycle and final audit all PASS in Run #631 | IMPLEMENTED / PARTIAL | increase negative, mutation and environmental coverage |

## Lifecycle Verification Closure

GitHub Actions Run #631 (`4a0a2dd694d38f7f5cfe1ce00ff1ead0467274b3`) completed the Node Core verification workflow successfully. The run passed Structural Audit, Python compilation, Node Core verification, AEAD conformance, installation manifest validation, E2E installation, cross-component lifecycle, full Node lifecycle, and the final Node Core audit.

The verified lifecycle sequence is:

```text
UNINITIALIZED → READY → RUNNING → DEGRADED → RECOVERY → READY → STOPPED
```

The lifecycle evidence does not constitute completion of the entire Node Core implementation. Subsystems explicitly marked PARTIAL remain partial, and Merkle implementation/vectors plus production cryptographic security review remain open.

## Negative-Path Verification Closure

The subsequent Node Core verification runs closed the current negative-path matrix without changing the positive lifecycle baseline:

| Gate | Evidence | Result |
|---|---|---|
| Runtime invalid transitions | GitHub Actions Run #634, commit `d4de4fedd5069cbd03f9ab8473b79093139bae15` | PASS |
| Recovery invalid transitions | GitHub Actions Run #635, commit `94a65ceac0ba0c8bf772feefd7a5357775b43c55` | PASS |
| Kubo unavailable → local fallback | GitHub Actions Run #636, commit `be117dd9d6394f3f109ae8effa964f415e1d7c1d` | PASS |
| Protocol compatibility/lifecycle negatives | GitHub Actions Run #637, commit `e9c17577fa5dde699981020f21e41b829e203f88` | PASS |

These runs also passed the complete Node Core verification workflow, including the final Node Core audit. The negative-path suite therefore strengthens the acceptance evidence but does not convert explicitly PARTIAL production components into fully verified production implementations.

Configuration fail-closed verification was subsequently confirmed by GitHub Actions Run #640 (commit `48234fc6f1178fd8577b949b6945dc737e32aa1c`), covering required-field, invalid-state, duplicate-association, fresh-node CPG activation, invalid storage-mode, and Dual Storage coherence-gate rejection cases. The complete Node Core audit workflow passed.

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

The repository now contains a reconciled formal cryptographic profile and normative AEAD profile. AEAD implementation and independent vectors are verified by GitHub Actions Run #605 and the subsequent documentation reconciliation gate Run #608.

Remaining cryptographic closure work is explicitly limited to:

1. Deterministic Merkle Tree Specification and test vectors.
2. Remaining production cryptographic-security requirements and external security review.
3. Broader cross-component and negative-path coverage.

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
8. Complete the deterministic Merkle specification and test vectors without altering the verified AEAD boundary.
9. Resolve remaining formal Identity production integration contracts.
10. Complete production cryptographic-security requirements/review.
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
