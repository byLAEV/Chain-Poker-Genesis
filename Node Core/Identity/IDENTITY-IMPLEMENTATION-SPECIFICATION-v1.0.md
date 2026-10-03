# Node Core Identity — Implementation Specification v1.0

**Project:** Chain Poker Genesis by LAEV  
**Component:** Node Core / Identity  
**Status:** Pre-implementation specification  
**Scope:** Node identity, identity approach, binding, verification, reputation evidence, lifecycle continuity, and propagation boundaries.

## 1. Purpose

This specification converts the current Identity design into an implementation-ready contract.

It defines identity objects, Node Life, Node ID, external identity approach, cryptographic binding, protocol-controlled identity requests, selective / zero-knowledge proof boundaries, verification states, reputation evidence, consensus inputs, propagation references, storage boundaries, recovery and continuity, interfaces, security constraints, and test requirements.

It does not define CPG player identity, poker identity, table membership, table consensus, settlement, rake, or the CPG ledger.

## 2. Normative language

The terms MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY indicate implementation requirements.

## 3. Architectural boundary

Identity is a Node Core service.

Identity MUST remain independent of poker rules, CPG table state, player seating, table wallet, settlement, rake, CPG ledger, and CPG-specific reputation policy.

CPG may consume Node Core identity capabilities through the Protocol Interface.

## 4. Canonical objects

The implementation SHALL model at least these logical objects:

### 4.1 Node Life

A unique lifecycle instance of a Node.

Minimum fields:

- node_life_id
- node_id
- creation_event
- creation_timestamp
- state
- state_history
- termination_event when applicable
- termination_timestamp when applicable
- continuity_reference when recovered

### 4.2 Node Identity

The cryptographically verifiable identity of the Node.

Minimum fields:

- identity_version
- node_id
- public_key
- public_key_algorithm
- creation_timestamp
- status
- registration_reference
- verification_reference

Private key material MUST NOT be stored in the canonical Node Identity record.

### 4.3 External Identity Reference

A reference to the cryptographic identity approaching the Node.

It MUST identify credential type, public verification material or reference, signature method, verification result, and provenance metadata.

It MUST NOT require Node Core to possess the external private key.

### 4.4 Identity Binding

A verifiable relationship between a Node Life and an External Identity Reference.

Minimum conceptual fields:

- binding_id
- node_life_id
- node_id
- external_identity_reference
- binding_method
- binding_signature
- created_at
- verification_state
- manifest_hash

### 4.5 Identity Request

A protocol-controlled request for a specific identity property or proof.

Minimum conceptual fields:

- request_id
- request_version
- request_type
- issuer_reference
- target_node_life_id
- required_property
- required_proof_type
- sequence_number
- previous_request_reference where chained
- issued_at
- expires_at
- verification_policy

### 4.6 Verification Result

A signed or integrity-protected record of verification.

Minimum conceptual fields:

- verification_id
- request_id
- subject_reference
- verification_type
- result
- verified_claim_reference
- proof_reference
- verified_at
- verifier_reference
- verification_policy_version

### 4.7 Reputation Evidence

Reputation SHALL be represented as evidence, not as an unexplained trust number.

Minimum conceptual fields:

- evidence_id
- subject_reference
- source_reference
- event_reference
- verification_reference
- evidence_type
- result
- timestamp
- integrity_reference

A future reputation engine may aggregate this evidence, but the underlying evidence MUST remain auditable.

## 5. Node Life state machine

Initial implementation SHALL use an explicit lifecycle model.

Proposed canonical states:

UNINITIALIZED → CREATED → INITIALIZED → ACTIVE → SUSPENDED → TERMINATED

Recovery MAY transition:

TERMINATED → RECOVERED

only if continuity of the same Node Life is cryptographically and procedurally established.

Otherwise:

TERMINATED → NEW CREATED

MUST create a new Node Life.

The implementation MUST retain lifecycle events rather than merely overwriting the current state.

## 6. Node ID

