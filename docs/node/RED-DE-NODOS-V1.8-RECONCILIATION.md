# Red de Nodos by LAEV V1.8 — Historical Reconciliation

**Project:** Chain Poker Genesis by LAEV  
**Layer:** Full Node Core / Red de Nodos infrastructure  
**Status:** Historical source recovered; minimum FN-024 scope derived  
**Authority:** Exact V1.8 source recovered from commit `4a99738de06fd3fee7952391fcb382c5053bb566`

## 1. Exact source recovery

The repository contains the V1.8 specification at the historical path:

`docs/developer-specifications/node-infrastructure/Unified Specification — Red de Nodos by LAEV — V1.7.md`

At commit `4a99738de06fd3fee7952391fcb382c5053bb566`, the file content itself declares **Version 1.8** and **Status: Architectural Specification — Path-Difficulty PoF Extension**.

The preceding commit `3a8843f39e5a3c40022e911e85f89af91f91d769` created the document as Version 1.7. Commit `4a99738de06fd3fee7952391fcb382c5053bb566` changes the document body from Version 1.7 to Version 1.8 and adds the Path-Based Proof of Function extension.

**Historical conclusion:** the exact V1.8 source is recovered. The filename was not renamed during that historical transition, so the repository currently contains a **filename/version discrepancy**: filename V1.7, document content V1.8. This reconciliation records that discrepancy rather than silently rewriting history.

## 2. Complete section inventory

| Section | Historical subject | Classification for Full Node Core |
|---|---|---|
| 1 | Purpose | FOUNDATIONAL |
| 2 | Fundamental State Principle | NODE CORE |
| 3 | Proof of Functions | FUTURE FN-027 |
| 4 | Cryptographic Identity | FN-024 FOUNDATION / FN-029 KEY MANAGEMENT |
| 5 | Node Bootstrap | VERIFIED FN-001/FN-002 |
| 6 | General Storage Architecture | VERIFIED STORAGE FOUNDATION |
| 7 | Local Storage | VERIFIED STORAGE FOUNDATION |
| 8 | Module Isolation | STORAGE |
| 9 | Identity and Reputation | NODE CORE / FUTURE REPUTATION |
| 10 | Kubo/IPFS Integration | VERIFIED FN-014/FN-015 |
| 11 | Distributed Policies | VERIFIED STORAGE POLICY / REPLICATION |
| 12 | Storage API | VERIFIED STORAGE FOUNDATION |
| 13 | Storage Address Manifest / Storage Locator | VERIFIED FN-007 |
| 14 | Executable Artifacts | FUTURE / EXECUTION POLICY |
| 15 | Complete State Manifest | VERIFIED MANIFEST FOUNDATION |
| 16 | Manifest and Propagation | FN-026 |
| 17 | Synchronization State | VERIFIED STORAGE; NETWORK EXTENSION FN-026 |
| 18 | Storage Coherence vs Network Synchronization | ARCHITECTURAL SEPARATION |
| 19 | Synchronization Threshold | FN-026 / FUTURE PROPAGATION POLICY |
| 20 | Propagation Roles | FN-026 |
| 21 | Node Activity | FN-024/FN-026 POLICY INPUT |
| 22 | Propagation Chain | FN-026 |
| 23 | Two Different Chains | ARCHITECTURAL SEPARATION |
| 24 | Current-State Propagation Block | FUTURE FN-026 |
| 25 | Merkle Tree Construction | FUTURE PROPAGATION EVIDENCE |
| 26 | Propagation Block | FUTURE FN-026 |
| 27 | Block Hash | FUTURE FN-026 |
| 28 | 3-of-5 Propagation | FUTURE FN-026 |
| 29 | Asymmetric Distribution | FUTURE FN-026 |
| 30 | Continuity Under Node Failure | FN-026/FUTURE RECOVERY |
| 31 | Chain Poker Genesis Application | CPG BOUNDARY |
| 32 | Meaning of SYNCHRONIZED | FN-026 |
| 33 | Meaning of BACKED_UP | BACKUP POLICY |
| 34 | Evidence Backup vs State Backup | ARCHITECTURAL SEPARATION |
| 35 | Merkle Proof | FUTURE FN-026 |
| 36 | Synchronization Checkpoint | FUTURE FN-026 |
| 37 | Checkpoint Chain | FUTURE FN-026 |
| 38 | Merkle Root Determinism | FUTURE FN-026 |
| 39 | External State Anchor | FUTURE / ANCHORING |
| 40 | Storage State Machine | VERIFIED STORAGE |
| 41 | Synchronization Registry | VERIFIED STORAGE / FUTURE NETWORK EXTENSION |
| 42 | Journal and Consistency | VERIFIED STORAGE PRINCIPLE |
| 43 | Concurrency | VERIFIED STORAGE PRINCIPLE |
| 44 | Reconciliation | VERIFIED STORAGE / FUTURE PEER RECONCILIATION |
| 45 | Conflicts | VERIFIED LOCAL/DISTRIBUTED CONFLICT BASELINE |
| 46 | Audit | VERIFIED NODE CORE AUDIT FOUNDATION |
| 47 | SREC | FUTURE BACKUP/RECOVERY EXTENSION |
| 48 | Recovery Package | FUTURE BACKUP/RECOVERY EXTENSION |
| 49 | Backup Encryption | FN-029 / RECOVERY SECURITY |
| 50 | Recovery Principles | VERIFIED RECOVERY BASELINE / FUTURE REMOTE RECOVERY |
| 51 | Recovery Failures | RECOVERY |
| 52 | Continuity vs Recovery | ARCHITECTURAL SEPARATION |
| 53 | Current State vs History | ARCHITECTURAL SEPARATION |
| 54 | Operational Continuity | FN-026 / RECOVERY |
| 55 | Failure Testing | CI REQUIREMENTS BY LAYER |
| 56 | Propagation Integrity Rules | FN-026 |
| 57 | Capacity and Saturation | FN-024/FN-026 POLICY INPUT |
| 58 | Separation Between Evidence and Data | ARCHITECTURAL SEPARATION |
| 59 | What Must NOT Be Interpreted | ARCHITECTURAL GUARDRAILS |
| 60 | Complete Conceptual Model | ARCHITECTURAL MODEL |
| 61 | Final Architectural Principle | ARCHITECTURAL MODEL |
| 62 | Operational Principle for Chain Poker Genesis | CPG BOUNDARY / APPLICATION |
| 63 | Definitive Architectural Rule | NODE CORE + FUTURE LAYERS |
| 64 | Proof of Functions — Architectural Position | FUTURE FN-027 |
| 65 | Specification Status | SOURCE METADATA |

