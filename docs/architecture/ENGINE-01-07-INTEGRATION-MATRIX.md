# Engine 01→07 Consolidated Technical Integration Matrix

**Chain Poker Genesis by LAEV**  
**Status:** Consolidated architectural baseline — 01→07  
**Scope:** Engine 01 Installation, 02 Graphical Interface, 03 Cryptographic Connection, 04 Private Off-Chain Ledger, 05 Rake & Settlement Flow, 06 Commitment & Reveal, 07 Table Creation.  
**Supporting dependencies:** Dual Shuffle/Card Distribution, Dealer, Poker Rules, Request & Permission, Consensus, Wallet and Monetary Settlement are referenced where necessary but are not renumbered into 01→07 by this matrix.

> **Purpose:** This document is the integration authority for the 01→07 boundary. Historical engine wording that conflicts with this matrix is treated as historical/source material until its individual specification is corrected. The matrix does not silently invent cryptographic algorithms or implementation details that remain unspecified.

---

## 1. Canonical ownership principle

Every authoritative protocol state has exactly one domain owner.

Other components may:

- read it;
- request a transition;
- validate it;
- consume it;
- transform an authorized representation;
- record evidence of it.

They may not silently become a second owner.

**Evidence is not ownership.**

This distinction is fundamental to Chain Poker Genesis.

---

## 2. Engine responsibility matrix

Legend:

- **OWN** — authoritative owner / state transition authority.
- **WRITE** — writes data within its own domain.
- **READ** — reads required information.
- **VALIDATE** — validates another domain's state without owning it.
- **REQUEST** — requests an authorized operation.
- **RECORD** — produces evidence for Engine 04.
- **FORBID** — must not perform that function.

| Domain / State | 01 | 02 | 03 | 04 | 05 | 06 | 07 | Authoritative Owner |
|---|---|---|---|---|---|---|---|---|
| Installation/environment state | **OWN** | READ | READ | RECORD | | | | 01 |
| UI/presentation state | | **OWN** | | | | | | 02 |
| Node cryptographic identity | | READ | **OWN** | RECORD | | READ | READ | 03 |
| Authentication/signature service | | REQUEST | **OWN** | RECORD | | REQUEST | REQUEST | 03 |
| Table identity | | READ | VALIDATE | RECORD | | READ | **OWN** | 07 |
| Table configuration | | READ | VALIDATE | RECORD | READ | READ | **OWN** | 07 |
| Table lifecycle | | READ | VALIDATE | RECORD | | READ | **OWN/REQUEST** | 07 + governing consensus/state rules |
| Active card-engine selection | | READ | VALIDATE | RECORD | | READ | **OWN at creation** | 07 |
| Card-engine change authorization | | READ | VALIDATE | RECORD | | | REQUEST | Table Consensus / governance |
| Active card-engine version | | READ | VALIDATE | RECORD | | READ | **OWN as table context** | 07 |
| Hand/game rules state | READ | READ | VALIDATE | RECORD | | READ | READ | Poker Rules Engine |
| Rake policy/configuration | READ | READ | VALIDATE | RECORD | | | READ | 05 / protocol configuration |
| Rake calculation | | | VALIDATE | RECORD | **OWN** | | READ | 05 |
| Settlement execution | | | VALIDATE | RECORD | REQUEST | | REQUEST | Monetary Settlement Engine |
| Private event history | | READ | RECORD | **OWN** | RECORD | RECORD | RECORD | 04 |
| Merkle consolidation | | | VALIDATE | **OWN** | | | READ | 04 |
| Bitcoin anchor evidence | | | VALIDATE | **OWN** | | | READ | 04 / anchor subsystem |
| Canonical hand context | | READ | VALIDATE | RECORD | READ | READ | **OWN table inputs** | Table + hand state owner |
| Card-engine cryptographic deck state | | | VALIDATE | RECORD | | CONSUME | READ | **Selected Card Engine** |
| Shuffle/deck randomness | | | VALIDATE | RECORD | | CONSUME | SELECTS | **Selected Card Engine / defined randomness contract** |
| Card assignment result | | | VALIDATE | RECORD | | CONSUME | READ | **Selected Card Engine / distribution contract** |
| Private-card commitment | | | VALIDATE | RECORD | | **OWN** | READ | 06 |
| Protected private-card payload | | | VALIDATE | RECORD | | **OWN** | | 06 + approved crypto subsystem |
| Reveal authorization request | REQUEST | UI only | VALIDATE | RECORD | | REQUEST/VERIFY | READ | Request & Permission |
| Poker legality of reveal | | | | RECORD | | CONSUME | | Poker Rules Engine |
| Reveal verification | | | VALIDATE | RECORD | | **OWN** | | 06 |
| Dealer consumption state | | | VALIDATE | RECORD | | CONSUME | READ | Dealer Engine |
| Table wallet/custody state | | | VALIDATE | RECORD | READ | | READ/REFER | Table Wallet / Settlement architecture |
| Replay evidence | | READ | VALIDATE | **OWN evidence** | RECORD | RECORD | RECORD | 04 |
| Live replay execution | | DISPLAY | VALIDATE | PROVIDE EVIDENCE | | VERIFY | READ | Replay subsystem / defined separately |
| Audit trail | | READ | RECORD | **OWN** | RECORD | RECORD | RECORD | 04 |

