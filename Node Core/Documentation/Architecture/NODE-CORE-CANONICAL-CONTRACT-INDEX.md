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
| Configuration | `Documentation/Interfaces/NODE-CORE-CONFIGURATION-CONTRACT.md` | CANONICAL / IMPLEMENTED_PARTIAL | `Configuration/configuration_manager.py`, `Configuration/Schemas/node-configuration.schema.json` | `Tests/Configuration/test_configuration_manager_canonical.py` | Schema boundary and explicit validated mutation path reconciled; full negative-path matrix and deeper schema execution integration remain |
| Identity | `Identity/FORMAL-IDENTITY-PROFILE-v1.0.md` | CANONICAL / IMPLEMENTED_PARTIAL | `Identity/identity_core.py`, `identity_api.py`, schema, binding, verification, recovery | `Tests/Identity/test_identity_core.py`, `test_identity_implementation.py`, `test_identity_completion.py` | Canonical identity lifecycle and activation boundary reconciled; trust/registration authority, revocation and durable secure identity storage remain partial |
| Cryptography | `Cryptography/Core/FORMAL-CRYPTOGRAPHIC-PROFILE-v1.0.md` | CANONICAL / IMPLEMENTED_PARTIAL | `Cryptography/Core/crypto_core.py`, `crypto_service.py`, `primitives.py`, `signatures.py` | `Tests/Cryptography/test_crypto_core.py`, `test_crypto_implementation.py`, `test_signatures.py` | Canonical serialization, SHA-256, CSPRNG and Ed25519 boundary reconciled; AEAD profile remains open and Merkle is explicitly deferred to a separate specification |
| Storage | `Documentation/Interfaces/NODE-CORE-STORAGE-CONTRACT.md` | CANONICAL / IMPLEMENTED | `Storage/storage_engine.py`, `Storage/API/storage_api.py`, `Storage/Storage Manager/storage_manager.py`, `Storage/Object Registry/object_registry.py`, `Storage/Providers/storage_provider.py`, `Storage/storage_locator.py`, `Storage/Synchronization/synchronization_manager.py`, `Storage/Disaster Recovery/storage_recovery.py` | `Tests/Storage/test_storage_engine.py`, `test_storage_api.py`, `test_storage_locator.py`, `test_object_registry.py`, `test_storage_complete.py` | Required create/read/write/update/delete/exists/locate/verify/synchronize/recover boundary reconciled; canonical metadata now enforced |
| Runtime | `Documentation/Runtime/NODE-CORE-RUNTIME-LIFECYCLE.md` | CANONICAL | `Runtime/State/runtime_state.py`, `Runtime/runtime_manager.py`, `Runtime/node_runtime.py` | Existing runtime tests plus lifecycle tests; dedicated contract coverage remains to be expanded | Lifecycle source and implementation state machine reconciled; readiness bug corrected |
| Recovery | `Documentation/Interfaces/NODE-CORE-RECOVERY-CONTRACT.md` | CANONICAL / IMPLEMENTED_PARTIAL | `Recovery/recovery_manager.py`, `recovery_state.py` | `Tests/Recovery/test_recovery_implementation.py`, `test_recovery_manager_canonical.py` | Canonical recovery state machine, traceability journal and non-overwrite behavior reconciled; broader restoration/reconciliation sources remain outside generic Recovery |
| Network | `Documentation/Interfaces/NODE-CORE-NETWORK-CONTRACT.md` | CANONICAL | `Network/network_manager.py`, `peer_registry.py`, `transport.py`, `Synchronization/synchronization_state.py` | `Tests/Network/test_network_contract.py`, `test_synchronization_state.py` | Contract, implementation, synchronization boundary and protocol isolation mapped |
| Node Manager | `Documentation/Interfaces/NODE-MANAGER-CONTRACT.md` | CANONICAL | `Node Manager/node_manager.py` | `Tests/Node Manager/test_node_manager_contract.py` | Contract/implementation aligned; protocol installation routed through Protocol Interface |
| Security | `Documentation/Interfaces/NODE-CORE-SECURITY-CONTRACT.md` | CANONICAL / IMPLEMENTED_PARTIAL | `Security/security_service.py` | `Tests/Security/test_security_contract.py` | Path, fail-closed authorization and protocol-isolation baseline reconciled; audit log and secure-configuration enforcement remain partial |
| Time | `Documentation/Interfaces/NODE-CORE-TIME-CONTRACT.md` | CANONICAL / IMPLEMENTED_PARTIAL | `Time/time_service.py` | `Tests/Time/test_time_contract.py` | Timestamp, logical ordering and hash-chain integrity including predecessor verification reconciled; network-time consensus intentionally excluded |
| Engine Runtime | `Documentation/Interfaces/NODE-CORE-ENGINE-RUNTIME-CONTRACT.md` | CANONICAL | `Engine Runtime/engine_runtime.py` | `Tests/Engine Runtime/test_engine_runtime_contract.py` | Boundary and baseline implementation/test now mapped |
| API | `Documentation/Interfaces/NODE-CORE-API-CONTRACT.md` | CANONICAL | `API/node_core_api.py` (partial facade) | `Tests/API/test_node_core_api_contract.py` | Contract authority established; implementation remains explicitly PARTIAL |
| CLI | `Documentation/Interfaces/NODE-CORE-CLI-CONTRACT.md` | CANONICAL / IMPLEMENTED_PARTIAL | `CLI/node_cli.py` | `Tests/CLI/test_node_cli_canonical.py` | Canonical command subset delegates to Node Manager; parser behavior remains standard and broader command catalog remains intentionally closed |
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


