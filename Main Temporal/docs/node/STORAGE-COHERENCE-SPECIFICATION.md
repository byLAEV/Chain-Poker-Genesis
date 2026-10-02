# Node Core Storage Coherence Specification

Project: Chain Poker Genesis by LAEV
Layer: Node Core
Version: 0.1.0
Status: Implementation baseline

## Purpose

Storage coherence determines whether the Node Core storage representation is internally consistent.

Storage coherence is distinct from network synchronization, backup, recovery, consensus, and protocol validity.

## Coherence conditions

A local Node Core storage state is COHERENT when:

- the canonical storage root exists;
- the storage manifest exists;
- every required canonical path exists;
- all managed metadata is readable;
- all declared object hashes verify;
- no object is outside its authorized class location.

The following are not required for local coherence:

- an IPFS/Kubo daemon;
- a remote peer;
- a CPG protocol installation;
- a network consensus state.

## Coherence states

- COHERENT
- MISSING_OBJECT
- HASH_MISMATCH
- STRUCTURE_MISMATCH
- INVALID_LOCATION
- PROVIDER_UNAVAILABLE

## Boundary

COHERENT means the Node Core can account for the state of its local storage substrate.

It does not mean SYNCHRONIZED, BACKED_UP, CONSENSUS_REACHED, or CPG_ACTIVE.

## Verification principle

The verifier must identify the exact failed condition instead of silently repairing the state.