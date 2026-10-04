# Node Core CLI Contract

**Status:** CANONICAL  
**Version:** 1.0.0  
**Scope:** Protocol-neutral Node Core operator interface

## 1. Purpose

The CLI is an operator interface to Node Core management functions. It is not a second lifecycle authority and is not a protocol-specific control surface.

## 2. Canonical command group

The reference CLI exposes:

- `node status`
- `node readiness`
- `node start`
- `node stop`
- `node recover`

Additional command groups may be added only through a future canonical contract update.

## 3. Boundary

CLI commands MUST delegate state transitions to Node Manager/Node Core services.

CLI MUST NOT mutate lifecycle state directly.

Read commands MUST NOT mutate state.

## 4. Output

Machine-readable JSON output is the reference output.

Success output MUST be deterministic for identical state.

Errors MUST be emitted as machine-readable JSON on stderr.

## 5. Exit codes

- `0`: requested operation completed successfully.
- `1`: deterministic operational failure (validation, lifecycle, dependency or permission failure).
- argument-parser failures use the parser's non-zero process semantics.

The CLI MUST NOT return success for an operation that failed.

## 6. Error determinism

The same invalid operation against the same Node Core state MUST return a non-zero exit result and a deterministic error structure.

## 7. Security

Sensitive identity material, private keys, credentials and secret cryptographic material MUST never be printed.

## 8. Protocol isolation

The Node Core CLI MUST NOT expose CPG-specific:

- poker commands;
- table state;
- Table Wallet;
- settlement;
- rake;
- ledger mutation;
- protocol consensus.

Protocol operations remain behind Protocol Interface.

## 9. Implementation status

The reference CLI is implemented for the canonical node lifecycle subset.

The complete command catalog remains intentionally partial until the remaining Node Core subsystem contracts are closed.

## 10. Verification

Canonical tests MUST verify:

1. status;
2. readiness;
3. start;
4. stop;
5. recovery boundary;
6. invalid-state failures;
7. deterministic non-zero failure;
8. JSON output;
9. CLI delegation to Node Manager;
10. protocol isolation.

Reference implementation:

`Node Core/CLI/node_cli.py`
