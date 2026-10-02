# Node Installation Reference Implementation

**Project:** Chain Poker Genesis by LAEV  
**Layer:** Node Core  
**Version:** 0.1.0

This directory contains the first executable reference implementation for bootstrapping a **protocol-neutral Node Core**.

It does **not** install Chain Poker Genesis.

## Bootstrap

From the repository root:

```bash
python3 reference-implementation/node-installation/bootstrap_node.py ./node-runtime
```

The command creates the canonical Node Core storage namespace and writes a node installation manifest.

## Verification

```bash
python3 reference-implementation/node-installation/verify_node_installation.py ./node-runtime
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

This is an implementation baseline for installation/bootstrap verification. It is not yet a production cryptographic installer or distributed node implementation.


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

## Current Scope

This reference implementation intentionally treats decentralized storage as a provider boundary. It records `NOT_PROVISIONED` rather than silently installing Kubo/IPFS. A later provider-specific installer can be added without changing the Node Core protocol-isolation invariant.
