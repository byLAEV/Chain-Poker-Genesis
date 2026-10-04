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
| Bootstrap / Installation | `Documentation/Interfaces/NODE-CORE-BOOTSTRAP-CONTRACT.md` | CANONICAL / IMPLEMENTED_PARTIAL | `Bootstrap/bootstrap.py`, `Installer/bootstrap_node.py`, `Initialization/node_initializer.py`, `Verification/bootstrap_verifier.py`, `Recovery/bootstrap_recovery_impl.py` | `Tests/Bootstrap/test_bootstrap.py`, `Tests/Integration/test_node_installation_e2e.py`, `test_installation_manifest.py` | Clean bootstrap, isolation, integrity, failure and idempotent recovery mapped; broader production identity remains separate |
| Configuration | `Documentation/Interfaces/NODE-CORE-CONFIGURATION-CONTRACT.md` | CANONICAL / IMPLEMENTED_PARTIAL | `Configuration/Schemas/node-configuration.schema.json`, Bootstrap, Runtime readiness | `Tests/Configuration/test_configuration_contract.py`, installation E2E | Schema/default/integrity/runtime boundary mapped; centralized manager and full negative matrix remain |
| Identity | `Identity/FORMAL-IDENTITY-PROFILE-v1.0.md` | CANONICAL | `Identity/identity_core.py`, schema, binding, manager, verification, recovery | `Tests/Identity/test_identity_core.py`, `test_identity_implementation.py`, `test_identity_completion.py` | Evidence mapped; semantic reconciliation remains |
| Cryptography | `Cryptography/Core/FORMAL-CRYPTOGRAPHIC-PROFILE-v1.0.md` | CANONICAL | `crypto_core.py`, `crypto_service.py`, `primitives.py`, `signatures.py` | `Tests/Cryptography/test_crypto_core.py`, `test_crypto_implementation.py`, `test_signatures.py` | Evidence mapped; AEAD/Merkle remain profile-dependent |
| Storage | `Documentation/Interfaces/NODE-CORE-STORAGE-CONTRACT.md` | CANONICAL | `Storage/storage_engine.py`, `storage_api.py`, `Storage Manager/storage_manager.py`, `storage_locator.py` | `Tests/Storage/test_storage_locator.py`, `test_storage_complete.py` | Evidence mapped |
| Runtime | `Documentation/Runtime/NODE-CORE-RUNTIME-LIFECYCLE.md` | CANONICAL | `Runtime/State/runtime_state.py`, `Runtime/runtime_manager.py`, `Runtime/node_runtime.py` | Existing runtime tests plus lifecycle tests; dedicated contract coverage remains to be expanded | Lifecycle source and implementation state machine reconciled; readiness bug corrected |
| Recovery | `Documentation/Interfaces/NODE-CORE-RECOVERY-CONTRACT.md` | CANONICAL | `Recovery/recovery_manager.py` | `Tests/Recovery/test_recovery_implementation.py`, `Tests/Engine Runtime/test_health_recovery.py` | Evidence mapped |
| Network | `Documentation/Interfaces/NODE-CORE-NETWORK-CONTRACT.md` | CANONICAL | `Network/network_manager.py`, `peer_registry.py`, `transport.py`, `Synchronization/synchronization_state.py` | `Tests/Network/test_network_contract.py`, `test_synchronization_state.py` | Contract, implementation, synchronization boundary and protocol isolation mapped |
| Node Manager | `Documentation/Interfaces/NODE-MANAGER-CONTRACT.md` | CANONICAL | `Node Manager/node_manager.py` | `Tests/Node Manager/test_node_manager_contract.py` | Contract/implementation aligned; protocol installation routed through Protocol Interface |
| Security | `Documentation/Interfaces/NODE-CORE-SECURITY-CONTRACT.md` | CANONICAL / IMPLEMENTED_PARTIAL | `Security/security_service.py`, security manifest | `Tests/Security/test_security_contract.py` | Boundary and baseline controls mapped; audit/secure-config remain partial |
| Time | `Documentation/Interfaces/NODE-CORE-TIME-CONTRACT.md` | CANONICAL / IMPLEMENTED_PARTIAL | `Time/time_service.py`, time manifest | `Tests/Time/test_time_contract.py` | Timestamp, logical ordering and hash-chain integrity mapped; network-time consensus intentionally excluded |
| Engine Runtime | `Documentation/Interfaces/NODE-CORE-ENGINE-RUNTIME-CONTRACT.md` | CANONICAL | `Engine Runtime/engine_runtime.py` | `Tests/Engine Runtime/test_engine_runtime_contract.py` | Boundary and baseline implementation/test now mapped |
| API | `Documentation/Interfaces/NODE-CORE-API-CONTRACT.md` | CANONICAL | `API/node_core_api.py` (partial facade) | `Tests/API/test_node_core_api_contract.py` | Contract authority established; implementation remains explicitly PARTIAL |
| CLI | `Documentation/Interfaces/NODE-CORE-CLI-CONTRACT.md` | CANONICAL / PARTIAL | `CLI/node_cli.py` | `Tests/CLI/test_cli_contract.py` | Lifecycle subset mapped; deterministic JSON/error/exit boundary established |
| Protocol Interface | `Documentation/Interfaces/NODE-CORE-PROTOCOL-INTERFACE-CONTRACT.md` | CANONICAL | `Protocol Interface/protocol_interface.py`, protocol installation boundary | `Tests/Protocol Interface/test_protocol_interface.py` | Single installation/activation boundary established; invalid transitions tested |
| Consensus Infrastructure | N/A for PHASE 1 Node Core scope | OUT OF SCOPE | `Consensus/` | Protocol-specific verification belongs to CPG Protocol | Node Core provides Engine Runtime/Protocol Interface boundaries; CPG consensus is excluded from generic Node Core authority |
| Manifest Authority | `Documentation/Interfaces/NODE-CORE-MANIFEST-AUTHORITY-CONTRACT.md` | CANONICAL | `NODE-CORE-MANIFEST.json`, `Configuration/Schemas/node-core-installation-manifest.schema.json`, installation-manifest generation/validation | `Tools/Validation/validate_manifest_authority.py`, `Tests/Test Vectors/NODE-MANIFEST-AUTHORITY-0001.json`, installation manifest tests | Component manifest vs instance installation manifest separated; legacy duplicate schema explicitly classified; conflict rules established |

