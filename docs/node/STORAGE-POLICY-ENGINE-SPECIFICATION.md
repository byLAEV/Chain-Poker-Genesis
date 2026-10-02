# Node Core Storage Policy Engine Specification

**Project:** Chain Poker Genesis by LAEV  
**Layer:** Full Node Core  
**Status:** Minimal implementation baseline  
**Scope:** Policy decision only; no replication, peer networking, or CPG behavior

## 1. Reconciled architectural source

The Storage Infrastructure Specification Manual establishes a dedicated **Storage Policy Engine** between the Storage Manager and the storage/synchronization layers.

Its purpose is to make an explicit policy decision instead of inferring behavior from physical filesystem availability.

The specification also states that:

- storage is independent from synchronization;
- local public data is not automatically published to IPFS;
- local private data is not automatically published;
- restricted data has synchronization disabled by default;
- personal data is not implicitly published or synchronized;
- placement decisions occur only after the canonical storage structure and bootstrap synchronization boundary;
- replication, retention, encryption, pinning, deletion, and synchronization are distinct policy dimensions.

The implementation therefore does not make Kubo, IPFS, replication, or CPG the policy authority.

## 2. Minimal decision model

The current Node Core policy engine resolves:

    storage_class
        ↓
    policy decision
        ├── sync
        ├── placement
        ├── visibility
        ├── persistence
        ├── encryption
        ├── pin
        ├── replicate
        ├── delete
        └── retention

Supported canonical classes:

- `TEMPORARY`
- `LOCAL_PUBLIC`
- `LOCAL_PRIVATE`
- `LOCAL_RESTRICTED`
- `LOCAL_PERSONAL`

These classes are taken directly from the Storage Infrastructure Specification Manual.

## 3. Conservative defaults

The minimum defaults are intentionally conservative:

| Class | Sync | Placement | Visibility | Encryption |
|---|---|---|---|---|
| TEMPORARY | DISABLED | LOCAL_ONLY | LOCAL | POLICY_DEFINED |
| LOCAL_PUBLIC | DISABLED | LOCAL_ONLY | PUBLIC_LOCAL | POLICY_DEFINED |
| LOCAL_PRIVATE | DISABLED | LOCAL_ONLY | PRIVATE | REQUIRED |
| LOCAL_RESTRICTED | DISABLED | LOCAL_ONLY | RESTRICTED | REQUIRED |
| LOCAL_PERSONAL | DISABLED | LOCAL_ONLY | PERSONAL | POLICY_DEFINED |

No class is implicitly published to IPFS.

No class is implicitly replicated to additional nodes.

## 4. Explicit overrides

The engine accepts explicit policy overrides only for fields already defined by the baseline policy model.

An override that attempts to introduce an undefined policy field is rejected.

A policy that disables synchronization cannot simultaneously claim non-local placement.

This keeps the policy engine from silently inventing distribution behavior.

## 5. Scope boundary

The engine **decides** policy; it does not execute policy actions.

It does not currently implement:

- replication;
- peer-to-peer networking;
- IPFS pin orchestration;
- encryption;
- deletion;
- retention scheduling;
- conflict resolution;
- remote policy propagation;
- CPG installation or protocol behavior.

Those remain separate Full Node Core requirements and must be implemented only after their source requirements are reconciled.

## 6. Verification gate

FN-022 is not considered VERIFIED merely because the engine exists.

The completion gate requires:

1. policy-class tests;
2. conservative default tests;
3. explicit override validation;
4. rejection of unknown classes/fields;
5. CI execution through the Node Core validation workflow.

Only after that evidence succeeds may FN-022 transition from `IN_PROGRESS` to `VERIFIED`.
