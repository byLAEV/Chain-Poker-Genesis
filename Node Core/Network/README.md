# Node Core Network

**Status:** SUPPORTING / RECONCILED
**Implementation:** IMPLEMENTED_PARTIAL
**Scope:** Protocol-neutral Node Core network boundary

The Network subsystem provides an executable provider-neutral boundary for peer registration, peer discovery, connection lifecycle, framed message exchange, propagation requests, and network state observation.

## Implemented reference boundary

- peer registry with explicit peer identifiers and endpoints;
- deterministic peer-state model;
- TCP reference transport using length-prefixed JSON frames;
- connect/disconnect lifecycle;
- send/receive message operations;
- propagation to registered peers;
- network state reporting without claiming Node Core readiness;
- synchronization-state integration without claiming global synchronization.

## Security boundary

The reference transport is an implementation baseline, not a production secure transport. Production deployments MUST place authenticated cryptographic channels and the selected external provider behind the same Network API boundary.

No private key material is handled by this subsystem.

## Protocol boundary

Network messages are transport envelopes only. CPG poker messages, table consensus, ledger semantics, and application-specific state transitions remain outside Node Core.

## Synchronization boundary

Network communication is not synchronization. Synchronization is represented separately by Network/Synchronization/synchronization_state.py and may only reach SYNCHRONIZED when its provider and threshold conditions are explicitly satisfied.

## Current status

IMPLEMENTED / PARTIAL means executable network behavior exists and is covered by deterministic local tests, while production-grade authenticated provider integration and live decentralized discovery remain pending.


## Authority

The canonical contract is `Documentation/Interfaces/NODE-CORE-NETWORK-CONTRACT.md`. The manifest is authoritative for implementation availability. This README is supporting documentation.

Network state such as `CONNECTED` is not Node Core `READY` or `RUNNING`.
