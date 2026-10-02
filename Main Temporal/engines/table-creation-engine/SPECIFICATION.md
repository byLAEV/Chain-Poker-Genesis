# Table Creation Engine

## Chain Poker Genesis by LAEV — Official Technical Specification v1.0

> Structured reconstruction of the historical Table Creation Engine specification. Normative implementation details remain subject to the 01→07 integration audit.

## 1. Purpose

The Table Creation Engine creates an isolated table context. A table is a cryptographically identifiable protocol object containing configuration, lifecycle state, participant context, engine selections, and references to its evidence records.

The engine creates the container and initial state of a table. It does not itself deal cards, determine poker outcomes, execute monetary settlement, or own the private ledger.

## 2. Genesis Table

The first protocol table is historically designated `Genesis Table #0`. Its provenance is recorded as part of protocol history. Later tables are independently identified table instances and do not inherit mutable state from another table.

## 3. Creation Output

A successful creation operation produces at minimum:

- `table_id`
- `creation_hash`
- `creation_timestamp`
- canonical configuration
- `configuration_hash`
- protocol/rules version identifiers
- initial table-state hash
- selected compatible engine identifiers and versions
- references/identifiers for the table evidence context
- initial lifecycle state

A table wallet, where required by the settlement architecture, is represented as a table-scoped financial component. Table Creation does not grant the engine custody authority over player funds.

## 4. Initial State

A newly created table enters `CREATED`.

`CREATED` means the table context exists, but no hand is active. Players, cards, hand funds, and active dealing state are created by subsequent authorized lifecycle transitions.

## 5. Configuration Immutability

Configuration affecting deterministic execution is canonicalized and committed at creation. Examples include:

- game variant;
- player capacity;
- blind/ante configuration;
- betting structure;
- currency/network context;
- applicable protocol/rules versions;
- compatible engine versions selected for the table.

A configuration change cannot silently alter an active hand. Any permitted future-table or lifecycle configuration change must produce a new explicit version/state transition.

## 6. Engine Selection

Table Creation is the boundary at which compatible versioned engines may be selected for a table, subject to protocol governance and compatibility rules.

For card generation/distribution, the table may select one authoritative shuffle/distribution implementation from the protocol's compatible set. If a second implementation is used as an independent verifier, its role and result must be recorded explicitly. Two engines must not create competing authoritative card states for the same hand.

The selected engine identifier and version become part of the canonical hand context before card commitments are finalized.

## 7. Cryptographic Identity

The table identity is derived from canonical creation data and includes:

`TABLE_ID + CREATION_HASH + CONFIGURATION_HASH + INITIAL_STATE_HASH`

The exact hash construction belongs to the Cryptographic Connection / canonicalization specification and must not be invented independently by this engine.

## 8. Lifecycle

Recommended lifecycle boundary:

`CREATED → CONFIGURED → READY → ACTIVE → PAUSED/SETTLEMENT → CLOSED`

The exact transition catalogue is subject to the Poker Rules, Permissions, and Settlement specifications. Table Creation owns creation; it does not own every later state transition.

## 9. Isolation

Each table has an independent namespace for:

- hand state;
- player participation;
- table-scoped evidence;
- engine selections;
- financial/session references;
- replay context.

An operation belonging to one table must not mutate another table's state.

## 10. Integration Boundaries

| Component | Table Creation relationship |
|---|---|
| Installation | provides the environment in which the engine can run |
| GUI | presents table-creation inputs; does not create authoritative state by itself |
| Cryptographic Connection | supplies canonical identity/hash primitives |
| Request & Permission | authorizes creation and lifecycle requests |
| Private Off-Chain Ledger | records creation/evidence events; does not own table state |
| Commitment & Reveal | operates after a table/hand context exists |
| Shuffle/Distribution | selected by table/hand context; performs card generation/distribution |
| Dealer | consumes the committed card state; does not create a competing deck |
| Poker Rules | defines game-phase semantics |
| Settlement/Rake | handles monetary operations according to their own specifications |

## 11. Security Invariants

1. `table_id` is unique within the protocol namespace.
2. Creation data is canonicalized before its cryptographic identity is finalized.
3. An unauthorized actor cannot create an authoritative table state.
4. A table cannot silently change its selected engine versions during an active hand.
5. Table Creation cannot inspect or expose private player cards merely because it created the table.
6. Table Creation cannot alter the card sequence after card commitments begin.
7. Evidence records identify the table context to which they belong.
8. Replay can reconstruct table creation from canonical creation inputs and recorded evidence.

## 12. Open Items Before Implementation

- Exact table wallet/custody semantics must be reconciled with Monetary Settlement.
- Exact Genesis Node authority must be reconciled with Permissions and Consensus.
- Exact engine-selection governance must be reconciled with Engine Evolution.
- Exact lifecycle transition catalogue must be reconciled with Poker Rules.
- Exact identity/hash construction must be inherited from the canonical cryptographic specification.

## 13. Historical Authorship

The historical source identifies the architecture as Chain Poker Genesis by LAEV (peroqtdigo) and attributes its architecture, concept, protocol, technical specifications, and system design to Lerry Alexander Elizondo Villalobos (LAEV — peroqtdigo).
