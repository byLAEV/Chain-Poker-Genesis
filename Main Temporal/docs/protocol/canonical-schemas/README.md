# Chain Poker Genesis — Canonical Schemas

**Status:** Working canonical schema layer
**Authority basis:** Audited repository specifications and the 01→07 integration baseline
**Normative status:** Provisional until canonical serialization and the integrated protocol state machine are accepted.

## Purpose
This directory defines the first machine-readable contract layer for Chain Poker Genesis by LAEV. The schemas are derived only from structures already established by the audited architecture.

## Initial canonical objects
| Schema | Domain | Basis |
|---|---|---|
| identity | Cryptographic identity | Cryptographic Connection Engine |
| node | Player/Genesis node | Cryptographic Connection + architecture |
| table | Table context | Table Creation Engine + 01→07 integration |
| participant | Player participation in one table | Table Join Engine |
| hand | Immutable hand execution context | 01→07 integration baseline |
| event | Canonical protocol evidence event | Private Off-Chain Ledger + integration baseline |

## Deliberate omissions
- Cryptographic algorithms and key derivation paths.
- Canonical serialization encoding.
- Consensus algorithm and quorum.
- Exact state-transition catalogue.
- Rake arithmetic and settlement fee rules.
- Dealer cut/burn algorithm.
- Internal implementation of card engines.

These remain separate specification tasks because the audit marks them as unresolved.

## Acceptance gate
These schemas become normative only after Canonical Serialization, Integrated State Machine, Cryptographic Profile, and Deterministic Test Vector specifications are accepted.

Version: 0.1.0
Revision: SCHEMA-FOUNDATION
Author: LAEV
Protocol: Chain Poker Genesis by LAEV