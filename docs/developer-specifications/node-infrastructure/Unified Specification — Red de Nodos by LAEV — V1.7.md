# Unified Specification of Storage, Identity, Reputation, Backup, Recovery, Propagation and State Anchoring Infrastructure

## Red de Nodos by LAEV

### Version 1.7

**Status:** Architectural Specification

## 1. Purpose

This specification defines the base infrastructure of Red de Nodos by LAEV for node installation and bootstrap, cryptographic identity, local and distributed storage, Kubo/IPFS integration, cryptographic reputation, state manifests, logical and physical object location, synchronization, cryptographic state propagation, operational continuity under node failures, backup and recovery, reconciliation, auditing, failure testing, cryptographic state anchoring, Proof of Functions, and support for applications installed on top of the infrastructure.

```text
IDENTITY → STORAGE → STATE MANIFEST → SYNCHRONIZATION
→ PROPAGATION → CONSENSUS / COORDINATION → APPLICATION
```

```text
SYNCHRONIZATION ≠ COMMUNICATION
SYNCHRONIZATION ≠ CONSENSUS
SYNCHRONIZATION ≠ BACKUP
BACKUP ≠ RECOVERY
ANCHORING ≠ CONSENSUS
PROOF OF FUNCTIONS ≠ PROOF OF WORK
```

Chain Poker Genesis by LAEV operates as an application on top of this infrastructure.

## 2. Fundamental State Principle

```text
NODE STATE → FULL MANIFEST → MANIFEST HASH → NODE IDENTITY → PROPAGATION
```

`FULL_MANIFEST` is the structured state. `MANIFEST_HASH` is its cryptographic commitment. Normal propagation does not require distributing the complete manifest to every node.

```text
PROPAGATED_HASH_RECORD = evidence that a node identified and propagated a state hash
BLOCK_HASH = commitment to a propagation block containing a Merkle Root
PROOF_OF_FUNCTIONS_RECORD = evidence that defined node-protocol functions were executed and verified
```

## 3. Proof of Functions (PoF)

### 3.1 Definition

**Proof of Functions (PoF)** is a protocol-level mechanism of Red de Nodos by LAEV that demonstrates, through verifiable evidence, that defined node-protocol functions are implemented, operational, and functioning according to their rules.

PoF is a property of the node protocol itself. It is not Bitcoin Proof of Work, mining, consensus, a replacement for consensus, backup, synchronization, or application validity.

```text
NODE PROTOCOL → DEFINED FUNCTIONS → FUNCTION EXECUTION
→ VERIFIABLE EVIDENCE → PROOF OF FUNCTIONS
```

### 3.2 Purpose

PoF answers: **Are the functions required by the node protocol actually operating and producing verifiable results?**

```text
NODE ONLINE ≠ NODE FUNCTIONALLY VERIFIED
```

### 3.3 Functional Evidence

Functions may include cryptographic identity, storage initialization, manifest generation and integrity, local state verification, Kubo/IPFS integration, state hash generation, propagation, peer evidence reception and verification, state continuity, recovery interface availability, and auditability.

Functions may be REQUIRED, OPTIONAL, CONDITIONAL, or APPLICATION-SPECIFIC.

### 3.4 Genesis Proof of Functions

The initial operational infrastructure may establish a **Genesis Proof of Functions** through five initial active nodes. Power or connectivity alone is insufficient.

```text
NODE 1 + NODE 2 + NODE 3 + NODE 4 + NODE 5
→ FUNCTIONAL VERIFICATION → PROOF OF FUNCTIONS → GENESIS NETWORK STATE
```

Required evidence may include identity validity, storage validity, manifest validity, state-hash validity, propagation validity, and peer-evidence validity.

The five-node configuration is the first explicit demonstration that the distributed node infrastructure operates as a protocol, provided the required functions are actually executed and verified.

### 3.5 PoF Is Not Proof of Work

```text
PROOF OF WORK → computational work
PROOF OF FUNCTIONS → protocol functionality
```

