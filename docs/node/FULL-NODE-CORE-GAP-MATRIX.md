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
| FN-014 | IPFS/Kubo operational adapter | Dual-storage/storage infrastructure | No complete implementation evidence | adapter tests + CI | NOT_IMPLEMENTED |
| FN-015 | IPFS/Kubo logical canonical namespace | Dual-storage bootstrap | Specification exists; implementation pending | bootstrap test + CI | IN_PROGRESS |
| FN-016 | Dual-storage structural verification | Dual-storage bootstrap | Not implemented for live Kubo | cross-domain test + CI | NOT_IMPLEMENTED |
| FN-017 | Canonical storage manifest across both domains | Dual-storage bootstrap | Local manifest exists; cross-domain manifest pending | deterministic cross-storage test | NOT_IMPLEMENTED |
| FN-018 | Local/IPFS synchronization engine | Dual-storage/storage infrastructure | State model exists; live dual-domain synchronization pending | integration test + CI | NOT_IMPLEMENTED |
| FN-019 | Conflict detection | Storage infrastructure | Model documented; live dual-domain implementation pending | conflict test + CI | NOT_IMPLEMENTED |
| FN-020 | Durable synchronization queue | Storage infrastructure | Not demonstrated | queue/restart test + CI | NOT_IMPLEMENTED |
| FN-021 | Retry/backoff/circuit-breaker behavior | Storage infrastructure | Not demonstrated | failure-injection test + CI | NOT_IMPLEMENTED |
| FN-022 | Storage Policy Engine | Storage infrastructure | Not demonstrated | policy tests + CI | NOT_IMPLEMENTED |
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

The highest-priority implementation gap is the **dual-storage bootstrap**:

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

The following layers depend on that foundation:

1. synchronization queues;
2. policy engine;
3. replication;
4. network substrate;
5. capability discovery;
6. propagation evidence;
7. Proof of Functions.

## Completion Rule

`FULL_NODE_CORE_COMPLETE` is blocked while any mandatory row is `IN_PROGRESS`, `NOT_IMPLEMENTED`, `SOURCE_RECONCILIATION_REQUIRED`, or `UNRESOLVED`.

The only permitted non-complete rows at the Full Node Core gate are explicitly classified `BOUNDARY`.
