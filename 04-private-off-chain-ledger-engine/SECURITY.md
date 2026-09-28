# 04 — Private Off-Chain Ledger Engine — Security Model

**Chain Poker Genesis by LAEV**  
**Version:** 1.0

## 1. Security Objective

The Private Off-Chain Ledger protects the confidentiality and integrity of detailed protocol history while providing externally verifiable cryptographic commitments through Merkle Roots and Bitcoin anchoring.

```text
Confidentiality       → Private Ledger
Record Integrity      → Event Hashes
Batch Integrity       → Merkle Tree / Root
External Certification → Bitcoin Anchor
```

## 2. Trust Boundaries

The engine crosses these boundaries:

- protocol event producers;
- ledger ingestion;
- private persistent storage;
- Merkle construction;
- Bitcoin anchoring;
- audit and verification clients.

Each boundary must be authenticated and authorized according to the broader protocol security architecture.

## 3. Confidentiality

Private event records may contain operational information that must not be exposed through Bitcoin.

The anchoring process therefore commits to cryptographic evidence rather than publishing complete event payloads.

Access to private records is controlled independently of blockchain verification.

## 4. Integrity Layers

Integrity is layered:

1. canonical event representation;
2. individual event hash;
3. optional previous-hash relationship;
4. deterministic Merkle consolidation;
5. external Bitcoin commitment.

Each layer has a distinct purpose and is not a substitute for the others.

## 5. Critical Security Boundary

A hash is tamper-evident, not an access-control mechanism.

If an attacker can modify a private record and every local copy of its hash before an external commitment is consulted, local comparison alone cannot establish the original state.

The external anchor helps detect rewriting of data already represented by an anchored commitment.

Bitcoin anchoring also does not prevent deletion of private data; it provides a commitment against which retained or recovered data can later be compared.

## 6. Event Ingestion Security

Event producers must not silently rewrite accepted records.

The implementation should define:

- authenticated event sources;
- authorization for event classes;
- schema validation;
- event-size limits;
- duplicate detection;
- idempotency;
- rejection logging;
- malformed-event handling.

## 7. Canonicalization Security

Verification is meaningful only when serialization is deterministic.

The implementation must define behavior for:

- field ordering;
- character encoding;
- Unicode normalization;
- numeric representation;
- null values;
- optional fields;
- whitespace;
- escaping;
- schema versions.

A change to canonicalization is a protocol-versioning concern.

## 8. Merkle Security

Merkle construction must be deterministic.

The implementation must define and test:

- leaf ordering;
- duplicate leaves;
- odd node counts;
- tree depth;
- parent hashing;
- root encoding;
- batch finalization.

A verifier must be able to reproduce exactly the same root from the same committed event set.

## 9. Anchor Security

The anchor mechanism must address:

- incorrect root submission;
- duplicate/conflicting anchor metadata;
- transaction replacement or rebroadcast confusion;
- incomplete confirmation;
- unavailable Bitcoin connectivity;
- incorrect transaction parsing.

Exact transaction and confirmation policies belong to the dedicated Bitcoin/cryptographic specification.

## 10. Access Control

The implementation should distinguish at minimum:

- event producers;
- ledger writers;
- ledger readers;
- auditors/verifiers;
- administrators;
- anchor operators, if separate.

Exact permissions remain TBD until node and administration architecture defines them.

## 11. Availability and Recovery

Security includes protection against operational loss.

The implementation should define:

- durable writes;
- crash recovery;
- backup;
- restoration;
- corruption detection;
- replication, if used;
- recovery ordering;
- anchor-state reconciliation.

Bitcoin unavailability must not destroy already persisted private history.

## 12. Audit Security

Audit operations should be read-oriented and should not mutate historical records.

Verification tooling should expose sufficient evidence to reproduce:

- event hashes;
- batch membership;
- Merkle proof material;
- Merkle Roots;
- anchor references.

## 13. Initial Threat Boundary

The initial model considers:

- accidental record corruption;
- unauthorized modification;
- malformed event injection;
- duplicate event submission;
- local hash inconsistency;
- Merkle reconstruction errors;
- anchor metadata errors;
- Bitcoin connectivity loss;
- storage failure;
- partial processing.

Compromised hosts, malicious participants, colluding nodes, key compromise, supply-chain attacks, and cryptographic algorithm failure require dedicated security specifications.

## 14. Security Claims Boundary

The engine must not claim:

- that hashing alone makes data immutable;
- that Bitcoin anchoring makes private storage indestructible;
- that an anchor proves every real-world event occurred;
- that an anchored root establishes the truth of an event payload;
- that a timestamp alone proves causal ordering.

The engine provides cryptographic evidence about the data committed to it.

## 15. Security Acceptance

Security conformance should demonstrate:

- deterministic hashing;
- detection of modified records;
- deterministic Merkle reconstruction;
- detection of altered batch membership;
- correct anchor comparison;
- controlled write/read access;
- recovery after interrupted processing;
- preservation of anchor metadata.

---

**Status:** Functional security boundary; detailed cryptographic and operational controls remain subject to dedicated specifications.
