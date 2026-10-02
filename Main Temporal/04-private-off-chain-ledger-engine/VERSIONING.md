# 04 — Private Off-Chain Ledger Engine — Versioning Policy

**Chain Poker Genesis by LAEV**

## 1. Purpose

Versioning applies separately to:

- engine implementation;
- event schema;
- event types;
- cryptographic rules;
- Merkle rules;
- anchor rules.

The objective is to evolve the engine without silently changing the interpretation of historical records.

## 2. Version Identity

Every event carries an `event_version` identifying the schema/rules under which it was produced.

Engine version and event version are related but are not assumed to be identical.

Historical event versions are never rewritten merely because the engine implementation changes.

## 3. Historical Immutability

Previously committed records must remain interpretable under their original rules.

If migration is required, preserve:

1. original record;
2. original hash;
3. original schema/version;
4. migration metadata;
5. new representation;
6. new hash, if generated.

## 4. Change Classes

### Patch

Bug fixes that do not alter interpretation of valid historical records.

### Minor

Backward-compatible additions such as optional metadata or new event types, subject to compatibility rules.

### Major

Changes affecting canonical serialization, hash input, Merkle construction, event ordering, required fields, verification semantics, or anchor interpretation.

Major changes require an explicit protocol-version transition.

## 5. Cryptographic Versioning

Cryptographic rule changes must be identifiable.

The implementation should record sufficient metadata to determine:

- hash algorithm/version;
- canonicalization version;
- Merkle construction version;
- anchor construction version.

A verifier must never guess these parameters.

## 6. Schema Evolution

New fields should be introduced without invalidating old records when backward compatibility is intended.

Removed or reinterpreted fields require a version transition.

Unknown fields must have defined behavior for canonicalization and verification.

## 7. Merkle Evolution

A change to leaf encoding, ordering, parent hashing, odd-leaf handling, domain separation, or root encoding is cryptographically significant.

Such changes require a new Merkle construction version.

Historical batches remain verifiable under their original rules.

## 8. Bitcoin Anchor Evolution

A change to the method used to commit a Merkle Root to Bitcoin requires an anchor-version identifier.

Historical anchor records retain their original transaction/reference information.

Future mechanisms must not invalidate prior verification.

## 9. Compatibility

An implementation should declare:

- supported engine versions;
- supported event-schema versions;
- supported cryptographic versions;
- supported Merkle versions;
- supported anchor versions.

Compatibility must be explicit rather than inferred.

## 10. Migration

Private-storage migration must be non-destructive.

A migration process should preserve the original representation and produce an auditable migration record.

No migration may alter a previously anchored historical commitment.

## 11. Rollback

Software rollback does not imply ledger rollback.

Software state may revert; committed historical evidence remains available for verification.

## 12. Future Features

Potential future additions include encrypted archival, replication, advanced indexing, compression, cross-node synchronization, optimized anchoring, and advanced proof formats.

A future feature becomes part of the protocol only when formally specified and versioned.

## 13. Open Versioning Decisions

Version 1.0 establishes the historical and architectural baseline.

Still open:

- exact semantic-versioning convention;
- event-schema compatibility matrix;
- cryptographic algorithm identifiers;
- migration tooling;
- formal deprecation policy;
- anchor-version registry.

---

**Historical source:** `04. Private Off-Chain Ledger Engine_- Chain Poker Genesis by LAEV.pdf`