## PHASE 2 — Time reconciliation

**Component:** Time  
**Status:** IMPLEMENTED_PARTIAL / RECONCILED

Reconciled chain:

`NODE-CORE-TIME-CONTRACT.md`
→ `Time/time_service.py`
→ `Tests/Time/test_time_contract.py`.

Resolved:
- Local system time remains an observation, not consensus authority.
- Timestamp validation rejects invalid and negative values.
- Logical sequence remains independent of wall-clock confidence.
- Record hashing follows the canonical deterministic serialization.
- The first record requires a null predecessor.
- Subsequent records reference the immediately preceding hash.
- Explicit predecessor/hash verification is now implemented and tested.
- Runtime and network components cannot promote Time into a consensus authority.
- CPG timers and protocol-specific temporal consensus remain outside Node Core.

Network-time consensus remains intentionally unimplemented.

**PHASE 2 Time reconciliation: SATISFIED.**


## PHASE 2 — Identity reconciliation

**Component:** Identity  
**Status:** IMPLEMENTED_PARTIAL / RECONCILED

Reconciled chain:

`FORMAL-IDENTITY-PROFILE-v1.0.md`
→ `Identity/identity_core.py`
→ `Identity/identity_api.py`
→ identity schema / binding / verification / recovery boundaries
→ Identity tests.

Resolved:
- The canonical Node Identity lifecycle is now explicit: `UNINITIALIZED → GENERATED_OR_IMPORTED → VALIDATED → REGISTERED → ACTIVE`.
- The previous implementation lifecycle `CREATED → INITIALIZED → ACTIVE` is no longer presented as the Identity lifecycle.
- Node Life remains a separate operational lifecycle with hash-linked events; it does not replace Identity state.
- Identity activation now requires an explicit `node_core_ready=True` readiness assertion.
- Identity records remain free of private-key material.
- Deterministic Node ID derivation and canonical identity validation remain enforced.
- The Identity API now imports the actual canonical Identity Manager implementation and exposes validate/register boundaries.
- CPG player identity, wallet ownership, table membership, CPG consensus and protocol-specific authorization remain outside Node Core Identity.

Remaining partial scope:
- authoritative registration/trust mechanism;
- explicit revocation authority;
- durable secure identity storage;
- full integration of identity activation with the Node Core Runtime/Node Manager lifecycle.

**PHASE 2 Identity reconciliation: SATISFIED.**

**Next PHASE 2 component:** Cryptography.


## PHASE 2 — Cryptography reconciliation

**Component:** Cryptography  
**Status:** IMPLEMENTED_PARTIAL / RECONCILED

Reconciled chain:

`FORMAL-CRYPTOGRAPHIC-PROFILE-v1.0.md`
→ `Cryptography/Core/crypto_core.py`
→ `crypto_service.py`
→ `signatures.py`
→ compatibility primitives
→ Cryptography tests.

