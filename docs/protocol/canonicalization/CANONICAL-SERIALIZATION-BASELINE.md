# Canonical Serialization Baseline

## Chain Poker Genesis by LAEV

**Status:** Working baseline for execution vectors  
**Version:** 0.1.0  
**Scope:** Machine-readable JSON execution objects and test vectors

## 1. Purpose

This document establishes the initial serialization rule required to make the first CPG execution vector reproducible.

It is a baseline, not a final protocol-wide serialization specification. It applies only to the execution/test-vector layer until the broader canonicalization audit is accepted.

## 2. Canonical JSON Form

For the baseline execution vectors:

1. Data MUST be represented as UTF-8 JSON.
2. Object keys MUST be ordered lexicographically by Unicode code point.
3. Objects MUST contain no insignificant whitespace.
4. Arrays MUST preserve their declared order.
5. Strings MUST use JSON string escaping.
6. Boolean, null, number, array, object, and string types MUST retain their JSON types.
7. Implementations MUST NOT add undeclared fields when calculating a canonical representation.
8. The resulting UTF-8 byte sequence is the canonical serialization input to hashing.

Conceptually:

```text
JSON OBJECT
   ↓
LEXICOGRAPHIC OBJECT-KEY ORDER
   ↓
COMPACT JSON
   ↓
UTF-8 BYTES
   ↓
HASH
```

## 3. Hash Baseline

The execution-vector baseline uses SHA-256 over the UTF-8 bytes of the canonical JSON representation of the object being hashed.

The algorithm identifier is represented as:

```text
sha256:<lowercase-hex>
```

This baseline does not establish SHA-256 as the final cryptographic algorithm for every CPG subsystem.

## 4. Scope

This rule currently applies to:

- execution test vectors;
- the minimal execution result used by CPG-EXEC-0001;
- reproducibility experiments derived from this execution layer.

It does not yet override any existing engine-specific serialization rule.

## 5. Deterministic Result Example

Canonical result object:

```json
{"status":"OK","value":"CPG-EXEC-0001"}
```

Its SHA-256 value is recorded in the corresponding test vector.

## 6. Future Acceptance Gate

The final protocol-wide canonical serialization specification must reconcile:

- existing canonical schemas;
- Engine 04 Event Model;
- state representation;
- CID/content addressing;
- signatures;
- manifests;
- execution records;
- deterministic replay.

Until that reconciliation is complete, this document remains a scoped baseline.

---

**End of document.**
