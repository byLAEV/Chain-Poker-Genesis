# Node Core Storage

**Status:** IMPLEMENTED
**Version:** 1.2.0
**Scope:** Protocol-neutral persistence subsystem of Node Core.

Node Core Storage is responsible for local persistence, optional decentralized mirroring, synchronization, integrity verification, fallback, and recovery. It does not implement CPG protocol semantics.

## Implementation architecture

1. Storage Manager — public orchestration boundary.
2. Storage Policy — storage-class and distribution rules.
3. Object Registry — canonical metadata and lifecycle/location record.
4. Providers — provider abstraction and provider registry.
5. Local — authoritative local persistence.
6. Kubo-IPFS — decentralized provider adapter.
7. Synchronization — explicit synchronization state transitions.
8. Integrity — SHA-256 content verification.
9. Disaster Recovery — verified distributed-to-local restoration.
10. API — programmatic boundary delegating to Storage Manager.

The low-level storage_engine.py performs provider/storage operations. It does not maintain an independent storage lifecycle or a second registry architecture.

## Storage classes

- temporary
- public
- private
- restricted
- personal

protocol-reserved is protected from Node Core writes.

Private and restricted objects require encrypted bytes before distribution. Node Core Storage does not own or persist encryption keys.

## Operational model

### Write

API → Storage Manager → Policy → Local → optional Kubo mirror → Registry

Local persistence is completed before decentralized mirroring.

If mirroring fails, the local object remains valid and the registry records:

SYNC_PENDING / SYNC_FAILED

### Read

Registry → Kubo/IPFS when CID is available → hash verification → local fallback

A distributed response is accepted only when its SHA-256 matches the registry.

If the distributed copy is unavailable or fails verification, the local copy is used when its integrity is valid.

### Recovery

When the local copy is missing:

Registry → CID → Kubo/IPFS → SHA-256 verification → Local restore → Registry update

Recovery is never performed from an unverified distributed object.

### Synchronization

Synchronization uses explicit states including:

LOCAL_ONLY, SYNC_PENDING, SYNC_PROCESSING, SYNCHRONIZED, SYNC_FAILED, MISSING_LOCAL, MISSING_DISTRIBUTED, CONFLICT, QUARANTINED.

## Protocol isolation

Storage contains no:

- CPG ledger
- CPG consensus
- poker table state
- poker rules
- settlement
- rake
- player protocol state

Those belong to protocol layers above Node Core Storage.

## Verification

Primary integration test:

python3 "Node Core/Tests/Storage/test_storage_complete.py"

The test suite includes local CRUD, policy enforcement, path traversal protection, Kubo mirroring, Kubo-preferred reads, local fallback, disaster recovery, and synchronization state transitions.

Live Kubo verification remains dependent on an available Kubo daemon.