Resolved:
- Canonical UTF-8 JSON serialization is centralized in `crypto_core.py`.
- SHA-256 and canonical-object hashing use one deterministic implementation.
- CSPRNG generation and invalid-size rejection remain fail-closed.
- Ed25519 key generation, exact-byte signing and verification are exposed through one service boundary.
- Invalid Ed25519 signatures now fail closed instead of propagating backend `InvalidSignature` exceptions.
- The previous duplicate Merkle implementation was removed from the generic primitive layer because the canonical profile explicitly reserves Merkle tree construction for a separate deterministic specification.
- Node Core composition now exposes the Cryptography Core path required by the Crypto Service import boundary.
- Private-key custody remains external; cryptographic functions only receive key material as operation input.
- CPG-specific cryptography remains outside this component.

Remaining partial scope:
- production AEAD algorithm/profile, nonce construction, key derivation and key lifecycle;
- AEAD test vectors;
- deterministic Merkle specification and test vectors.

**PHASE 2 Cryptography reconciliation: SATISFIED.**

**Next PHASE 2 component:** Bootstrap residual / cross-component validation.


## PHASE 2 — Storage reconciliation

**Component:** Storage  
**Status:** IMPLEMENTED / RECONCILED

Reconciled chain:

`Documentation/Interfaces/NODE-CORE-STORAGE-CONTRACT.md`
→ Storage Engine
→ Storage Manager
→ Storage API
→ Object Registry
→ Provider boundary
→ Locator
→ Synchronization
→ Disaster Recovery
→ Storage tests.

Resolved:
- The public Storage boundary now exposes the complete required operation set: `create`, `read`, `write`, `update`, `delete`, `exists`, `locate`, `verify`, `synchronize`, and `recover`.
- `StorageManager` remains the orchestration authority; `StorageEngine` remains the physical/provider execution layer.
- Canonical metadata is now explicit: `object_id`, `version`, `content_hash`, `storage_class`, `location`, `state`, `created_at`, and `updated_at`, while compatibility fields remain available where required.
- Object version increments on update while creation time remains stable.
- Object Registry now enforces the canonical metadata relationship `object_class == storage_class` and `state == object_state`.
- Protocol-reserved storage remains protected from ordinary Node Core writes.
- Local Storage remains the authoritative node-local fallback.
- Kubo/IPFS remains an external provider adapter and is never treated as a second local registry.
- Distributed reads require content-hash verification; invalid/unavailable distributed data falls back to valid local state.
- Recovery requires a verified distributed source before restoring local state.
- Storage path traversal and provider/state validation remain fail-closed.
- CID remains distinct from `object_id`, `operation_id`, and `content_hash`.
- Storage contains no CPG ledger, consensus, poker state, settlement or rake semantics.

**PHASE 2 Storage reconciliation: SATISFIED.**

**Next PHASE 2 component:** Recovery.


## PHASE 2 — Recovery reconciliation

**Component:** Recovery  
**Status:** IMPLEMENTED_PARTIAL / RECONCILED

Reconciled chain:

`Documentation/Interfaces/NODE-CORE-RECOVERY-CONTRACT.md`
→ `Recovery/recovery_manager.py`
→ `Recovery/recovery_state.py`
→ Recovery tests
→ Node Manager recovery boundary.

Resolved:
- Generic Recovery now has the canonical lifecycle: `NORMAL → FAILURE_DETECTED → RECOVERY_PENDING → RECOVERING → VERIFYING → RECOVERED / FAILED`.
- Recovery attempts are traceable through a persistent journal.
- A previously verified recovered state is not silently overwritten on a repeated recovery call.
- Post-recovery verification is explicit.
- Node Manager accepts the canonical recovered completion state while retaining its own Node Manager lifecycle.
- Generic Recovery does not invent protocol-specific restoration semantics.
- Storage object restoration remains owned by Storage Recovery.
- Private-key recovery remains external to Node Core.
- CPG ledger/table/consensus recovery remains outside Node Core.

Remaining partial scope:
- full failure-source detection integration;
- generalized checkpoint/journal reconciliation;
- broader component restoration orchestration;
- cryptographic identity continuity recovery integration.

**PHASE 2 Recovery reconciliation: SATISFIED.**

**Next PHASE 2 component:** CLI / Configuration residual.


## PHASE 2 — CLI / Configuration residual reconciliation

### CLI
**Status:** IMPLEMENTED_PARTIAL / RECONCILED

