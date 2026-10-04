# Node Core — Canonical Contract Index

**Status:** PHASE 1 — CANONICAL CONTRACTS / RECONCILIATION PASS
**Version:** 1.1.0
**Scope:** Protocol-neutral Node Core
**Project:** Chain Poker Genesis by LAEV

## 1. Governing classification

- **CANONICAL** — authoritative normative source.
- **SUPPORTING** — subordinate explanatory/specification material.
- **DRAFT** — non-normative work in progress.
- **IMPLEMENTATION** — executable/reference implementation.
- **TEST** — verification material.
- **OBSOLETE** — superseded/non-authoritative material.

Normative chain:

`CANONICAL CONTRACT → SUPPORTING → IMPLEMENTATION → TEST / VERIFICATION`

Implementation may not silently create behavior that contradicts a canonical contract. A README is descriptive unless explicitly promoted here.

## 2. Reconciliation matrix

| Capability | Canonical source | Status | Implementation mapped | Test mapped | Decision |
|---|---|---|---|---|---|
| Bootstrap / Installation | Existing Bootstrap contract/specification; exact authoritative path requires final audit | CANONICAL CANDIDATE | `Node Core/Bootstrap/` | `Tests/Bootstrap/test_bootstrap.py` | Confirm exact normative source |
| Configuration | `Documentation/Interfaces/NODE-CORE-CONFIGURATION-CONTRACT.md` | CANONICAL CANDIDATE | Runtime/Node Manager consumers; dedicated implementation mapping open | Dedicated configuration test not confirmed | Mapping blocks PASS |
| Identity | `Identity/FORMAL-IDENTITY-PROFILE-v1.0.md` | CANONICAL | `Identity/identity_core.py`, schema, binding, manager, verification, recovery | `Tests/Identity/test_identity_core.py`, `test_identity_implementation.py`, `test_identity_completion.py` | Evidence mapped; semantic reconciliation remains |
| Cryptography | `Cryptography/Core/FORMAL-CRYPTOGRAPHIC-PROFILE-v1.0.md` | CANONICAL | `crypto_core.py`, `crypto_service.py`, `primitives.py`, `signatures.py` | `Tests/Cryptography/test_crypto_core.py`, `test_crypto_implementation.py`, `test_signatures.py` | Evidence mapped; AEAD/Merkle remain profile-dependent |
| Storage | `Documentation/Interfaces/NODE-CORE-STORAGE-CONTRACT.md` | CANONICAL | `Storage/storage_engine.py`, `storage_api.py`, `Storage Manager/storage_manager.py`, `storage_locator.py` | `Tests/Storage/test_storage_locator.py`, `test_storage_complete.py` | Evidence mapped |
| Runtime | `Documentation/Runtime/NODE-CORE-RUNTIME-LIFECYCLE.md` | CANONICAL | `Runtime/State/runtime_state.py`, `Runtime/runtime_manager.py`, `Runtime/node_runtime.py` | Existing runtime tests plus lifecycle tests; dedicated contract coverage remains to be expanded | Lifecycle source and implementation state machine reconciled; readiness bug corrected |
| Recovery | `Documentation/Interfaces/NODE-CORE-RECOVERY-CONTRACT.md` | CANONICAL | `Recovery/recovery_manager.py` | `Tests/Recovery/test_recovery_implementation.py`, `Tests/Engine Runtime/test_health_recovery.py` | Evidence mapped |
| Network | `Documentation/Interfaces/NODE-CORE-NETWORK-CONTRACT.md` | CANONICAL | `Network/network_manager.py`, `peer_registry.py`, `transport.py`, `Synchronization/synchronization_state.py` | `Tests/Network/test_network_contract.py`, `test_synchronization_state.py` | Contract, implementation, synchronization boundary and protocol isolation mapped |
| Node Manager | `Documentation/Interfaces/NODE-MANAGER-CONTRACT.md` | CANONICAL | `Node Manager/node_manager.py` | `Tests/Node Manager/test_node_manager_contract.py` | Contract/implementation aligned; protocol installation routed through Protocol Interface |
| Security | `Documentation/Security Model/NODE-CORE-SECURITY-BOUNDARY.md` | CANONICAL CANDIDATE | `Security/SECURITY-CORE-MANIFEST.json` plus enforcement | Dedicated Security test mapping not confirmed | Conformance open |
| Time | `Documentation/Time/NODE-CORE-TIME-SERVICE-CONTRACT.md` | CANONICAL CANDIDATE | `Time/`, `TIME-CORE-MANIFEST.json`, external references | Dedicated Time conformance test not identified | Test mapping blocks PASS |
| Engine Runtime | `Documentation/Interfaces/NODE-CORE-ENGINE-RUNTIME-CONTRACT.md` | CANONICAL | `Engine Runtime/engine_runtime.py` | `Tests/Engine Runtime/test_engine_runtime_contract.py` | Boundary and baseline implementation/test now mapped |
| API | `Documentation/Interfaces/NODE-CORE-API-CONTRACT.md` | CANONICAL | `API/node_core_api.py` (partial facade) | `Tests/API/test_node_core_api_contract.py` | Contract authority established; implementation remains explicitly PARTIAL |
| CLI | `Documentation/Interfaces/NODE-CORE-CLI-CONTRACT.md` | CANONICAL CANDIDATE | Explicit implementation path requires mapping | Dedicated CLI test not identified | Mapping blocks PASS |
| Protocol Interface | `Documentation/Interfaces/NODE-CORE-PROTOCOL-INTERFACE-CONTRACT.md` | CANONICAL | `Protocol Interface/protocol_interface.py`, protocol installation boundary | `Tests/Protocol Interface/test_protocol_interface.py` | Single installation/activation boundary established; invalid transitions tested |
| Consensus Infrastructure | No single canonical contract | CANONICAL REQUIRED | `Consensus/` | Explicit state/evidence mapping required | Protocol-neutral scope only |
| Manifests | `NODE-CORE-MANIFEST.json` plus subsystem manifests | CANONICAL CANDIDATE | `*MANIFEST*` | Audit/verification tooling exists | Hierarchy reconciled in PHASE 2 |

