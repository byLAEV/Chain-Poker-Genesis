# Engine API

**Status:** SUPPORTING interface documentation

The canonical internal execution boundary is:
`Documentation/Interfaces/NODE-CORE-ENGINE-RUNTIME-CONTRACT.md`.

The Engine Runtime implementation is `Engine Runtime/engine_runtime.py`.

## Implemented baseline

- register
- unregister
- start
- stop
- snapshot

## API surface classification

The following operations may exist at the broader API boundary but are **not** part of the current canonical Engine Runtime baseline unless separately implemented and tested:

- discover
- describe
- initialize
- health
- capabilities
- invoke

Execution remains subordinate to Node Core Runtime and must not bypass Protocol Interface for protocol installation or activation.

CPG-specific ledger, table state, poker rules, Table Wallet, settlement, rake and consensus are outside this boundary.
