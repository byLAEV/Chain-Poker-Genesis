# Repository Migration Matrix

This is the controlled migration matrix for the implementation-oriented repository tree. It is conservative: no artifact is deleted or moved until its role and references are reconciled.

| Current Path / Pattern | Type | Architectural Layer | Canonical Role | Target Path | Action | Dependency / Reference Impact |
|---|---|---|---|---|---|---|
| README.md | MD | Repository | Public project entry point | README.md | KEEP / UPDATE LATER | Must point to canonical layers |
| .github/ | DIR | Automation | CI/workflows | .github/ | KEEP | Validate paths after migration |
| IMPLEMENTATION-REVIEW/ | DIR | Implementation governance | Existing implementation audit material | documentation/implementation-review/ | MOVE LATER | Update links/workflow references |
| docs/ | DIR | Documentation | Existing general documentation | documentation/ | CONSOLIDATE | First inspect contents |
| engines/ | DIR | Protocol architecture | Engine index/current engine work | protocol-engines/ | CONSOLIDATE AFTER AUDIT | Reconcile with numbered engines |
| reference-implementation/ | DIR | Implementation | Reference implementation | implementation/reference/ | RENAME/MOVE | Preserve package/import paths |
| deterministic-manifest-based-node-and-protocol-storage-architecture/ | DIR | Node Core / Storage | Deterministic storage architecture | documentation/node-core/storage/ initially; implementation destination TBD | RECLASSIFY | Reconcile with Node Core canonical model |
| poker-table-viewer-creation-engine/ | DIR | Protocol/UI engine | Table viewer creation | protocol-engines/poker-table-viewer-creation/ | MOVE LATER | Preserve specification references |
| My Vision with CPG by LAEV/ | DIR | Provenance / vision | Original project vision material | historical/vision/ | MOVE LATER | Preserve provenance; do not treat as executable spec |
| decentralized-theories/ | DIR | Research / provenance | Supporting theories | documentation/research/decentralized-theories/ | MOVE LATER | Research references only |
| 04-private-off-chain-ledger-engine/ | DIR | Protocol Engine | Private off-chain ledger specification | protocol-engines/private-off-chain-ledger/ | RENAME/MOVE LATER | Update links |
| 05-rake-and-settlement-engine/ | DIR | Protocol Engine | Rake and settlement | protocol-engines/rake-and-settlement/ | RENAME/MOVE LATER | Update links |
| 06-commitment-reveal-card-dealing-engine/ | DIR | Protocol Engine | Commitment/reveal dealing | protocol-engines/commitment-reveal-card-dealing/ | RENAME/MOVE LATER | Update links |
| 07-dual-shuffle-card-distribution-engine/ | DIR | Protocol Engine | Dual shuffle distribution | protocol-engines/dual-shuffle-card-distribution/ | RENAME/MOVE LATER | Update links |
| 08-table-join-engine/ | DIR | Protocol Engine | Table joining | protocol-engines/table-join/ | RENAME/MOVE LATER | Update links |
| 09-table-wallet-engine/ | DIR | Protocol Engine | Table wallet | protocol-engines/table-wallet/ | RENAME/MOVE LATER | Update links |
| 10-player-node-disconnection-management-engine/ | DIR | Protocol Engine / Node boundary | Player/node disconnection handling | protocol-engines/player-node-disconnection/ pending boundary review | RECLASSIFY FIRST | May depend on Node Core recovery/state |
| 11-protocol-documentation-engine/ | DIR | Documentation infrastructure | Documentation generation/management | documentation/protocol-documentation/ | RECLASSIFY | Not a gameplay engine |
| 12-monetary-settlement-engine/ | DIR | Protocol Engine | Monetary settlement | protocol-engines/monetary-settlement/ | RENAME/MOVE LATER | Reconcile with rake/settlement |
| 13-request-and-permission-engine/ | DIR | Node Core / Protocol boundary | Requests and permissions | node-core/permissions/ or protocol engine pending audit | RECLASSIFY FIRST | Requires architectural boundary decision |
| 14-p2p-conflict-resolution-engine/ | DIR | Node Core / Networking | P2P conflict resolution | node-core/networking/conflict-resolution/ candidate | RECLASSIFY FIRST | Strong Node Core dependency |
| 15-poker-rules-engine/ | DIR | Protocol Engine | Poker rules | protocol-engines/poker-rules/ | RENAME/MOVE LATER | Independent of Node Core |
| Root-level numbered engine PDFs | PDF | Documentation artifact | Rendered specifications | documentation/engines/<engine>/specification.pdf | MOVE LATER | Update links; retain provenance |
| Root-level protocol PDFs | PDF | Documentation / provenance | Protocol-level rendered documents | documentation/protocol/ or historical/ after review | CLASSIFY FIRST | Some may be publications, others historical |
| CHAIN POKER GENESIS by LAEV.pdf | PDF | Protocol / provenance | Large consolidated project document | documentation/protocol/ candidate | CLASSIFY FIRST | Determine canonical status |
| 0.0 CHAIN POKER GENESIS...pdf | PDF | Protocol architecture | Original protocol document | documentation/protocol/ candidate | CLASSIFY FIRST | Preserve original provenance |
| Screenshot_20260712-165528_MetaMask.png | PNG | Evidence / documentation | Supporting visual artifact | documentation/assets/ | MOVE LATER | Update references |
| Root-level miscellaneous PDFs | PDF | Research / example | Supporting/example material | documentation/examples/ or historical/ | CLASSIFY FIRST | Must not enter canonical implementation path |

## Node Core candidates

These require explicit architectural reconciliation before placement: identity and cryptographic identity; key lifecycle; storage; deterministic manifest-based storage; state/event persistence; request/permission; P2P networking; conflict resolution; synchronization; disconnection/recovery; versioning.

## Protocol Engine candidates

These are clearly protocol-specific candidates unless detailed audit proves otherwise: poker rules; table join; table wallet; card dealing; dual shuffle; rake; monetary settlement; private off-chain ledger; viewer/table creation.

## Migration policy

1. No bulk moves yet.
2. No deletion based on filename similarity.
3. Preserve historical provenance.
4. Preserve canonical source before rendered PDFs.
5. Repair links only after target paths are approved.
6. Run validation after every migration batch.
7. Node Core placement requires architectural evidence, not naming alone.

## Next audit

Inspect the contents of engines/, reference-implementation/, docs/, IMPLEMENTATION-REVIEW/, and deterministic-manifest-based-node-and-protocol-storage-architecture/, then complete the root-PDF classification.