# Kubo Adapter

Purpose: translate the Node Core Storage Provider API into the selected Kubo HTTP/RPC operations.

Pinned upstream: Kubo v0.43.1 — 46a53f55dd670059c86b7315919cd2e01caa3113.

Node Core owns the provider-neutral contract; Kubo owns IPFS implementation semantics.

## Adapter boundary

Node Core: put/get/has/stat/remove/list/resolve/verify/health/capabilities.

Kubo mapping is version-pinned and must be tested before activation.

## Security

Administrative Kubo RPC must not be exposed publicly. Credentials and API endpoints belong in secure configuration, never in manifests or evidence.