# libp2p Adapter

Purpose: translate Node Core Network API operations into the selected libp2p provider.

Pinned reference: py-libp2p v0.6.0 — b09e3fae5cd1f121a63e266789c0fa6a67603fc1.

The adapter boundary covers peer identity, transport, secure channels, multiplexing, discovery and stream/message lifecycle required by Node Core.

Node Core does not expose provider internals as its public Network API.