# FN-024A Node Data Networking / Transport Substrate — Minimum Specification

**Project:** Chain Poker Genesis by LAEV  
**Layer:** Full Node Core / Node Identity Core  
**Source:** Red de Nodos by LAEV V1.8 reconciliation  
**Status:** Architectural Definition — Implementation Pending

## Purpose

FN-024A defines the protocol-neutral data-networking substrate through which an Identity Node can establish and maintain data communication with another Identity Node.

It closes the architectural gap between the logical peer relationship represented by FN-024 and the actual transport of node data.

FN-024A does not install, infer, or activate Chain Poker Genesis.

## Architectural position

```text
Identity Node
    ↓
Peer Relationship
    ↓
FN-024A Data Networking / Transport
    ↓
Node Data Exchange
    ↓
Capability / Propagation / Synchronization layers
```

The transport substrate is part of the Node Identity Core.

## Minimum responsibilities

FN-024A must provide a protocol-neutral model for:

1. **Endpoint / Addressing** — a node may expose a transport endpoint associated with a peer relationship.
2. **Connection lifecycle** — a transport connection has explicit lifecycle state.
3. **Transport identity binding** — a transport session is associated with the intended local and remote Node identities.
4. **Data exchange** — the substrate provides a defined boundary for sending and receiving node data.
5. **Connectivity state** — the node can distinguish unavailable, connecting, connected and degraded transport conditions.
6. **Network conditions** — latency, availability and capacity/bandwidth are represented as network-policy inputs without becoming CPG semantics.
7. **Failure isolation** — transport failure must not corrupt the local Node Core state.
8. **Protocol neutrality** — the transport layer does not create Player Identity Nodes, Channel Nodes, CPG consensus, or settlement semantics.

## Minimum state model

The implementation must distinguish at least:

```text
UNAVAILABLE
    ↓
CONNECTING
    ↓
CONNECTED
    ↓
DEGRADED
    ↓
DISCONNECTED
```

A failed connection attempt must not be represented as a successful peer connection.

## Endpoint model

An endpoint is transport addressing information, not a Node Identity.

Therefore:

```text
Node Identity ≠ Node Instance ≠ Network Endpoint
```

Multiple endpoints may later represent the same Node Identity, and endpoint changes must not change the cryptographic Node Identity.

The minimum implementation may use an abstract endpoint reference. A concrete transport protocol is not selected by this specification.

## Internet / IP boundary

The Node Core must be capable of operating over an IP-based network, including LAN/WAN/Internet environments, but FN-024A does not yet mandate a specific transport stack such as TCP, UDP, QUIC, libp2p, or another implementation.

Those are implementation choices to be reconciled separately unless a later source specification makes one normative.

## Network conditions

The following are descriptive infrastructure properties:

- connectivity;
- availability;
- latency;
- capacity/bandwidth;
- connection state.

They may be used by later Node Core policy and propagation decisions.

They must not be interpreted as poker state, player state, consensus state, or settlement state.

## Security boundary

FN-024A binds transport communication to Node identities at the architectural level, but it does not define production private-key provisioning, key custody, certificate authority, or a complete transport-encryption protocol.

Production cryptographic key management remains FN-029.

## Relationship to storage networking

Kubo/IPFS networking is a decentralized storage integration and must not be treated as a substitute for the generic Identity Node transport substrate.

```text
Node Data Networking ≠ IPFS Storage Networking
```

Both may use the underlying Internet, but they have different responsibilities.

## Relationship to FN-025 and FN-026

```text
FN-024
Identity / Peer substrate
    ↓
FN-024A
Data Networking / Transport
    ↓
FN-025
Capability Discovery
    ↓
FN-026
Propagation / Peer Evidence
    ↓
FN-027
Proof of Functions
```

FN-025 may describe transport-related capabilities later, but capability evidence does not replace transport execution.

FN-026 may use FN-024A to exchange propagation data, but propagation semantics do not define transport.

## Explicit non-goals

FN-024A does not define:

- Player Identity Nodes;
- Channel Nodes;
- poker tables;
- table wallets;
- CPG consensus;
- CPG settlement;
- Lightning settlement;
- protocol-specific messages;
- application-specific wire formats;
- production cryptographic key provisioning.

## Completion condition

FN-024A may only become VERIFIED after:

1. the specification is implemented;
2. automated tests cover endpoint identity separation, connection lifecycle, data exchange boundary, failure behavior and deterministic state representation;
3. GitHub Actions verifies the implementation;
4. the implementation remains protocol-neutral;
5. the result is reconciled with the historical Node architecture.

Until then its status remains SOURCE_RECONCILIATION_REQUIRED / implementation pending.