They have different purposes and security assumptions.

### 3.6 PoF and Identity

PoF evidence should be attributable to a cryptographically identifiable node:

```text
NODE_ID + FUNCTION_ID + FUNCTION_VERSION + FUNCTION_RESULT
+ STATE_REFERENCE + TIMESTAMP + SIGNATURE
```

### 3.7 PoF and State

PoF may reference MANIFEST_HASH, VERSION, OBJECT_HASH, PROPAGATION_EVENT, CHECKPOINT, or BLOCK_HASH without becoming equivalent to synchronization or consensus.

### 3.8 PoF and Synchronization

```text
PROOF OF FUNCTIONS ≠ SYNCHRONIZED
```

PoF demonstrates functional capability/evidence. Synchronization demonstrates that the current state reached the defined propagation threshold.

### 3.9 PoF and Consensus

```text
PoF ≠ CONSENSUS POWER ≠ VOTING WEIGHT ≠ AUTHORITY
```

Consensus/coordination belongs to the applicable engine.

### 3.10 PoF State

```text
POF_NOT_STARTED
POF_PENDING
POF_RUNNING
POF_PARTIALLY_VERIFIED
POF_VERIFIED
POF_EXPIRED
POF_FAILED
POF_QUARANTINED
```

Typical flow:

```text
NODE_READY → POF_PENDING → POF_RUNNING → FUNCTIONS VERIFIED → POF_VERIFIED
```

A failure must never silently become a valid state.

## 4. Cryptographic Identity

Separate **Node Identity** (logical cryptographic identity) from **Node Instance** (a concrete installation). A new instance may recover an existing identity only with authorization and sufficient cryptographic evidence.

Installation must allow importing an existing identity, using the Kubo/IPFS-managed identity, or authorized recovery. In the first version, bootstrap may abort when no valid identity exists and no authorized generation mechanism exists.

Private keys must not be ordinary files inside `cryptographic_identity/` or `cryptographic_reputation/`. Those structures contain public identity, identifiers, metadata, references, history, proofs, records, and state. Kubo-managed private material must be handled through supported Kubo mechanisms.

## 5. Node Bootstrap

```text
UNINSTALLED → PROGRAM_INSTALLED → IDENTITY_REQUIRED
→ IDENTITY_VALIDATED → STORAGE_INITIALIZED → NODE_READY
```

Possible failures: IDENTITY_INVALID, IDENTITY_MISMATCH, STORAGE_INITIALIZATION_FAILED, BOOTSTRAP_FAILED, QUARANTINED.

PoF may begin after the required operational state is reached.

## 6. General Storage Architecture

```text
NODE/
├── storage/
├── services/
├── applications/
├── config/
├── runtime/
└── logs/
```

```text
storage/
├── local/
├── synchronization/
├── distributed/
├── metadata/
└── recovery/
```

## 7. Local Storage

```text
storage/local/
├── system/
├── shared/
├── modules/
├── temporary/
├── public/
├── private/
├── restricted/
├── personal/
└── backup/
```

Classes: TEMPORARY, LOCAL_PUBLIC, LOCAL_PRIVATE, LOCAL_RESTRICTED, LOCAL_PERSONAL.

## 8. Module Isolation

```text
storage/local/modules/<module>/
├── data/
├── temporary/
├── public/
├── private/
├── restricted/
├── personal/
├── cache/
├── metadata/
└── sync/
```

## 9. Identity and Reputation

The logical structures exist in both local storage and the distributed representation of Kubo/IPFS:

```text
NODE/
├── LOCAL STORAGE
│   ├── cryptographic_identity/
│   │   ├── node_id
│   │   ├── public_identity
│   │   ├── metadata/
│   │   ├── references/
│   │   └── history/
│   └── cryptographic_reputation/
│       ├── records/
│       ├── attestations/
│       ├── proofs/
│       ├── references/
│       ├── history/
│       └── metadata/
└── IPFS/KUBO STORAGE
    ├── cryptographic_identity/
    └── cryptographic_reputation/
```

