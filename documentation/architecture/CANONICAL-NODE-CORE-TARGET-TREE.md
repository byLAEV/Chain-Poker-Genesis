# Canonical Node Core Target Tree

**Status:** Target architecture for repository migration
**Scope:** Repository source structure only; runtime `node-storage/` is separate.

## 1. Canonical source tree

```text
node-core/
├── README.md
├── bootstrap/
│   ├── bootstrap.py
│   └── contracts/
├── identity/
│   ├── README.md
│   └── cryptographic-connection/
├── cryptography/
│   └── core/
├── configuration/
├── storage/
│   ├── README.md
│   ├── manager/
│   ├── locator/
│   ├── providers/
│   ├── object-registry/
│   └── coherence/
├── manifests/
├── runtime/
│   ├── lifecycle/
│   └── readiness/
├── state/
├── recovery/
├── networking/
│   ├── substrate/
│   └── conflict-boundary/
├── synchronization/
├── versioning/
└── release/
```

## 2. Supporting repository layers

```text
implementation/
├── reference/
├── protocol/
└── schemas/

tests/
├── node-core/
├── protocol/
└── integration/

tools/
├── validation/
├── generation/
└── release/

documentation/
├── architecture/
├── node-core/
├── protocol/
├── engines/
├── implementation-review/
└── historical/
```

## 3. Protocol boundary

The generic Node Core must not absorb CPG-specific protocol semantics.

```text
node-core/
    ↓ provides substrate

protocol-core/
    ↓ provides CPG semantics

protocol-engines/
    ↓ provide protocol functions

application / table / viewer layers
```

At minimum, the following remain outside generic Node Core:

- CPG Dedicated Ledger semantics
- poker rules
- table semantics
- rake policy
- monetary settlement semantics
- CPG-specific cryptographic profiles
- CPG protocol consensus/conflict semantics
- protocol membership

## 4. Cryptographic boundary

```text
node-core/cryptography/core/
        ↓
protocol-core/cryptography/
        ↓
node-core/identity/cryptographic-connection/
```

The physical package dependency must be validated before migration. The diagram expresses architecture, not Python import paths.

## 5. Storage boundary

Repository source:

```text
node-core/storage/
```

Runtime storage created by the node:

```text
node-storage/
├── identity/
├── cryptography/
├── configuration/
├── state/
├── records/
├── recovery/
└── protocol/
```

The two names must remain distinct. `node-core/storage/` is source code/specification; `node-storage/` is node runtime state.

## 6. Documentation relationship

Canonical technical documentation should map to the implementation boundary without becoming runtime code:

```text
documentation/node-core/
├── bootstrap/
├── identity/
├── cryptography/
├── storage/
├── runtime/
├── recovery/
├── networking/
├── synchronization/
└── release/
```

Existing `docs/node/` content should be migrated into these locations only after duplicate/specification status is reconciled.

## 7. Test and validation relationship

Executable tests should eventually be separated from implementation source:

```text
tests/node-core/
├── bootstrap/
├── identity/
├── storage/
├── runtime/
├── recovery/
├── networking/
└── synchronization/
```

Verification utilities that are not tests should move to `tools/validation/`.

## 8. First migration batch

The first physical migration batch should be intentionally small:

1. Create `documentation/node-core/` and place canonical Node Core documentation there after path reconciliation.
2. Move the reference Node installation implementation into `implementation/reference/node-core/` only after import/CI path analysis.
3. Move its tests into `tests/node-core/` only after the reference implementation path is stable.
4. Move cryptographic documentation according to the established Node Core vs Protocol Core boundary.

Do not move the numbered protocol-engine directories in the same commit.

## 9. Migration invariant

After each migration batch:

```text
old references = repaired
CI = passing
tests = passing
canonical links = valid
no source duplicated accidentally
historical provenance = preserved
```

## 10. Important limitation

This target tree is an implementation-oriented architecture, not a claim that every listed directory is already implemented.

Empty directories should not be added merely to make the tree look complete. A directory should be created when a canonical artifact is ready to inhabit that boundary.

## 11. Exit condition for structural migration

Physical migration is considered complete when:

- every current Node Core artifact has a target path or explicit keep/historical classification;
- no canonical Node Core specification remains ambiguously located;
- reference implementation and tests have a clear source/test boundary;
- Node Core and CPG Protocol Core boundaries are reflected in the tree;
- root-level engine PDFs no longer determine software organization;
- CI and path validation pass after migration.