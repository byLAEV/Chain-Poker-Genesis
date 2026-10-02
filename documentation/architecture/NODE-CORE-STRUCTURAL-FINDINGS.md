# Node Core Structural Findings

## Audit status

This audit confirms that the repository already contains a substantial Node-oriented architecture. The Node Core should therefore not be created as an empty conceptual directory by moving documents arbitrarily.

## Confirmed existing Node-oriented material

### Cryptographic layer

The current `engines/` tree contains:

- `cryptographic-core-engine`
- `cryptographic-connection-engine`
- `cryptographic-engine`

These are architectural candidates for the Node Core cryptographic layer. Their specifications must be reconciled before any move.

### Node storage and deterministic manifests

The repository already contains:

- `deterministic-manifest-based-node-and-protocol-storage-architecture/`
- `docs/node/`
- storage manifest schemas;
- storage object schemas;
- storage object registry schemas;
- storage provider schemas;
- node test-vector space.

This means storage is not merely a future concept. It already has specification and schema artifacts and should be treated as a first-class Node Core workstream.

### Node architecture documentation

`docs/architecture/NODE-CORE-AND-CPG-PROTOCOL-CORE.md` exists and should be treated as a primary architectural reference during reconciliation.

The architecture directory also contains integration audits, integration matrices, system component matrices, and installation/bootstrap specifications.

### Reference implementation

`reference-implementation/` already contains executable Python material, including:

- execution verification;
- node installation/bootstrap;
- node runtime;
- object registry;
- health/readiness;
- Node Core audit tooling.

This is significant: the repository is already beyond a documentation-only state.

### Protocol canonicalization

`docs/protocol/` already contains:

- canonical schemas;
- canonicalization;
- execution model;
- test-vector areas.

Therefore the proposed target tree must preserve these assets rather than duplicate them.

## Structural conclusion

The previous proposal to create a new empty `node-core/` tree is too early.

The correct migration is:

CURRENT NODE ARTIFACTS
→ RECONCILIATION
→ CANONICAL NODE CORE BOUNDARY
→ TARGET NODE CORE TREE
→ CONTROLLED MOVE/RENAME

The existing `docs/node/`, cryptographic engines, deterministic storage architecture, reference node installation/runtime and Node Core architecture documentation are evidence that the Node Core is already partially materialized across the repository.

## Immediate next action

Before moving anything, reconcile these specific areas:

1. `docs/architecture/NODE-CORE-AND-CPG-PROTOCOL-CORE.md`
2. `docs/node/`
3. `docs/developer-specifications/node-infrastructure/`
4. `docs/developer-specifications/storage/`
5. `deterministic-manifest-based-node-and-protocol-storage-architecture/`
6. `engines/cryptographic-core-engine/`
7. `engines/cryptographic-connection-engine/`
8. `engines/cryptographic-engine/`
9. `reference-implementation/node-installation/`
10. `reference-implementation/execution/`

Only after this reconciliation should the final `node-core/` directory be created or existing material moved.

## Key architectural rule

A directory named `node-core` should represent a canonical implementation boundary, not merely a documentation category. Its contents must correspond to components required for a protocol node to exist, initialize, maintain identity, persist state, communicate, synchronize, recover and execute protocol engines.