“Same structure” means the same logical organization and functional model, not identical bytes at every moment. Temporary divergence such as LOCAL v15 / IPFS v14 / SYNC PENDING is valid.

## 10. Kubo/IPFS Integration

Kubo/IPFS is not an ordinary file directory.

```text
Application / Module
→ Storage API
→ Storage Manager
→ Policy Engine
→ Local / Distributed Adapter
→ Kubo Adapter
→ Kubo API / RPC
→ Kubo Repository
→ IPFS Network
```

Do not arbitrarily write inside Kubo's internal repository.

## 11. Distributed Policies

Network: IPFS_PUBLIC_NETWORK, IPFS_PRIVATE_NETWORK.

Encryption: ENCRYPTED, UNENCRYPTED.

Access: PUBLIC, PRIVATE, RESTRICTED, PERSONAL.

Persistence: EPHEMERAL, PERSISTENT, PINNED, ARCHIVAL.

Replication: LOCAL, MULTI_NODE, EXTERNAL_PINNING.

Integrity: HASH, CID, SIGNATURE, MERKLE.

```text
CID ≠ ENCRYPTION KEY
CID ≠ PERMISSION
CID ≠ IDENTITY
PINNED ≠ STORAGE CLASS
IPFS_PRIVATE_NETWORK ≠ CONTENT_ENCRYPTED
```

## 12. Storage API

Required operations include:

```text
create read update delete classify store retrieve prepareSync
publish receive verify quarantine restore backup
resolveLocation getManifest getStateManifest
compareRepresentations getDistributedEvidence
```

Policies must express WHERE, WHO, WHEN, HOW LONG, ENCRYPTED, SYNC, PIN, REPLICATE, DELETE, VERSION, REPRESENTATION, PEER, and EVIDENCE.

## 13. Storage Address Manifest / Storage Locator

The state machine must not guess physical locations.

```text
OBJECT ID → LOGICAL PATH → STORAGE ADDRESS MANIFEST
→ PHYSICAL / DISTRIBUTED LOCATION
```

The locator records object_id, logical_path, object_type, version, hash, local presence/reference/version/hash, and IPFS/Kubo presence/CID/reference/version/hash.

Location states:

```text
LOCAL_ONLY
DISTRIBUTED_ONLY
LOCAL_AND_DISTRIBUTED
SYNC_PENDING
SYNC_PROCESSING
MISSING_LOCAL
MISSING_DISTRIBUTED
CONFLICT
QUARANTINED
```

Normal resolution is logical path → manifest → storage address → adapter → object. Backend scanning is reserved for discovery, recovery, and diagnosis.

## 14. Executable Artifacts

Never execute an object merely because it was found in local, IPFS, or Kubo storage. Verify HASH, SIGNATURE, PROVENANCE, VERSION, and EXECUTION POLICY. An eventual Execution Artifact Manifest may formalize this.

## 15. Complete State Manifest

A canonical manifest represents node state:

```text
MANIFEST
├── node_id
├── version
├── identity_reference
├── storage_state
├── local_state
├── ipfs_state
├── previous_manifest_hash
├── timestamps
└── ...
```

Deterministic serialization is required:

```text
CANONICAL MANIFEST → HASH(MANIFEST) → MANIFEST_HASH
```

## 16. Manifest and Propagation

`FULL_MANIFEST`, `MANIFEST_HASH`, and `PROPAGATED_HASH_RECORD` are distinct.

```text
NODE_ID + MANIFEST_VERSION + MANIFEST_HASH + SIGNATURE
```

The propagated hash does not contain the complete manifest.

## 17. Synchronization State

```text
NOT_SYNCHRONIZED
PROPAGATION_PENDING
PROPAGATING
THRESHOLD_NOT_REACHED
THRESHOLD_REACHED
SYNCHRONIZED
SYNC_FAILED
RETRY_WAIT
```

Flow:

```text
NEW STATE
→ FULL MANIFEST UPDATED
→ LOCAL VERIFIED
→ IPFS/KUBO VERIFIED
→ HASH
→ NODE-BOUND HASH
→ PROPAGATION
→ PEER EVIDENCE VERIFIED
→ SYNC_THRESHOLD
→ SYNCHRONIZED
```

## 18. Storage Coherence vs Network Synchronization

Local/IPFS equality of hashes demonstrates storage coherence. Propagation of node-bound manifest hashes demonstrates network synchronization.

```text
STORAGE COHERENCE ≠ NETWORK SYNCHRONIZATION
```

## 19. Synchronization Threshold

The network need not require 100% propagation. A configurable `SYNC_THRESHOLD` and independent `BACKUP_THRESHOLD` must exist.

Example: `3/5 = 60%`. This is a configurable reference, not a universal security guarantee.

```text
T ≤ R ≤ N
```

where T is the minimum threshold, R the relevant node set, and N the total considered for that policy.

## 20. Propagation Roles

```text
PRIMARY
SECONDARY
BACKUP
```

Selection may depend on availability, capacity, latency, activity, connectivity, and node function.

## 21. Node Activity

```text
HIGH_ACTIVITY
MEDIUM_ACTIVITY
LOW_ACTIVITY
```

Activity may influence propagation frequency and participation to reduce saturation. Activity is not consensus authority.

## 22. Propagation Chain

Propagation is a cryptographic event chain, not merely timestamps.

```text
propagation_event_id
previous_propagation_hash
node_id
manifest_hash
manifest_version
propagation_role
source_node
destination_node
timestamp
signature
provenance
```

`timestamp` is temporal metadata; `previous_propagation_hash` provides cryptographic continuity.

## 23. Two Different Chains

**Manifest Chain** represents state evolution:

```text
MANIFEST v1 → HASH_1 → MANIFEST v2 → HASH_2 → MANIFEST v3 → HASH_3
```

**Propagation Chain** represents distribution of evidence. They are related but distinct.

## 24. Current-State Propagation Block

The aggregation mechanism is primarily for synchronization and continuity of current state. It is not by itself historical backup, recovery, consensus, or an external archive.

## 25. Merkle Tree Construction

A validated set of manifest hashes may form a Merkle Tree.

The leaf set must be deterministic by explicit rules for leaf ordering, hash set, batch/range/epoch, algorithm, and tree version.

## 26. Propagation Block

```text
PROPAGATION BLOCK
├── block_id
├── network_id
├── epoch / range
├── leaf_count
├── aggregation_algorithm
├── merkle_root
├── participating_nodes
├── sync_threshold
├── timestamp
├── previous_block_hash
├── provenance
└── signatures
```

This is a cryptographically chained propagation-evidence block, not a blockchain consensus block.

## 27. Block Hash

```text
BLOCK_HASH =
H(block_id + network_id + range/epoch + merkle_root
+ participating_nodes + previous_block_hash + timestamp + metadata)
```

Model:

```text
MANIFEST_HASHES → MERKLE_ROOT → PROPAGATION BLOCK → BLOCK_HASH
```

## 28. 3-of-5 Propagation

A policy may define five nodes, with three constructing/verifying the hash set and Merkle Root. The resulting block receives a BLOCK_HASH. The remaining two may receive only the BLOCK_HASH as compact evidence.

D and E do not necessarily receive all leaves, the Merkle Tree, or the complete block.

## 29. Asymmetric Distribution

The purpose is synchronization resilience and current-state continuity.

```text
A B C
 \|/
  3 OF 5
    ↓
HASH SET → MERKLE ROOT → BLOCK HASH
                           /      \
                          D        E
```

D and E can retain compact evidence without being full state replicas.

## 30. Continuity Under Node Failure

If one constructing node fails, preserved BLOCK_HASH evidence may allow continued recognition of the current state, subject to the active policy, cryptographic evidence, conflict rules, and application requirements.

## 31. Chain Poker Genesis Application

Example:

