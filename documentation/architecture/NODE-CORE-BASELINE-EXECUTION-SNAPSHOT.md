# Node Core Baseline Execution Snapshot

## Purpose

Freeze the observable behavior of the existing Node Core reference implementation before any executable relocation.

## Baseline source

Repository branch:

`architecture/repository-structure-audit`

Current branch head:

`8cdfa38e9d3807b50e6298a474b20c855c0560be`

## Available CI evidence

Workflow:

`CPG Node Installation Baseline Validation`

Observed run:

- Run: #315
- Run ID: 37037624804
- Job: `verify-node-installation`

The run was not a clean baseline because the repository structure was being migrated at the time. The final audit failed on a stale documentation path:

`docs/node/NODE-CORE-INSTALLATION-MANIFEST.md`

This failure is structural, not evidence that the Node Core runtime behavior failed.

## Behavioral evidence captured before the failing integrity gate

### Bootstrap

```
status = VERIFIED
node_status = NODE_CORE_READY
cpg_protocol = NOT_INSTALLED
```

### Runtime lifecycle

```
status = BOOTSTRAPPED
node_status = NODE_CORE_READY
cpg_protocol = NOT_INSTALLED
runtime lifecycle tests: PASS
```

### Health / recovery

```
status = BOOTSTRAPPED
node_status = NODE_CORE_READY
cpg_protocol = NOT_INSTALLED
health/recovery tests: PASS
```

### End-to-end installation

```
e2e_status = PASS
node_core = READY
health = HEALTHY
recovery = VERIFIED
cpg_protocol = NOT_INSTALLED
coherence = COHERENT
network_synchronization = NOT_EVALUATED
external_provider = NOT_PROVISIONED
```

### Installation manifest

```
manifest_status = VALID
node_core = READY
cpg_protocol = NOT_INSTALLED
```

### Protocol boundary

The final audit reached:

```
status = VERIFIED
boundary_state = ARMED
protocol_associations = []
cpg_protocol = NOT_INSTALLED
synchronization = NOT_EVALUATED
```

## Baseline invariants

These values are now treated as migration invariants:

| Invariant | Expected |
|---|---|
| Node Core status | READY |
| Readiness | NODE_CORE_READY |
| Health | HEALTHY |
| Recovery | VERIFIED |
| Coherence | COHERENT |
| Synchronization | NOT_EVALUATED |
| External provider | NOT_PROVISIONED |
| Protocol associations | [] |
| CPG Protocol | NOT_INSTALLED |
| Installation manifest | VALID |
| Protocol boundary | ARMED |

## Important qualification

This snapshot is a **behavioral baseline**, not a claim that the current branch has a clean CI pass.

A clean validation run after the path-repair commits is required before executable relocation.

## Migration rule

After the executable move, the same invariants must be observed.

A difference in any invariant blocks the next structural migration until explained and reconciled.

## Sequence

```
BEHAVIORAL BASELINE CAPTURED
        ↓
CLEAN CURRENT-BRANCH VALIDATION
        ↓
EXECUTABLE MOVE
        ↓
REVALIDATE SAME INVARIANTS
        ↓
COMPARE
        ↓
ONLY THEN SUBDIVIDE NODE CORE
```

## Current gate

**MOVE GATE: CLOSED**

Reason: the behavioral baseline exists, but a clean validation of the current post-path-repair branch has not yet been established.
