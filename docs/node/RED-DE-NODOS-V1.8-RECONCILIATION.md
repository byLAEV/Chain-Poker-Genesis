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

The next implementation artifact is intentionally limited to the protocol-neutral Identity Node networking substrate. FN-025 capability discovery and FN-026 propagation remain closed until FN-024 is independently implemented and CI-verified.
