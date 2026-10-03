# Kubo Upstream File and Component Map

This file records which upstream Kubo areas are relevant to the Node Core provider integration.

Official repository: https://github.com/ipfs/kubo

## Repository areas

| Upstream area | Node Core treatment |
|---|---|
| `.github/` | Upstream CI/community metadata; not part of Node Core |
| `cmd/` | Kubo CLI/daemon entry points; external provider |
| `commands/` | Kubo command implementation; accessed through adapter/API where required |
| `client/rpc/` | RPC client boundary; relevant to adapter |
| `config/` | Kubo configuration implementation; provider-owned |
| `blocks/` | Block handling; provider-owned |
| `core/` and daemon internals | Provider-owned |
| datastore implementation | Provider-owned |
| Bitswap | Provider-owned |
| libp2p integration | Provider-owned |
| routing | Provider-owned |
| gateway | Provider-owned |
| IPNS | Provider-owned |
| pinning | Provider capability consumed through policy |
| repository management | Provider-owned |
| metrics/monitoring | Provider-owned; selected telemetry may be consumed |
| docs/ | Upstream reference material |
| tests/ | Upstream provider tests |
| licenses | Must remain with any redistributed Kubo source |

## Important rule

“Complete Kubo integration” does not mean copying every upstream file into Node Core.

Kubo is a large independent implementation. Node Core integrates its stable provider surface.

If Kubo source is vendored in a future distribution, it must be kept in an explicitly isolated third-party subtree with its original licensing and attribution, pinned to an exact upstream release/commit, and never mixed into Node Core source ownership.

## Upstream capabilities to track

- CIDs/content addressing
- UnixFS
- DAGs
- blockstore
- datastore
- Bitswap
- libp2p
- peer discovery
- routing/delegated routing
- IPNS
- Gateway
- RPC
- CLI
- repository management
- pinning
- garbage collection
- metrics
- AutoConf
- AutoNAT
- FUSE
- content blocking

## Source of truth

The Kubo repository remains the source of truth for Kubo implementation behavior. Node Core documents the compatibility contract it depends upon.