## 3. Evidence-mapped canonical candidates

All in-scope Node Core capabilities have a named normative profile/contract plus mapped implementation and test evidence. Security and Time are explicitly partial in implementation status, but their normative boundaries and verification mappings are closed. Consensus Infrastructure is excluded from generic Node Core authority because CPG consensus is protocol-specific.

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

**PHASE 1 — CANONICAL CONTRACTS / PASS**

All currently scoped Node Core capabilities have a named canonical authority, implementation mapping and verification mapping. Manifest authority is explicitly resolved.

**PHASE 1 PASS CONDITION: SATISFIED.**

**PHASE 2 — MANIFEST ↔ README ↔ CODE may now begin.**

## 8. Governing principle

> One capability. One normative contract. Supporting documents may explain it. Implementations must conform to it. Tests must verify it.


## PHASE 2 — Bootstrap reconciliation

**Component:** Bootstrap / Installation  
**Status:** PASS

Manifest, README/supporting documentation and implementation were reconciled against the canonical Bootstrap Contract.

Resolved conflicts:
- bootstrap documentation versions below the canonical contract;
- legacy `NODE_BOOTSTRAPPED` state wording versus implementation `NODE_CORE_READY`;
- identity wording implying deterministic test identity generation;
- README flow omitting verification/integrity boundaries;
- installation schema not requiring `storage.required_paths`;
- distinction between local provider readiness and decentralized-storage provider provisioning.

**Authority remains:** canonical contract → manifest/schema → implementation → tests.

**Next PHASE 2 component:** Configuration.
