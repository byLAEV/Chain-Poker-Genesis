# Node Core Installation Manifest

**Project:** Chain Poker Genesis by LAEV
**Component:** Node Core
**Status:** Canonical Installation Manifest Specification

## Purpose

The Node Core installation manifest is the machine-readable declaration of a successfully installed protocol-neutral Node Core.

It records identity, storage, provider, recovery, runtime, integrity, and protocol-isolation status.

## Mandatory Invariants

A valid Node Core installation manifest MUST declare:

- Node Core version.
- Manifest version.
- storage structure version.
- readiness state.
- integrity state.
- recovery state.
- provider state.
- synchronization state.
- empty protocol associations.
- CPG status as NOT_INSTALLED.

The manifest MUST NOT claim that local coherence is network synchronization.

## Canonical Baseline

    node_core.status           = READY
    readiness.state            = NODE_CORE_READY
    provider.status            = READY
    coherence.status           = COHERENT
    synchronization.state      = NOT_EVALUATED
    recovery.status            = READY
    integrity.status           = VERIFIED
    protocol_associations      = []
    cpg_protocol.status        = NOT_INSTALLED

## Scope

This manifest describes Node Core installation only. It is not a Chain Poker Genesis protocol manifest and it does not install or activate the protocol.