```text
HAND #184
→ MANIFEST v41
→ MANIFEST_HASH_41
→ PROPAGATION
→ SYNC_THRESHOLD
→ SYNCHRONIZED
→ CONTINUITY
→ HAND #185
→ MANIFEST v42
```

A temporary failure must not automatically stop a transition if current state remains valid, synchronization evidence remains sufficient, no conflict exists, and application policy permits continuation.

## 32. Meaning of SYNCHRONIZED

SYNCHRONIZED means the current state reached the minimum propagation threshold defined by the applicable policy. It does not mean 100% network propagation or that all nodes possess the full manifest.

Valid evidence may require node_id, manifest_hash, version, signature, and provenance.

## 33. Meaning of BACKED_UP

BACKED_UP is independent from SYNCHRONIZED and is determined by BACKUP_THRESHOLD or another redundancy policy.

```text
SYNCHRONIZED ≠ BACKED_UP
```

## 34. Evidence Backup vs State Backup

`BLOCK_HASH` is compact cryptographic evidence. It cannot reconstruct the manifest or node data.

```text
BLOCK_HASH ≠ FULL STATE BACKUP
```

Recovery requires sufficient material to reconstruct trustworthy state.

## 35. Merkle Proof

Nodes retaining the Merkle structure may provide inclusion proofs:

```text
MANIFEST_HASH + MERKLE_PROOF + MERKLE_ROOT + BLOCK_METADATA
```

This permits complete data at participating nodes and compact evidence at additional nodes.

## 36. Synchronization Checkpoint

A checkpoint may represent a recognized propagation period:

```text
CHECKPOINT 001
├── range
├── merkle_root
├── block_hash
├── participating_nodes
├── sync_threshold
└── timestamp
```

Checkpoints may form a chain.

## 37. Checkpoint Chain

```text
BLOCK 001 → HASH B1
BLOCK 002 → PREVIOUS B1 → HASH B2
BLOCK 003 → PREVIOUS B2 → HASH B3
```

This is cryptographically linked and tamper-evident. It is not, by itself, an absolute guarantee of immutability. External anchoring can strengthen evidence.

## 38. Merkle Root Determinism

All participating nodes must use the same network_id, epoch/range, ordered manifest hashes, aggregation algorithm, and tree version. Leaf ordering must be explicit and deterministic.

## 39. External State Anchor

```text
MANIFEST → HASH → MERKLE ROOT → BLOCK HASH → STATE ANCHOR → EXTERNAL NETWORK
```

Anchoring may use Bitcoin or another compatible network. Anchoring does not itself establish consensus, validity, legitimacy, latest-version status, or authority.

## 40. Storage State Machine

```text
CREATED → CLASSIFIED → STORED_LOCAL → SYNC_PENDING
→ SYNC_PROCESSING → DISTRIBUTED
```

Exceptions: TEMPORARY_FAILURE → RETRY_WAIT → SYNC_PROCESSING; INVALID → QUARANTINED.

Keep OBJECT_STATE, SYNC_STATE, and DISTRIBUTED_STATE separate.

## 41. Synchronization Registry

```text
storage/synchronization/
├── outgoing/
├── incoming/
├── pending/
├── processing/
├── published/
├── failed/
├── retry/
├── quarantine/
└── manifests/
```

Minimum fields: object_id, module_id, local_path, content_hash, cid, version, storage_class, visibility, encryption, sync_policy, retention_policy, persistence_policy, sync_status.

## 42. Journal and Consistency

Filesystem, Kubo, IPFS, and external storage are not assumed to form one ACID transaction. Use a metadata store, journal, and reconciliation.

## 43. Concurrency

Protect against lost updates, stale versions, races, double publish, and double delete using appropriate version checks, hashes, parent references, manifest sequences, locks, and idempotency.

## 44. Reconciliation

Never use “highest version always wins” automatically. Verify identity, signature, version, hash, previous_manifest_hash, parent_reference, provenance, CID, anchor, historical continuity, and peer evidence.

