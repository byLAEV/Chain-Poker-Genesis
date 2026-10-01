# Node Core and Chain Poker Genesis Protocol Core

**Status:** Architectural clarification — non-normative  
**Scope:** Node substrate, storage, synchronization, protocol association, and record distribution  
**Project:** Chain Poker Genesis by LAEV

## 1. Purpose

This document establishes a boundary between the **Node Core** and the **Chain Poker Genesis Protocol Core**.

The Node Core is the autonomous substrate that operates a node independently of Chain Poker Genesis. It provides the node's identity, cryptographic capabilities, local state, storage, decentralized storage connectivity, synchronization, and operational integrity.

The Chain Poker Genesis Protocol Core is the protocol-specific layer that associates an operational node with Chain Poker Genesis and defines protocol execution, protocol state, protocol records, and the **Dedicated Ledger**.

The Dedicated Ledger is therefore a protocol resource. It is not a generic component of the Node Core.

## 2. Architectural Model

The provisional dependency model is:

```text
NODE DOMAIN
|
+-- Node Core
|   |
|   +-- Node Identity
|   +-- Node Cryptographic Core
|   +-- Node State / Configuration
|   +-- Local Storage
|   +-- Decentralized Node Storage (IPFS)
|   +-- Storage Synchronization
|   +-- Node Recovery / Integrity
|   +-- Node Networking Substrate
|
+-- Protocol Association Boundary
    |
    +-- Chain Poker Genesis Protocol Core
        |
        +-- Protocol Identity / Membership
        +-- Protocol State
        +-- Tables / Hands / Events
        +-- Dedicated Ledger
        +-- Protocol Synchronization
        +-- Consensus / Conflict Rules
        +-- Settlement Coordination
        +-- Protocol-specific Cryptographic Policies
```

The important boundary is:

**Node Core exists first. CPG Protocol Core is associated with it later.**

## 3. Node Core

The Node Core must be capable of operating as a coherent node substrate without requiring the Chain Poker Genesis Dedicated Ledger.

It owns or coordinates:

- node identity;
- node cryptographic core;
- node keys and key references;
- node configuration;
- node operational state;
- local persistent storage;
- decentralized node storage;
- storage synchronization;
- integrity verification;
- backup and recovery mechanisms;
- node-level networking;
- capability discovery;
- node lifecycle.

The Node Core does not define poker semantics and does not become a poker ledger merely because it stores data.

## 4. Two Node Storage Domains

The Node Core includes two complementary persistent storage domains.

### 4.1 Local Node Storage

Local storage is the node's directly controlled persistent storage.

It may contain:

- node configuration;
- identity material and references;
- operational state;
- cryptographic metadata;
- local indexes;
- cached protocol data;
- synchronized records;
- recovery metadata.

The exact physical implementation remains open until the storage specification defines it.

### 4.2 Decentralized Node Storage

The node also operates a decentralized storage counterpart, initially modeled around **IPFS**.

Its purpose is to provide a distributed content-addressed persistence/replication layer for data that the node is authorized to store.

The IPFS storage domain is not a replacement for local storage.

It is a second storage domain that can provide:

- decentralized replication;
- content addressing;
- recovery material;
- distributed availability;
- cross-node synchronization;
- independent verification of stored objects.

## 5. Storage Synchronization

The local and decentralized storage domains are intended to operate as synchronized representations of the node's authorized persistent data.

Conceptually:

```text
          Node Core
              |
       Storage Manager
          /       \
         /         \
 Local Storage <-> IPFS Storage
         \         /
          \       /
       Integrity / Sync
```

Synchronization must eventually define:

- object identity;
- canonical serialization;
- content addressing;
- synchronization direction;
- version/state markers;
- conflict detection;
- conflict resolution;
- integrity verification;
- missing-object recovery;
- retry behavior;
- authorization;
- failure states;
- recovery guarantees.

These rules are not yet assumed normative merely because IPFS is selected as the current architectural direction.

## 6. Node Readiness Before Protocol Distribution

A node should not be treated as a reliable protocol execution/storage location until its own storage substrate is operational.

The intended dependency is:

```text
Node Core
  ↓
Local Storage Operational
  ↓
IPFS Storage Operational
  ↓
Local/IPFS Synchronization Verified
  ↓
Node Integrity / Recovery Verified
  ↓
Node Ready
  ↓
CPG Protocol Association
  ↓
Protocol Distribution Configuration
```