Resolved:
- canonical command set remains limited to `status`, `readiness`, `start`, `stop`, `recover`;
- CLI delegates lifecycle operations to Node Manager;
- CLI does not own lifecycle state;
- successful output is deterministic compact JSON;
- operational failures return non-zero status with structured JSON errors;
- CPG-specific operations remain outside the Node Core CLI;
- canonical CLI tests were added.

Remaining:
- complete command catalog is intentionally not expanded until remaining Node Core contracts close.

### Configuration
**Status:** IMPLEMENTED_PARTIAL / RECONCILED

Resolved:
- canonical schema remains the structural authority;
- Configuration Manager retains validation as the runtime implementation boundary;
- explicit `update()` operation now validates the complete candidate configuration before atomic replacement;
- unknown properties and invalid states fail closed;
- CPG cannot be installed or activated through Configuration Manager;
- configuration writes use an atomic replacement boundary;
- canonical configuration mutation is separated from Protocol Interface lifecycle control;
- canonical Configuration tests were added.

Remaining:
- complete negative-path matrix;
- deeper automated execution against the JSON Schema authority rather than relying primarily on equivalent runtime validation.

**PHASE 2 CLI / Configuration reconciliation: SATISFIED.**

**Next PHASE 2 component:** Bootstrap residual / cross-component validation.


## PHASE 4 — Cross-component integration started

After Storage, Recovery, CLI and Configuration reconciliation, the reference composition was updated so that:

- `NodeCore` owns one Storage API boundary;
- `NodeCore` owns one Recovery Manager;
- the same Recovery Manager is injected into Node Manager;
- Engine Runtime remains shared between Node Manager and Protocol Interface;
- Protocol Interface does not receive or own Recovery;
- Storage remains separate from protocol semantics;
- a composition integration test now checks these dependency boundaries.

**PHASE 4 initial composition gate: IMPLEMENTED / TEST VECTOR ADDED.**

This does **not** yet mean the full Node Core lifecycle integration is closed. Runtime ↔ Identity ↔ Storage ↔ Recovery ↔ Network ↔ Protocol Interface still requires end-to-end validation.

**Next logical work:** cross-component lifecycle tests, then full Node lifecycle.


## PHASE 4 — Managed Kubo / Dual Storage architectural decision

The previous adapter-only model is superseded by the following canonical provider architecture:

**Adapter layer**
- remains small;
- translates Node Core Storage operations to Kubo API/RPC;
- does not contain Kubo itself.

**Managed provider layer**
- downloads the complete official Kubo distribution;
- verifies the release package;
- installs the selected version under the Node Core root;
- initializes a dedicated Kubo repository;
- sets an explicit absolute `IPFS_PATH`;
- records version, repository, runtime and health state;
- starts/stops the Kubo node through a controlled provider manager.

**Canonical Linux layout**

`<Node Core Root>/External Providers/Kubo/<version>/`

for Kubo installation, and

`<Node Core Root>/node-storage/providers/kubo/repository/`

for the Kubo repository.

Node Core does not modify Kubo's internal repository structure. The explicit `IPFS_PATH` is the relocation mechanism that prevents Kubo's default `~/.ipfs` assumptions from leaking into the installation.

**Dual Storage activation**

`LOCAL_ONLY → KUBO_PROVISIONING → INITIAL_SYNC → COHERENCE_VERIFIED → DUAL_STORAGE`

The user-facing Storage Preference `DUAL_STORAGE` is enabled only after complete Kubo provisioning and successful initial synchronization.

Initial synchronization is a logical Storage Manager operation, not a filesystem copy. Restricted/private objects are encrypted before distribution. Temporary or policy-excluded objects remain governed by Storage Policy.

Linux is the first implementation target. Windows follows the same logical contract. iOS remains a later platform-specific target and must not be assumed to run the same Kubo daemon model.

This decision preserves the Node Core baseline invariant: Kubo is **never silently installed**, but it can be fully provisioned when the operator explicitly chooses decentralized/dual storage.


## PHASE 4 — Kubo Node Installer / Manager design gate

**Status:** CANONICAL DESIGN / IMPLEMENTATION NOT STARTED

The Kubo provider is now divided into two explicit boundaries:

1. **Kubo Adapter** — translates Node Core Storage operations to Kubo's supported API/RPC.
2. **Kubo Node Installer / Manager** — provisions the complete official Kubo distribution, owns the installation environment and manages its lifecycle.

