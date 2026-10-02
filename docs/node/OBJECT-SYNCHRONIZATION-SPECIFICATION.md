# Node Core Object Synchronization Specification

**Project:** Chain Poker Genesis by LAEV  
**Layer:** Full Node Core  
**Status:** Initial implementation baseline

## Purpose

This specification defines object-level synchronization between Local Node Storage and the decentralized Kubo/IPFS representation.

The implementation MUST reuse the existing Object Registry and Storage Locator model. It MUST NOT introduce an independent object identity model.

## Canonical object identity

Each synchronized object is identified by:

- `object_id`
- `content_hash`
- `storage_version`
- `relative_path`
- `location_state`
- `synchronization_state`
- decentralized `CID` obtained from Kubo after successful storage

The registry remains authoritative for local identity and canonical path. The Kubo CID is distributed-location evidence, not a replacement for `object_id`.

## Synchronization sequence

```
OBJECT REGISTRY
      ↓
LOCAL PATH RESOLUTION
      ↓
LOCAL CONTENT HASH VERIFICATION
      ↓
KUBO MFS WRITE
      ↓
KUBO READ-BACK
      ↓
REMOTE CONTENT HASH VERIFICATION
      ↓
KUBO MFS STAT
      ↓
CID EVIDENCE
      ↓
LOCAL_AND_DISTRIBUTED / SYNCHRONIZED
```

## Safety boundary

The implementation uses Kubo's API/RPC and MFS interface. It does not write directly into Kubo's internal repository.

Kubo installation, peer networking, replication policy, and CPG protocol association remain outside this component.

## Current limitation

The synchronization layer now includes a durable local queue for synchronization intent. Queue entries persist the canonical object identifier, content hash, storage version, and lifecycle status. A PROCESSING entry is recovered to PENDING when a new queue instance is created, allowing a restarted Node Core process to resume unfinished synchronization. Completion is persisted only after successful Local ↔ Kubo synchronization and verification.

This does not implement conflict resolution policies that choose a winner, distributed replication, or peer-to-peer propagation. Retry/backoff/circuit-breaker reliability is now implemented as a separate policy wrapper around queued synchronization.


## Divergence and conflict policy

Before writing an object to Kubo, the synchronizer MUST inspect the existing distributed representation.

- If no distributed representation exists, the object MAY be written and verified.
- If the distributed representation exists and its content hash matches the local canonical hash, synchronization MAY complete without rewriting the object.
- If the distributed representation exists and its content hash differs, the synchronizer MUST NOT overwrite it automatically.
- A divergent representation MUST be recorded in the Object Registry with `location_state=CONFLICT` and `synchronization_state=CONFLICT`, retaining the observed distributed CID as evidence.
- Conflict resolution is a separate operation and requires an explicit policy; synchronization itself is not allowed to silently choose a winner.


## Durable synchronization queue

The durable queue is stored under:

    node-storage/state/synchronization-queue.json

The queue lifecycle is intentionally minimal:

    PERSIST PENDING
          ↓
    PROCESSING
          ↓
    LOCAL ↔ KUBO VERIFICATION
          ↓
    COMPLETED

If the process stops after PROCESSING is persisted but before completion is persisted, the next queue instance MUST convert the unfinished entry back to PENDING. The synchronizer then resumes the object using the canonical Object Registry state.

The queue MUST NOT silently replace canonical content, resolve distributed conflicts, or introduce retry/backoff policy. Those behaviors belong to later Full Node Core layers.

CI verification covers:

- durable queue persistence;
- simulated process restart;
- recovery of PROCESSING to PENDING;
- resumption against real Kubo v0.43.1;
- Local ↔ Kubo content verification;
- persistent COMPLETED queue state;
- persistent SYNCHRONIZED Object Registry state.


## Synchronization reliability

The Node Core reliability wrapper provides:

- bounded retries;
- exponential backoff;
- failure-threshold circuit opening;
- recovery-time half-open probing;
- successful-probe reset to CLOSED;
- durable queue return to PENDING after an exhausted synchronization attempt.

The reliability policy is intentionally separate from the durable synchronization queue. Queue persistence is the durable source of unfinished work; the retry/circuit-breaker state is reconstructed by the process when needed.

CI verification covers transient retry with backoff, failure-threshold circuit opening, recovery timeout, half-open probing, and successful reset.

This layer does not add peer networking, distributed replication, automatic conflict resolution, or CPG behavior.