The Node ID MUST be unique within the Node Core identity namespace, reproducible from canonical identity material according to the final cryptographic profile, integrity-protected, and independently verifiable.

The exact derivation algorithm is a prerequisite decision before production implementation.

The implementation MUST NOT invent a hardware-wallet-specific or password-derived Node ID rule.

Until formally selected, the derivation algorithm SHALL be represented as an explicit configuration/profile dependency rather than hard-coded by assumption.

## 7. Node Life creation

The installer is responsible for initiating Node Life creation.

Creation SHALL produce a verifiable creation event.

At minimum:

1. generate or establish the Node cryptographic identity;
2. derive the Node ID using the approved profile;
3. create the Node Life record;
4. record the creation timestamp;
5. create the initial lifecycle event;
6. persist the canonical identity record;
7. run identity validation;
8. expose the resulting Node identity to Node Manager.

The installer MUST NOT silently create multiple active Node Lives for one installation event.

## 8. External identity approach

Supported approach profiles SHALL be abstracted behind a credential interface.

Initial profiles:

- PGP;
- GPG/OpenPGP-compatible signatures;
- generic cryptographic signatures;
- hardware USB wallet signature results.

Each adapter MUST return a normalized verification result.

Node Core MUST receive public verification material and/or signature results.

Node Core MUST NOT require external private-key custody.

## 9. Identity binding

A binding SHALL be created only after successful cryptographic verification of the approach credential.

Binding MUST include:

- the Node Life reference;
- the Node ID;
- the external identity reference;
- the binding method;
- the canonical signed binding payload;
- timestamp;
- binding result;
- integrity reference.

Binding records MUST be immutable after creation.

Corrections or replacement bindings SHALL create new events and references rather than mutating historical evidence.

## 10. United identity representation

The United Identity Representation is a relationship object.

It MUST NOT erase, replace, or merge the independent identity records into an indistinguishable object.

Conceptually:

Node Life + Node Identity + External Identity + Binding → United Identity Reference

The representation SHOULD contain references rather than duplicating sensitive identity data.

## 11. Protocol request engine

Identity requests SHALL be processed as explicit protocol-controlled objects.

The request processor MUST:

1. authenticate the issuer;
2. validate request schema;
3. validate target Node Life;
4. validate sequence rules;
5. determine the required property;
6. determine acceptable proof types;
7. collect or receive the proof;
8. verify the proof;
9. produce a Verification Result;
10. append the resulting evidence to the identity history.

Invalid, expired, duplicated, or incorrectly sequenced requests MUST be rejected or placed into a defined non-valid state.

## 12. Zero-knowledge boundary

ZK proof support SHALL be an independent verification adapter.

The adapter MUST expose:

- proof type;
- statement / property identifier;
- public inputs;
- verification key or verification reference;
- proof;
- verification result;
- verifier version.

The system MUST NOT require disclosure of witness/private information when the selected ZK protocol does not require it.

The initial implementation MAY provide an adapter boundary before selecting concrete ZK protocols.

## 13. Verification

Verification MUST be deterministic for a given canonical input, verification policy version, cryptographic algorithm, proof, and verification context.

Verification MUST produce a durable result.

Minimum results:

- VERIFIED
- UNVERIFIED
- INVALID
- EXPIRED
- REJECTED

A failure MUST NOT be silently converted into reputation or trust.

## 14. Reputation evidence

The reputation subsystem SHALL consume verified events and evidence.

It MUST NOT treat an identity identifier alone, an unverified claim, a signature without successful verification, or a previous reputation value as sufficient proof of a new fact.

Reputation policy is a separate layer from the Identity Core.

Node Core Identity SHALL provide evidence interfaces without embedding CPG-specific reputation scoring.

## 15. Consensus interface

Consensus may query verified identity and reputation evidence.

The Identity subsystem SHALL expose:

- subject reference;
- verification state;
- applicable evidence;
- evidence timestamps;
- integrity references;
- lifecycle state;
- binding state.

It MUST NOT expose private keys.

