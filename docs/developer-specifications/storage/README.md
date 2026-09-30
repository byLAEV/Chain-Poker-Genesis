# Storage Infrastructure of the Red de Nodos by LAEV

**Document:** Technical architecture and development specification  
**Version:** 1.1  
**Status:** Development baseline  
**Scope:** storage, classification, integrity, persistence, synchronization, recovery, and Kubo/IPFS integration  
**Conceptual owner:** Red de Nodos by LAEV  
**Higher-level dependencies:** No specific application or protocol

## Purpose

The storage infrastructure is an independent cross-cutting layer for modules, applications, engines, and protocols installed later on the Red de Nodos by LAEV. It does not depend on Chain Poker Genesis.

## Architecture

```text
Application / Engine
        │
        ▼
   Storage API
        │
        ▼
 Storage Manager
   ┌────┴────┐
   ▼         ▼
Policy     Metadata
Engine
   │
   ├── Local Storage
   ├── Synchronization
   ├── Recovery
   └── Distributed Adapter
             │
             ▼
        Kubo Adapter
             │
             ▼
            Kubo
             │
             ▼
            IPFS
```

## Main structure

```text
NODE/
├── storage/
├── services/
├── applications/
├── config/
├── runtime/
└── logs/
```

```text
storage/
├── local/
├── synchronization/
├── distributed/
├── metadata/
└── recovery/
```

```text
storage/local/
├── system/
├── shared/
├── modules/
├── temporary/
├── public/
├── private/
├── restricted/
├── personal/
└── backup/
```

```text
storage/synchronization/
├── outgoing/
├── incoming/
├── pending/
├── processing/
├── published/
├── failed/
├── retry/
├── quarantine/
└── manifests/
```

## Mandatory principles

1. **Separation of responsibilities:** Storage API, Storage Manager, Policy Engine, Local Storage, Synchronization, Metadata, Kubo Adapter, and Kubo/IPFS are distinct components.
2. **Independent local storage:** valid local state must remain available even when Kubo, IPFS, or a synchronization queue is unavailable.
3. **Storage does not equal synchronization:** distribution must result from an explicit policy decision.
4. **Location-independent integrity:** an object must be verifiable locally, in Kubo/IPFS, or during recovery.
5. **Module isolation:** a module must not write directly into another module's private storage.
6. **Kubo encapsulation:** never write directly into Kubo's internal repository; use its API/RPC through an adapter.
7. **Storage is not consensus:** storage, identity, synchronization, and consensus remain separate layers.

## Storage classes

- `TEMPORARY`
- `LOCAL_PUBLIC`
- `LOCAL_PRIVATE`
- `LOCAL_RESTRICTED`
- `LOCAL_PERSONAL`

`LOCAL_PUBLIC` does not imply automatic publication to IPFS. `LOCAL_RESTRICTED` must have synchronization disabled by default and additional controls.

## API and components

Every higher-level module uses a unified API, conceptually:

```text
StorageManager.put(object, policy)
```

The Storage Manager coordinates at minimum:

```text
CREATE READ UPDATE DELETE
CLASSIFY STORE RETRIEVE VERIFY
PREPARE_SYNC PUBLISH RECEIVE
QUARANTINE RESTORE BACKUP
```

The Policy Engine must be able to express at minimum:

```text
WHERE
WHO
WHEN
HOW LONG
ENCRYPTED
SYNC
PIN
REPLICATE
DELETE
```

## Object model

```text
Object
├── object_id
├── module_id
├── version
├── local_location
├── content_hash
├── cid
├── storage_class
├── visibility
├── encryption
├── persistence
├── sync_policy
├── retention_policy
├── replication_policy
├── object_state
├── sync_state
└── distributed_state
```

The identifiers `object_id`, `operation_id`, `version`, `content_hash`, and `CID` have distinct purposes. UUIDv4 is not deterministic. Two logical objects may legitimately share the same CID; accidental logical duplication must be avoided without preventing legitimate content reuse.

## Manifest and consistency

The manifest is the durable record relating an object to local storage, integrity, synchronization, distribution, and version. Operational directories (`pending`, `processing`, `published`, `failed`, `retry`, `quarantine`, etc.) are not, by themselves, the source of truth.

Consistency across the filesystem, Metadata Store, Kubo, and IPFS must be handled through durable operations, states, recovery, reconciliation, retries, and post-operation verification. A single transaction spanning all these systems must not be assumed.