This ordering is important.

The protocol should not first decide where records are distributed and then discover whether the underlying node storage works.

The node establishes a functioning and verifiable storage substrate first.

## 7. Chain Poker Genesis Protocol Core

Once a node is operational, the CPG Protocol Core can associate with that node.

The Protocol Core owns protocol-specific semantics, including:

- protocol participation;
- protocol state;
- tables;
- hands;
- protocol events;
- protocol synchronization;
- consensus rules;
- protocol conflict handling;
- settlement coordination;
- the Dedicated Ledger.

The Protocol Core may use Node Core services, but it does not redefine them.

## 8. Dedicated Ledger Boundary

The Dedicated Ledger belongs to Chain Poker Genesis.

It must not be conflated with:

- node local storage;
- the IPFS storage substrate;
- a node's generic event log;
- a node backup;
- a node database.

The same physical storage technology may eventually host multiple classes of data, but ownership and semantics remain distinct.

For example:

```text
Node Local Storage
    |
    +-- Node data
    +-- Node state
    +-- Identity / crypto metadata
    +-- Replicated protocol objects
    |
    +-- CPG Dedicated Ledger data
         [only when the node is associated with CPG]
```

The physical medium does not determine protocol ownership.

## 9. Distribution Configuration Comes Later

After the Node Core and the CPG Protocol Core are both defined, the architecture can introduce a higher-level **distribution configuration** that determines where particular protocol records are executed, persisted, replicated, or recovered.

This configuration must answer questions such as:

- Which node executes a given protocol function?
- Which node stores a given record?
- Which records require local persistence?
- Which records require IPFS replication?
- Which records require multiple independent node replicas?
- Which nodes participate in synchronization?
- Which records belong to the Dedicated Ledger?
- Which records are cached versus authoritative?
- Where is recovery performed?
- Which placement decisions are deterministic?
- Which placement decisions are configurable?

This is a later layer.

It must not be embedded prematurely into the Node Core or into individual canonical schemas.

## 10. Three Distinct Concepts

The architecture must preserve three separate concepts:

### Node Storage

Storage operated by the Node Core.

### Protocol Ledger

The CPG Dedicated Ledger defined by the Protocol Core.

### Distribution Policy

The configuration that determines how protocol data and responsibilities are distributed across operational nodes and their available storage domains.

They may interact, but they are not the same thing.

## 11. Architectural Invariant

A useful invariant for subsequent specifications is:

> **A node provides the substrate. The protocol provides the semantics. The ledger belongs to the protocol. Distribution determines how protocol responsibilities and records are placed across valid node substrates.**

## 12. Consequences for Canonical Schemas

This boundary must be respected before canonical fields are finalized.

In particular, future schema work must distinguish:

- `node_id` — identity of the operational node;
- `identity_id` — cryptographic identity, where applicable;
- `storage_id` — a storage resource, if eventually required;
- `ipfs_node_id` or equivalent — only if the decentralized storage specification establishes such an identifier;
- `protocol_id` — CPG protocol association, if required;
- `ledger_id` — identity of the CPG Dedicated Ledger, if required;
- record/event identifiers — identifiers belonging to the relevant protocol record model.

No equivalence between these identifiers should be inferred.

## 13. Open Specifications

The following remain open and should be formalized separately:

1. Node Core specification.
2. Node local storage specification.
3. Decentralized/IPFS storage specification.
4. Storage synchronization state machine.
5. Node recovery model.
6. Node readiness criteria.
7. Protocol association model.
8. CPG Protocol Core specification.
9. Dedicated Ledger ownership and interface.
10. Distribution configuration model.
11. Record placement rules.
12. Replication and recovery policy.
13. Canonical serialization for stored objects.
14. Storage-related canonical schemas.

Until these are resolved, the present document is an architectural boundary rather than a complete implementation specification.

## 14. Non-Goals

This document does not yet:

- prescribe a database engine;
- prescribe an IPFS implementation;
- define the Dedicated Ledger event schema;
- define consensus;
- define record placement algorithms;
- define replication factors;
- define node election;
- define exact cryptographic algorithms;
- define implementation-specific storage paths.

Those decisions require their respective specifications.

---

**Architectural direction:** establish the autonomous Node Core and its synchronized local/IPFS storage substrate first; establish the CPG Protocol Core and Dedicated Ledger on top of that substrate; only then define configurable distribution of protocol execution and record storage across nodes.
