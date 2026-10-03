# Node Core API

## API Surface Specification

The Node Core API directory defines the stable interfaces through which Node Core subsystems and authorized higher-level protocols consume node infrastructure.

The APIs are contracts. They are not application implementations and must remain independent from CPG semantics.

## Required API surface

1. Node API
2. Node Manager API
3. Runtime API
4. Health / Readiness API
5. Recovery API
6. Configuration API
7. Identity API
8. Cryptography API
9. Time API
10. Storage API
11. Storage Provider API
12. Network API
13. Synchronization API
14. Consensus API
15. Proof of Function API
16. Evidence API
17. Engine API
18. Protocol API
19. Security API
20. Manifest API

## External provider APIs

External implementations are integrated through adapters rather than copied into Node Core:

- Kubo HTTP/RPC API — IPFS/Kubo
- libp2p APIs — networking provider
- GPGME API — GnuPG provider where selected
- OpenPGP.js API — OpenPGP provider where selected

Node Core owns the adapter contract and security boundary.

## API rule

A higher-level protocol must use Node Core APIs instead of writing directly to private subsystem storage or implementation internals.

## Dependency direction

~~~text
Higher-Level Protocol
        ↓
Protocol API
        ↓
Node Core APIs
        ↓
Node Core Subsystems
        ↓
External Provider Adapters
~~~

CPG must not become a dependency of these APIs.
