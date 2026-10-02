# System Component Matrix

**Status:** Working architectural matrix — derived from the current structured documentation layer and the historical PDF inventory.  
**Normative status:** Not yet normative. Any item marked `POR VERIFICAR` requires confirmation against the corresponding historical PDF before implementation.

## 1. Purpose

This matrix is the architectural bridge between the historical PDF corpus and the new structured repository.

The original PDFs remain historical source documents. This file does not replace them. Its purpose is to identify the principal components of Chain Poker Genesis by LAEV, define their provisional boundaries, and establish which relationships must be verified during the PDF audit.

## 2. Architectural boundaries

| Component | Primary responsibility | Must not absorb | Current status |
|---|---|---|---|
| Node | Networked operational representation of an identity; generic node services | CPG-specific poker rules, CPG ledger semantics | Structured |
| Node Manager | Control-plane management of identity, node configuration, protocols, engines, tables and verification workflows | Protocol state execution itself | Structured |
| Protocol | Defines CPG rules, state transitions, permissions and protocol-level coordination | Generic node infrastructure | Structured |
| Engine | Specialized implementation/specification unit used by the protocol | Generic node responsibilities unless explicitly specified | Structured |
| Integration layer | Contracts between Node, Protocol, Engines, Ledger, Consensus and other subsystems | Owning domain semantics | Structured |
| Ledger | CPG-specific recording, verification and replay of protocol history/state/accounting information | Generic-node identity or network services | Structured |
| Main Consensus | Network-level consensus boundary | Table-specific poker execution unless explicitly escalated | Structured |
| Table Consensus | Player/table-level agreement for a game state | Generic network governance | Structured |
| Security | Cross-cutting protection of identity, code, communications, engines and execution | Business logic ownership | Structured |
| Simulation | Deterministic model for validating architecture and failure behavior | Production execution | Planned |
| Schemas | Machine-readable contracts for states, events, engines, nodes and errors | Human narrative specification | Planned |
| Tests | Verification of implementation/specification behavior | Protocol definition itself | Planned |
| Standards | Interoperability and compatibility conventions | Runtime ownership | Planned |
| Archive | Preservation of historical source material | Current normative specification | Historical |

## 3. Core execution relationship

```text
INDIVIDUAL
    |
    v
NODE MANAGER
    |
    v
CRYPTOGRAPHIC IDENTITY
    |
    v
NODE / P2P NETWORK
    |
    v
SELECTED PROTOCOL
    |
    v
CHAIN POKER GENESIS
    |
    +--> ENGINES
    |
    +--> TABLE CONSENSUS
    |
    +--> CPG LEDGER
    |
    +--> SETTLEMENT
```

The generic Node is therefore treated as infrastructure capable of using a protocol. Chain Poker Genesis is the protocol being reconstructed in this repository.

## 4. Consensus boundary

The current architecture distinguishes two consensus scopes:

```text
NODE NETWORK
     |
     v
MAIN CONSENSUS
     |
     v
CPG PROTOCOL
     |
     v
TABLE CONSENSUS
```

The exact consensus algorithms, quorum rules, escalation conditions and conflict-selection rules remain **POR VERIFICAR** against the historical specifications.

## 5. Ledger boundary

The CPG Ledger is treated as protocol-specific infrastructure.

It records/verifies/replays protocol history and state-related information required by CPG. It is not currently defined as a generic requirement of every Node.

The exact ledger technology, persistence model, synchronization mechanism and relationship with external networks remain **POR VERIFICAR**.

Historical candidate source:
- `04. Private Off-Chain Ledger Engine_- Chain Poker Genesis by LAEV.pdf`

## 6. Engine families identified from the repository corpus