### Ownership rule for Engine 07

Engine 07 owns the **table context**, not every subsystem instantiated by that table.

Therefore 07 may create/reference:

- table identifier;
- canonical configuration;
- configuration hash;
- initial table-state hash;
- supported card-engine identifiers;
- selected active card-engine identifier/version;
- table-scoped references/namespaces;
- creation lifecycle evidence.

It does **not** own:

- private keys;
- private cards;
- card randomness;
- deck permutation;
- poker rules;
- rake calculation;
- settlement execution;
- ledger history;
- reveal authorization;
- dealer consumption state.

---

# 3. Canonical architecture after consolidation

The architecture is divided into five distinct layers:

### A. Node preparation

`Installation Engine → Cryptographic Connection Engine → Player Node Ready`

### B. Table context

`GUI → Request & Permission → Table Creation Engine → Table Context`

### C. Card subsystem

`Selected Card Engine → Card Assignment Contract → Engine 06 → Dealer / Poker Rules`

### D. Economic subsystem

`Poker Rules / Hand Completion → Engine 05 → Monetary Settlement`

### E. Evidence subsystem

`All authoritative protocol events → Engine 04 → Merkle Consolidation → Bitcoin Anchor`

The GUI is never an authority merely because the user initiated an action through it.

The ledger is never the live-state authority merely because it records the state.

---

# 4. Critical contradictions identified and corrected

## C01 — Engine-number collision: Engine 07 versus Dual Shuffle Architecture

**Problem**

The repository contains:

- Engine 07 — Table Creation Engine;
- a supporting directory named `07-dual-shuffle-card-distribution-engine`.

This can incorrectly imply that two different systems own Engine 07.

**Correction**

**Engine 07 remains Table Creation Engine.**

The Dual Shuffle & Card Distribution Architecture is a **supporting card subsystem**, not a replacement for Engine 07 and not a second numbered Engine 07.

**Status:** RESOLVED at integration level.

---

## C02 — Table-level card-engine selection versus hand-level selection

**Problem**

The dual-shuffle document currently describes selection during each hand, while the accepted architecture requires selection when the table is created.

**Correction**

At table creation:

`CARD_ENGINE_SELECTED = A | B`

The selected engine and version become part of the table's canonical configuration.

For every subsequent hand, that active engine is inherited from the table context.

A later change requires table consensus.

**Status:** RESOLVED.

---

## C03 — Mid-hand engine switching

**Problem**

A generic fallback mechanism could permit a different engine after an authoritative card state already exists.

**Correction**

