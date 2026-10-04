# Node Core — Canonical Contract Index

**Status:** PHASE 1 — CANONICAL CONTRACTS / WORKING INDEX  
**Version:** 1.0.0  
**Scope:** Protocol-neutral Node Core  
**Project:** Chain Poker Genesis by LAEV

## 1. Purpose

This index is the normative registry for Node Core contract artifacts during PHASE 1 of the Node Core closure program.

It does not replace subsystem specifications. It identifies which existing artifact is authoritative, which artifacts support it, which artifacts are implementation or verification material, and which artifacts must not be treated as normative.

The classification values are:

- **CANONICAL** — authoritative normative source for the capability.
- **SUPPORTING** — supporting specification, schema, architecture, or explanatory material; it must not contradict the canonical source.
- **DRAFT** — work-in-progress material; non-normative.
- **IMPLEMENTATION** — executable/reference implementation material.
- **TEST** — tests, vectors, fixtures, or verification material.
- **OBSOLETE** — historical or superseded material; must not be used as authority.

## 2. Canonicalization rule

For each Node Core capability:

`CANONICAL CONTRACT → SUPPORTING SPECIFICATIONS → IMPLEMENTATION → TEST / VERIFICATION`

No implementation may introduce normative behavior that is absent from, or contradictory to, the canonical contract without first updating the canonical contract.

A README is descriptive unless this index explicitly identifies it as the canonical contract.

## 3. Contract index

| Capability | Canonical artifact | Classification | Supporting artifacts | Implementation boundary | Verification |
|---|---|---|---|---|---|
| Bootstrap / Installation | `Node Core/Documentation/Interfaces/NODE-CORE-BOOTSTRAP-CONTRACT.md` if present; otherwise existing bootstrap specification must be reconciled before freeze | CANONICAL CANDIDATE | Bootstrap / installation specifications | `Node Core/Bootstrap/` | installation + verification tests |
| Configuration | `Node Core/Documentation/Interfaces/NODE-CORE-CONFIGURATION-CONTRACT.md` | CANONICAL CANDIDATE | configuration schemas/specifications | `Node Core/Configuration/` | configuration validation tests |
| Identity | `Node Core/Identity/FORMAL-IDENTITY-PROFILE-v1.0.md` | CANONICAL CANDIDATE | `IDENTITY-IMPLEMENTATION-SPECIFICATION-v1.0.md`, implementation plan | `Node Core/Identity/` | identity tests / vectors |
| Cryptography | `Node Core/Cryptography/FORMAL-CRYPTOGRAPHIC-PROFILE-v1.0.md` | CANONICAL CANDIDATE | `Cryptography/Core/SPECIFICATION.md`, provider specifications | `Node Core/Cryptography/` | cryptographic conformance tests / vectors |
| Storage | `Node Core/Documentation/Interfaces/NODE-CORE-STORAGE-CONTRACT.md` | CANONICAL CANDIDATE | storage architecture / provider specifications | `Node Core/Storage/` | storage coherence + integrity tests |
| Runtime | `Node Core/Documentation/Interfaces/NODE-CORE-RUNTIME-CONTRACT.md` if present; otherwise lifecycle/readiness specifications must be reconciled | CANONICAL CANDIDATE | lifecycle, readiness, health specifications | `Node Core/Runtime/` | lifecycle/readiness tests |
| Recovery | `Node Core/Documentation/Interfaces/NODE-CORE-RECOVERY-CONTRACT.md` | CANONICAL CANDIDATE | recovery integration specification | `Node Core/Recovery/` | recovery/failure tests |
| Network | `Node Core/Documentation/Interfaces/NODE-CORE-NETWORK-CONTRACT.md` | CANONICAL CANDIDATE | transport/framing/discovery specifications | `Node Core/Network/` | network + two-node tests |
| Node Manager | `Node Core/Documentation/Interfaces/NODE-MANAGER-CONTRACT.md` | CANONICAL CANDIDATE | Node Manager API README | `Node Core/Node Manager/` | lifecycle/integration tests |
| Security | `Node Core/Documentation/Interfaces/NODE-CORE-SECURITY-BOUNDARY.md` | CANONICAL CANDIDATE | security specifications | `Node Core/Security/` | security/boundary tests |
| Time | `Node Core/Documentation/Interfaces/NODE-CORE-TIME-SERVICE-CONTRACT.md` | CANONICAL CANDIDATE | time service specifications | `Node Core/Time/` | time/conformance tests |
| Engine Runtime | **To be consolidated** | CANONICAL REQUIRED | Engine Runtime README/specifications | `Node Core/Engine Runtime/` | engine lifecycle tests |
| API | **Subsystem contracts + API contract consolidation required** | CANONICAL REQUIRED | individual API READMEs | `Node Core/API/` | API contract tests |
| CLI | `Node Core/Documentation/Interfaces/NODE-CORE-CLI-CONTRACT.md` | CANONICAL CANDIDATE | CLI README/help definitions | `Node Core/CLI/` | CLI/exit-code tests |
| Protocol Interface | `Node Core/Documentation/Interfaces/NODE-CORE-PROTOCOL-INTERFACE-CONTRACT.md` if present; otherwise existing protocol boundary must be reconciled | CANONICAL CANDIDATE | protocol installation boundary | `Node Core/Protocol Interface/` | protocol-boundary tests |
| Consensus Infrastructure | **Scope boundary required before freeze** | CANONICAL REQUIRED | consensus infrastructure specifications | `Node Core/Consensus/` | state/evidence/validation tests |
| Manifests | Existing Node Core manifest/schema contract | CANONICAL CANDIDATE | manifest API README | `Node Core/*MANIFEST*` + manifest APIs | schema/integrity tests |