## 3. Historical networking requirements extracted from V1.8

The minimum network substrate is not a poker network and does not install CPG.

V1.8 explicitly establishes:

- **Node Identity** is a logical cryptographic identity distinct from a concrete **Node Instance**.
- Node identity must exist before the node reaches operational readiness.
- Propagation records have a source node and destination node.
- Node activity, connectivity, availability, capacity and latency are relevant network-policy inputs.
- Network synchronization is distinct from storage coherence.
- Propagation evidence is cryptographically attributable to a node identity.
- Peer evidence is part of the synchronization model.
- The infrastructure supports nodes that can exist before application association.

These requirements justify the minimum FN-024 substrate:

1. represent a protocol-neutral Identity Node;
2. distinguish Node Identity from Node Instance;
3. register peer Identity Nodes;
4. represent peer relationship/connection state;
5. represent a network endpoint/reference without defining CPG semantics;
6. preserve the invariant that base Identity Nodes do not require CPG installation.

## 4. Classification boundary

### FN-024 — Node Networking Substrate

Allowed now:

- identity-node representation;
- node-instance reference;
- peer registry;
- endpoint/reference;
- connection lifecycle state;
- deterministic network snapshot;
- protocol-neutral operation.

Not allowed in FN-024:

- CPG installation;
- poker table/channel semantics;
- player semantics;
- CPG consensus;
- settlement;
- Lightning settlement implementation;
- propagation Merkle blocks;
- PoF generation;
- production private-key provisioning.

Those belong to later layers or explicit boundaries.

## 5. Relationship to the LAEV clarification

The current architectural clarification that networking begins with **cryptographic Identity Nodes**, followed by **Player Identity Nodes**, and that a **Channel Node** can represent a poker table with channel capabilities, is treated here as a design clarification to be reconciled against V1.8.

V1.8 confirms the base concept of cryptographically identifiable nodes and separates identity from application behavior, but it does **not** by itself define the complete Player Identity Node / Channel Node model or Lightning-compatible table-channel semantics.

Therefore those concepts must not be silently inserted into FN-024. They remain candidates for the later protocol/network reconciliation.

## 6. Result

`V1.8 → inventory → historical requirements → classification → minimum FN-024` is now complete.

The minimum FN-024 implementation is now CI-verified by Node Installation Baseline Validation #267 (run 36983968563). FN-025 capability discovery and FN-026 propagation remain closed until their own historical requirements are reconciled and independently implemented.


## 7. FN-025 / FN-026 historical reconciliation

The exact V1.8 source was checked directly at commit 4a99738de06fd3fee7952391fcb382c5053bb566, including sections 4, 15–30, 55–57 and 60–64.

### 7.1 Identity Node → Capability Discovery

