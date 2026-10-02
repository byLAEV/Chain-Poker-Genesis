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

The first implementation synchronizes one registered object at a time. It does not yet provide durable queues, conflict resolution, retry/backoff, distributed replication, or peer-to-peer propagation.

These are subsequent Full Node Core requirements.