## 4. Supporting artifacts

The following classes must remain supporting material unless explicitly promoted by this index:

- subsystem READMEs;
- architecture diagrams;
- implementation plans;
- reconciliation reports;
- implementation-gap inventories;
- canonicalization maps;
- migration plans;
- rendered documentation;
- completion reports.

Supporting material may explain a contract but may not silently redefine it.

## 5. Implementation artifacts

The following are implementation artifacts and are never normative by themselves:

- Python modules;
- managers;
- services;
- adapters;
- providers;
- CLI executables;
- runtime entry points;
- verification utilities.

Implementation behavior that differs from a canonical contract is a conformance failure, not an alternative contract.

## 6. Test artifacts

Tests and vectors are verification authority for behavior, but they do not independently define protocol semantics.

Test artifacts include:

- unit tests;
- integration tests;
- negative-path tests;
- recovery tests;
- test vectors;
- schema validators;
- installation verification;
- conformance tests;
- CI checks.

A test that contradicts a canonical contract must be corrected or explicitly used to expose a contract defect.

## 7. Draft artifacts

Known draft/working material must remain explicitly non-normative.

In particular:

- `IDENTITY-DESIGN-CONSOLIDATION-DRAFT-v0.1.md` is DRAFT unless formally promoted.
- `NODE-CORE-CANONICALIZATION-MAP.md` is a working migration/canonicalization map, not itself the contract authority.
- Implementation-gap inventories are audit documents, not normative contracts.

## 8. Protocol isolation

The following are outside generic Node Core contract scope:

- CPG ledger;
- CPG table state;
- CPG-specific consensus rules;
- poker/NLHE rules;
- Table Wallet;
- settlement;
- rake;
- CPG-specific cryptographic semantics.

The Node Core Protocol Interface may expose capabilities required by protocols, but a protocol must not redefine Node Core semantics.

## 9. Existing canonicalization map relationship

The existing:

`Main Temporal/documentation/architecture/NODE-CORE-CANONICALIZATION-MAP.md`

remains a migration and reconciliation artifact. It must be used as supporting evidence for this index and must not be treated as a replacement for this contract registry.

## 10. PHASE 1 freeze conditions

PHASE 1 cannot be declared complete until:

1. every Node Core subsystem has exactly one normative contract source;
2. duplicate normative-looking documents are classified;
3. all drafts are explicitly marked non-normative;
4. implementation paths are mapped;
5. tests/vectors are mapped;
6. Runtime vs Engine Runtime boundaries are resolved;
7. Identity and Cryptography profiles are reconciled with their implementation specifications;
8. API contracts are consolidated without duplicating subsystem semantics;
9. Consensus Infrastructure scope is explicitly limited to protocol-neutral infrastructure;
10. Manifest, README, contract, implementation, and test references are ready for PHASE 2.

## 11. Current phase status

**PHASE 1 — IN PROGRESS**

This index establishes the registry structure. It does not falsely declare all candidates canonical.

The next operation is contract-by-contract reconciliation against the actual repository paths and implementation before the final canonical status is frozen.

## 12. Governing principle

> One capability. One normative contract. Supporting documents may explain it. Implementations must conform to it. Tests must verify it.
