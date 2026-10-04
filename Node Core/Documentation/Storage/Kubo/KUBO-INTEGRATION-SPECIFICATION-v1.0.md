# Kubo Integration Specification v1.1

**Project:** Chain Poker Genesis by LAEV  
**Layer:** Node Core  
**Subsystem:** Storage  
**Provider:** Kubo / IPFS  
**Status:** CANONICAL ARCHITECTURAL INTEGRATION SPECIFICATION

---

## 1. Objective

Provide a complete provider contract for the dual-storage architecture:

```text
Local Node Storage
        +
Kubo/IPFS Storage
        =
Node Core Dual Storage
```

The two providers expose the same logical Node Core object model while retaining independent physical storage implementations.

---

## 2. Canonical ownership

Node Core is the canonical owner of the logical storage contract.

Kubo is a provider and must not redefine:

- Node Core object classes;
- Node Core storage policy;
- Node Core authorization;
- Node Core lifecycle;
- Node Core recovery semantics;
- Node Core protocol isolation.

Kubo's repository layout is not the Node Core storage layout.

---


## 2A. Kubo installation model

Node Core shall support two provider levels:

1. **Kubo Adapter Available** — the Node Core adapter exists and can communicate with an already provisioned Kubo node.
2. **Kubo Node Provisioned** — Node Core downloads and installs the complete official Kubo binary distribution selected for the host platform, initializes a dedicated Kubo repository, and manages the resulting local Kubo node through the adapter.

The adapter is therefore **not** the Kubo implementation. It is the integration boundary.

The Kubo installation package is acquired at installation time from the official upstream release distribution. "Latest" means the latest compatible stable release selected by the installer at that moment; the installed version is then recorded and treated as immutable until an explicit provider upgrade.

Node Core MUST verify the downloaded package before installation using the upstream release integrity information available for that distribution. An unverified package MUST NOT be activated.

## 2B. Canonical Node Core paths

The installer defines one absolute **Node Core Root**. All Node Core-managed Kubo paths are derived from that root.

Linux reference layout:

```text
<NODE_CORE_ROOT>/
├── External Providers/
│   └── Kubo/
│       └── <kubo-version>/
│           ├── bin/
│           │   └── ipfs
│           ├── release/
│           └── metadata/
│
└── node-storage/
    └── providers/
        └── kubo/
            ├── repository/
            ├── runtime/
            ├── logs/
            ├── state/
            └── synchronization/
```

The Kubo repository MUST be an absolute path supplied to Kubo through `IPFS_PATH`.

Node Core MUST NOT rewrite Kubo's internal repository layout to resemble the Node Core storage layout.

The separation is intentional:

```
Node Core Storage
    └── canonical logical objects

Kubo Repository
    └── Kubo-owned IPFS datastore/configuration/state
```

The Node Core storage metadata and the Kubo repository therefore remain physically and logically independent.

## 2C. Relocation rule

Changing the Node Core installation root MUST change the generated absolute Kubo paths together.

Node Core MUST NOT rely on:
- the operator's home-directory `.ipfs`;
- implicit current working directory;
- hard-coded `~/.ipfs`;
- relative paths that escape the selected Node Core root.

The installer sets `IPFS_PATH` explicitly for every Kubo process.

Kubo's own default internal paths remain Kubo-owned. Node Core controls only the outer repository location and process environment.

## 2D. Installation lifecycle

```text
NOT_PROVISIONED
      ↓
RELEASE_SELECTED
      ↓
PACKAGE_DOWNLOADED
      ↓
PACKAGE_VERIFIED
      ↓
KUBO_INSTALLED
      ↓
REPOSITORY_INITIALIZED
      ↓
CONFIGURED
      ↓
HEALTHY
      ↓
INITIAL_SYNC_PENDING
      ↓
INITIAL_SYNCING
      ↓
DUAL_STORAGE_READY
```

Failure at any installation stage MUST leave the provider unavailable rather than falsely reporting Dual Storage readiness.

## 2E. Initial synchronization

After a complete Kubo node is initialized, Node Core performs an initial local-to-Kubo synchronization before enabling Dual Storage.

```
Node Core Local Storage
        ↓
eligibility + encryption policy
        ↓
Kubo provider
        ↓
CID/integrity verification
        ↓
coherence verification
        ↓
DUAL_STORAGE_READY
```

The initial synchronization is not a blind filesystem copy. It is a Storage Manager operation over logical Node Core objects.