No card-engine change is valid after the hand has crossed its execution boundary.

A consensus-approved change becomes effective only at the next valid table boundary, normally the **next hand**.

Historical hands retain the engine identifier/version that was active when they were executed.

**Status:** RESOLVED.

---

## C04 — Two engines executing the same hand

**Problem**

Running both engines as competing producers could create two possible card assignments.

**Correction**

Exactly one selected engine is authoritative.

The non-selected engine may independently verify a result only where the protocol explicitly defines compatible verification.

Verification does not create a second authoritative state.

**Status:** RESOLVED.

---

## C05 — Randomness ownership

**Problem**

Historical wording distributes randomness between Shuffle, Dealer, UTXO scripts, commitment logic and cut/burn operations.

**Correction**

The selected Card Engine owns the generation and commitment of card-generation randomness under its declared cryptographic construction.

Dealer does not invent card randomness.

Engine 06 does not generate deck randomness.

Commitment nonce randomness is separate from deck/shuffle randomness.

If cut/burn requires an additional entropy input, that input must be explicitly supplied by the selected card/randomness contract and committed before it becomes authoritative.

**Status:** ARCHITECTURALLY RESOLVED; exact algorithms remain specification work.

---

## C06 — Dealer versus Card Engine

**Problem**

The historical documents can be read as if Dealer receives a committed deck while also participating in shuffle/randomness.

**Correction**

Dealer is a **consumer of the selected card engine's authoritative state**.

Dealer may perform only the consumption transitions assigned to it by its own specification, such as:

- cut;
- burn;
- dealing/consumption;
- phase-boundary operations.

Dealer cannot:

- create a competing deck;
- change the authoritative permutation;
- invent randomness;
- choose poker winners;
- replace the selected card engine.

**Status:** RESOLVED at 01→07 boundary; detailed Dealer specification remains outside this matrix.

---

## C07 — Cut versus immutable deck permutation

**Problem**

“Cut changes the deck” conflicts with the requirement that the committed deck permutation remains immutable.

**Correction**

A cut must be modeled as a **new consumption/state context over the same committed deck**, not as mutation of the underlying deck permutation.

Conceptually:

`CommittedDeckState + CutParameter → NewConsumptionContext`

The original deck commitment remains verifiable.

**Status:** RESOLVED architecturally; exact pointer/index representation remains a Dealer specification item.

---

## C08 — Burn randomness versus deterministic Dealer

**Problem**

Dealer is described as deterministic/state-derived while burn count is described as random.

**Correction**

Dealer execution itself is deterministic with respect to its authorized inputs.

If a burn count is variable, the randomness selecting that count must already exist in the authorized card/randomness state.

Thus:

`CommittedRandomness → BurnParameter → Deterministic Dealer Transition`

Dealer is the executor, not the entropy source.

**Status:** RESOLVED.

---

## C09 — Wallet signature versus card confidentiality

**Problem**

A wallet signature can be mistaken for encryption.

**Correction**

The protocol separates:

- signature = identity/authorization/integrity;
- encryption = confidentiality;
- commitment = binding/integrity;
- reveal authorization = permission to disclose;
- reveal verification = proof that disclosed data matches the commitment.

The Commit Pair / Reveal Pair model in Engine 06 is retained.

**Status:** RESOLVED.

---

## C10 — Signing key versus encryption/decryption key

**Problem**

Engine 03 establishes cryptographic identity, while Engine 06 requires protected private-card data. The architecture must not assume that a signing key can decrypt ciphertext.

**Correction**

Engine 03 owns node identity and signing services.

Engine 06 consumes an approved encryption/key-agreement interface.

The exact key architecture remains an explicit cryptographic specification item.

**Status:** OPEN IMPLEMENTATION SPECIFICATION — not an architectural contradiction.

---

## C11 — Engine 04 ledger versus live protocol state

**Problem**

Because Engine 04 records every event, it could become a second source of truth.

**Correction**