Same version + same hash = coherent. Same version + different hash = conflict. Divergent local/IPFS versions may reconcile only after continuity verification.

## 45. Conflicts

Use CONFLICT_DETECTED and, when continuity cannot be established, QUARANTINED. Do not silently patch data merely to make hashes match.

## 46. Audit

The programmer/auditor must inspect local storage, Kubo/IPFS, full manifest, manifest hash, identity, reputation, storage coherence, propagation, thresholds, Merkle root, block hash, propagation/checkpoint chains, PoF, anchor, backup, and recovery.

```text
NO GUESSING
NO SILENT PATCHING
```

## 47. SREC — Encrypted External Backup System

SREC is the Backup, Recovery and Operational Continuity Subsystem of Red de Nodos by LAEV.

It does not replace Storage, Synchronization, Kubo/IPFS, Propagation, Consensus, or PoF.

Purpose:

```text
BACKUP
RECOVERY
DISASTER RECOVERY
OPERATIONAL CONTINUITY
```

## 48. Recovery Package

```text
recovery_package/
├── manifest
├── identity.enc
├── reputation.enc
├── metadata.enc
├── history/
├── proofs/
├── integrity/
└── recovery/
```

Provider-independent support may include S3-compatible storage, SFTP, WebDAV, Remote IPFS, object storage, and custom providers.

## 49. Backup Encryption

Possible authenticated-encryption algorithms include AES-256-GCM and ChaCha20-Poly1305. Separate Node Identity Key, Backup Encryption Key, Recovery Key, and Application Secret when appropriate.

## 50. Recovery Principles

External backup is initially UNTRUSTED INPUT and not automatically a root of trust.

```text
NEW INSTANCE → RECOVERY REQUIRED → BACKUP SELECTED → RECOVERY AUTHORIZED
→ BACKUP VERIFIED → DECRYPTING → IDENTITY VALIDATING → IDENTITY VALID
→ REPUTATION VALIDATING → REPUTATION VALID → RESTORING
→ RECONCILING → RECOVERY COMPLETE → NODE READY
```

## 51. Recovery Failures

Possible states: INVALID_BACKUP, DECRYPTION_FAILED, IDENTITY_MISMATCH, REPUTATION_MISMATCH, INTEGRITY_FAILURE, UNAUTHORIZED_RECOVERY, ROLLBACK_DETECTED, CONFLICT_DETECTED, QUARANTINED, RECOVERY_FAILED.

Protect against replay, rollback, identity substitution, corruption, invalid chronology, and incompatible versions.

## 52. Continuity vs Recovery

Synchronization continuity preserves the current operational state through manifest hash, propagation, and threshold. Recovery restores trustworthy state from backup, identity, history, integrity evidence, and reconciliation.

Temporary propagation-node loss is not automatically a recovery disaster.

## 53. Current State vs History

Merkle Root + Block Hash + Propagation Chain primarily preserve compact evidence of current state and recent synchronization transitions. Historical storage and recovery belong to history, backup, recovery, and SREC.

## 54. Operational Continuity

```text
VALID CURRENT STATE + SYNCHRONIZATION EVIDENCE
+ THRESHOLD REACHED + NO CONFLICT
→ CONTINUE
```

Chain Poker Genesis can use this to continue its state machine without treating every partial infrastructure failure as a full recovery event.

## 55. Failure Testing

At minimum test power loss, local/Kubo/IPFS interruption, corruption, USB removal, external-storage outage, encryption/upload interruption, manifest conflict, invalid signature, broken parent, divergent CID, missing anchor, rollback, concurrent modification, propagation interruption, threshold failure, invalid/duplicate/stale peer evidence, broken chains, Merkle mismatch, leaf-order mismatch, block mismatch, checkpoint replay/rollback/missing/corruption.

For 3-of-5: test loss of one or two constructing nodes, loss of one or both compact-evidence receivers, operational-set changes, repeated/duplicate/out-of-sequence blocks, wrong Merkle Root, metadata mismatch, and incorrect previous_block_hash.

