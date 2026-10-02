# Reference Execution Slice

This directory contains the first minimal reference implementation for the CPG execution workflow.

## Scope

The implementation verifies the vertical slice:

```text
TEST VECTOR
    ↓
MANIFEST CONSISTENCY
    ↓
DETERMINISTIC STATE TRANSITION
    ↓
CANONICAL RESULT
    ↓
SHA-256
    ↓
VERIFICATION
```

It is deliberately not a production node, poker engine, consensus engine, wallet, dealer, or P2P implementation.

## Run

From the repository root:

```bash
python3 reference-implementation/execution/verify_vector.py docs/protocol/test-vectors/CPG-EXEC-0001.json
```

The verifier must report:

```text
status = VERIFIED
result_hash = sha256:bb61b7af7576d708471c8d930252f251343899b7564c48b79d90f5fdcf270eff
```

The reference implementation uses only Python's standard library.

## Reproducibility rule

The verifier uses the scoped canonical serialization baseline at:

```text
docs/protocol/canonicalization/CANONICAL-SERIALIZATION-BASELINE.md
```

This implementation must not be interpreted as freezing the final CPG-wide serialization or cryptographic profile.

**Author:** Lerry Alexander Elizondo Villalobos — LAEV / byLAEV
