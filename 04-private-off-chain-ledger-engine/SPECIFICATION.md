# 04 — Private Off-Chain Ledger Engine — Functional Specification

**Chain Poker Genesis by LAEV**  
**Version:** 1.0  
**Status:** Repository engineering specification derived from the historical v1.0 source  
**Author:** Lerry Alexander Elizondo Villalobos (LAEV)

## 1. Scope

The Private Off-Chain Ledger Engine is the cross-cutting persistence and historical-evidence subsystem of Chain Poker Genesis.

It receives protocol events, validates and normalizes them, assigns the protocol timestamp, serializes a canonical event representation, computes an event hash, persists the private record, assigns the event to a Merkle batch, and maintains the metadata required for external Bitcoin certification.

This specification defines the functional boundary. It does not silently choose cryptographic algorithms, database technology, Bitcoin transaction construction, key custody, or deployment architecture where those decisions are not yet fixed by the protocol.

## 2. Functional Contract

For each accepted event, the engine shall provide:

1. A unique event identity.
2. A protocol timestamp.
3. An identifiable source.
4. An event type and version.
5. A canonical record representation.
6. An individual cryptographic commitment.
7. Private persistent storage.
8. Deterministic membership in a Merkle batch.
9. Sufficient metadata for later verification.
10. An anchor state independent from event persistence.

The ledger shall preserve the event record even when its Bitcoin anchor is pending or unavailable, subject to the implementation's storage and recovery policies.

## 3. Event Lifecycle

```text
RECEIVED → VALIDATED → NORMALIZED → TIMESTAMPED → CANONICALIZED
    → HASHED → PERSISTED → BATCHED → MERKLE_COMMITTED
    → ANCHOR_PENDING → ANCHORED
```

Failure states must not silently become successful states.

## 4. Canonical Event Model

The repository baseline is:

```json
{
  "event_id": "EVENT_ID",
  "timestamp": "UTC_TIMESTAMP",
  "node_id": "NODE_ID",
  "session_id": "SESSION_ID",
  "game_id": "GAME_ID",
  "hand_id": "HAND_ID",
  "engine_id": "ENGINE_ID",
  "event_type": "EVENT_TYPE",
  "event_version": "1.0",
  "payload": {},
  "previous_hash": "PREVIOUS_HASH",
  "event_hash": "EVENT_HASH",
  "merkle_batch_id": "BATCH_ID",
  "anchor_status": "PENDING",
  "bitcoin_anchor_id": null
}
```

The final implementation shall explicitly classify each field as required, conditional, or optional.

## 5. Canonical Serialization

The event hash shall be calculated from a deterministic canonical representation.

Before production implementation, the protocol must formally fix:

- serialization format;
- character encoding;
- field ordering;
- number representation;
- boolean representation;
- null handling;
- whitespace and escaping;
- optional-field treatment;
- unknown-field treatment;
- schema/version identifier;
- hash input boundary.

No implementation-specific serializer shall become an implicit protocol rule.

## 6. Cryptographic Hashing

Each event shall have an individual event hash.

```text
Canonical Event Representation
          ↓
   Approved Hash Function
          ↓
       Event Hash
```

The exact algorithm and output representation remain a protocol decision unless already established by a dedicated cryptographic specification.

## 7. Previous Hash

`previous_hash` is supported as a historical architectural concept, but its production scope remains undefined.

The protocol must establish whether it applies per node, session, event stream, batch, or globally, and must define behavior for first records, concurrent streams, missing records, recovery, forks, and migration.

A previous-hash chain is complementary to, not a replacement for, Merkle consolidation.

## 8. Ordering and Time

The ledger shall preserve explicit event sequencing.

A timestamp is temporal metadata; it is not by itself a sufficient total-order mechanism when concurrent events are possible.

The final implementation must define, where required:

- timestamp precision;
- clock source;
- synchronization mechanism;
- sequence identifier;
- tie-breaking rule;
- clock-drift behavior;
- late-event behavior.

## 9. Private Persistence

The ledger is the detailed operational record and must support:

- append-oriented event storage;
- durable retrieval;
- integrity verification;
- batch reconstruction;
- historical querying;
- controlled access;
- backup and recovery.

