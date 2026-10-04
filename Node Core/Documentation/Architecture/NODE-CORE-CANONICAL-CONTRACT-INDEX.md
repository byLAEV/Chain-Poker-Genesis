# Node Core — Canonical Contract Index

**Status:** PHASE 1 — CANONICAL CONTRACTS / RECONCILIATION PASS
**Version:** 1.2.0
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
| Security | `Documentation/Interfaces/NODE-CORE-SECURITY-CONTRACT.md` | CANONICAL / IMPLEMENTED_PARTIAL | `Security/security_service.py` | `Tests/Security/test_security_contract.py` | Path, fail-closed authorization and protocol-isolation baseline reconciled; audit log and secure-configuration enforcement remain partial |
| Time | `Documentation/Interfaces/NODE-CORE-TIME-CONTRACT.md` | CANONICAL / IMPLEMENTED_PARTIAL | `Time/time_service.py`, time manifest | `Tests/Time/test_time_contract.py` | Timestamp, logical ordering and hash-chain integrity mapped; network-time consensus intentionally excluded |
| Engine Runtime | `Documentation/Interfaces/NODE-CORE-ENGINE-RUNTIME-CONTRACT.md` | CANONICAL | `Engine Runtime/engine_runtime.py` | `Tests/Engine Runtime/test_engine_runtime_contract.py` | Boundary and baseline implementation/test now mapped |
| API | `Documentation/Interfaces/NODE-CORE-API-CONTRACT.md` | CANONICAL | `API/node_core_api.py` (partial facade) | `Tests/API/test_node_core_api_contract.py` | Contract authority established; implementation remains explicitly PARTIAL |
| CLI | `Documentation/Interfaces/NODE-CORE-CLI-CONTRACT.md` | CANONICAL / PARTIAL | `CLI/node_cli.py` | `Tests/CLI/test_cli_contract.py` | Lifecycle subset mapped; deterministic JSON/error/exit boundary established |
| Protocol Interface | `Documentation/Interfaces/NODE-CORE-PROTOCOL-INTERFACE-CONTRACT.md` | CANONICAL / IMPLEMENTED_PARTIAL | `Protocol Interface/protocol_interface.py`, `protocol_catalog.py`, `protocol_source_resolver.py`, `protocol_download.py`, `protocol_package.py` | `Tests/Protocol Interface/test_protocol_interface.py`, `test_protocol_catalog.py`, `test_protocol_package_installation.py` | Catalog/download, manifest verification, identity, persistent installation and baseline shared Engine Runtime association are mapped; final administrative UI remains separate work |
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


## PHASE 2 — Configuration reconciliation

**Component:** Configuration  
**Status:** PASS

Reconciled chain:

`NODE-CORE-CONFIGURATION-CONTRACT.md`
→ `Configuration/Schemas/node-configuration.schema.json`
→ Bootstrap-generated `node-config.json`
→ `Configuration/configuration_manager.py`
→ Runtime readiness
→ Node Manager loading boundary
→ Configuration tests.

Resolved authority conflicts:
- schema identifier `0.1.0` versus canonical contract `1.0.0`;
- Runtime previously checked field presence without invoking the canonical configuration validator;
- Node Manager contract required configuration loading but implementation did not load configuration;
- Configuration API documentation did not identify the canonical contract/manager;
- duplicate configuration semantics were centralized in the Configuration Manager.

No second configuration authority is permitted.

**Next PHASE 2 component:** Runtime.


## PHASE 2 — Runtime reconciliation

**Component:** Runtime  
**Status:** PASS

Reconciled chain:

`Documentation/Runtime/NODE-CORE-RUNTIME-LIFECYCLE.md`
→ `Runtime/State/runtime_state.py`
→ `Runtime/node_runtime.py`
→ `Runtime/runtime_manager.py`
→ Runtime tests / installation E2E.

