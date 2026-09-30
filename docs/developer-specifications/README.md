# Developer Specifications and Manuals

This directory contains the technical specifications and developer manuals for the **Chain Poker Genesis by LAEV** repository and the infrastructure layers that support it.

## Base structure

```text
docs/
└── developer-specifications/
    ├── README.md
    ├── storage/
    │   └── README.md
    ├── identity/
    ├── synchronization/
    ├── consensus/
    ├── recovery/
    ├── security/
    ├── engines/
    ├── APIs/
    ├── testing/
    └── integration/
```

Future directories will be introduced with their respective README manuals, keeping shared infrastructure separate from higher-level engines and applications.

## Architectural separation

```text
RED DE NODOS BY LAEV
        │
        ├── Storage Infrastructure
        ├── Cryptographic Identity
        ├── Identity Synchronization
        ├── SREC / Recovery
        └── Consensus Engine
                │
                ▼
        CHAIN POKER GENESIS
        ├── Poker Engines
        ├── Wallet Engines
        ├── Settlement Engines
        └── Application Components
```

The infrastructure specifications of the Red de Nodos by LAEV must remain independent from Chain Poker Genesis. Higher-level protocols and engines consume these capabilities through defined APIs and contracts.

## Documentation directories

- `storage/` — local storage, metadata, policies, synchronization, recovery, and Kubo/IPFS integration.
- `identity/` — node cryptographic identity.
- `synchronization/` — synchronization and distribution.
- `consensus/` — coordination and consensus between nodes.
- `recovery/` — recovery, continuity, and backups.
- `security/` — cross-cutting security.
- `engines/` — specifications for installable engines.
- `APIs/` — interface contracts between layers.
- `testing/` — tests and acceptance criteria.
- `integration/` — integration between infrastructure, engines, and applications.

## Status

This structure is the documentation baseline for developing formal specifications before implementing each component.