The exact consensus policy belongs to the consuming consensus engine.

## 16. Proof-of-function interface

Identity/reputation MAY provide inputs for selecting proof-of-function requirements.

The Identity subsystem MUST NOT declare a function proven merely because reputation or identity is valid.

Proof-of-function verification SHALL return its own independently verifiable result.

## 17. Propagation

Propagation SHALL prefer compact references.

A propagated identity package MAY contain:

- Node ID;
- Node Life reference;
- binding reference;
- verification references;
- manifest hashes;
- CIDs;
- lifecycle state;
- consensus-relevant public evidence.

It MUST NOT propagate:

- private keys;
- secret witnesses;
- unencrypted sensitive identity material;
- credentials that are not authorized for propagation.

## 18. Storage

The implementation SHALL support a storage abstraction capable of local persistence, content-addressed references, encrypted object storage, Kubo/IPFS integration, local fallback, and recovery from authorized backup.

The Identity subsystem MUST NOT depend on Kubo availability for basic local identity verification.

CID resolution failure MUST NOT invalidate already locally verified identity records.

## 19. Encryption

Identity objects classified as sensitive MUST be encrypted at rest according to the Node Core cryptographic profile.

Encryption keys MUST be managed through an approved key-management interface.

External private keys MUST remain outside Node Core.

The implementation MUST distinguish:

- public identity metadata;
- integrity metadata;
- encrypted sensitive material;
- secret proof material.

## 20. Lifecycle metrics

The system MUST be able to reconstruct:

- total Node Lives created;
- active Node Lives;
- suspended Node Lives;
- terminated Node Lives;
- creation timestamps;
- termination timestamps;
- recovery events;
- new-life creation after termination;
- continuity references.

Metrics MUST be derived from lifecycle events rather than mutable counters alone.

## 21. Recovery

Recovery SHALL first attempt to establish continuity.

Continuity verification MUST use the approved recovery evidence and cryptographic profile.

If continuity cannot be established, the system MUST NOT label the result as recovery of the same Node Life.

A new Node Life MUST then be created.

## 22. Event integrity

Identity lifecycle, binding, request, and verification events SHOULD be append-only.

Every event SHOULD contain:

- event ID;
- event type;
- subject;
- timestamp;
- previous event reference;
- canonical payload hash;
- producer/verifier reference;
- schema version.

This creates an auditable event chain without requiring the Node Core Identity subsystem itself to own a blockchain ledger.

## 23. Canonical serialization

All identity objects participating in hashes or signatures MUST use a single canonical serialization profile.

Canonicalization MUST occur before:

- hashing;
- signing;
- Node ID derivation;
- binding;
- manifest generation.

The canonical serialization profile MUST be selected before implementation.

## 24. Interfaces

The implementation SHOULD expose logical interfaces equivalent to:

NodeIdentityManager
- create_identity()
- load_identity()
- validate_identity()
- get_identity()
- get_status()

NodeLifeManager
- create_life()
- transition_life()
- get_life()
- list_lives()
- recover_life()

CredentialVerifier
- verify_signature()
- verify_pgp()
- verify_gpg()
- verify_hardware_signature()

IdentityBinder
- create_binding()
- verify_binding()
- get_binding()

IdentityRequestProcessor
- validate_request()
- execute_request()
- get_request()
- list_requests()

ProofVerifier
- verify_zk_proof()
- verify_claim()

EvidenceStore
- append_event()
- get_event()
- list_events()
- verify_event_chain()

IdentityPropagation
- create_reference()
- resolve_reference()
- export_public_identity_package()

Exact programming-language APIs are implementation details and SHALL be defined after the architecture is approved.

## 25. Security requirements

The implementation MUST:

- keep private keys outside Node Core where the credential model is external;
- validate every signature before accepting a binding;
- prevent replay of expired or already-consumed requests;
- validate request sequencing;
- protect sensitive identity data at rest;
- maintain immutable historical evidence;
- distinguish verification failure from absence of evidence;
- prevent protocol-specific code from changing Node Core identity semantics;
- make security-relevant state transitions auditable.

