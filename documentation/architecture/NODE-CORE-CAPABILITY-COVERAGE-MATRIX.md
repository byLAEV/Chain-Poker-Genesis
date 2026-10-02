# Node Core Capability Coverage Matrix

**Status:** Reconciled working matrix  
**Purpose:** Establish which Node Core capabilities already have specification, implementation, and verification evidence before physical repository migration.

| Capability | Specification evidence | Implementation evidence | Test / verification evidence | Current state |
|---|---|---|---|---|
| Bootstrap / installation | `docs/node/NODE-CORE-BOOTSTRAP-SPECIFICATION.md`, `NODE-INSTALLATION-CONTRACT.md`, `INSTALLATION-BASELINE.md` | `reference-implementation/node-installation/` | installation manifest, E2E installation tests, verification scripts | **IMPLEMENTED + VERIFIED (baseline)** |
| Runtime lifecycle | `NODE-CORE-RUNTIME-LIFECYCLE.md` | `node_runtime.py`, runtime state module | `test_runtime_lifecycle.py` | **IMPLEMENTED + TESTED** |
| Readiness | `NODE-READINESS-STATE-MODEL.md`, `HEALTH-AND-READINESS-SPECIFICATION.md` | runtime/readiness implementation | health/recovery tests | **IMPLEMENTED + TESTED** |
| Storage manager | `STORAGE-COHERENCE-SPECIFICATION.md`, storage specifications | `storage_manager.py` | `test_storage_manager.py` | **IMPLEMENTED + TESTED** |
| Storage locator | storage architecture/specifications | `storage_locator.py` | `test_storage_locator.py` | **IMPLEMENTED + TESTED** |
| Storage provider abstraction | deterministic storage architecture + storage provider specification | `storage_provider.py` | `test_storage_provider.py` | **IMPLEMENTED + TESTED (baseline)** |
| Storage manifest | `NODE-CORE-INSTALLATION-MANIFEST.md` and storage specifications | installation manifest tooling | schema validation + installation tests | **IMPLEMENTED + VERIFIED** |
| Object registry | `OBJECT-REGISTRY-SPECIFICATION.md` | `object_registry.py` | `test_object_registry.py` | **IMPLEMENTED + TESTED** |
| Recovery | `RECOVERY-INTEGRATION-SPECIFICATION.md` | runtime/recovery material | `test_health_recovery.py` + installation verification | **IMPLEMENTED + TESTED (baseline)** |
| Specification coverage | `NODE-CORE-SPECIFICATION-COVERAGE-AUDIT.md` | `test_specification_coverage.py` | coverage test | **AUDITED** |
| Release integrity | `NODE-CORE-RELEASE-INTEGRITY.md`, release artifact specification | release/verification tooling | CI coverage material | **SPECIFIED; verification path exists** |
| Node identity | node installation architecture + cryptographic connection material | identity/bootstrap material | partially covered by installation verification | **PARTIAL / RECONCILIATION REQUIRED** |
| Cryptographic primitives | Cryptographic Core Engine specification | reference implementation boundary exists, but not yet canonicalized as Node Core package | needs unified conformance set | **SPECIFIED / PARTIAL IMPLEMENTATION** |
| Cryptographic connection / credentials | Cryptographic Connection Engine specification | identity/bootstrap integration | requires dedicated conformance tests | **SPECIFIED / PARTIAL** |
| Protocol cryptography | Cryptographic Engine specification | separate from generic Node Core | protocol-level tests required | **PROTOCOL CORE, NOT NODE CORE** |
| Synchronization | node/storage architecture + synchronization state specification | `synchronization_state.py` | `test_synchronization_state.py` | **STATE MODEL IMPLEMENTED; DISTRIBUTED SYNC INCOMPLETE** |
| Networking substrate | Node Core architecture + P2P material | distributed networking implementation boundary | needs conformance coverage | **OPEN / PARTIAL** |
| Conflict resolution | P2P conflict-resolution engine | protocol/network implementation boundary | needs explicit Node/Core ownership tests | **BOUNDARY REQUIRES RECONCILIATION** |
| Versioning | release/versioning specifications | partial tooling | requires compatibility tests | **OPEN** |
| Canonical Node Core package boundary | multiple architecture documents | currently distributed across repository | audit documents exist | **NOT YET CANONICALIZED** |

## State interpretation

- **IMPLEMENTED + TESTED**: executable reference material and tests are present.
- **IMPLEMENTED + VERIFIED (baseline)**: executable baseline has explicit verification but is not a claim of production distributed completeness.
- **SPECIFIED / PARTIAL**: architecture exists but implementation/conformance is incomplete or distributed.
- **OPEN**: architectural or implementation work remains.
- **PROTOCOL CORE**: intentionally outside generic Node Core.

## Key result

The current repository has enough evidence to define a canonical Node Core source boundary without inventing new functionality.

The strongest completed baseline is:

```
bootstrap
→ storage
→ manifest
→ object registry
→ runtime
→ readiness
→ recovery
→ verification
```

The major remaining Node Core work is not basic bootstrap. It is:

```
identity
+ cryptographic identity lifecycle
+ networking substrate
+ distributed synchronization
+ recovery semantics
+ versioning
+ conformance
```

## Canonicalization rule

Do not create duplicate implementations while reorganizing.

The existing reference implementation should become the source from which the future canonical `node-core/` implementation boundary is derived, while the existing specifications remain the architectural source of truth until each implementation component is explicitly reconciled.

## Next step

Create the **Node Core canonicalization map**:

```
current file
→ capability
→ canonical package
→ specification
→ schema
→ implementation
→ test
→ migration action
```

Only after that map is complete should physical files be moved.