V1.8 establishes the Node Identity as the cryptographic identity of the infrastructure node and explicitly separates it from the concrete Node Instance. V1.8 also describes node functions and distinguishes REQUIRED, OPTIONAL, CONDITIONAL and APPLICATION-SPECIFIC functions in the PoF model.

The later Node Core architectural boundary explicitly lists capability discovery as a Node Core responsibility.

Therefore FN-025 is correctly classified as a Node Core capability layer, but its minimum responsibility is:

Identity Node → discover/describe node capabilities → capability evidence

It must not yet become:

Identity Node → CPG Player

Capability discovery must describe what the node can do; it must not install or infer the CPG protocol.

### 7.2 Identity Node → Propagation / Peer Evidence

V1.8 explicitly requires node-bound propagation evidence:

NODE_ID + MANIFEST_VERSION + MANIFEST_HASH + SIGNATURE

and defines propagation records with:

propagation_event_id, previous_propagation_hash, node_id, manifest_hash, manifest_version, propagation_role, source_node, destination_node, timestamp, signature, provenance.

V1.8 also separates:

STORAGE COHERENCE ≠ NETWORK SYNCHRONIZATION

and requires peer evidence to be verified before reaching the synchronization threshold.

Therefore FN-026 is correctly classified as the network propagation/evidence layer above FN-024, using Identity Nodes as its cryptographic participants.

### 7.3 Correct dependency model

IDENTITY NODE
    ↓
NODE CAPABILITIES
    ↓
PEER RELATIONSHIPS
    ↓
NODE-BOUND PROPAGATION EVIDENCE
    ↓
SYNC THRESHOLD
    ↓
SYNCHRONIZED NODE STATE

The layers are distinct:

- FN-024: identity/network substrate.
- FN-025: capability description/discovery.
- FN-026: propagation, peer evidence and synchronization threshold.
- FN-027: Proof of Functions.
- Application/Protocol layer: application-specific semantics.

### 7.4 Placement of Player Identity Nodes

V1.8 does not define a Player Identity Node as a base networking node type.

The correct interpretation is therefore:

Identity Node + CPG protocol association + player capability/role → Player Identity Node

A Player Identity Node should remain an application/protocol specialization of an existing Identity Node, not a replacement for the base Identity Node and not a new infrastructure class inside FN-024.

This preserves the Node Core invariant:

A node provides the substrate. The protocol provides the semantics.

### 7.5 Placement of Channel Nodes

V1.8 does not define a poker Channel Node or Lightning-compatible table channel.

Therefore a Channel Node cannot be introduced as a historical V1.8 requirement of FN-024/FN-025/FN-026.

The architecture may later define:

Channel Node = Identity Node + CPG channel capability + table/channel state

and then determine the exact relationship between:

- channel identity;
- participating Player Identity Nodes;
- table state;
- consensus state;
- group table wallet;
- commitment state;
- settlement state;
- Bitcoin/Lightning settlement.

That is a later CPG protocol/channel specification and must not be silently inserted into the generic Red de Nodos networking substrate.

### 7.6 Historical conclusion

The requested chain is confirmed:

Identity Node
      ↓
Capability Discovery
      ↓
Propagation / Peer Evidence
      ↓
Synchronization Threshold

This is supported by the historical V1.8 architecture.

The Player Identity Node belongs after protocol association, and the Channel Node belongs after the protocol defines its channel/table semantics.

FN-025 and FN-026 therefore remain NOT_IMPLEMENTED until their minimum implementations are separately specified and CI-verified. No CPG player/channel semantics are opened by this reconciliation.


## 8. Node Data Networking / Internet Transport Reconciliation

The historical V1.8 source was reviewed specifically for the distinction between logical node networking and the transport of data between nodes.

### 8.1 What V1.8 explicitly defines

V1.8 defines or references the following network-relevant concepts:

- cryptographic Node Identity and concrete Node Instance;
- source and destination nodes in propagation records;
- peer evidence;
- connectivity;
- availability;
- capacity;
- latency;
- propagation paths;
- network synchronization as distinct from storage coherence;
- IPFS/Kubo as a distributed-storage/network integration path.

These establish that node-to-node distribution and network conditions are part of the infrastructure model.

### 8.2 What V1.8 does not define as a complete transport specification

The recovered V1.8 document does not provide a standalone normative data-transport specification for:

- IP addressing;
- network endpoint semantics beyond the generic endpoint/reference needed by the node substrate;
- TCP/UDP/QUIC or equivalent transport selection;
- connection/session framing;
- byte/message transport;
- LAN/WAN/Internet transport behavior;
- NAT traversal;
- firewall traversal;
- relay behavior;
- transport retry/timeout semantics;
- bandwidth measurement/management;
- transport-level encryption/session security;
- a concrete P2P transport stack.

