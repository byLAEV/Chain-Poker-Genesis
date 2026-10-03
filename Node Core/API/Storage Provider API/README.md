# Storage Provider API

Defines the provider-neutral contract used by Storage Manager.

## Providers

- Local Provider
- Kubo/IPFS Provider
- Recovery Provider

## Contract

- put
- get
- has
- stat
- remove
- list
- resolve
- verify
- health
- capabilities
- version

Provider-specific behavior must remain behind the adapter.
