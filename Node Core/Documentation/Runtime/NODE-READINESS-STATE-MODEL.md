# Node Readiness State Model

**Project:** Chain Poker Genesis by LAEV  
**Layer:** Node Core  
**Version:** 1.0.0  
**Status:** SUPPORTING / RECONCILED

## States

| State | Meaning |
|---|---|
| UNINITIALIZED | No valid Node Core bootstrap exists |
| ENVIRONMENT_VALIDATED | Installer environment passed validation |
| IDENTITY_INITIALIZED | Node identity metadata exists |
| STORAGE_INITIALIZED | Canonical local storage namespace exists |
| STORAGE_STRUCTURE_VERIFIED | Required structure has been verified |
| INTEGRITY_VERIFIED | Installation metadata passed integrity checks |
| RECOVERY_READY | Recovery metadata exists and is internally valid |
| NODE_CORE_READY | Node substrate is ready for later protocol association |

## Failure States

- ENVIRONMENT_INVALID
- IDENTITY_FAILED
- STORAGE_FAILED
- STRUCTURE_MISMATCH
- INTEGRITY_FAILED
- RECOVERY_FAILED
- MANIFEST_INVALID
- PROTOCOL_ISOLATION_FAILED

## Readiness Invariant

`NODE_CORE_READY` is valid only when all required predecessor checks pass.

## Protocol Isolation Invariant

`NODE_CORE_READY` does not imply protocol installation.

The expected state for the current baseline is:

```
NODE_CORE_READY
+
CPG_PROTOCOL = NOT_INSTALLED
+
PROTOCOL_ASSOCIATIONS = []
```

## Transition Rule

A transition may occur only when the output conditions of the current state are satisfied.

No transition may silently skip a required verification step.

## Future Extension

Future specifications may add:

- decentralized-storage readiness;
- peer-network readiness;
- remote synchronization readiness;
- cryptographic trust-anchor readiness.

Such states must not change the current meaning of `NODE_CORE_READY` without a versioned specification change.


**Authority:** `Documentation/Runtime/NODE-CORE-RUNTIME-LIFECYCLE.md`.

This document is a supporting state/readiness reference and does not define a second lifecycle vocabulary.
