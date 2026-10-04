# Node Installation Reference Implementation

**Project:** Chain Poker Genesis by LAEV  
**Layer:** Node Core  
**Version:** 0.1.0

The executable reference implementation is now maintained in `Node Core/Bootstrap/` and validated by the Node Core test and audit suites. This documentation page preserves the installation boundary and expected behavior. for bootstrapping a **protocol-neutral Node Core**.

It does **not** install Chain Poker Genesis.

## Bootstrap

From the repository root:

```bash
python3 "Node Core/Bootstrap/Installer/bootstrap_node.py" ./node-runtime
```

The command creates the canonical Node Core storage namespace and writes a node installation manifest.

## Verification

```bash
python3 "Node Core/Tools/Validation/verify_node_installation.py" ./node-runtime
```

Expected result:

```text
status = VERIFIED
node_status = NODE_CORE_READY
cpg_protocol = NOT_INSTALLED
```

## Isolation

The reference implementation:

- uses Python standard library only;
- downloads no protocol packages;
- imports no CPG engine;
- creates no CPG ledger;
- creates no table state;
- creates no protocol membership.

## Scope

This is the Node Core installation baseline for installation/bootstrap verification. The canonical implementation lives under `Node Core/Bootstrap/`; validation utilities live under `Node Core/Tools/Validation/`. It is not yet a production cryptographic installer or distributed node implementation.


## Installation Boundary

The current baseline now also creates and verifies a canonical storage manifest at:

`node-storage/state/storage-manifest.json`

The reference verifier rejects:

- protocol associations;
- any CPG status other than `NOT_INSTALLED`;
- missing canonical storage paths;
- a missing storage manifest;
- a storage manifest with a different canonical path set.

The CI workflow includes both a positive readiness test and a negative protocol-isolation test.

## Canonical Implementation Boundary

- Installer: `Node Core/Bootstrap/Installer/bootstrap_node.py`
- Initialization: `Node Core/Bootstrap/Initialization/node_initializer.py`
- Verification: `Node Core/Bootstrap/Verification/bootstrap_verifier.py`
- Recovery: `Node Core/Bootstrap/Recovery/bootstrap_recovery_impl.py`
- Manifest schema: `Node Core/Configuration/Schemas/node-core-installation-manifest.schema.json`

## Current Scope

This reference implementation intentionally treats decentralized storage as a provider boundary. It records `NOT_PROVISIONED` rather than silently installing Kubo/IPFS. A later provider-specific installer can be added without changing the Node Core protocol-isolation invariant.