Engine 04 is the authoritative owner of **historical evidence**, not live business state.

Live state remains with its domain owner.

Ledger evidence may prove what was recorded; it does not gain authority to rewrite the table, cards, rake, or settlement state.

**Status:** RESOLVED.

---

## C12 — Replay versus private-card secrecy

**Problem**

“Complete replay” could be interpreted as requiring public plaintext private cards.

**Correction**

Replay is divided into:

1. **Public verification replay** — verifies public commitments, hashes, transitions and proofs.
2. **Authorized private replay** — reconstructs private state only for an authorized verifier.
3. **Cryptographic reproduction** — reproduces a historical result only when the required original cryptographic inputs are available under the protocol's replay policy.

No replay mode may invent missing private material.

**Status:** ARCHITECTURALLY RESOLVED; replay specification remains future work.

---

## C13 — Request & Permission versus domain authority

**Problem**

The intermediary could become a global state owner.

**Correction**

Request & Permission owns the **request/authorization lifecycle**, not the underlying domain state.

It can authorize:

`Requester → Request & Permission → Domain Engine`

but it does not become owner of:

- cards;
- randomness;
- table state;
- rake;
- settlement;
- ledger state.

**Status:** RESOLVED.

---

## C14 — GUI versus authoritative protocol state

**Problem**

A GUI action could be interpreted as directly changing protocol state.

**Correction**

GUI actions are requests/intents.

The authoritative engine performs the validated transition.

The GUI may display the result but cannot create protocol authority by itself.

**Status:** RESOLVED.

---

## C15 — Rake calculation versus settlement execution

**Problem**

Engine 05 could be interpreted as both calculating and paying rake.

**Correction**

Engine 05 owns:

`HAND_COMPLETED → ELIGIBILITY → RAKE_CALCULATED → RAKE_OBLIGATION`

The Monetary Settlement Engine owns the actual monetary transfer.

The stable bridge is the canonical **Rake Obligation ID**.

**Status:** RESOLVED.

---

## C16 — Rake determinism versus Bitcoin precision

**Problem**

Percentage formulas alone do not uniquely define satoshi-level settlement.

**Correction**

The architecture requires Engine 05 to produce a deterministic obligation, but the following remain mandatory specification items before production:

- integer-satoshi calculation;
- rounding direction;
- dust/minimum rules;
- network-fee treatment;
- aggregation/batching;
- failed-settlement recovery.

**Status:** OPEN IMPLEMENTATION SPECIFICATION.

---

## C17 — HAND_COMPLETED ownership

**Problem**

Engine 05 must know when a hand is complete but cannot infer completion from UI, elapsed time, card reveal or wallet movement.

**Correction**

Poker Rules / canonical game-state authority emits the authoritative `HAND_COMPLETED` transition.

Engine 05 consumes that transition.

**Status:** RESOLVED at integration boundary.

---

## C18 — Table wallet versus Table Creation

**Problem**

Creating a table could be interpreted as creating a custodial authority.

**Correction**

Engine 07 may establish a table-wallet reference/context.

Custody, spending and settlement authority remain in the wallet/settlement architecture.

**Status:** RESOLVED.

---

## C19 — Table configuration versus card-engine change

**Problem**

If Engine 07 owns table configuration, a later card-engine change could appear to require rewriting the original table configuration.

**Correction**

The original table configuration remains immutable historical context.

A card-engine change is a **versioned governance/state transition**:

`Proposal → Table Consensus → Approved/Rejected/No Consensus → Activation Boundary`

The active engine context changes forward from the activation boundary without rewriting prior hands.

**Status:** RESOLVED.

---

## C20 — Historical source versus normative integration

**Problem**

Historical PDFs contain terms such as UTXO, random cut, dealer, shuffle and commitment in overlapping responsibilities.

**Correction**

The integration matrix establishes the cross-engine ownership boundary.

Historical wording remains valuable as source material, but no ambiguous sentence may override an explicit ownership rule in this matrix.