| Engine family | Historical source(s) | Architectural placement | Status |
|---|---|---|---|
| Installation | `1.0 INSTALLATION ENGINE - Chain Poker Genesis by LAEV .pdf` | `engines/installation/` | Source identified |
| Graphical Interface | `2.0 Graphical Interface Engine - Chain Poker Genesis by LAEV .pdf` | `engines/graphical-interface/` | Source identified |
| Ledger | `04. Private Off-Chain Ledger Engine_- Chain Poker Genesis by LAEV.pdf` | `ledger/` | Boundary established; semantics audit pending |
| Rake / Settlement | `5.0_Rake Engine and Monetary Settlement Flow_CPG.pdf` | `engines/rake/`, settlement integration | Source identified |
| Commitment / Reveal | `6.0 Commitment and Reveal Card Dealing Engine__.pdf` | `engines/commitment-reveal/` | Source identified |
| Table Creation | `7.0 Table Creation Engine_- CHAIN POKER GENESIS BY LAEV (peroqtdigo).pdf` | `engines/table-creation/` | Source identified |
| Table Join | `8.0 Table Join Engine_- CHAIN POKER GENESIS BY LAEV (peroqtdigo).pdf` | `engines/table-join/` | Source identified |
| Table Wallet | `9.0 Table Wallet Engine_- CHAIN POKER GENESIS BY LAEV (peroqtdigo).pdf` | `engines/table-wallet/` | Source identified |
| Disconnection | `10.0 Player Node Disconnection Management Engine__.pdf` | `engines/disconnection-management/` | Source identified |
| Protocol Documentation | `11.0 Protocol Documentation Engine__.pdf` | `engines/protocol-documentation/` | Source identified |
| Monetary Settlement | `12.0 Monetary Settlement Engine__.pdf` | `engines/monetary-settlement/` | Source identified |
| Requests / Permissions | `13.0 Motor de Solicitudes y Permisos (Request & Permission Engine)__.pdf` | `engines/request-permission/` | Source identified |
| P2P Conflict Resolution | `14.0 P2P Conflict Resolution Engine.pdf` | `engines/conflict-resolution/` | Source identified |
| Poker Rules | `15.0 Documento Formal Oficial del Motor de Reglas de Póker__.pdf` | `engines/poker-rules/` | Source identified |
| Dealer | `16.0 Dealer Engine (Crupier Engine)__.pdf` | `engines/dealer/` | Source identified |
| Reputation | `17.0 Reputation Engine_Chain Poker Genesis.pdf` | Node/CPG integration boundary | Source identified; placement audit pending |
| Protocol Adoption | `18.0 Protocol Adoption Engine.pdf` | `engines/protocol-adoption/` | Source identified |
| Multi-Domain Game Protocol | `21.0 Multi-Domain Game Protocol_.pdf` | `standards/multi-domain-game/` or protocol | Classification pending |
| Security Architecture | `22.0 Security Architecture Specification.pdf` | `security/architecture/` | Source identified |
| Basic Infrastructure Installation | `23.0 Basic Infrastructure Installation.pdf` | Node / installation architecture | Classification pending |
| Cryptographic Dealer Defense | `25. Cryptographic Defense of the Dealer.pdf` | `security/dealer-security/` | Source identified |
| Lightning Interpretation Layer | `27. Early Access Version Architecture- Lightning Network Interpretation Layer Without Off-Chain Ledger.pdf` | integration / external-network adapter | Classification pending |
| Engine Governance Layer | `28.0 Engine Governance Layer (EGL) — Engine of Engines__.pdf` | `engines/engine-governance/` | Source identified |
| Card Distribution / Dealer | `29. Motor de Repartición de Cartas y Motor de Crupier.pdf` | card dealing / dealer | Possible overlap requires audit |
| Table Permission Widget | `30. Table Permission Widget Specification.pdf` | permissions / interface | Classification pending |
| HanBot Widget | `31. HanBot Widget.pdf` | interface / optional tooling | Classification pending |
| Hash Paper | `32. Hash Paper Engine_Chain Poker Genesis.pdf` | `engines/hash-paper/` | Source identified |
| International Poker Table Standard | `33. International Poker Table Standard.pdf` | `standards/international-poker-table/` | Source identified |
| Engine Evolution | `34. Formal Specification of Engine Evolution.pdf` | architecture / lifecycle | Source identified |

## 7. Explicit overlaps requiring audit

The following are not treated as errors yet. They are audit targets:

1. Dealer functionality appears in both the Dealer Engine and the Card Distribution/Dealer document.
2. Monetary Settlement and Rake/Settlement documents may define overlapping settlement responsibilities.
3. Infrastructure Installation and Installation Engine may represent different layers or successive versions.
4. The two main CPG documents may represent different revisions, consolidations, or scopes.
5. Reputation may belong partly to generic Node infrastructure and partly to CPG protocol logic.
6. Lightning interpretation and Ledger documents may define alternative or successive settlement architectures.

No implementation decision should be made solely from filenames.

## 8. Historical source priority

Until the PDF audit is complete, the repository uses the following classification:

- **Historical source:** original PDF.
- **Structured working documentation:** Markdown under `docs/`.
- **Normative specification:** only after the relevant source material has been audited and contradictions resolved.
- **Implementation:** only after the specification and interfaces are sufficiently deterministic.
- **Simulation:** validation mechanism for detecting unresolved specification gaps before implementation.

This prevents a convenient Markdown interpretation from silently becoming a new protocol rule.

## 9. Required next audit

The next audit pass must resolve, in order:

1. Which of the two principal CPG documents is the canonical historical protocol source, or whether both represent distinct revisions/scopes.
2. Exact Node / Node Manager / Protocol boundary from the infrastructure documents.
3. Security and cryptographic assumptions.
4. Engine evolution and compatibility rules.
5. Ledger and settlement boundary.
6. Table consensus and conflict-resolution behavior.
7. Dealer / commitment / reveal / card-distribution interaction.
8. Permissions and table lifecycle.
9. Historical overlaps and superseded designs.

## 10. Source documents

The principal historical documents for this matrix are:

- `0.0 CHAIN POKER GENESIS__by LAEV__Digital Poker Protocol__.pdf`
- `CHAIN POKER GENESIS by LAEV.pdf`
- `23.0 Basic Infrastructure Installation.pdf`
- `22.0 Security Architecture Specification.pdf`
- `34.0 Formal Specification of Engine Evolution.pdf`
- `04. Private Off-Chain Ledger Engine_- Chain Poker Genesis by LAEV.pdf`

See `docs/PDF-MAPPING.md` for the complete historical PDF inventory and provisional mapping.

## 11. Audit status vocabulary

- `SOURCE IDENTIFIED` — historical document exists in the repository.
- `STRUCTURED` — architectural boundary has been represented in Markdown, but may still change after audit.
- `POR VERIFICAR` — source content has not yet been sufficiently confirmed.
- `CONFLICT` — two or more audited sources provide incompatible definitions.
- `SUPERSEDED` — historical design retained for provenance but replaced by a later documented design.
- `IMPLEMENTATION-READY` — deterministic enough to define implementation contracts.
- `IMPLEMENTED` — code exists.
- `VERIFIED` — implementation behavior has been tested against the applicable specification.

---

**Important:** This matrix deliberately does not introduce cryptographic algorithms, consensus algorithms, ledger technologies, fork semantics, or implementation languages that have not yet been established by the audited source material.