The Installer / Manager design freezes:
- versioned Kubo installation paths;
- separate Kubo repository path;
- absolute `IPFS_PATH` management;
- explicit stable-release selection;
- package verification before activation;
- repository initialization through Kubo's own mechanisms;
- persistent provider state;
- complete installation/runtime lifecycle;
- failure-closed activation;
- explicit upgrade boundary;
- Linux-first platform policy;
- `KUBO READY ≠ DUAL STORAGE READY`.

No installer implementation is authorized yet. The next gate is to freeze the release-source/architecture matrix, provider-state schema and installation test vectors.


## PHASE 4 — Kubo release/platform/state/test gate

**Status:** DESIGN GATE SATISFIED

Frozen artifacts:
- KUBO-RELEASE-AND-PLATFORM-MATRIX-v1.0.md
- KUBO-PROVIDER-STATE-SCHEMA-v1.0.md
- KUBO-NODE-INSTALLER-TEST-VECTORS-v1.0.md

The release resolver now has a normative source boundary, Linux-first architecture matrix, explicit Windows future boundary and deferred iOS contract.

Provider state separates lifecycle, health and synchronization state. READY is stronger than HEALTHY.

The test vectors establish fail-closed behavior for package integrity, paths, executable/version mismatch, initialization, process failure, synchronization, coherence, Dual Storage gating, restart and upgrade.

Implementation may now begin for Linux only, subject to the canonical contracts.


## PHASE 4 — Kubo Linux implementation foundation

**Status:** IMPLEMENTED_PARTIAL / FOUNDATION PASS

Implemented:
- release resolution from supplied official metadata;
- stable/exact-version selection policy;
- Linux architecture normalization;
- canonical Node Core Kubo path derivation;
- absolute IPFS_PATH generation;
- path containment validation;
- atomic provider-state persistence;
- READY gating on health + synchronization state;
- foundation test vectors.

Not yet implemented:
- live upstream metadata retrieval;
- package download;
- package integrity verification;
- extraction/install;
- repository initialization;
- Kubo process manager;
- health manager;
- initial synchronization;
- Dual Storage activation.

The implementation deliberately stops before executing external Kubo code.


## PHASE 4 — Kubo verified acquisition implementation

**Status:** IMPLEMENTED_PARTIAL / ACQUISITION PASS

Implemented:
- official Kubo distribution source boundary;
- stable release metadata retrieval;
- release artifact URL construction;
- official SHA-512 sidecar retrieval;
- bounded temporary package download;
- SHA-512 verification before promotion;
- atomic promotion from incoming package to verified package area.

Not yet implemented:
- Kubo installation/extraction;
- repository initialization;
- process lifecycle;
- health management;
- initial synchronization;
- Dual Storage activation.

The acquisition layer cannot execute the downloaded Kubo binary.


## PHASE 4 — Kubo verified package installation

**Status:** IMPLEMENTED_PARTIAL / INSTALLATION PASS

Implemented:
- verified-package-only installation boundary;
- Linux tar.gz safe extraction with traversal/link checks;
- immutable versioned installation directory;
- executable discovery and version verification;
- Kubo installation manifest generation;
- installation manifest JSON schema;
- installer safety tests.

The installer does not initialize the Kubo repository, configure the daemon, start Kubo, or activate Dual Storage.


## PHASE 4 — Kubo repository initialization

**Status:** IMPLEMENTED_PARTIAL / REPOSITORY INITIALIZATION PASS

The installed Kubo executable is invoked with an explicit absolute IPFS_PATH. The initializer verifies the generated repository config, Kubo PeerID and repository version marker. Kubo repository identity is explicitly separate from Node Core cryptographic identity.

The initializer does not start the daemon, perform initial synchronization or activate Dual Storage.


## PHASE 4 — Kubo coherence and Dual Storage readiness

**Status:** IMPLEMENTED_PARTIAL / COHERENCE PASS

The Kubo mirror is now independently verified against the canonical local Storage Manager registry, local content hash, distributed content hash, CID and provider integrity result. Dual Storage readiness is an evidence-based gate and cannot be asserted merely because Kubo is running.

The persistent configuration/UI preference is intentionally still separate: the readiness gate proves the provider pair is coherent; configuration may only activate Dual Storage after that evidence exists.
