# Node Core Reference Implementation Dependency Map

## Baseline result

The reference implementation is tightly coupled to its current relative file layout. A physical move is therefore not a cosmetic operation.

## Direct executable dependencies

| Source | Depends on | Migration implication |
|---|---|---|
| `health_readiness.py` | `node_runtime.py` | same package boundary required or import rewrite |
| `node_runtime.py` | `storage_provider.py`, `runtime_state.py` | runtime/storage imports must remain resolvable |
| `storage_locator.py` | `object_registry.py`, `storage_provider.py` | storage package dependency |
| `storage_provider.py` | `storage_manager.py` | storage package dependency |
| `recovery_manager.py` | `node_runtime.py`, `runtime_state.py` | runtime/recovery boundary must be explicit |
| `protocol_installation_boundary.py` | installation manifest | protocol boundary remains coupled to generated node manifest |
| `validate_installation_manifest_schema.py` | `docs/node/node-core-installation-manifest.schema.json` | schema path must be repaired before code move |
| `release_integrity.py` | multiple `docs/node/*` and implementation files | release verifier must be path-independent or updated |
| `test_node_installation_e2e.py` | runtime, health, recovery, generated manifest | test must move only after source path is stable |

## Critical finding

The implementation contains direct relative imports such as `from node_runtime import ...` and `from storage_provider import ...`. Therefore the target package cannot be created by simply copying files into nested package directories without changing the import model.

## Second critical finding

`validate_installation_manifest_schema.py` directly computes a schema path using its current repository depth and references `docs/node/node-core-installation-manifest.schema.json`.

Therefore the earlier documentation migration creates a temporary compatibility dependency that must be repaired before executable migration.

## Third critical finding

`release_integrity.py` contains a list of repository-relative documentation and implementation paths. This is part of the release integrity contract and must be updated atomically with any physical relocation.

## Safe migration strategy

Do not restructure individual modules into nested Python packages yet.

First create the target executable boundary as a **flat compatibility package**:

```text
implementation/reference/node-core/
├── bootstrap_node.py
├── health_readiness.py
├── node_runtime.py
├── object_registry.py
├── protocol_installation_boundary.py
├── recovery_manager.py
├── release_integrity.py
├── runtime_state.py
├── storage_locator.py
├── storage_manager.py
├── storage_provider.py
└── synchronization_state.py
```

This preserves the current import topology while establishing the new canonical location.

Tests and validation scripts should remain in the old directory until the source move is validated. They should then be migrated as a separate operation.

## Migration gate

Before moving executable source:

1. repair schema references caused by documentation migration;
2. identify every path literal in `release_integrity.py`;
3. identify all remaining `docs/node/` references;
4. create a path compatibility checklist;
5. move the flat implementation as one atomic change;
6. update only path references required by the move;
7. run the complete Node Core test set;
8. compare generated manifest and readiness behavior against baseline;
9. only then reorganize the flat implementation into deeper packages.

## Decision

**Executable migration gate: CLOSED.**

The implementation itself is healthy enough to preserve, but its path dependencies must be repaired first.