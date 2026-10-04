# Kubo Failure and Recovery

Kubo failure does not make Node Core Storage unavailable. Local storage remains the fallback read/write authority while the decentralized provider is degraded.

## Failure

`HEALTHY` → `DEGRADED`

The provider is marked unhealthy when local Kubo RPC health fails. The local storage path remains usable.

## Recovery

`DEGRADED` → `STARTING` → `HEALTHY` → `RECONCILIATION` → `COHERENCE` → `READY`

Recovery never jumps directly from process start to READY.

Before READY:
1. Kubo must answer health checks.
2. Registry-backed reconciliation must complete without conflicts.
3. Local/Kubo coherence must pass.
4. Only then may the provider state return to READY.

Conflicts stop recovery and remain explicit. No blind overwrite is performed.

## Boundary

Kubo recovery manages the provider lifecycle. Storage Recovery manages individual object restoration. Node Core Configuration records the resulting allowed state; it does not administer the Kubo process.