For PoF: test unavailable functions, invalid results, missing/replayed evidence, wrong signatures, state inconsistency, partial PoF, timeout, rollback, stale protocol version, incomplete five-node genesis PoF, and loss of required functionality on one or multiple genesis nodes.

## 56. Propagation Integrity Rules

Evidence should verify, when applicable:

```text
NODE_ID
MANIFEST_HASH
VERSION
SIGNATURE
PROVENANCE
TIMESTAMP
PREVIOUS_REFERENCE
```

Equivalent evidence must not be counted twice. Reject stale, invalid, replayed, unrelated, unsigned, or incorrectly attributed evidence when required by policy.

## 57. Capacity and Saturation

Propagation may adapt to node activity, role, capacity, latency, connectivity, and availability. Full hash propagation may be restricted to relevant nodes, while Merkle Root and Block Hash provide compact evidence to nodes that do not require full data.

## 58. Separation Between Evidence and Data

```text
LEVEL 1 — DATA
FULL MANIFEST

LEVEL 2 — INDIVIDUAL EVIDENCE
MANIFEST HASH

LEVEL 3 — AGGREGATED EVIDENCE
MERKLE ROOT

LEVEL 4 — BLOCK EVIDENCE
BLOCK HASH
```

PoF adds a functional layer:

```text
FUNCTION EXECUTION → FUNCTION RESULT → FUNCTION EVIDENCE → PoF RECORD
```

## 59. What Must NOT Be Interpreted

```text
BLOCK_HASH ≠ FULL BACKUP
BLOCK_HASH ≠ FULL STATE
BLOCK_HASH ≠ CONSENSUS
BLOCK_HASH ≠ AUTHORITY
BLOCK_HASH ≠ VALIDITY
BLOCK_HASH ≠ LATEST STATE
BLOCK_HASH ≠ ABSOLUTE IMMUTABILITY
POF ≠ CONSENSUS
POF ≠ PROOF OF WORK
POF ≠ AUTHORITY
POF ≠ BACKUP
POF ≠ SYNCHRONIZATION
```

## 60. Complete Conceptual Model

```text
NODE IDENTITY
      ↓
FULL MANIFEST
      ↓
MANIFEST HASH
      ↓
NODE-BOUND PROPAGATION
      ↓
PROPAGATION EVENTS
      ↓
VALIDATION / THRESHOLD
      ↓
SET OF MANIFEST HASHES
      ↓
MERKLE TREE
      ↓
MERKLE ROOT
      ↓
PROPAGATION BLOCK
      ↓
BLOCK HASH
     /   \
    ↓     ↓
EVIDENCE  CONTINUITY
PEERS     REFERENCE
```

In parallel:

```text
NODE FUNCTIONS → FUNCTION EXECUTION → FUNCTION EVIDENCE
→ PROOF OF FUNCTIONS → GENESIS / OPERATIONAL VERIFICATION
```

And independently:

```text
FULL MANIFEST → LOCAL STORAGE / IPFS-KUBO
FULL STATE → SREC → BACKUP → RECOVERY
```

## 61. Final Architectural Principle

Identity identifies who maintains state.

Manifest describes what the state is.

Manifest hash commits cryptographically to that state.

Propagation distributes evidence.

Sync threshold determines when sufficient propagation exists.

Merkle Root summarizes a set of propagated hashes.

Propagation Block organizes the set as a cryptographically linked unit.

Block Hash provides a compact reference to that block.

Backup Threshold defines independent redundancy.

SREC provides backup and recovery.

Proof of Functions demonstrates that defined node-protocol functions are operating and producing verifiable evidence.

Consensus Engine provides coordination/consensus when applicable.

Application consumes the infrastructure through its own state machine.

## 62. Operational Principle for Chain Poker Genesis

```text
CURRENT STATE
→ MANIFEST
→ MANIFEST_HASH
→ PROPAGATION
→ SYNCHRONIZATION THRESHOLD
→ SYNCHRONIZED
→ CONTINUE STATE MACHINE
→ NEW TRANSITION
→ NEW MANIFEST
```

