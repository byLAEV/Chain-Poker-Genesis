# Node Core Canonicalization Map

**Status:** Working canonicalization map  
**Purpose:** Map existing Node Core artifacts to their future canonical capability, implementation boundary, tests, and migration action before physical movement.

## Canonicalization principle

The repository is not to be reorganized by filename alone. Every artifact must have a traceable relationship:

`current artifact → capability → canonical package → specification/schema → implementation → test → migration action`

## Map

| Current artifact / family | Capability | Canonical package | Specification source | Implementation source | Verification | Migration action |
|---|---|---|---|---|---|---|
| `docs/node/NODE-CORE-BOOTSTRAP-SPECIFICATION.md` | Bootstrap | `node-core/bootstrap` | Same | `reference-implementation/node-installation/` | installation E2E + verification | DOC MOVE LATER |
| `docs/node/NODE-INSTALLATION-CONTRACT.md` | Installation contract | `node-core/bootstrap` | Same | installation scripts | installation tests | DOC MOVE LATER |
| `docs/node/INSTALLATION-BASELINE.md` | Installation baseline | `node-core/bootstrap` | Same | installation reference | baseline verification | DOC MOVE LATER |
| `docs/node/NODE-CORE-RUNTIME-LIFECYCLE.md` | Runtime lifecycle | `node-core/runtime` | Same | `node_runtime.py` / runtime modules | `test_runtime_lifecycle.py` | DOC MOVE LATER |
| `docs/node/NODE-READINESS-STATE-MODEL.md` | Readiness state | `node-core/runtime/readiness` | Same | runtime/readiness | readiness tests | DOC MOVE LATER |
| `docs/node/HEALTH-AND-READINESS-SPECIFICATION.md` | Health/readiness | `node-core/runtime/readiness` | Same | reference runtime | health/recovery tests | DOC MOVE LATER |
| `docs/node/OBJECT-REGISTRY-SPECIFICATION.md` | Object registry | `node-core/storage/object-registry` | Same | `object_registry.py` | `test_object_registry.py` | DOC MOVE LATER |
| `docs/node/STORAGE-COHERENCE-SPECIFICATION.md` | Storage coherence | `node-core/storage/coherence` | Same | storage manager + verifier | storage coherence verification | DOC MOVE LATER |
| `docs/node/NODE-CORE-INSTALLATION-MANIFEST.md` | Installation manifest | `node-core/manifests` | Same | manifest tooling | schema validation + E2E | DOC MOVE LATER |
| `docs/node/RECOVERY-INTEGRATION-SPECIFICATION.md` | Recovery | `node-core/recovery` | Same | recovery/runtime modules | recovery tests | DOC MOVE LATER |
| `docs/node/PROTOCOL-INSTALLATION-BOUNDARY.md` | Node/Protocol boundary | `documentation/architecture` | Same | N/A | architecture audit | DOC RECLASSIFY |
| `docs/node/NODE-CORE-SPECIFICATION-COVERAGE-AUDIT.md` | Specification audit | `documentation/architecture/audits` | Same | coverage test | `test_specification_coverage.py` | DOC RECLASSIFY |
| `docs/node/FINAL-NODE-CORE-AUDIT.md` | Completion audit | `documentation/architecture/audits` | Same | verification scripts | final audit | DOC RECLASSIFY |
| `docs/node/NODE-CORE-COMPLETION-GATE.md` | Completion gate | `documentation/architecture/audits` | Same | completion verification | gate test | DOC RECLASSIFY |
| `docs/node/NODE-CORE-COMPLETION-RECORD.md` | Completion record | `documentation/architecture/audits` | Same | N/A | audit record | DOC RECLASSIFY |
| `docs/node/NODE-CORE-RELEASE-INTEGRITY.md` | Release integrity | `node-core/release` + documentation | Same | release verification | CI/release checks | SPLIT DOC/TOOL LATER |
| `docs/node/NODE-CORE-RELEASE-ARTIFACT-SPECIFICATION.md` | Release artifact | `node-core/release` | Same | release tooling | release validation | DOC MOVE LATER |
| `docs/node/LAEV-NODE-CORE-SPECIFICATION-RECONCILIATION.md` | Architectural reconciliation | `documentation/architecture/audits` | Same | N/A | audit | DOC RECLASSIFY |
| `reference-implementation/node-installation/node_runtime.py` | Runtime | `node-core/runtime` | runtime lifecycle spec | Same | runtime lifecycle tests | CODE MOVE LATER |
| `reference-implementation/node-installation/runtime_state.py` | Runtime state | `node-core/runtime/state` | readiness/lifecycle specs | Same | runtime tests | CODE MOVE LATER |
| `reference-implementation/node-installation/storage_manager.py` | Storage manager | `node-core/storage` | storage coherence specs | Same | storage manager tests | CODE MOVE LATER |
| `reference-implementation/node-installation/storage_locator.py` | Storage locator | `node-core/storage` | storage architecture | Same | locator tests | CODE MOVE LATER |
| `reference-implementation/node-installation/storage_provider.py` | Provider abstraction | `node-core/storage/providers` | storage/provider specs | Same | provider tests | CODE MOVE LATER |
| `reference-implementation/node-installation/object_registry.py` | Object registry | `node-core/storage/object-registry` | object registry spec | Same | registry tests | CODE MOVE LATER |
| `reference-implementation/node-installation/verify_storage_coherence.py` | Storage verification | `tests/node-core/storage` or `tools/validation` | storage coherence | Same | executable verifier | RECLASSIFY AFTER TEST/TOLL SPLIT |
| `reference-implementation/node-installation/verify_node_installation.py` | Installation verification | `tests/node-core/bootstrap` or `tools/validation` | installation contract | Same | executable verifier | RECLASSIFY AFTER TEST/TOOL SPLIT |
| `reference-implementation/node-installation/validate_installation_manifest_schema.py` | Schema validation | `tools/validation` | manifest schema | Same | schema validation | MOVE LATER |
| `reference-implementation/node-installation/test_*.py` | Node Core tests | `tests/node-core` | corresponding specs | tests | test runner | MOVE LATER |
| `engines/cryptographic-core-engine/SPECIFICATION.md` | Cryptographic primitives | `node-core/cryptography/core` | Same | implementation not yet canonicalized | dedicated crypto conformance required | RECLASSIFY + MOVE LATER |
| `engines/cryptographic-connection-engine/` | Identity/credential lifecycle | `node-core/identity/cryptographic-connection` | Same | implementation boundary requires reconciliation | dedicated identity/credential tests required | RECLASSIFY + MOVE LATER |
| `engines/cryptographic-engine/` | CPG-specific cryptography | `protocol-core/cryptography` candidate | Same | protocol implementation | protocol conformance | KEEP OUTSIDE GENERIC NODE CORE |
| `deterministic-manifest-based-node-and-protocol-storage-architecture/` | Storage architecture | `documentation/architecture/storage` + canonical schemas | existing storage architecture | reference storage implementation | storage tests | SPLIT DOC/SCHEMA LATER |
| `docs/developer-specifications/node-infrastructure/` | Node infrastructure specs | `documentation/node-core` | existing specs | N/A | coverage audit | CONSOLIDATE DOCS |
| `docs/developer-specifications/storage/` | Storage specs/schemas | `documentation/node-core/storage` + schemas | existing specs | storage implementation | storage tests | CONSOLIDATE DOCS/SCHEMAS |

## Important classification

### Canonical implementation candidates

These are candidates to become actual source packages:

- bootstrap;
- identity;
- cryptography/core;
- storage;
- manifests;
- object registry;
- runtime;
- recovery;
- networking;
- synchronization;
- versioning.

### Documentation-only candidates

These should not become runtime packages:

- completion records;
- completion audits;
- specification coverage audits;
- reconciliation reports;
- architecture matrices;
- rendered PDFs.

### Test/tool candidates

Verification scripts and tests should not remain mixed with runtime modules indefinitely. They should be separated into test and validation/tooling boundaries while preserving execution behavior.

## Critical unresolved boundaries

1. Cryptographic Connection Engine → Node Core identity.
2. Cryptographic Engine → CPG Protocol Core.
3. P2P networking substrate → Node Core.
4. P2P conflict resolution semantics → Node Core vs Protocol Core.
5. Synchronization state model → Node Core implementation.
6. Verification scripts → tests vs tools.
7. Deterministic storage architecture → documentation vs schemas vs implementation.

## Migration readiness

The repository is **not yet ready for bulk migration**.

It is ready for the next controlled operation:

> create a canonical target tree specification, without moving source files yet.

That target tree should be generated from this map and then compared against every existing path before the first physical migration commit.