**Status:** RESOLVED as documentation precedence.

---

# 5. Canonical card-engine contract

The rest of the protocol must not depend on the internal construction of Engine A or Engine B.

Both implementations must expose a normalized contract equivalent to:

| Operation | Required result |
|---|---|
| INITIALIZE_TABLE_CARD_CONTEXT | Engine/version/context identity |
| INITIALIZE_HAND | Hand-scoped card state |
| COMMIT_RANDOMNESS | Canonical randomness commitment |
| FINALIZE_DECK_STATE | Canonical deck/state commitment |
| COMMIT_ASSIGNMENT | Assignment commitment/proof |
| DEAL / CONSUME | Authorized card-consumption transition |
| CUT | New consumption context, no permutation mutation |
| BURN | Authorized consumption transition |
| PROTECT_PRIVATE_CARD | Protected card object |
| VERIFY | Cryptographic verification result |
| REVEAL | Authorized disclosure transition |
| FINALIZE_HAND | Final card-state evidence |

The exact operation names are implementation-neutral placeholders until the two individual card-engine specifications are finalized.

---

# 6. Table-level card-engine lifecycle

The canonical lifecycle is:

`TABLE_CREATE`
→ `CARD_ENGINE_A_OR_B_SELECTED`
→ `CARD_ENGINE_VERSION_BOUND`
→ `TABLE_READY`

For each hand:

`HAND_INITIALIZED`
→ active table card engine loaded
→ hand context snapshots engine ID/version
→ card execution
→ hand close

For a later engine change:

`CHANGE_PROPOSED`
→ `TABLE_CONSENSUS`
→ `APPROVED`
→ `CHANGE_SCHEDULED`
→ **next valid hand boundary**
→ `NEW_ENGINE_ACTIVE`

Rejected/no-consensus path:

`CHANGE_PROPOSED`
→ `REJECTED / NO_CONSENSUS`
→ current engine remains active.

No change is retroactive.

---

# 7. Canonical hand context

Before authoritative card execution begins, the hand must bind at minimum:

- table_id;
- hand_id;
- protocol version;
- rules version;
- active card-engine identifier;
- active card-engine version;
- commitment/reveal version;
- dealer version;
- canonicalization version;
- randomness context/commitment;
- participant set/order;
- table configuration hash;
- prior relevant state identifier.

This context is immutable for the hand.

A hand cannot silently migrate to another card engine.

---

# 8. Canonical evidence events

Engine 04 should receive, at minimum, normalized evidence for:

### Table

- `TABLE_CREATED`
- `TABLE_CONFIGURED`
- `CARD_ENGINE_SELECTED`

### Engine changes

- `CARD_ENGINE_CHANGE_PROPOSED`
- `CARD_ENGINE_CHANGE_CONSENSUS_REACHED`
- `CARD_ENGINE_CHANGE_REJECTED`
- `CARD_ENGINE_CHANGE_NO_CONSENSUS`
- `CARD_ENGINE_CHANGE_ACTIVATED`

### Hand/card

- `HAND_INITIALIZED`
- `RANDOMNESS_COMMITTED`
- `DECK_STATE_FINALIZED`
- `CARD_ASSIGNMENT_COMMITTED`
- `CARD_COMMITMENT_CREATED`
- `CARD_REVEAL_REQUESTED`
- `CARD_REVEAL_AUTHORIZED`
- `CARD_REVEAL_ACCEPTED`
- `CARD_REVEAL_REJECTED`
- `HAND_COMPLETED`

### Economic

- `RAKE_OBLIGATION_CREATED`
- `SETTLEMENT_REQUESTED`
- `SETTLEMENT_EXECUTED`
- `SETTLEMENT_FAILED`
- `SETTLEMENT_CONFIRMED`

Private plaintext card data is not automatically included in the general event ledger.

---

# 9. Canonical state flow

The integrated architecture is:

`INSTALLATION`
→ `CRYPTOGRAPHIC_IDENTITY`
→ `TABLE_CREATION`
→ `CARD_ENGINE_SELECTION`
→ `TABLE_READY`
→ `HAND_INITIALIZATION`
→ `SELECTED_CARD_ENGINE`
→ `DECK/CARD_ASSIGNMENT`
→ `ENGINE_06_COMMITMENT`
→ `DEALER_CONSUMPTION`
→ `POKER_RULES`
→ `AUTHORIZED_REVEALS`
→ `HAND_COMPLETED`
→ `ENGINE_05_RAKE`
→ `MONETARY_SETTLEMENT`
→ `ENGINE_04_EVIDENCE`

Engine 04 records evidence throughout the flow; it does not become the owner of those live transitions.

---

# 10. Replay rule

A historical hand must be associated with the exact:

`protocol_version + rules_version + card_engine_id + card_engine_version + commitment_version + canonicalization_version + randomness_context`

Therefore a future card-engine change cannot invalidate the interpretation of an earlier hand.

The replay verifier loads the historical engine version specified by the hand context.

---

# 11. Remaining open items after the 01→07 audit

These are **not reasons to stop the architecture**, but they must be specified before implementation claims full protocol determinism:

1. Exact cryptographic algorithms and domain separation.
2. Signing-key versus encryption/key-agreement architecture.
3. Exact randomness construction for Card Engine A.
4. Exact cryptographic construction and adapter contract for Card Engine B.
5. Exact Dealer pointer/cut representation.
6. Exact cut/burn entropy input contract.
7. Canonical hand-completion state machine.
8. Integer-satoshi rake rules.
9. Settlement-fee and failure rules.
10. Replay authorization and private-material policy.
11. Formal Table Consensus threshold/algorithm.
12. Version activation and compatibility rules.
13. Canonical event serialization/schema.
14. Formal test vectors for both card engines.

These are now clearly isolated as specification tasks rather than hidden architectural contradictions.

---

# 12. Final consolidated audit result

### 01 — Installation
Prepares and validates the node environment.

### 02 — Graphical Interface
Presents and requests actions; never becomes protocol authority.

### 03 — Cryptographic Connection
Owns cryptographic identity/connection services; does not own table or card state.

### 04 — Private Off-Chain Ledger
Owns historical evidence, canonical event persistence, Merkle consolidation and anchor evidence.

### 05 — Rake
Owns deterministic rake calculation and the resulting rake obligation; does not execute monetary settlement.

### 06 — Commitment & Reveal
Owns private-card commitment, protected-card state, reveal-pair verification and cryptographic disclosure validation.

### 07 — Table Creation
Owns the table context and the initial selection/version binding of exactly one card engine.

### Selected Card Engine
Owns the authoritative card-generation/shuffle/distribution state for the table and its hands, subject to the common card-engine contract.

### Dealer
Consumes the selected card state and executes authorized consumption operations; it does not generate competing randomness or mutate the underlying deck permutation.

### Table Consensus
Authorizes a future card-engine change at a valid table boundary; it does not rewrite history.

---

## 13. Gate before Document 08

Document 08 may proceed only after accepting this baseline:

> **One table → one active card engine at a time.  
> One hand → one authoritative card engine/version.  
> Card-engine changes require table consensus and activate only at a valid future boundary.  
> The ledger records history but does not own live state.  
> The GUI requests but does not decide.  
> Request & Permission authorizes but does not own domain state.  
> Dealer consumes but does not shuffle.  
> Engine 06 protects and verifies cards but does not generate deck randomness.  
> Engine 05 calculates rake but does not settle funds.  
> Engine 07 creates table context but does not become custodian of every subsystem.**

**Audit status:** 01→07 consolidated.  
**Document 08 gate:** OPEN only after this matrix is accepted as the integration baseline.

---

© 2026 Lerry Alexander Elizondo Villalobos (LAEV).  
Chain Poker Genesis by LAEV.
