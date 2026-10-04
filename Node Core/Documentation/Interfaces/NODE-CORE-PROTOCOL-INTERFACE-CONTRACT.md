# Node Core Protocol Interface Contract

**Status:** CANONICAL  
**Version:** 1.0.0  
**Scope:** Boundary between protocol-neutral Node Core and independently installed protocol engines

## 1. Purpose

Protocol Interface is the single Node Core boundary through which an independently versioned protocol may be discovered, compatibility-checked, registered, installed and transitioned through its lifecycle.

It does not implement protocol semantics.

## 2. Canonical lifecycle

`DISCOVERED → COMPATIBLE → REGISTERED → INSTALLED → ACTIVE`

Alternative controlled states:

- SUSPENDED
- REMOVED

An implementation MUST reject invalid forward transitions.

## 3. Required descriptor

Every protocol descriptor MUST identify:

- `protocol_id`;
- `version`;
- `engine_id`;
- `manifest_hash`.

Optional capabilities and metadata may be supplied.

## 4. Required operations

The reference interface provides:

- `discover(descriptor)`;
- `check_compatibility(protocol_id, node_capabilities)`;
- `register(protocol_id)`;
- `install(protocol_id)`;
- `activate(protocol_id)`;
- `suspend(protocol_id)`;
- `remove(protocol_id)`;
- `get(protocol_id)`;
- `all()`.

## 5. Compatibility gate

A protocol MUST NOT be treated as compatible unless its declared required capabilities are satisfied by the Node Core capability set.

Compatibility is a prerequisite for registration in the canonical lifecycle.

## 6. Installation and activation gates

Installation MUST require REGISTERED state.

Activation MUST require INSTALLED state.

Node Core MUST NOT silently activate an uninstalled protocol.

## 7. Independent versioning

Protocol engine versions are independent of Node Core versions.

Updating Node Core MUST NOT imply an automatic update of installed protocol engines.

## 8. Protocol isolation

Protocol Interface MUST NOT define or implement:

- CPG consensus;
- CPG ledger;
- poker/NLHE rules;
- table state;
- Table Wallet;
- settlement;
- rake;
- protocol-specific cryptographic semantics.

The interface only establishes the controlled boundary.

## 9. Node Core completion boundary

Before any protocol is installed:

```text
protocol_associations = []
cpg_protocol = NOT_INSTALLED
synchronization = NOT_EVALUATED
```

The installation boundary may report `ARMED`; this means a verified separation point exists, not that CPG is installed.

## 10. Verification

The canonical test suite MUST verify:

1. descriptor validation;
2. discovery;
3. capability compatibility;
4. registration;
5. installation;
6. activation;
7. suspension;
8. removal;
9. invalid lifecycle transitions;
10. protocol isolation.

Reference implementation:

`Node Core/Protocol Interface/protocol_interface.py`

Reference manifest:

`Node Core/Protocol Interface/PROTOCOL-INTERFACE-MANIFEST.json`
