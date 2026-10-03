# Node Manager Contract

**Status:** Normative design baseline  
**Scope:** Protocol-neutral Node Core

## Purpose
The Node Manager is the control-plane component responsible for node lifecycle coordination, configuration selection, identity activation state, engine registration, health/status exposure, and explicit protocol installation requests.

It does not implement CPG rules, CPG consensus, CPG settlement, or a CPG ledger.

## Responsibilities
1. Load and validate Node Core configuration.
2. Coordinate Bootstrap and Runtime lifecycle.
3. Expose node status and readiness.
4. Coordinate registered Node Core engines.
5. Enforce the protocol-installation boundary.
6. Route recovery requests to Recovery.
7. Refuse lifecycle transitions that violate the canonical state model.
8. Record auditable management events.

## Required states
`UNINITIALIZED`, `READY`, `RUNNING`, `DEGRADED`, `RECOVERY`, `SHUTTING_DOWN`, `STOPPED`.

## Invariants
- Node Manager MUST NOT install CPG implicitly.
- Empty `protocol_associations` means no protocol is associated.
- `cpg_protocol = NOT_INSTALLED` is required for an unassociated baseline node.
- A failed readiness check MUST NOT produce `READY`.
- Protocol installation MUST occur through Protocol Interface.
- Node Manager MUST NOT own protocol-specific ledger or settlement state.

## Interface operations
- `status()`
- `readiness()`
- `start()`
- `stop()`
- `recover()`
- `register_engine()`
- `unregister_engine()`
- `request_protocol_installation()`

## Error behavior
Operations MUST fail closed on invalid state transitions, malformed configuration, unavailable required dependencies, or protocol-boundary violations.

## Non-goals
No poker logic, protocol consensus, wallet custody, settlement, or CPG ledger behavior belongs here.
