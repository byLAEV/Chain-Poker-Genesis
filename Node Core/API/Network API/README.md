# Network API

**Status:** SUPPORTING / RECONCILED

The canonical Network authority is:
`Documentation/Interfaces/NODE-CORE-NETWORK-CONTRACT.md`.

## Implemented reference surface

- discoverPeers
- connectPeer
- disconnectPeer
- sendMessage
- propagate
- getNetworkState

The following remain declared/future unless separately implemented and tested:

- getPeerState
- receiveMessage
- getNetworkCapabilities

Network state is transport/network state. It MUST NOT be interpreted as Node Core readiness, Runtime state, protocol synchronization, or CPG consensus.

Network API carries Node Core transport envelopes only; application-specific poker semantics remain behind Protocol Interface.
