# Node Core API Contract

**Status:** CANONICAL  
**Version:** 1.0.0  
**Scope:** Protocol-neutral programmatic Node Core service boundary

## 1. Purpose

This contract defines the authoritative API boundary for Node Core.

The API is a service surface, not proof that every declared operation is implemented. Implementation availability is tracked separately.

## 2. Availability states

Every operation MUST be classified as one of:

- IMPLEMENTED
- PARTIAL
- DECLARED
- UNAVAILABLE

The API manifest is the implementation availability record.

The API contract MUST NOT be interpreted as declaring every operation implemented.

## 3. Core principles

The API MUST:

- validate authorization;
- validate lifecycle state before state-changing operations;
- return deterministic errors;
- preserve protocol isolation;
- never expose private-key material or sensitive credential material;
- distinguish local coherence from network synchronization;
- avoid silently performing unsupported operations.

## 4. Canonical service domains

The Node Core API domains are:

### Node
- health
- readiness
- status
- start
- stop
- recover

### Identity
- identity.status
- identity.create
- identity.verify

### Storage
- storage.create
- storage.read
- storage.write
- storage.delete
- storage.verify
- storage.status

### Engines
- engines.list
- engines.register
- engines.start
- engines.stop

### Protocol Interface
- protocols.list
- protocols.validate
- protocols.install
- protocols.activate
- protocols.deactivate

### Verification
- verify.manifest
- verify.integrity
- verify.environment

These domains form the canonical Node Core API surface. Subsystem-specific API READMEs are supporting contracts beneath this boundary and MUST NOT contradict it.

## 5. Implementation status

Current manifest:

`Node Core/API/NODE-CORE-API-MANIFEST.json`

currently declares the facade **IMPLEMENTED_PARTIAL**.

The reference facade currently exposes:

- `health()`
- `node_status()`
- `read(object_id)`

Therefore the Node Core API is **not fully implemented**.

This distinction is normative.

## 6. Protocol isolation

The API may expose the Protocol Interface, but CPG-specific table state, poker rules, Table Wallet, settlement, rake and CPG consensus are not Node Core API semantics.

## 7. Errors and authorization

State-changing operations MUST validate authorization and lifecycle state.

Unsupported operations MUST return an explicit deterministic unavailable/unsupported result rather than silently succeeding.

## 8. Conformance

API conformance MUST verify:

1. manifest availability agrees with implementation;
2. implemented operations behave according to their domain contract;
3. unsupported operations are not falsely reported as implemented;
4. sensitive material is not returned;
5. protocol isolation is preserved.