The specific database or file format remains outside this specification unless separately approved.

## 10. Merkle Batch Contract

A Merkle batch is a deterministic ordered collection of event hashes.

The implementation must establish:

- batch identifier;
- membership rule;
- event ordering;
- leaf representation;
- parent-node construction;
- odd-leaf handling;
- domain separation, if used;
- root encoding;
- batch finalization state.

Candidate policies inherited from the historical source include completed poker hand, completed game/table, operational cycle, event-count threshold, time interval, and explicit certification request.

## 11. Bitcoin Anchor Contract

The ledger does not publish private event records to Bitcoin.

The anchor layer receives the finalized Merkle commitment and returns certification metadata.

The implementation must separately define:

- Bitcoin transaction construction;
- commitment placement;
- fee policy;
- broadcaster;
- confirmation policy;
- rebroadcast behavior;
- failure handling;
- anchor finality;
- transaction identifier format;
- proof retrieval.

The ledger retains the resulting anchor reference without making operational persistence dependent on immediate blockchain availability.

## 12. Verification Contract

```text
Private Records
      ↓
Canonical Serialization
      ↓
Event Hashes
      ↓
Deterministic Batch Ordering
      ↓
Merkle Tree
      ↓
Merkle Root
      ↓
Anchor Comparison
      ↓
Verification Result
```

A matching root establishes correspondence with the anchored commitment under the specified reconstruction rules. It does not by itself prove facts outside the committed data or prove that every real-world event was recorded.

## 13. Interfaces

### Inputs

- internal protocol events;
- engine events;
- Player Node events;
- administrative events;
- cryptographic events;
- communication events;
- game events;
- security events;
- synchronization events;
- system events.

### Outputs

- normalized event records;
- event hashes;
- private ledger entries;
- Merkle batches and Roots;
- anchor state;
- Bitcoin anchor metadata;
- verification data;
- audit history.

## 14. Error and Recovery Boundary

The implementation shall distinguish at least:

- rejected event;
- validation failure;
- serialization failure;
- hash failure;
- persistence failure;
- batch failure;
- Merkle construction failure;
- anchor unavailable;
- anchor rejected;
- verification mismatch.

Anchoring failure must not be represented as event-storage failure when the private record has already been durably persisted.

Recovery, retry, idempotency, and crash-recovery behavior require dedicated implementation rules.

## 15. Non-Functional Requirements

The implementation should provide:

- durable persistence;
- deterministic serialization;
- cryptographic integrity;
- low write latency;
- complete traceability;
- audit compatibility;
- scalable storage;
- controlled access;
- recovery mechanisms;
- resistance to unauthorized modification;
- operational independence from Bitcoin availability.

Quantitative performance targets remain TBD.

## 16. Engine Boundaries

The Ledger Engine records evidence; it does not own installation, cryptographic identity/key custody, network communication semantics, graphical presentation, node administration policy, poker rules, settlement policy, or consensus governance.

Other engines publish relevant events to the ledger.

## 17. Acceptance Criteria

Functional conformance should demonstrate:

1. deterministic event validation;
2. canonical event representation;
3. reproducible event hashes;
4. durable private persistence;
5. deterministic batch membership;
6. reproducible Merkle Roots;
7. explicit anchor-state management;
8. successful verification of an anchored batch;
9. detection of modified committed data;
10. documented recovery after interrupted processing.

Cryptographic algorithms, exact schema, and Bitcoin anchoring construction require separate approval before production conformance.

## 18. Open Engineering Decisions

Unless established elsewhere, these remain open:

- hash algorithm;
- canonical serialization standard;
- event sequence mechanism;
- previous-hash scope;
- Merkle construction rules;
- Bitcoin commitment format;
- Bitcoin confirmation threshold;
- storage technology;
- encryption-at-rest design;
- access-control model;
- replication topology;
- backup format;
- recovery objectives;
- performance targets.

These are not silently inferred from the historical PDF.

---

**Historical source:** `04. Private Off-Chain Ledger Engine_- Chain Poker Genesis by LAEV.pdf`
