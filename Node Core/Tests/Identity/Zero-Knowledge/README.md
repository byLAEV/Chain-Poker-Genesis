# Node Core Tests — Identity / Zero-Knowledge

## Purpose

This directory contains tests and deterministic test vectors for the Node Core zero-knowledge verification boundary.

Tests here validate the **adapter contract**, not CPG poker rules.

## Test categories

### Envelope validation

- required field missing;
- malformed proof envelope;
- unsupported proof-system identifier;
- unsupported proof-system version.

### Verification-key handling

- known verification key;
- unknown verification key;
- altered verification key material;
- verification-key identifier mismatch.

### Public inputs

- valid public inputs;
- altered public inputs;
- public-input encoding mismatch;
- statement identifier mismatch.

### Proof results

- valid proof;
- invalid proof;
- proof generated for another statement;
- proof generated with another verification key.

### Request binding

- valid request binding;
- wrong request identifier;
- replayed request;
- expired request;
- context mismatch.

### Reference compatibility

The external reference repository is used only as a compatibility/reference target. No external source code is copied into Node Core.

## Completion rule

A proof-system adapter is not complete until:

1. positive vectors pass;
2. negative vectors fail deterministically;
3. error classes are stable;
4. verification-key selection is tested;
5. public-input binding is tested;
6. request/context binding is tested;
7. the implementation remains independent of CPG poker state.
