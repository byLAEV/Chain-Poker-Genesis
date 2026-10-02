# Node Core Reconciliation Matrix

**Status:** Working architectural audit  
**Branch:** `architecture/repository-structure-audit`

## Purpose
This document reconciles the Node Core material already present in the repository before any directory migration.

The key finding is that Node Core is already partially implemented across architecture documentation, storage specifications, cryptographic engines, and a protocol-neutral Python reference implementation.

## Reconciliation

| Domain | Existing evidence | Current assessment | Target architectural layer |
|---|---|---|---|
| Node boundary | `docs/architecture/NODE-CORE-AND-CPG-PROTOCOL-CORE.md` | Explicit boundary already defined | `node-core/` architecture |
| Local storage | dual-storage bootstrap specification + runtime | Partially specified and executable | Node Core / storage |
| Decentralized storage | IPFS/Kubo provider boundary | Architectural direction; provider not provisioned by baseline | Node Core / storage provider |
| Canonical storage structure | `node-storage/{identity,cryptography,configuration,state,records,recovery,protocol}` | Executable baseline exists | Node Core / storage |
| Storage manifest | `storage-manifest.json` | Executable verification exists | Node Core / manifests |
| Object registry | `object-registry.json` + `object_registry.py` | Executable baseline exists | Node Core / storage |
| Node identity | node installation + identity material | Bootstrap exists; full cryptographic identity remains to reconcile | Node Core / identity |
| Cryptographic Core | `engines/cryptographic-core-engine/` | Specification exists; boundary needs canonicalization | Node Core / cryptography |
| Cryptographic Engine | `engines/cryptographic-engine/` | Protocol cryptography layer defined | CPG Protocol Core / cryptographic services |
| Cryptographic Connection Engine | `engines/cryptographic-connection-engine/` | Identity/credential lifecycle defined | Node Core / identity connection boundary |
| Runtime lifecycle | `reference-implementation/node-installation/node_runtime.py` | Executable readiness model exists | Node Core / runtime |
| Bootstrap | `bootstrap_node.py` and verification scripts | Executable baseline exists | Node Core / installation |
| Recovery | recovery metadata + readiness checks | Baseline exists; full recovery semantics remain open | Node Core / recovery |
| Networking | architectural Node Core boundary + P2P/conflict engine | Needs explicit separation of substrate vs protocol conflict semantics | Node Core + Protocol Core |
| Synchronization | storage sync architecture | Conceptual/specification work remains | Node Core / synchronization |
| Protocol association | explicit isolation in reference implementation | Strong boundary already demonstrated | Protocol Core boundary |
| Dedicated Ledger | architecture document explicitly assigns it to CPG Protocol Core | Must not be moved into generic Node Core storage semantics | CPG Protocol Core |
| Execution | reference execution slice | Exists as conformance/reference slice, not full node execution | implementation/reference |
| Test vectors | protocol execution and node installation tests | Existing baseline; needs expansion | tests/test-vectors |

## Critical finding: `NODE_CORE_COMPLETE` is scoped

The executable audit prints `completion_gate = NODE_CORE_COMPLETE` but the same audit explicitly reports `synchronization = NOT_EVALUATED`. The installation README also states that the implementation is an installation/bootstrap baseline rather than a production distributed node.

Therefore the completion message should be interpreted as:

> **Node Core bootstrap/reference slice passes its defined completion gate.**

It must not yet be interpreted as:

> **The entire production Node Core architecture is complete.**

## Canonical dependency model

```text
Node Core
│
├── Identity
├── Cryptographic Core
├── Local Storage
├── Decentralized Storage Provider Boundary
├── Storage Manifest / Object Registry
├── State / Runtime
├── Integrity / Recovery
├── Networking Substrate
└── Synchronization
        │
        ▼
CPG Protocol Core
│
├── Protocol Identity / Membership
├── Protocol State
├── Tables / Hands / Events
├── Protocol Cryptography
├── Consensus / Conflict Rules
├── Settlement
└── Dedicated Ledger
```

## Three cryptographic layers

The cryptographic architecture currently defines three distinct layers:

1. **Cryptographic Core** — primitive operations.
2. **Cryptographic Engine** — CPG protocol cryptography and profiles.
3. **Cryptographic Connection Engine** — identity and credential lifecycle.

These must not be collapsed during repository restructuring.

## Recommended target placement

The final repository should not blindly move the three cryptographic engines together.

```text
node-core/
├── identity/
│   └── cryptographic-connection/
├── cryptography/
│   └── core/
├── storage/
├── state/
├── runtime/
├── networking/
├── synchronization/
├── recovery/
└── versioning/

protocol-engines/
└── cryptography/
    └── cpg-cryptographic-engine/
```

This is a **candidate target**, not yet a migration command.

The exact placement of the Cryptographic Engine must be reconciled with the protocol-core boundary because it implements CPG-specific cryptographic semantics while depending on Node Core cryptographic primitives.

## Storage target

The existing canonical storage model should remain conceptually:

```text
node-storage/
├── identity/
├── cryptography/
├── configuration/
├── state/
├── records/
├── recovery/
└── protocol/
```

The physical runtime directory `node-storage/` should not be confused with the repository source directory `node-core/storage/`.

One is runtime state; the other is implementation source/specification.

## Immediate architectural decisions to close

1. Final Node Core cryptographic boundary.
2. Exact identity ownership between Node Core and CPG Protocol Core.
3. Networking substrate vs protocol conflict-resolution ownership.
4. Synchronization state machine.
5. Recovery state machine.
6. Canonical serialization for Node Core objects.
7. Manifest versioning.
8. Object registry canonical schema.
9. Provider abstraction for local/IPFS storage.
10. Runtime package/source location.

## Next migration step

The repository should now be reorganized conceptually around **existing canonical assets**, not newly invented folders.

The next operation is therefore:

**reconcile `docs/node/` + `docs/developer-specifications/node-infrastructure/` + `docs/developer-specifications/storage/` against the reference implementation files and the three cryptographic engines.**

Only after that comparison should the physical `node-core/` source tree be created.