# Node Core API

**Status:** SUPPORTING / RECONCILED

The canonical API authority is:
`Documentation/Interfaces/NODE-CORE-API-CONTRACT.md`.

This directory contains supporting documentation for Node Core service domains. A documented operation is not automatically implemented.

## Canonical API domains

1. Node
2. Identity
3. Storage
4. Engines
5. Protocol Interface
6. Verification

These domains form the canonical Node Core API surface. Domain READMEs are supporting documentation and MUST NOT expand or contradict the canonical contract.

## Implementation availability

Current implementation availability is authoritative in:
`API/NODE-CORE-API-MANIFEST.json`.

The current reference facade is **IMPLEMENTED_PARTIAL** and exposes:
- `health()`
- `node_status()`
- `read(object_id)`

Other domain operations remain DECLARED or PARTIAL until implementation and tests establish availability.

## Dependency direction

Higher-Level Protocol
        ↓
Protocol Interface API
        ↓
Node Core API
        ↓
Node Core Subsystems
        ↓
External Provider Adapters

CPG-specific table state, poker rules, Table Wallet, settlement, rake, ledger and consensus are outside Node Core API semantics.

## External providers

External provider APIs are integrated through adapters. Node Core owns the adapter contract and security boundary; provider APIs do not become Node Core authorities.