## 3. Evidence-mapped canonical candidates

These currently have a named normative profile/contract plus mapped implementation and test evidence:

- Identity
- Cryptography
- Storage
- Recovery
- Runtime
- Engine Runtime
- API
- Node Manager
- Network
- Protocol Interface
- Security

This is **not** a global PHASE 1 PASS; semantic contract-to-code-to-test reconciliation remains.

## 4. Supporting / draft rules

Supporting material includes subsystem READMEs, architecture catalogs, implementation plans, gap inventories, reconciliation reports, canonicalization maps, migration plans and completion reports.

Specifically:

- `Documentation/Architecture/NODE-CORE-SUBSYSTEM-CATALOG.md` = architectural inventory, not implementation proof.
- `Main Temporal/documentation/architecture/NODE-CORE-CANONICALIZATION-MAP.md` = migration/reconciliation artifact, not contract authority.
- `Identity/IDENTITY-DESIGN-CONSOLIDATION-DRAFT-v0.1.md` = DRAFT.

## 5. Protocol isolation

Generic Node Core contracts do not include:

- CPG ledger;
- CPG table state;
- CPG-specific consensus;
- poker/NLHE rules;
- Table Wallet;
- settlement;
- rake;
- CPG-specific cryptographic semantics.

## 6. PHASE 1 PASS gate

Every Node Core capability must have:

`ONE CANONICAL SOURCE + IMPLEMENTATION MAPPING + TEST MAPPING`

and Consensus Infrastructure and manifest authority must be explicitly resolved.

## 7. Current status

**PHASE 1 — RECONCILIATION IN PROGRESS**

Identity, Cryptography, Storage and Recovery have reached the evidence-mapping stage.

Remaining blockers are missing dedicated verification mappings, unresolved single-source authority, or unresolved subsystem boundaries.

**PHASE 2 — MANIFEST ↔ README ↔ CODE must not begin until this gate passes.**

## 8. Governing principle

> One capability. One normative contract. Supporting documents may explain it. Implementations must conform to it. Tests must verify it.
