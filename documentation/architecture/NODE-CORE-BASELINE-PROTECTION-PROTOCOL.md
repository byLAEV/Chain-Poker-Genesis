# Node Core Baseline Protection Protocol

**Purpose:** Protect the existing Node Core reference implementation while repository restructuring is performed.

## Non-negotiable rule

No physical movement of executable Node Core code is permitted until path, import, schema, test, CI, and documentation dependencies have been explicitly mapped.

## Protected baseline

The current reference implementation is treated as the behavioral baseline.

Structural refactoring must preserve:

- runtime behavior;
- installation behavior;
- readiness states;
- storage layout;
- manifest generation;
- object registry behavior;
- recovery behavior;
- synchronization state behavior;
- test-vector interpretation.

## Migration method

BASELINE → DEPENDENCY INVENTORY → TARGET PATH → PATH/IMPORT REWRITE PLAN → MIGRATION → TESTS → REFERENCE IMPLEMENTATION COMPARISON → NEXT MIGRATION

## Schema protection

No schema is deleted or renamed merely because another schema appears newer.

For each overlapping schema:

1. identify consumers;
2. identify tests;
3. identify generated artifacts;
4. identify version relationship;
5. define canonical `$id`;
6. preserve superseded generations explicitly;
7. migrate consumers;
8. validate;
9. only then consider archival.

## Rollback principle

Every migration commit must be independently revertible.

No commit should simultaneously change runtime semantics, rename multiple architectural boundaries, change schema semantics, relocate tests, and reorganize unrelated protocol engines.

## Current gate

The repository is currently **STRUCTURAL-AUDIT SAFE**.

The next executable migration gate is **NOT YET OPEN** because schema generations and reference-implementation path dependencies remain to be reconciled.

## Decision

Continue auditing the existing implementation before moving `reference-implementation/node-installation/`.

Preservation of working behavior has priority over achieving the target directory tree quickly.