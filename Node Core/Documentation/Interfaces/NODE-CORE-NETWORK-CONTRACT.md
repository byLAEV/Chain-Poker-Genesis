# Node Core Network Contract

**Status:** CANONICAL
**Version:** 1.0.0
**Scope:** Protocol-neutral Node Core network boundary

## 1. Purpose

The Network subsystem provides the node-to-node communication boundary for Node Core.

It is infrastructure for peer registration, connection, framed messages, propagation and observation of network state. It is not a protocol consensus layer.

## 2. Canonical capabilities

- peer registration;
- deterministic peer state;
- transport;
- length-prefixed framing;
- Node Core handshake;
- Node Core message envelope;
- message propagation;
- network state observation;
- synchronization-state representation;
- retry/failure handling.

## 3. Peer state

The reference peer states are:

`DISCOVERED → CONNECTING → CONNECTED → DISCONNECTED / FAILED`

Invalid states MUST be rejected.

## 4. Transport boundary

The reference implementation uses a provider-neutral Network API with a TCP reference transport and deterministic length-prefixed JSON framing.

Production secure authenticated transport is a future provider requirement. The reference transport MUST NOT be interpreted as production-grade authenticated networking.

## 5. Node Core envelope

Network transport envelopes identify Node Core communication and contain sender, recipient and payload information.

Network transport MUST NOT require application-specific CPG message semantics.

## 6. Node Manager / Runtime boundary

Network is subordinate infrastructure.

Node Manager coordinates node lifecycle; Runtime determines Node Core readiness and lifecycle.

Network MUST NOT independently declare Node Core RUNNING, READY, RECOVERY or synchronized protocol state.

A network connection does not imply Node Core readiness.

## 7. Synchronization boundary

Communication is not synchronization.

Synchronization state is maintained separately under:

`Node Core/Network/Synchronization/synchronization_state.py`

The state `SYNCHRONIZED` requires both:

- provider readiness;
- threshold evidence.

Network connectivity alone MUST NOT produce `SYNCHRONIZED`.

## 8. Protocol isolation

Network MUST NOT implement:

- CPG consensus;
- CPG table state;
- CPG ledger;
- poker/NLHE rules;
- Table Wallet;
- settlement;
- rake;
- protocol-specific state transitions.

Network messages are transport envelopes. Protocol engines own application semantics after crossing the Protocol Interface boundary.

## 9. Security boundary

No private-key material belongs in Network.

Authenticated production channels, peer authorization and decentralized discovery remain separate security/provider concerns and are not falsely declared implemented by the reference transport.

## 10. Failure behavior

Unknown peers, invalid peer identifiers, invalid ports, disconnected sends and failed connections MUST fail explicitly.

Propagation MAY report per-peer failure without converting the entire Network subsystem into a consensus mechanism.

## 11. Verification

The canonical Network test suite MUST verify:

1. peer registration/state;
2. deterministic ordering;
3. connection lifecycle;
4. message envelope;
5. propagation;
6. deterministic framing;
7. synchronization gating;
8. protocol isolation.

Reference implementation:

`Node Core/Network/network_manager.py`

Reference manifest:

`Node Core/Network/NETWORK-CORE-MANIFEST.json`
