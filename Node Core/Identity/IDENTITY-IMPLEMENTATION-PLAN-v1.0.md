# Node Core Identity — Implementation Plan v1.0

This document defines the execution order required to implement the Identity subsystem without prematurely coupling it to CPG protocol logic.

## 1. Implementation rule

Implementation SHALL follow:

DESIGN → SPECIFICATION → ARCHITECTURE → CONTRACTS → TEST VECTORS → REFERENCE IMPLEMENTATION → INTEGRATION → AUDIT

No production implementation should bypass unresolved cryptographic decisions.

## 2. Work packages

### WP-01 — Canonical identity model
Deliver:
- schemas;
- canonical serialization;
- validation;
- versioning;
- object identifiers.

Depends on:
- final Node ID profile.

### WP-02 — Node Life
Deliver:
- lifecycle event model;
- state machine;
- event persistence;
- lifecycle reconstruction;
- lifecycle metrics.

Depends on:
- canonical event format.

### WP-03 — Node Identity
Deliver:
- identity generation;
- identity loading;
- validation;
- Node ID derivation;
- identity status.

Depends on:
- cryptographic profile.

### WP-04 — Credential adapters
Deliver:
- generic signature verifier;
- PGP adapter;
- GPG/OpenPGP adapter;
- hardware-wallet signature adapter.

Depends on:
- supported algorithms and hardware interface.

### WP-05 — Binding
Deliver:
- binding payload;
- binding signature;
- binding validation;
- united identity reference.

Depends on:
- WP-02, WP-03, WP-04.

### WP-06 — Request and proof verification
Deliver:
- request schema;
- issuer validation;
- sequence validation;
- proof routing;
- verification result;
- replay protection.

Depends on:
- request authorization model.

### WP-07 — ZK adapter
Deliver:
- ZK verifier interface;
- selected proof-system adapter;
- public-input validation;
- deterministic verification result.

Depends on:
- final ZK protocol selection.

### WP-08 — Evidence and reputation boundary
Deliver:
- append-only evidence store;
- evidence queries;
- verification references;
- consensus-facing evidence interface.

The Node Core Identity implementation MUST NOT implement CPG-specific reputation scoring.

### WP-09 — Storage
Deliver:
- local persistence;
- encrypted object persistence;
- CID references;
- Kubo/IPFS adapter;
- local fallback;
- integrity verification.

### WP-10 — Propagation
Deliver:
- public identity package;
- compact references;
- manifest references;
- sensitive-data exclusion.

### WP-11 — Recovery
Deliver:
- continuity verification;
- recovery event;
- same-life recovery;
- new-life fallback.

### WP-12 — Testing
Deliver:
- unit tests;
- integration tests;
- negative tests;
- deterministic test vectors;
- lifecycle reconstruction tests;
- cryptographic compatibility tests.

### WP-13 — Reference implementation
Deliver:
- minimal complete implementation;
- documented interfaces;
- reproducible test execution;
- implementation-to-spec traceability.

### WP-14 — Audit
Deliver:
- security review;
- cryptographic review;
- lifecycle review;
- privacy review;
- protocol-boundary review;
- remediation record.

## 3. Dependency order

The minimum dependency graph is:

Canonical Model
    ↓
Node Life ─────────────┐
    ↓                  │
Node Identity          │
    ↓                  │
Credential Adapters    │
    ↓                  │
Binding ◀──────────────┘
    ↓
Requests
    ↓
Verification
    ├── ZK Adapter
    └── Evidence
          ↓
     Reputation Boundary
          ↓
      Consensus API

Storage and Propagation integrate with the verified identity/evidence layer.

Recovery depends on Node Life, Identity, Event Integrity, and Storage.

## 4. Repository implementation mapping

The implementation should map to the existing Node Core architecture rather than create an unrelated parallel architecture.

Primary area:

Node Core/Identity/

Related Node Core areas:

- Bootstrap/
- Cryptography/
- Storage/
- Recovery/
- Node Manager/
- Network/
- Consensus/
- Protocol Interface/
- Tests/
- Documentation/

Identity remains the owner of identity semantics. Related components provide infrastructure through defined interfaces.

## 5. Definition of done

A work package is not complete merely because files exist.

It is complete only when:

- the documented contract exists;
- implementation behavior matches the contract;
- positive and negative tests exist;
- deterministic vectors pass where applicable;
- failure behavior is defined;
- security boundaries are verified;
- integration does not violate Node Core / CPG separation.

## 6. First implementation milestone

The first executable milestone should be a minimal offline Identity Core capable of:

1. creating a Node Life;
2. generating/establishing Node Identity;
3. deriving Node ID according to the selected profile;
4. validating the identity;
5. recording lifecycle events;
6. reconstructing lifecycle state;
7. producing deterministic test output.

External identity approach, ZK, Kubo/IPFS, and network propagation should be added only after this core is stable.

## 7. Integration milestone

After the offline core passes tests:

1. add credential adapters;
2. add identity binding;
3. add request processing;
4. add verification evidence;
5. add storage adapters;
6. add propagation;
7. add recovery;
8. expose Node Manager interfaces;
9. expose Protocol Interface capabilities.

## 8. CPG integration rule

CPG Protocol MUST consume Node Core Identity through documented interfaces.

CPG MUST NOT directly manipulate:

- Node identity private material;
- Node lifecycle internals;
- identity event history;
- credential adapter internals;
- identity storage internals.

This preserves the architectural separation between Node Core and CPG Protocol.

## 9. Traceability

Every implementation component SHALL be traceable to:

- a specification section;
- an architectural component;
- an interface contract;
- one or more tests;
- and, where cryptographic behavior is involved, approved test vectors.

## 10. Current status

The implementation plan is complete at the planning level.

Production coding is blocked until the cryptographic and lifecycle decisions listed in the Identity Implementation Specification are formally resolved.