## States

At minimum, separate:

```text
OBJECT_STATE
SYNC_STATE
DISTRIBUTED_STATE
```

Minimum lifecycle:

```text
CREATED → CLASSIFIED → STORED_LOCAL
                         │
                         ├── NO_SYNC
                         │
                         └── SYNC_PENDING → SYNC_PROCESSING → DISTRIBUTED
                                                   │
                                                   └→ RETRY_WAIT

INVALID → QUARANTINED
```

## Synchronization and failures

Queues must be durable and record `operation_id`, `attempt`, `next_retry_at`, `last_error`, `backoff`, `created_at`, and `updated_at`. Use exponential backoff, jitter, error classification, attempt limits, backpressure, and a circuit breaker.

A saturated queue must not necessarily block local storage.

## Integrity, encryption, and network

The following distinctions must remain explicit:

```text
CID ≠ Encryption Key
CID ≠ Permission
CID ≠ Identity
CID ≠ Authorization
IPFS ≠ Encryption
PIN ≠ Consensus
Replication ≠ Backup
Sync ≠ Replication
```

`IPFS_PUBLIC_NETWORK` and `IPFS_PRIVATE_NETWORK` are distinct properties from `CONTENT_ENCRYPTION` and `ACCESS_POLICY`. Sensitive data must be encrypted before distribution when required by policy.

## Persistence and distribution

Distinguish:

```text
STORED
PINNED
PROVIDED / ANNOUNCED
REPLICATED
```

Replication policies may be `LOCAL_ONLY`, `MULTI_NODE`, or `EXTERNAL_PINNING`.

## Kubo

Kubo is integrated as a specialized service:

```text
Storage API
 → Storage Manager
 → Distributed Adapter
 → Kubo Adapter
 → Kubo API/RPC
 → Kubo Repository
 → IPFS
```

Kubo's internal repository belongs to Kubo and must not be used as the application's database. The infrastructure maintains its own metadata, manifests, policies, and states.

## Recovery and graceful degradation

After a restart or failure, state must be reconstructed using metadata, operation records, filesystem inspection, and Kubo/IPFS verification.

Example:

```text
Kubo OFFLINE
    ↓
Local storage continues
    ↓
Sync queue accumulates
    ↓
Retry policy
    ↓
Kubo returns
    ↓
Synchronization resumes
```

Operations must be reconcilable to resolve partial failures such as a completed publication without local confirmation or a failed manifest update after a successful write.

## Backup and recovery

Backup is independent from synchronization, replication, pinning, and IPFS publication:

```text
BACKUP ≠ REPLICATION
BACKUP ≠ SYNC
BACKUP ≠ PINNING
```

## Concurrency, idempotency, and versioning

The implementation must define locking or optimistic concurrency, version checks, and operation ordering. Silent overwrites are not permitted.

Operations should be idempotent whenever possible. A logical object may maintain multiple versions, and each version retains its `content_hash`, CID, metadata, creation time, and operation history.

## Security

Explicitly separate:

```text
IDENTITY
AUTHENTICATION
AUTHORIZATION
ENCRYPTION
INTEGRITY
STORAGE POLICY
```

Automatic publication of secrets or cryptographic material is not permitted.

## Observability

The system must make it possible to determine which object exists, where it is stored, which version it represents, its hash/CID, whether it was synchronized/published/pinned/replicated, when the last operation occurred, and why an attempt failed.

Logs are operational evidence but do not replace the Metadata Store or durable records.

## Minimum acceptance criteria

```text
[ ] Storage API
[ ] Storage Manager
[ ] Policy Engine
[ ] Isolated Local Storage
[ ] Durable Metadata
[ ] object_id
[ ] Versioning
[ ] content_hash
[ ] Manifest
[ ] State Machine
[ ] Separate object/sync/distributed states
[ ] Synchronization queue
[ ] Retry + backoff + jitter
[ ] Saturation control
[ ] Recovery
[ ] Quarantine
[ ] Kubo Adapter
[ ] No direct writes to Kubo Repository
[ ] Stored/Pinned/Provided/Replicated distinction
[ ] Encryption separated from IPFS network scope
[ ] CID separated from identity
[ ] Module isolation
[ ] Operation traceability
[ ] Controlled degradation
```

## Document status

This specification constitutes the **development baseline** for the Storage Infrastructure of the Red de Nodos by LAEV and must evolve through documented versions before architectural changes are introduced.