## 26. Test plan

Before production implementation is considered complete, tests SHALL cover:

### Identity
- valid identity creation;
- invalid public key;
- invalid Node ID derivation;
- canonicalization mismatch;
- duplicate identity;
- malformed identity.

### Node Life
- creation;
- activation;
- suspension;
- termination;
- recovery with valid continuity;
- recovery without continuity;
- creation of a new life after failed continuity;
- lifecycle metric reconstruction.

### External credentials
- valid PGP signature;
- invalid PGP signature;
- valid GPG/OpenPGP signature;
- invalid signature;
- valid hardware-wallet signature result;
- altered signed payload;
- unsupported credential type.

### Binding
- valid binding;
- altered binding;
- wrong Node Life;
- wrong external identity;
- replayed binding;
- duplicate binding.

### Requests
- valid request;
- expired request;
- invalid issuer;
- invalid sequence;
- duplicate request;
- wrong target Node;
- unsupported proof type.

### ZK
- valid proof;
- invalid proof;
- altered public input;
- wrong verification key;
- proof for wrong statement.

### Reputation evidence
- verified evidence accepted;
- unverified claim rejected;
- altered evidence detected;
- duplicate event handled;
- historical evidence remains auditable.

### Storage
- local write/read;
- Kubo write/read;
- Kubo unavailable with local fallback;
- CID integrity mismatch;
- encrypted object recovery;
- unauthorized decryption denied.

### Propagation
- public reference generation;
- sensitive data excluded;
- private keys excluded;
- integrity references preserved.

## 27. Test vectors

The project SHALL create deterministic fixtures for:

- canonical identity records;
- Node ID derivation;
- signatures;
- binding payloads;
- request payloads;
- verification results;
- lifecycle events;
- event-chain hashes;
- CIDs;
- encrypted object metadata.

No production implementation should be accepted without matching the approved vectors.

## 28. Implementation phases

### Phase 1 — Specification lock
Resolve all open cryptographic and lifecycle decisions.

### Phase 2 — Canonical data model
Implement schemas and canonical serialization.

### Phase 3 — Node Life
Implement creation, lifecycle events, state reconstruction, and metrics.

### Phase 4 — Node Identity
Implement identity generation/validation according to the selected profile.

### Phase 5 — Credential adapters
Implement PGP/GPG/signature/hardware-wallet interfaces.

### Phase 6 — Binding
Implement binding and united identity references.

### Phase 7 — Request and verification engine
Implement protocol request processing and verification results.

### Phase 8 — Evidence and reputation interface
Implement append-only evidence and consensus-facing queries.

### Phase 9 — Storage and propagation
Implement local storage, encrypted objects, CIDs, Kubo integration, and propagation references.

### Phase 10 — Recovery
Implement continuity verification and new-life fallback.

### Phase 11 — Test vectors and reference implementation
Freeze vectors and validate all components against them.

### Phase 12 — Security review and audit
Perform independent review before declaring the component production-ready.

## 29. Implementation blockers

The following MUST be resolved before production implementation:

1. canonical serialization format;
2. exact Node ID derivation algorithm;
3. exact Node Life identifier algorithm;
4. lifecycle event taxonomy;
5. recovery continuity proof;
6. approved PGP/GPG profile;
7. hardware-wallet interface;
8. cryptographic signature profile;
9. ZK protocol selection;
10. request authorization model;
11. reputation evidence schema;
12. event-chain format;
13. encryption/key-management profile;
14. Kubo/IPFS storage adapter contract.

## 30. Definition of implementation readiness

Identity is implementation-ready when all blockers are resolved, schemas are canonical, state transitions are explicit, cryptographic algorithms are selected, interfaces are versioned, test vectors are frozen, security boundaries are documented, and the reference implementation can be tested independently of CPG poker logic.

**Status:** Pre-implementation specification.  
**No production implementation is implied by this document.**