Resolved:
- RuntimeManager previously implemented a reduced readiness model separate from the canonical evaluator; it now delegates to `node_runtime.evaluate_readiness()`.
- Runtime readiness now uses the canonical Configuration Manager and storage coherence/provider checks.
- Runtime README and readiness model are explicitly supporting documentation and cannot define a second lifecycle.
- Readiness model version aligned to 1.0.0.
- Stale lifecycle tests using `INITIALIZING`, `VERIFYING` and `READY` were replaced with the canonical Node Core states.
- Engine Runtime remains subordinate to Node Core Runtime and cannot redefine Node Core lifecycle.

Boundary:
`Node Core Runtime → Engine Runtime → protocol/application engines`.

**Next PHASE 2 component:** Engine Runtime.


## PHASE 2 — Engine Runtime reconciliation

**Component:** Engine Runtime  
**Status:** PASS

Reconciled chain:

`NODE-CORE-ENGINE-RUNTIME-CONTRACT.md`
→ `ENGINE-RUNTIME-MANIFEST.json`
→ `Engine Runtime/engine_runtime.py`
→ Engine API supporting documentation
→ `Tests/Engine Runtime/test_engine_runtime_contract.py`.

Resolved:
- Engine Runtime implementation now rejects duplicate registration and invalid engine identity/version.
- Engine lifecycle transitions are explicit: `REGISTERED → ACTIVE → STOPPED`.
- Unknown-engine and invalid-state operations fail deterministically.
- Active engines cannot be unregistered.
- STOPPED engines may be restarted according to the canonical baseline.
- Engine API documentation no longer implies that unimplemented operations are part of the implemented baseline.
- Node Core Runtime remains the owner of Node lifecycle; Engine Runtime cannot redefine it.
- Protocol installation/activation remains owned by Protocol Interface.
- CPG-specific semantics remain outside Engine Runtime.

The manifest remains `IMPLEMENTED_PARTIAL` because sandbox/resource-limit controls are not yet implemented; this is an implementation-status fact, not a contract-authority conflict.

**Next PHASE 2 component:** API.


## PHASE 2 — API reconciliation

**Component:** Node Core API  
**Status:** PASS

Reconciled chain:

`Documentation/Interfaces/NODE-CORE-API-CONTRACT.md`
→ `API/NODE-CORE-API-MANIFEST.json`
→ `API/node_core_api.py`
→ API supporting READMEs
→ `Tests/API/test_node_core_api_contract.py`.

Resolved:
- The top-level API README previously listed a broader set of 20 required API domains than the canonical API contract; it now defers to the six canonical domains and treats domain READMEs as supporting documentation.
- API implementation availability remains governed by the API manifest; the facade remains IMPLEMENTED_PARTIAL.
- `health()` no longer unconditionally claims READY when no manager exists.
- `read()` now rejects an empty object identifier deterministically.
- Domain documentation remains subordinate to the canonical API contract and cannot promote DECLARED operations to IMPLEMENTED.
- Protocol isolation is preserved; CPG-specific application semantics remain outside Node Core API.

**Next PHASE 2 component:** Node Manager.


## PHASE 2 — Node Manager reconciliation

**Component:** Node Manager  
**Status:** PASS

Reconciled chain:

`Documentation/Interfaces/NODE-MANAGER-CONTRACT.md`
→ `Node Manager/NODE-MANAGER-MANIFEST.json`
→ `Node Manager/README.md`
→ `Node Manager/node_manager.py`
→ Configuration Manager / Runtime Manager / Engine Runtime / Protocol Interface / Recovery boundaries
→ `Tests/Node Manager/test_node_manager_contract.py`.

Resolved:
- Node Manager now requires canonical configuration before reaching READY.
- Runtime readiness is delegated to Runtime Manager; Node Manager no longer creates an independent readiness interpretation.
- Engine registration is delegated to Engine Runtime instead of maintaining a second engine registry.
- Protocol installation remains delegated to Protocol Interface.
- Recovery is explicitly delegated to Recovery rather than implemented as a local state shortcut.
- Management events are recorded as an auditable control-plane record.
- Node Core composition now injects the single Engine Runtime instance into Node Manager, eliminating duplicate engine authority.
- Node Manager README now identifies itself as supporting documentation and states the subsystem boundaries.
- CPG protocol, ledger, consensus, settlement and Table Wallet remain outside Node Manager.

