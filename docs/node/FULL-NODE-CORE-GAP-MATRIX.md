# Full Node Core Gap Matrix

**Project:** Chain Poker Genesis by LAEV  
**Authority:** `FULL-NODE-CORE-MASTER-SPECIFICATION.md`  
**Purpose:** Requirement-by-requirement implementation gate for the Full Node Core.

## Status Vocabulary

- `VERIFIED` — implemented, tested, and CI-verified.
- `IN_PROGRESS` — implementation has started but the completion gate is not yet satisfied.
- `NOT_IMPLEMENTED` — required but no sufficient implementation exists.
- `BOUNDARY` — intentionally outside Node Core and prohibited at this phase.
- `SOURCE_RECONCILIATION_REQUIRED` — historical source still requires direct requirement mapping.

| ID | Requirement | Source family | Current state | Target evidence | Status |
|---|---|---|---|---|---|
| FN-001 | Environment/bootstrap validation | Node installation | Local bootstrap verified | CI | VERIFIED |
| FN-002 | Node identity initialization | Node Core | Local identity verified | CI | VERIFIED |
| FN-003 | Cryptographic namespace/boundary | Node Core/Security | Boundary verified; production key provisioning separate | CI + security audit | VERIFIED |
| FN-004 | Canonical local storage structure | Dual-storage bootstrap | Local structure verified | CI | VERIFIED |
| FN-005 | Local Storage Manager | Storage infrastructure | Implemented and tested | CI | VERIFIED |
| FN-006 | Object Registry | Storage infrastructure | Implemented and tested | CI | VERIFIED |
| FN-007 | Storage Locator | Storage infrastructure | Implemented and tested | CI | VERIFIED |
| FN-008 | Local coherence/integrity | Storage infrastructure | Implemented and tested | CI | VERIFIED |
| FN-009 | Installation manifest | Node installation | Implemented and tested | CI | VERIFIED |
| FN-010 | Runtime lifecycle | Node Core | Implemented and tested | CI | VERIFIED |
| FN-011 | Health/readiness | Node Core | Implemented and tested | CI | VERIFIED |
| FN-012 | Recovery | Node Core | Implemented and tested | CI | VERIFIED |
| FN-013 | Protocol isolation | Node/CPG boundary | Implemented and tested | CI | VERIFIED |
| FN-014 | IPFS/Kubo operational adapter | Dual-storage/storage infrastructure | Adapter implemented and live Kubo v0.43.1 CI-verified | adapter tests + CI | VERIFIED |
| FN-015 | IPFS/Kubo logical canonical namespace | Dual-storage bootstrap | Namespace initialization/verification implemented and live Kubo v0.43.1 CI-verified | bootstrap test + CI | VERIFIED |
| FN-016 | Dual-storage structural verification | Dual-storage bootstrap | Local + Kubo structural paths implemented and live Kubo CI-verified | cross-domain test + CI | VERIFIED |
| FN-017 | Canonical storage manifest across both domains | Dual-storage bootstrap | Deterministic local manifest + Kubo reconciliation implemented and CI-verified | deterministic cross-storage test + CI | VERIFIED |
| FN-018 | Local/IPFS synchronization engine | Dual-storage/storage infrastructure | Registered-object synchronization, content-hash verification, persistent distributed evidence, and multi-object reconciliation implemented and CI-verified | integration test + CI | VERIFIED |
| FN-019 | Conflict detection | Storage infrastructure | Divergence detection, CONFLICT state persistence, and no-overwrite regression test implemented and CI-verified | conflict test + CI | VERIFIED |
| FN-020 | Durable synchronization queue | Storage infrastructure | Durable local queue, restart recovery, pending resumption, and completion persistence implemented and CI-verified | queue/restart test + CI | VERIFIED |
| FN-021 | Retry/backoff/circuit-breaker behavior | Storage infrastructure | Retry/backoff, failure threshold, circuit open/half-open recovery, and durable queue return-to-pending implemented and CI-verified | failure-injection test + CI | VERIFIED |
| FN-022 | Storage Policy Engine | Storage infrastructure | Minimal policy decision layer reconciled to the storage specification, implemented for canonical storage classes, and CI-verified | policy tests + CI | VERIFIED |
| FN-023 | Replication policy | Storage infrastructure | Not demonstrated | replication tests + CI | NOT_IMPLEMENTED |
| FN-024 | Node networking substrate | Node architecture | Not demonstrated | node-network tests + CI | NOT_IMPLEMENTED |
| FN-025 | Capability discovery | Red de Nodos | Not demonstrated | capability evidence + CI | NOT_IMPLEMENTED |
| FN-026 | Propagation/peer evidence | Red de Nodos | Not demonstrated | propagation tests + CI | NOT_IMPLEMENTED |
| FN-027 | Proof of Functions | Red de Nodos | Not demonstrated | PoF generation/verification + CI | NOT_IMPLEMENTED |
| FN-028 | Remote installation synchronization | Installation Engine | Historical requirement; scope must be reconciled | source mapping + integration test | SOURCE_RECONCILIATION_REQUIRED |
| FN-029 | Production cryptographic key management | Security architecture | Separate/open | security implementation + CI | SOURCE_RECONCILIATION_REQUIRED |
| FN-030 | Historical PDF requirements | Historical sources | PDFs identified but not fully reconciled | requirement mapping | SOURCE_RECONCILIATION_REQUIRED |
| FN-031 | CPG protocol installation | CPG boundary | Explicitly prohibited in Node Core | isolation test | BOUNDARY |
| FN-032 | CPG Dedicated Ledger | CPG protocol | Explicitly outside Node Core | architecture boundary | BOUNDARY |
| FN-033 | CPG consensus/settlement | CPG protocol | Explicitly outside Node Core | architecture boundary | BOUNDARY |

## Current Gap Concentration

The highest-priority remaining implementation gap is the **synchronization reliability layer**:

```text
LOCAL STORAGE
    ↓
IPFS/KUBO ADAPTER
    ↓
CANONICAL IPFS NAMESPACE
    ↓
CROSS-STORAGE STRUCTURAL VERIFICATION
    ↓
MANIFEST RECONCILIATION
    ↓
SYNCHRONIZATION
    ↓
STORAGE_READY
```

The current branch implements manifest synchronization, registered-object Local ↔ Kubo synchronization, content-hash verification, CID evidence, persistent distributed evidence, multi-object reconciliation, conservative divergence detection, and a durable local synchronization queue with restart recovery. A divergent distributed object is recorded as CONFLICT rather than overwritten. This does **not** claim conflict resolution policies that choose a winner or distributed replication. Retry/backoff/circuit-breaker reliability is now separately implemented and CI-verified.

The following layers depend on that foundation:

1. conflict detection;
2. synchronization queues;
3. policy engine;
5. replication;
6. network substrate;
7. capability discovery;
8. propagation evidence;
9. Proof of Functions.

## Completion Rule

`FULL_NODE_CORE_COMPLETE` is blocked while any mandatory row is `IN_PROGRESS`, `NOT_IMPLEMENTED`, `SOURCE_RECONCILIATION_REQUIRED`, or `UNRESOLVED`.

The only permitted non-complete rows at the Full Node Core gate are explicitly classified `BOUNDARY`.
