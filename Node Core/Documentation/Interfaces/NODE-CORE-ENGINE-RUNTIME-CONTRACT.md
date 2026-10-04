# Node Core Engine Runtime Contract

**Status:** Normative contract baseline  
**Scope:** Protocol-neutral engine lifecycle inside Node Core

## 1. Purpose

Engine Runtime is the execution boundary for registered Node Core engines.

It is subordinate to Node Core Runtime. It does not replace Node Core lifecycle management and it does not define CPG or application protocol behavior.

## 2. Boundary

Node Runtime owns:

- Node Core initialization;
- readiness;
- Node Core lifecycle;
- shutdown;
- recovery of the Node Core.

Engine Runtime owns:

- engine registration;
- engine identity/version metadata;
- engine lifecycle state;
- engine start/stop;
- engine runtime snapshot.

## 3. Engine states

The minimum canonical states are:

`REGISTERED → ACTIVE → STOPPED`

An implementation may add failure or initialization states only through a future contract revision.

## 4. Required operations

The baseline Engine Runtime implementation MUST provide:

- `register(name, version)`;
- `start(name)`;
- `stop(name)`;
- `snapshot()`.

Engine names and versions are required.

## 5. Isolation

An engine MUST NOT:

- redefine Node Core lifecycle;
- directly modify private storage outside its authorized boundary;
- install or activate CPG by bypassing Protocol Interface;
- introduce CPG-specific semantics into Node Core Engine Runtime.

## 6. Relationship to Engine API

Engine API is the external contract surface.

Engine Runtime is the internal lifecycle boundary implementing that surface.

The API may expose capabilities not yet implemented, but such capabilities MUST be explicitly classified as unavailable/partial until implemented and tested.

## 7. Determinism

Invalid engine operations MUST fail explicitly. Engine state transitions MUST NOT be silently accepted when the target engine does not exist or required identity/version information is missing.

## 8. Verification requirement

The canonical test suite MUST verify:

1. registration;
2. required name/version validation;
3. start transition;
4. stop transition;
5. snapshot state;
6. unknown-engine failure;
7. protocol isolation.

## 9. Protocol isolation

CPG ledger, table state, poker rules, Table Wallet, settlement, rake and CPG-specific consensus are outside this contract.