For private/restricted objects, Node Core encryption occurs before distribution. Kubo receives the resulting bytes; Kubo does not become the key-custody layer.

Temporary objects and objects excluded by Storage Policy remain excluded according to the canonical policy.

The synchronization process MUST be resumable and MUST preserve a durable pending/retry state.

## 2F. Dual Storage preference

Node Core configuration exposes the provider mode:

```text
LOCAL_ONLY
DUAL_STORAGE
```

`DUAL_STORAGE` may be selected only after:

- Kubo is installed;
- the Kubo repository is initialized;
- the provider health check succeeds;
- the initial synchronization completes;
- CID/content integrity has been verified;
- no unresolved synchronization conflict blocks readiness.

Selecting `DUAL_STORAGE` changes the active Storage Policy; it does not replace the Local Provider.

When Dual Storage is active, Kubo is the preferred distributed read provider when available and valid, while Local Storage remains the authoritative node-local fallback.

## 3. Provider capabilities

The Kubo provider adapter must expose capabilities at the Node Core abstraction level.

Conceptual operations:

```text
put
get
has
stat
remove
pin
unpin
list
resolve
verify
health
version
sync
publish
retrieve
```

Not every Kubo command needs to be exposed directly. The adapter exposes only the operations required by the Node Core Storage API.

---

## 4. Content addressing

Kubo uses content-addressed identifiers (CIDs). Node Core must preserve the CID as an external content identity/reference where applicable.

The adapter must never silently replace a CID with a mutable local path.

The Node Core object metadata should retain:

- object identifier;
- CID when present;
- object class;
- logical path;
- version;
- content digest;
- encryption state;
- provider state;
- integrity state;
- synchronization state.

---

## 5. Dual storage

A dual object may have:

```text
Logical Object
   |
   +-- Local Provider
   |      |
   |      +-- local object
   |
   +-- Kubo Provider
          |
          +-- CID
```

The copies are logically equivalent only after integrity/coherence validation.

---

## 6. Read algorithm

```text
READ REQUEST
    |
    v
Validate object identity/policy
    |
    v
Kubo available?
   / \
 yes  no
  |    |
  v    v
Kubo   Local
read   fallback
  |
  v
Verify CID/integrity
  |
  +---- invalid ----> coherence failure
  |
 valid
  |
  v
return object
```

The local fallback is an availability mechanism, not an authority override.

---

## 7. Write algorithm

For DUAL policy:

```text
WRITE REQUEST
    |
    v
Validate policy
    |
    v
Write/prepare local state
    |
    v
Kubo operation
    |
    +---- success ----> commit provider state
    |
    +---- failure ----> durable retry/recovery state
```

The implementation must define atomicity and recovery before production use.

---

## 8. Coherence states

At minimum:

```text
UNKNOWN
LOCAL_ONLY
KUBO_ONLY
DUAL_COHERENT
LOCAL_AHEAD
KUBO_AHEAD
CONFLICT
PROVIDER_UNAVAILABLE
INVALID_LOCATION
INTEGRITY_FAILURE
SYNC_PENDING
SYNCING
RECOVERY_REQUIRED
```

The exact state machine must be canonicalized before implementation.

---

## 9. Synchronization

Synchronization is a Node Core operation coordinated through the provider abstraction.

It must distinguish:

- object synchronization;
- metadata synchronization;
- provider availability;
- replication intent;
- retry state;
- conflict state;
- recovery state.

Kubo's own peer-to-peer mechanisms remain Kubo responsibilities.

---

## 10. Kubo repository boundary

The Kubo repository contains Kubo-managed state. Node Core must not place its own canonical storage metadata inside Kubo's internal repository layout.

The Node Core application structure and Kubo repository remain independent.

---

## 11. Kubo configuration

The upstream Kubo configuration is JSON and is read when the node is instantiated/started; commands operating against a running daemon do not reread the file at runtime.

Relevant configuration domains include:

- Addresses;
- API;
- Bootstrap;
- Datastore;
- Discovery;
- Bitswap;
- AutoNAT;
- AutoTLS;
- AutoConf;
- Routing;
- Version;
- Gateway;
- provider/network options.

Node Core must generate or validate provider configuration without assuming that all Kubo options are part of the Node Core contract.

---

## 12. RPC security

Kubo's RPC is an administrative interface.

Node Core integration must:

- prefer local-only RPC;
- authenticate any authorized non-local access;
- restrict allowed paths;
- never expose unrestricted admin RPC publicly;
- record provider health and compatibility;
- fail closed for unauthorized administrative operations.