The manifest remains `IMPLEMENTED_PARTIAL` because full recovery integration and broader management capabilities are not yet complete. This does not block the contract reconciliation.

**Next PHASE 2 component:** Network.


## PHASE 2 — Network reconciliation

**Component:** Network  
**Status:** PASS

Reconciled chain:

`Documentation/Interfaces/NODE-CORE-NETWORK-CONTRACT.md`
→ `Network/NETWORK-CORE-MANIFEST.json`
→ `Network/README.md`
→ `Network/network_manager.py`
→ `Network/peer_registry.py`
→ `Network/transport.py`
→ synchronization state
→ Network API documentation
→ Network contract tests.

Resolved:
- Network manifest version aligned from 0.1.0 to canonical contract version 1.0.0.
- Duplicate peer registration is now rejected deterministically.
- Network state no longer reports `READY`, avoiding collision with Node Core Runtime readiness.
- Network state uses transport semantics: `IDLE`, `REGISTERED`, `CONNECTED`.
- Network API documentation distinguishes implemented reference operations from declared/future operations.
- Synchronization remains separate from connectivity and requires provider readiness plus threshold evidence.
- Protocol isolation is preserved; transport envelopes cannot imply CPG consensus, table state, ledger or synchronization.
- Production authenticated transport, live decentralized discovery and live state synchronization remain explicitly unimplemented in the manifest.

The absence of `message_envelope.py` is not treated as a missing authority: envelope construction is currently implemented in `network_manager.py`; the contract does not require a separate file/module.

**Next PHASE 2 component:** Protocol Interface.


## PHASE 2 — Protocol Interface reconciliation

**Component:** Protocol Interface  
**Status:** IMPLEMENTED_PARTIAL / CONTRACT RECONCILED

Reconciled chain:

`NODE-CORE-PROTOCOL-INTERFACE-CONTRACT.md`
→ `PROTOCOL-INTERFACE-MANIFEST.json`
→ `Protocol Interface/README.md`
→ `Protocol Interface/protocol_interface.py`
→ `API/Protocol API/README.md`
→ `Tests/Protocol Interface/test_protocol_interface.py`.

Resolved:
- Protocol Interface is explicitly the boundary between protocol-neutral Node Core and independently installed protocols.
- The administrative interface is now specified as a minimal Protocols layer with Installed Protocols and Install Protocol sections.
- Visual baseline is fixed at white / black / dark gray / light gray, with hierarchy driven by information importance.
- The remote protocol catalog is the source boundary for available protocols. Supported sources include CID and GitHub. Downloaded packages are written to `Node Core/Protocols/` and become the local source for verification and installation.
- The canonical installed-protocol boundary is `Node Core/Protocols/Installed/`. The remote catalog is never itself treated as an installed protocol.
- The distinction `AVAILABLE INSTALLER ≠ INSTALLED ≠ ACTIVE ≠ RUNNING` is normative.
- Protocol identity remains manifest/descriptor authority.
- Required engine association is delegated to Engine Runtime; Protocol Interface cannot create a second engine lifecycle.
- CPG-specific consensus, ledger, poker rules, table state, Table Wallet, settlement and rake remain outside Node Core.

Implementation remains partial because the repository does not yet implement the complete persistent installer/installed directory workflow, installer verification execution, engine-association execution and a rendered administrative UI.

**Next PHASE 2 action:** integrate the catalog/download boundary with Protocol Interface verification and persistent installation before declaring Protocol Interface PASS.



## PHASE 2 — Protocol Catalog / Source Resolver / Download Boundary

**Component:** Protocol Catalog + Source Resolver + Download Boundary  
**Status:** PASS / SUPPORTING SUBCOMPONENT

Implemented:

