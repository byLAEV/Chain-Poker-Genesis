# Kubo / IPFS Storage Provider

## Node Core Dual-Storage Integration

This directory defines the integration boundary between Node Core Storage and the upstream Kubo IPFS implementation.

Kubo is an external storage provider. Node Core does not become Kubo and does not duplicate Kubo's internal repository structure.

The dual-storage architecture is:

```text
                    NODE CORE STORAGE
                           |
                    Storage Manager
                           |
                  Provider Abstraction
                     /           \
                    /             \
             LOCAL PROVIDER     KUBO PROVIDER
                  |                  |
          Node Storage         Kubo Repository
                  |                  |
             Local Objects          CIDs
                  \                  /
                   \                /
                    Coherence / Policy
                           |
                     Node Core API
```

## Read policy

For content classified as dual/distributed:

1. Prefer the Kubo/IPFS provider when the object is available and its CID/integrity checks succeed.
2. If Kubo is unavailable, unreachable, or fails a permitted read, use the local Node Storage copy when available.
3. A local fallback does not silently redefine the canonical identity of content.
4. If both copies exist but disagree with the canonical content identifier or integrity metadata, the object enters a coherence/error state and is not silently overwritten.
5. Local-only objects do not require Kubo.
6. Kubo-only objects do not imply that a local mirror exists.

## Write policy

Writes are controlled by Storage Policy. Node Core must distinguish:

- LOCAL_ONLY
- DISTRIBUTED_ONLY
- DUAL
- TEMPORARY
- PUBLIC
- PRIVATE
- RESTRICTED
- PERSONAL
- ENCRYPTED_RESTRICTED

A DUAL write requires explicit provider operations and durable operation state. Provider failure must not silently convert a required DUAL write into LOCAL_ONLY.

## Kubo boundary

Kubo is accessed through its supported local API/RPC or another explicitly supported provider interface. The Node Core installer MUST NOT silently install Kubo merely because a protocol requests decentralized storage.

## Upstream

Official upstream repository: https://github.com/ipfs/kubo

Kubo is an IPFS implementation in Go providing content-addressed storage, CLI, HTTP Gateway and RPC API. Its current repository also contains datastore, networking, routing, Bitswap, configuration and daemon subsystems.

## Important security rule

Kubo's administrative RPC grants extensive control over the daemon. It must remain local or be protected by an explicit authorization boundary. Node Core must never expose an unprotected administrative Kubo RPC endpoint to LAN or the public Internet.

## Relationship to Node Core

Kubo owns its internal repository and implementation details.

Node Core owns:

- Storage API;
- Storage Manager;
- provider abstraction;
- storage policy;
- canonical object metadata;
- local mirror;
- coherence state;
- synchronization state;
- retry/recovery policy;
- authorization boundary;
- integration lifecycle.

Kubo owns:

- IPFS daemon implementation;
- Kubo repository;
- blockstore/datastore internals;
- Bitswap;
- libp2p integration;
- routing;
- gateway;
- Kubo RPC;
- Kubo CLI;
- Kubo-specific configuration.

Node Core must integrate these capabilities through an adapter rather than reimplementing them.