Therefore the historical source supports the existence of the networking substrate, but does not justify claiming that the Internet/data-transport layer is already fully specified.

### 8.3 Important separation

The V1.8 storage path through Kubo/IPFS describes distributed storage networking. It must not be interpreted as the complete Node Identity data-network transport layer.

Likewise, STORAGE COHERENCE ≠ NETWORK SYNCHRONIZATION means that a storage adapter reaching the IPFS network does not, by itself, define the transport substrate used by Identity Nodes for protocol/network messages.

### 8.4 Architectural conclusion

The Full Node Core therefore requires an explicit Node Data Networking / Transport sublayer inside the Node Identity Core:

NODE IDENTITY CORE
├── Cryptographic Identity
├── Node Instance
├── Peer Networking
├── Endpoint / Addressing
├── Data Transport
├── Connection Lifecycle
├── Connectivity
├── Availability
├── Capacity / Bandwidth
└── Latency / Network State

The transport layer remains protocol-neutral. It must exist before CPG Player Identity or Channel semantics and must not install or infer Chain Poker Genesis.

### 8.5 Gap classification

This review identifies a previously unformalized Full Node Core requirement:

FN-024
Node networking substrate
        ↓
FN-024A
Node data networking / transport substrate
        ↓
FN-025
Capability discovery
        ↓
FN-026
Propagation / peer evidence

FN-024A is a specification/reconciliation gap at this stage. It is not implemented and must not be counted as verified merely because FN-024 peer relationships are verified.

This does not invalidate the FN-024 verification. It narrows the claim: FN-024 verifies the minimum logical Identity Node/peer substrate, while FN-024A covers the still-open data-transport layer.

### 8.6 Scope boundary

The following remain outside this generic transport layer:

- Player Identity Node semantics;
- Channel Node / poker table semantics;
- table wallet semantics;
- CPG consensus;
- CPG settlement;
- Lightning settlement logic.

Those may consume the Node Data Networking / Transport substrate later.


## 9. FN-025 → FN-026 Interface Reconciliation

FN-024A is now CI-verified and FN-025 is now CI-verified. Before FN-026 implementation, the interface between capability evidence, transport state and propagation evidence is explicitly fixed.

### 9.1 Capability evidence is not transport execution

FN-025 answers:

```text
"What does this Identity Node declare that its Node Core supports?"
```

FN-024A answers:

```text
"Can this Node Core represent and operate a transport session with a peer?"
```

Therefore:

```text
network.transport capability
        ≠
CONNECTED transport session
```

Capability evidence must not be used as proof that a remote peer is reachable or that a transport session is currently connected.

### 9.2 FN-026 dependency on transport

FN-026 may use a transport session to exchange propagation data, but propagation evidence is a separate object.

The minimum dependency chain is:

```text
Identity Node
    ↓
Peer Relationship
    ↓
Transport Session
    ↓
Data Exchange
    ↓
Propagation Record
    ↓
Peer Evidence
    ↓
Synchronization Threshold
```

A transport message is not automatically a propagation record.

A propagation record must carry the historical node-bound evidence required by V1.8.

### 9.3 Minimum propagation handoff

FN-026 must consume, at minimum:

- source Node Identity;
- destination Node Identity;
- transport/session context sufficient to identify the communication path;
- manifest version;
- manifest hash;
- propagation role;
- timestamp;
- signature;
- provenance;
- previous propagation hash where required by the propagation chain.

FN-026 must not derive CPG player, table, wallet, consensus or settlement semantics from this handoff.

### 9.4 Failure boundaries

Transport failure belongs to FN-024A.

Propagation validation failure belongs to FN-026.

Capability description belongs to FN-025.

Therefore a failed transport session must not become propagation evidence merely because a propagation attempt was initiated.

Likewise, valid capability evidence must not be treated as proof that propagation occurred.

### 9.5 Correct interface model

```text
FN-024
Identity / Peer
      │
      ▼
FN-024A
Transport / Data Exchange
      │
      ├──────────────┐
      ▼              │
FN-025              │
Capability           │
Evidence             │
      │              │
      └──────┬───────┘
             ▼
          FN-026
 Propagation / Peer Evidence
             │
             ▼
    Synchronization Threshold
```

FN-026 may inspect FN-025 capability evidence when propagation policy requires capability compatibility, but FN-026 must not assume that capability evidence proves transport connectivity.

### 9.6 Gate before FN-026 implementation

The interface is now considered architecturally reconciled. FN-026 may proceed to its own specification and implementation cycle, while retaining the following invariants:

1. transport remains protocol-neutral;
2. capability evidence remains descriptive;
3. propagation evidence remains cryptographically attributable to Node Identity;
4. storage coherence remains distinct from network synchronization;
5. CPG application semantics remain outside the generic Node Core propagation layer.

