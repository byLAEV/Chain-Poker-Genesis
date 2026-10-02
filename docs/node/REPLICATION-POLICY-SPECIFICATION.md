# Node Core Replication Policy Specification

**Project:** Chain Poker Genesis by LAEV  
**Layer:** Full Node Core  
**Status:** Minimal implementation baseline  
**Scope:** Policy decision only; replication execution remains separate

## 1. Reconciled source

The Storage Infrastructure Specification Manual explicitly requires the infrastructure to distinguish:

- `STORED`
- `PINNED`
- `PROVIDED / ANNOUNCED`
- `REPLICATED`

It defines the replication policy values:

- `LOCAL_ONLY`
- `MULTI_NODE`
- `EXTERNAL_PINNING`

It also explicitly states that backup, synchronization, pinning, and replication are different concepts.

The implementation therefore models replication intent without treating Kubo, IPFS pinning, backup, or synchronization as automatic replication.

## 2. Minimal policy model

| Policy | Minimum copies | External service | Local copy required |
|---|---:|---|---|
| LOCAL_ONLY | 1 | No | Yes |
| MULTI_NODE | 2 | No | Yes |
| EXTERNAL_PINNING | 2 | Yes | Yes |

`minimum_copies` is a policy requirement, not evidence that those copies already exist.

## 3. Separation of concerns

The replication policy engine only answers:

> What replication treatment is required?

It does not execute:

- peer discovery;
- remote writes;
- pinning operations;
- provider announcements;
- backup;
- synchronization;
- conflict resolution;
- network transport.

Those are separate infrastructure layers.

## 4. Safety rules

An unknown replication policy is rejected.

`BACKUP` is not accepted as a replication policy.

`EXTERNAL_PINNING` is represented distinctly from `MULTI_NODE`; external pinning is not silently equated with ordinary node replication.

The engine does not modify objects or storage state.

## 5. Verification gate

FN-023 remains `IN_PROGRESS` until CI verifies:

1. `LOCAL_ONLY`;
2. `MULTI_NODE`;
3. `EXTERNAL_PINNING`;
4. invalid-policy rejection;
5. absence of replication side effects from policy evaluation.

Only then may FN-023 become `VERIFIED`.

## 6. Explicit boundary

CPG protocol behavior remains outside this phase.

Replication policy is a Node Core storage-infrastructure concern and does not activate or install CPG.
