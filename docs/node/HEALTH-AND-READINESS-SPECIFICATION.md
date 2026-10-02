# Node Core Health and Readiness Specification

**Project:** Chain Poker Genesis by LAEV
**Component:** Node Core
**Status:** Formal Specification

Health and readiness are separate runtime observations.

- Health describes the current operational condition.
- Readiness determines whether the Node Core may enter an operational state.
- Local coherence is not network synchronization.

## Required checks

1. Identity metadata.
2. Configuration metadata.
3. Storage structure.
4. Local storage provider.
5. Storage coherence.
6. Recovery metadata.
7. Protocol isolation.

A healthy baseline reports HEALTHY.

## Readiness gate

The gate is satisfied only when every required condition is true:

    Identity        READY
    Configuration   READY
    Storage         READY
    Provider        READY
    Coherence       COHERENT
    Recovery        READY
    Synchronization NOT_EVALUATED
    CPG             NOT_INSTALLED

If any required condition fails, readiness is NOT_READY.

Health or readiness MUST NOT report a protocol as installed, associated, active, or synchronized when the Node Core baseline does not contain that protocol.
