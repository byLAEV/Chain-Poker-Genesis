# Engine 01→07 Integration Matrix

**Chain Poker Genesis by LAEV**
**Status:** Working architectural integration matrix
**Scope:** Engine 01 Installation, 02 Graphical Interface, 03 Cryptographic Connection, 04 Private Off-Chain Ledger, 05 Rake, 06 Commitment & Reveal Card Dealing, 07 Table Creation.

> This matrix is an integration control document. It does not silently convert unresolved historical wording into normative implementation rules.

## 1. Ownership rule

Every persistent or authoritative state must have exactly one domain owner. Other engines may request, validate, transform, consume, or record that state, but may not silently become its owner.

Evidence of a state is not ownership of that state.

## 2. Primary responsibility matrix

| Domain / State | 01 | 02 | 03 | 04 | 05 | 06 | 07 | Owner |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Installation state | **W** | R | R | | | | | 01 |
| UI state | | **W** | | | | | | 02 |
| Cryptographic identity/session | | R | **W** | R | | R | R | 03 |
| Table identity | | R | R | R | | | **W** | 07 |
| Table configuration | | R | R | R | | | **W** | 07 |
| Table lifecycle | | R | R | R | | | **W*** | 07 |
| Hand/game rules state | | R | R | R | | | R | Poker Rules Engine |
| Event history/evidence | | | R | **W** | R | R | R | 04 |
| Merkle consolidation | | | R | **W** | | | R | 04 |
| Bitcoin anchoring evidence | | | R | **W** | | | R | 04 |
| Rake policy/calculation | | R | R | R | **W** | | R | 05 |
| Monetary settlement | | | R | R | **R** | | R | Settlement Engine |
| Deck randomness | | | **R** | R | | R | R/selects | Dedicated Shuffle/Randomness architecture |
| Canonical deck state | | | R | R | | **W*** | R | Shuffle/Distribution Engine |
| Card commitment | | | R | R | | **W** | R | 06 |
| Card encryption/private payload | | | R | R | | **W** | | 06 / crypto subsystem |
| Reveal authorization | | | R | R | | R | | Request & Permission + Poker Rules |
| Reveal verification | | | R | **R** | | **W** | | 06 |
| Dealer consumption pointer | | | R | R | | R | R | Dealer Engine |
| Table wallet authority | | | R | R | R | | R | Settlement/Wallet subsystem |
| Engine selection/version context | | R | R | R | | R | **W** | 07 |
| Replay context | | | R | **W** | R | R | **W(context)** | Ledger + Table context |
| Audit trail | | | R | **W** | R | R | R | 04 |

**W = authoritative write/ownership. R = may read/use/validate. W* = creates/initializes or coordinates lifecycle, but later domain transitions remain subject to the owning protocol engine.**

## 3. What Engine 07 owns

Engine 07 owns the creation of the **table context**:

- table_id
- creation record
- canonical initial configuration
- configuration hash
- initial table-state hash
- selected compatible engine identifiers/versions
- table-scoped namespaces/references
- creation lifecycle transition

Engine 07 does **not** own:

- player private keys;
- player cards;
- deck randomness;
- poker rules;
- the private ledger;
- rake calculation;
- settlement;
- the dealer's consumption state;
- reveal authorization.

## 4. Critical integration contracts

### 4.1 Engine 07 ↔ Engine 03

07 asks 03 for canonical cryptographic primitives/identity services.

03 must not create a second table state.

### 4.2 Engine 07 ↔ Engine 04

07 emits table-creation evidence.

04 records, validates, indexes, consolidates, and supports replay of that evidence.

04 does not become the owner of the live table state.

### 4.3 Engine 07 ↔ Engine 06

07 establishes the table context and records which compatible card/commitment engine versions are selected.

06 creates and verifies commitments only after the relevant hand context exists.

06 cannot modify table configuration retroactively.

### 4.4 Engine 07 ↔ Shuffle/Distribution

07 may select/version the compatible implementation.

It must not itself generate the deck.

Two shuffle/distribution engines are available as alternatives. At table creation, exactly one is selected. Only the selected engine is authoritative for the table. The other does not participate unless a later table-consensus decision selects it.

