# Node Core Synchronization State Machine

Project: Chain Poker Genesis by LAEV
Layer: Node Core
Version: 0.1.0
Status: Implementation baseline

## Scope

This state machine describes synchronization of Node Core storage representations.

It is separate from communication, consensus, backup, recovery, and CPG protocol execution.

## States

```text
NOT_SYNCHRONIZED
      ↓
PROPAGATION_PENDING
      ↓
PROPAGATING
      ↓
THRESHOLD_NOT_REACHED
      ↓
THRESHOLD_REACHED
      ↓
SYNCHRONIZED
```

Failure states:

- SYNC_FAILED
- RETRY_WAIT
- CONFLICT
- QUARANTINED

## Baseline behavior

Node Core 0.1.0 does not claim network synchronization because no external provider is provisioned. The baseline reports `network_synchronization = NOT_EVALUATED`.

## Transition invariant

A transition must be caused by an explicit verification result. SYNCHRONIZED requires provider evidence and an applicable threshold. Conflicts are never resolved by silently selecting one version.