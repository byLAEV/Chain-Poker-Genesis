# Protocol Execution Model

## Chain Poker Genesis by LAEV

**Author:** Lerry Alexander Elizondo Villalobos — LAEV / byLAEV  
**Project:** Chain Poker Genesis by LAEV  
**Document Type:** Normative Execution Architecture  
**Status:** Initial execution-model foundation  
**Version:** 1.0

---

## 1. Purpose

This directory establishes the first execution-oriented layer connecting the CPG protocol specifications to reproducible execution.

The objective is to define a common execution sequence that can later be implemented independently by compatible implementations.

This document does not replace the existing protocol specifications. It establishes the execution boundary between canonical protocol data, manifests, state, execution, results, and verification.

---

## 2. Execution Principle

A compatible implementation SHOULD be able to transform the same valid canonical input into the same protocol-defined result.

Conceptually:

```text
CANONICAL INPUT
      ↓
MANIFEST VALIDATION
      ↓
STATE VALIDATION
      ↓
DETERMINISTIC EXECUTION
      ↓
CANONICAL RESULT
      ↓
EVIDENCE / HASH
      ↓
REPLAY / VERIFICATION
```

Implementation-specific mechanisms may vary where they do not change the protocol-defined result.

---

## 3. Execution Units

An execution is identified by the combination of:

```text
manifest_id
manifest_version
function_id
input_reference
state_reference
```

An implementation SHOULD additionally record an operation identifier for traceability.

---

## 4. Execution Lifecycle

The initial lifecycle is:

```text
RECEIVED
   ↓
VALIDATING
   ↓
READY
   ↓
EXECUTING
   ↓
RESULT_GENERATED
   ↓
EVIDENCE_GENERATED
   ↓
VERIFIED
```

Failure MUST remain observable and MUST NOT silently become a successful state.

Possible terminal or exceptional states include:

```text
REJECTED
FAILED
INVALID_INPUT
INVALID_MANIFEST
INVALID_STATE
VERIFICATION_FAILED
QUARANTINED
```

---

## 5. Determinism Boundary

The protocol MUST distinguish between:

1. deterministic protocol inputs;
2. implementation-specific execution mechanisms; and
3. protocol-defined outputs.

An implementation may use different internal algorithms, storage engines, programming languages, or operating systems provided that the resulting canonical protocol output remains compatible with the specification.

---

## 6. Canonical Execution Record

The conceptual execution record is:

```text
execution_id
manifest_id
manifest_version
function_id
function_version
input_reference
state_reference
result_reference
result_hash
evidence_reference
execution_status
```

The exact serialization format is to be established through the canonical-schema layer.

---

## 7. Replay

A valid execution SHOULD be replayable when the required historical inputs, manifest, and state references remain available.

Replay means:

```text
HISTORICAL INPUT
      +
HISTORICAL MANIFEST
      +
REQUIRED STATE
      ↓
RE-EXECUTION
      ↓
CANONICAL RESULT
```

The replayed result can then be compared with the recorded result and evidence.

---

## 8. Relationship to Manifests

A manifest defines the permitted execution space.

The execution model consumes that definition; it does not silently create protocol rules that are absent from the applicable manifest or normative specification.

```text
NORMATIVE SPECIFICATION
        ↓
MANIFEST
        ↓
VALIDATION
        ↓
EXECUTION
```

---

## 9. Relationship to Test Vectors

Test vectors SHALL become the reproducibility mechanism for the execution model.

A test vector should define at minimum:

```text
input
manifest
initial_state
expected_result
expected_state
expected_evidence
```

The first test-vector layer will be introduced separately so that execution rules and verification data remain distinguishable.

---

## 10. Scope Boundary

This document does NOT yet define:

- poker hand rules;
- betting semantics;
- dealer cryptography;
- settlement rules;
- P2P transport;
- consensus;
- specific storage implementation;
- a production programming language;
- a final cryptographic construction.

Those remain governed by their respective specifications.

---

## 11. Next Formalization Step

The next layer is:

```text
EXECUTION MODEL
      ↓
CANONICAL EXECUTION SCHEMA
      ↓
MINIMAL MANIFEST SCHEMA
      ↓
REFERENCE TEST VECTOR
      ↓
REFERENCE IMPLEMENTATION
```

This sequence is intended to prevent implementation-specific assumptions from becoming accidental protocol rules.

---

**End of document.**