### 4.5 Engine 07 ↔ Dealer

07 creates the table context.

Dealer consumes the canonical committed card state during a hand.

Dealer cannot create a competing deck.

### 4.6 Engine 07 ↔ Request & Permission

07 requests authorization for table creation/lifecycle operations.

Request & Permission validates communication and authorization; it does not become the owner of table state.

### 4.7 Engine 07 ↔ Wallet/Settlement

A table wallet is a financial component, not an implicit privilege of Table Creation.

Custody/spend authority must remain with the Settlement/Wallet architecture.

## 5. Contradictions detected in Engines 01→07

### C01 — Table wallet ownership

**Original risk:** Engine 07 could be interpreted as owning a custodial wallet.

**Resolution:** Table Creation creates or references the table-scoped wallet context only. Custody and spending authority belong to the financial subsystem.

**Status:** Resolved architecturally; exact wallet protocol remains open.

### C02 — Ledger versus table state

**Original risk:** Engine 04 could become a second owner of table state because it stores all events.

**Resolution:** Ledger stores evidence/history. Table state remains owned by the appropriate domain engine.

**Status:** Resolved.

### C03 — Signature versus encryption

**Original risk:** A wallet signature was described as if it made cards private.

**Resolution:** Signature = authorization/integrity. Encryption = confidentiality. Commitment = binding/integrity. Reveal = controlled disclosure.

**Status:** Resolved in Engine 06 boundary.

### C04 — Randomness versus commitment

**Original risk:** Engine 06 could implicitly become the randomness owner.

**Resolution:** randomness/deck generation belongs to the dedicated shuffle/randomness architecture; Engine 06 commits to and verifies the resulting private card state.

**Status:** Open until the two-engine shuffle design is formally specified.

### C05 — Two card engines

**Resolution:** Two compatible card engines are available, but they are alternatives. A table selects exactly one. There is no requirement for both to execute the same hand.

**Status:** Resolved architecturally; individual engine specifications remain open.

### C06 — Dealer versus randomness

**Original risk:** Dealer cut/burn language could make Dealer appear to generate randomness.

**Resolution:** Dealer executes authorized deterministic/state-derived consumption transitions. Any entropy used for cut/burn must originate from the designated randomness/shuffle architecture and be committed before execution where required.

**Status:** Requires reconciliation with the final Dealer + Shuffle specification.

### C07 — Request & Permission versus state ownership

**Original risk:** the intermediary could become an implicit global state machine.

**Resolution:** Request & Permission owns request lifecycle/authorization evidence, not domain state.

**Status:** Resolved architecturally.

### C08 — Replay versus live execution

**Original risk:** replay could accidentally execute engines instead of reconstructing historical state.

**Resolution:** replay consumes canonical events, versions, hashes and proofs. It must not mutate production state.

**Status:** Architectural rule established.

## 6. Canonical hand boundary

Before card commitments begin, the following must be fixed for a hand:

- table_id
- hand_id
- protocol version
- rules version
- active card-engine identifier and version
- commitment/reveal version
- dealer version
- canonicalization version
- randomness context
- participant set/order
- relevant table configuration hash

After this point, an engine cannot silently substitute another implementation.

## 7. Required future state machine

The integration audit requires the following conceptual boundary:

TABLE_CREATED
→ TABLE_CONFIGURED
→ TABLE_READY
→ HAND_INITIALIZED
→ RANDOMNESS_COMMITTED
→ DECK_CANONICALIZED
→ PLAYER_COMMITMENTS_COMPLETE
→ CARD_COMMITMENTS_COMPLETE
→ DEALING
→ COMMUNITY_REVEALS
→ SHOWDOWN
→ SETTLEMENT
→ HAND_CLOSED

The exact state machine must be reconciled with Poker Rules, Dealer, Settlement, Consensus, and Request & Permission specifications before implementation.

## 8. Audit result

**No Engine 01→07 should be permitted to silently own another engine's domain state.**

The two-engine architecture is now defined as a table-level selection mechanism. The remaining work is to specify Engine A and Engine B independently and define their common card-engine interface.

The next specification should define the two card engines independently before adding further game engines.