The 3-of-5 mechanism is intended to allow partial node failure without automatically losing the cryptographic reference required for current-state continuity. Complete information remains subject to storage, distribution, backup, and recovery policies.

## 63. Definitive Architectural Rule

The node must answer:

```text
WHO? → node identity
WHAT STATE? → manifest
WHAT HASH? → manifest hash
WHERE? → storage locator
IS IT PROPAGATED? → propagation evidence
THRESHOLD? → sync threshold
WHAT BLOCK? → propagation block
WHAT COMMITMENT? → block hash
DO FUNCTIONAL PROOFS EXIST? → Proof of Functions
WHAT FUNCTIONS? → PoF evidence
IS THERE REDUNDANCY? → backup/evidence policy
HOW RECOVERED? → SREC
HOW COORDINATED? → consensus/application layer
```

Trust arises from a chain of verifiable evidence, not assumptions about location, availability, authority, or connectivity.

## 64. Proof of Functions — Architectural Position

```text
RED DE NODOS by LAEV
│
├── NODE IDENTITY
├── STORAGE
├── STATE MANIFEST
├── SYNCHRONIZATION
├── PROPAGATION
├── PROOF OF FUNCTIONS
│   ├── FUNCTION DEFINITION
│   ├── FUNCTION EXECUTION
│   ├── FUNCTION RESULT
│   ├── FUNCTION EVIDENCE
│   └── FUNCTION VERIFICATION
├── BACKUP / RECOVERY
├── CONSENSUS / COORDINATION
└── APPLICATION LAYER
```

PoF belongs to the protocol infrastructure layer. The initial network may establish Genesis Proof of Functions through five initial active nodes, provided required functions are executed and evidence is verified.

The subsequent 3-of-5 model may be used by policies requiring a five-node operational set.

## 65. Specification Status

```text
DOCUMENT
Red de Nodos by LAEV

VERSION
1.7

STATUS
ARCHITECTURAL SPECIFICATION

MAIN FOCUS
Identity
Storage
Manifest
Synchronization
Propagation
Current-State Continuity
Proof of Functions
Backup
Recovery
Reconciliation
Audit
Anchoring

KEY SYNCHRONIZATION MODEL
MANIFEST
→ MANIFEST HASH
→ PROPAGATION
→ THRESHOLD
→ MERKLE ROOT
→ PROPAGATION BLOCK
→ BLOCK HASH
→ CONTINUITY

KEY FUNCTIONAL MODEL
NODE FUNCTIONS
→ FUNCTION EXECUTION
→ FUNCTION EVIDENCE
→ PROOF OF FUNCTIONS

GENESIS FUNCTIONAL MODEL
5 INITIAL ACTIVE NODES
→ FUNCTIONAL VERIFICATION
→ GENESIS PROOF OF FUNCTIONS

REFERENCE THRESHOLD EXAMPLE
3 / 5

IMPORTANT
3 / 5 is a configurable protocol example,
not a universal security guarantee.

SEPARATION
Proof of Functions
≠ Synchronization
≠ Backup
≠ Recovery
≠ Consensus
≠ External Anchor
≠ Bitcoin Proof of Work
```

## Final Clarification

**Proof of Functions (PoF) is a protocol-level aspect of Red de Nodos by LAEV used to demonstrate the functionality of the node protocol itself. The initial five active nodes provide the initial functional infrastructure from which the Genesis Proof of Functions can be established. PoF is operational evidence; it is not Bitcoin Proof of Work, not consensus, and not a substitute for synchronization or backup.**

The **Merkle Root aggregates the manifest hashes participating in propagation; the resulting propagation block receives a BLOCK_HASH, which can be distributed as compact evidence to additional nodes. The immediate objective remains continuity of the current state, while complete backup and recovery remain separate systems.**

PoF is therefore incorporated as part of the protocol of **Red de Nodos by LAEV**, not as a property specific to Chain Poker Genesis.