- `Protocol Interface/PROTOCOL-CATALOG-MANIFEST.json`;
- `Protocol Interface/protocol_catalog.py`;
- `Protocol Interface/protocol_source_resolver.py`;
- `Protocol Interface/protocol_download.py`;
- `Tests/Protocol Interface/test_protocol_catalog.py`.

Canonical flow:

`Remote Catalog → Source Resolver → Download → Node Core/Protocols/ → Verification → Protocol Interface Installation`

Supported catalog source classes:

- CID;
- GitHub.

The remote source is not itself an installed protocol. Download transport does not activate or install the protocol.

The download boundary currently uses HTTP(S) as the transport mechanism. CID remains the content-addressed source identity and may resolve through an approved HTTP(S) gateway or configured equivalent.

The remaining Protocol Interface gap is integration of these components with persistent package verification, protocol registration/installation and engine association.


## PHASE 2 — Protocol package verification and persistent installation

**Status:** IMPLEMENTED / INTEGRATION RECONCILED

Implemented:
- `Protocol Interface/protocol_package.py` — manifest verification, canonical manifest hashing, protocol identity verification and persistent installation.
- `Protocol Interface/protocol_interface.py` — compatibility gate, registration gate, persistent installation and shared Engine Runtime association.
- `Tests/Protocol Interface/test_protocol_package_installation.py` — verified installation, identity, integrity failure and engine activation path.
- `Node Core/node_core.py` — injects the shared Engine Runtime and Node Core protocol storage boundary into Protocol Interface.

Security boundary:
- ZIP extraction rejects unsafe traversal paths.
- A downloaded package is not installed until its manifest validates and its declared manifest hash matches the canonical hash.
- Installed protocol contents are stored under the Node Core protocol installation boundary with an installation record.
- Protocol Interface never implements CPG semantics.

Current status remains **IMPLEMENTED_PARTIAL** because the complete multi-engine declaration/execution model and rendered administrative UI are not yet closed.


## PHASE 2 — Manifest Authority reconciliation

**Component:** Manifest Authority  
**Status:** PASS

Reconciled chain:

`NODE-CORE-MANIFEST-AUTHORITY-CONTRACT.md`
→ `NODE-CORE-MANIFEST.json`
→ canonical installation schema
→ manifest authority validator
→ manifest authority test vector.

Resolved:
- `NODE-CORE-MANIFEST.json` remains the sole component-manifest authority.
- `Configuration/Schemas/node-core-installation-manifest.schema.json` remains the sole installation-manifest schema authority.
- The legacy `node-installation-manifest.schema.json` remains explicitly classified as legacy/conflicting and cannot become a second authority.
- Component implementation status is now checked against the reconciled state; Protocol Interface is correctly declared `IMPLEMENTED_PARTIAL`.
- Fresh Node Core installation remains protocol-neutral: `protocol_associations=[]` and `cpg_protocol.status=NOT_INSTALLED`.
- Version and status contradictions are treated as validation failures rather than implementation choices.

**Manifest Authority PHASE 2 gate: SATISFIED.**


## PHASE 2 — Security reconciliation

**Component:** Security  
**Status:** IMPLEMENTED_PARTIAL / RECONCILED

Reconciled chain:

`NODE-CORE-SECURITY-CONTRACT.md`
→ `Security/security_service.py`
→ `Tests/Security/test_security_contract.py`.

Resolved:
- Security remains a protocol-neutral boundary and does not replace Identity, Cryptography, Storage, Runtime, Network or Protocol Interface.
- Path validation now fails closed for invalid/empty input, absolute paths, traversal components and protocol-reserved prefixes.
- Authorization guard remains fail-closed and cannot silently elevate privileges.
- Protocol-reserved state remains protected without implementing CPG semantics.
- Security does not define cryptographic algorithms or custody private keys.
- Negative-path coverage was expanded.

Remaining partial scope is explicit: security audit logging and secure-configuration enforcement are not yet implemented.

**PHASE 2 Security reconciliation: SATISFIED.**