Kubo itself documents that its RPC can control configuration and secret key management.

---

## 13. Gateway boundary

Kubo's HTTP Gateway is a content retrieval interface, not a replacement for the Node Core Storage API.

Node Core may use a gateway only where its provider policy explicitly permits gateway retrieval.

Administrative control remains through the provider's authorized API.

---

## 14. Kubo capabilities relevant to Node Core

The upstream implementation provides, among other components:

- content addressing / CIDs;
- UnixFS;
- DAG/content traversal;
- block storage;
- datastore;
- Bitswap;
- libp2p networking;
- peer discovery;
- routing;
- delegated routing;
- IPNS;
- HTTP Gateway;
- RPC API;
- CLI;
- configuration profiles;
- repository management;
- garbage collection;
- pinning;
- metrics/monitoring;
- FUSE support;
- content blocking;
- AutoConf;
- AutoNAT;
- WebUI.

Node Core should integrate only the capabilities required by its provider contract.

---

## 15. Pinning and retention

Kubo pinning is provider-level retention behavior.

Node Core Storage Policy must separately determine whether a logical object requires distributed retention.

Therefore:

```text
Node Core Retention Policy
          ↓
Kubo Pin/Unpin operation
```

A Kubo pin is not by itself a Node Core policy decision.

---

## 16. Garbage collection

Kubo datastore garbage collection must never be treated as equivalent to Node Core object deletion.

Before requesting provider-side deletion/GC, Node Core must know:

- whether the logical object is still required;
- whether another provider contains the canonical copy;
- whether retention permits removal;
- whether the object is pinned;
- whether recovery requirements are satisfied.

---

## 17. Encryption

Kubo/IPFS content addressing does not replace Node Core encryption policy.

For restricted/private content:

```text
Plain object
    ↓
Node Core encryption
    ↓
Encrypted bytes
    ↓
Kubo/IPFS
    ↓
CID
```

The encryption keys remain outside Kubo's generic storage-provider role.

---

## 18. Recovery

Recovery must work when:

- Kubo is offline;
- local storage is offline;
- one copy is corrupt;
- synchronization is interrupted;
- provider configuration is unavailable;
- the node restarts during a pending operation.

SREC remains an additional disaster-recovery layer and does not replace the dual-storage system.

---

## 19. Provider lifecycle

```text
NOT_PROVISIONED
      ↓
DISCOVERED
      ↓
CONFIGURED
      ↓
HEALTHY
      ↓
DEGRADED
      ↓
UNAVAILABLE
      ↓
RECOVERING
      ↓
HEALTHY
```

Provider lifecycle must not determine whether the Node Core itself is operational.

---

## 20. Version compatibility

The adapter must record:

- Kubo version;
- provider API compatibility;
- supported capability profile;
- configuration profile;
- repository state;
- compatibility result.

Kubo upgrades must be tested against Node Core provider contract before being accepted.

---

## 21. Required test vectors

At minimum:

1. local-only write/read;
2. Kubo-only write/read;
3. dual write/read;
4. Kubo unavailable → local fallback;
5. local unavailable → Kubo read;
6. both unavailable;
7. CID mismatch;
8. local content mismatch;
9. Kubo content mismatch;
10. synchronization interruption;
11. retry;
12. recovery;
13. encryption;
14. unauthorized decryption;
15. unauthorized RPC;
16. provider restart;
17. Node Core restart;
18. garbage-collection safety;
19. pin/unpin policy;
20. version incompatibility.

---

## 22. Implementation sequence

```text
DUAL STORAGE CONTRACT
        ↓
CANONICAL OBJECT MODEL
        ↓
PROVIDER INTERFACE
        ↓
LOCAL PROVIDER
        ↓
KUBO ADAPTER
        ↓
COHERENCE ENGINE
        ↓
SYNC QUEUE
        ↓
RECOVERY
        ↓
POLICY ENGINE
        ↓
TEST VECTORS
        ↓
REFERENCE IMPLEMENTATION
```

---

## 23. Boundary conclusion

Kubo is not a second Node Core.

It is a decentralized storage provider integrated into Node Core through a controlled adapter.

The Node Core dual-storage model therefore preserves:

```text
Node Core authority
+
Local persistence
+
Kubo/IPFS content addressing
+
Provider independence
+
Local fallback
+
Coherence verification
+
Recovery
=
Dual Storage
```
