# Node Core CLI Contract

**Status:** Normative design baseline  
**Scope:** Protocol-neutral Node Core

## Purpose
The CLI is an operator interface to Node Core management functions. It must expose Node Core state without becoming a protocol-specific control surface.

## Command groups
- `node status`
- `node readiness`
- `node start`
- `node stop`
- `node recover`
- `node identity`
- `node storage`
- `node engines`
- `node protocols`
- `node verify`

## Rules
1. Read commands MUST NOT mutate node state.
2. Mutating commands MUST return explicit success/failure status.
3. Protocol installation MUST require an explicit protocol operation and pass through Protocol Interface.
4. The CLI MUST NOT expose CPG-specific poker, wallet, settlement, or ledger commands in the Node Core namespace.
5. Machine-readable output MUST be available for automation.
6. Errors MUST be deterministic and non-zero at process level when an operation fails.
7. Sensitive identity material MUST never be printed.

## Exit semantics
- `0`: requested operation completed.
- non-zero: validation, state, dependency, permission, or execution failure.

## Non-goals
The CLI does not define protocol behavior.
