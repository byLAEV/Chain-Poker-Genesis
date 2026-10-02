# First Node Core Migration Batch Plan

## Objective

Prepare the first physical migration without changing runtime behavior or mixing protocol-engine restructuring into the same change.

## Batch 1 — documentation canonicalization

### Source
`docs/node/`

### Target
`documentation/node-core/`

### Rule
Move only documents that are genuinely Node Core specifications. Architecture audits, completion records, reconciliation reports, and historical evidence remain under `documentation/architecture/` or `historical/`.

### Required checks before merge

- update internal Markdown links;
- update README indexes;
- update references from root documentation;
- search for old `docs/node/` paths;
- verify every moved document has exactly one canonical location.

## Batch 2 — reference implementation

### Source
`reference-implementation/node-installation/`

### Candidate target
`implementation/reference/node-core/`

### Important constraint

Do not move until import paths, test discovery, CI workflows, scripts and documentation references are reconciled.

The move must preserve:

- runtime behavior;
- module imports;
- test execution;
- installation commands;
- verification commands;
- schema locations.

## Batch 3 — tests and validation

After the reference implementation path is stable:

- Node Core tests → `tests/node-core/`;
- reusable verification utilities → `tools/validation/`;
- one-off audit reports → `documentation/architecture/audits/`.

## Batch 4 — cryptographic boundaries

Only after the first three batches:

- Cryptographic Core → Node Core candidate;
- Cryptographic Connection → Node Core identity candidate;
- CPG Cryptographic Engine → Protocol Core candidate.

These must not be moved together merely because their current names contain “cryptographic”.

## Explicitly excluded from Batch 1

Do not move:

- numbered protocol engines;
- Poker Rules Engine;
- Rake and Settlement Engine;
- Dedicated Ledger material;
- P2P Conflict Resolution Engine;
- Poker Table Viewer Engine;
- root-level PDFs;
- historical vision material.

Those require their own protocol/architecture reconciliation.

## Migration gate

The first physical commit should not happen until the following checks pass:

```text
TARGET PATHS DEFINED
        ↓
OLD-PATH REFERENCES IDENTIFIED
        ↓
INTERNAL LINKS REPAIRABLE
        ↓
CI / TEST PATHS IDENTIFIED
        ↓
NO DUPLICATE CANONICAL SOURCE
        ↓
MIGRATION COMMIT
        ↓
VALIDATION
```

## Current decision

The correct first physical migration candidate is documentation, not runtime code.

This minimizes implementation risk while establishing the canonical Node Core documentation boundary. The reference implementation should follow only after its path dependencies are explicitly mapped.
