# CHAIN POKER GENESIS BY LAEV

## 16 — Dealer Engine (Crupier Engine)

### Consolidated Formal Technical Specification v1.1

**Document Class:** CORE ENGINE  
**Document Status:** CONSOLIDATED / CORRECTED  
**Architecture Role:** Deterministic Deck-Access and Burn Control  
**Previous Specification:** v1.0 historical source  
**Revision:** v1.1  
**Protocol:** Chain Poker Genesis by LAEV

---

## 0. Document Control

[LCCP]  
SEQ: 16  
PREV: 15  
SELF: 16  
NEXT: 17  
CLASS: CORE ENGINE  
STATUS: CONSOLIDATED  
[/LCCP]

This document reconstructs and formalizes the historical specification supplied as **16.0 Dealer Engine (Crupier Engine).pdf**.

The Dealer Engine is responsible for controlled consumption of a previously committed deck. It does not create the deck, modify its permutation, interpret card semantics, evaluate poker hands, determine winners, or authorize monetary settlement.

---

# 1. Purpose

The Dealer Engine controls the access position through which cards are consumed from the committed deck during a hand.

Its canonical responsibilities are:

1. Apply a protocol-defined cut operation when the lifecycle permits one.
2. Apply protocol-defined burn operations.
3. Advance the canonical deck-consumption state.
4. Produce sufficient evidence for deterministic replay and verification.

Architectural flow:

    COMMITTED DECK
          ↓
    DEALER ENGINE
          ↓
    CUT / BURN / CONSUMPTION STATE
          ↓
    CARD ACCESS
          ↓
    POKER / HAND EXECUTION

---

# 2. Architectural Principle

The Dealer Engine preserves strict separation between:

    DECK ORDER
        ≠
    DECK ACCESS POSITION
        ≠
    CARD SEMANTICS
        ≠
    POKER OUTCOME

The committed deck is an ordered immutable object. Dealer operations affect how the protocol reaches positions in that ordered object; they do not rewrite the object itself.

---

# 3. Formal State

Let:

    D = committed deck permutation
    N = |D| = 52
    c = canonical consumption state
    b = burn record
    q = hand lifecycle state

The deck is:

    D = [d0, d1, ..., d51]

Every element is unique.

The Dealer Engine treats D as immutable.

For a sequential non-wrapping consumption phase:

    c_next = c_current + n

where n is the number of cards consumed by the operation.

---

# 4. Critical Correction — Cut vs. Monotonic Consumption

The historical v1.0 wording allows the cut to modify the pointer while also requiring that the pointer remain monotonically increasing. Those statements conflict if the pointer is interpreted as one absolute deck index.

This revision separates:

    CUT POSITION

from:

    ABSOLUTE CONSUMPTION COUNT

A cut may establish the starting access origin before sequential consumption begins. Once consumption begins, the canonical consumption count is monotonically increasing.

Normative rule:

> A valid cut may establish the initial access origin; it must never retroactively alter already-consumed history or make consumed cards available again.

---

# 5. Deck Immutability

The Dealer Engine MUST NOT modify D.

No Dealer operation may:

- reorder cards;
- replace cards;
- duplicate cards;
- delete cards from the committed deck object;
- generate a replacement permutation;
- alter card identities.

A burn is therefore a consumption event, not a deck mutation.

The committed deck remains available as historical evidence for replay.

---

# 6. Responsibility 1 — Cut

A cut establishes a protocol-authorized alternative starting position for deck access.

Conceptually:

    CUT(D, k) → access_origin

where k is the protocol-defined cut parameter.

The exact cut algorithm must be defined by the canonical protocol configuration or upstream entropy/randomness specification.

The Dealer Engine executes the cut rule. It does not independently create entropy.

A valid cut:

- does not modify D;
- does not duplicate or destroy cards;
- does not interpret card meaning;
- is recorded as a protocol event;
- is reproducible from canonical inputs;
- occurs only at an authorized lifecycle boundary.

The Dealer Engine must not introduce an implicit cut.

---

# 7. Responsibility 2 — Burn

A burn operation consumes one or more cards without assigning them to a player or community-board position.

Conceptually:

    BURN(n)
        ↓
    consume next n cards
        ↓
    advance consumption state

For a sequential burn:

    c_next = c_current + n

The canonical poker-rule specification must define the permitted value of n.

The historical source permits a protocol-defined range of 1..5. This is retained as a configurable range, not as a universal assertion about standard poker.

If Chain Poker Genesis adopts a specific poker format, that format must define the exact burn count for each lifecycle point. The Dealer Engine executes the configured rule rather than inferring it.

---

# 8. Burn Properties

A burned card:

- is consumed from the committed deck sequence;
- is not assigned to a player;
- is not assigned to the community board;
- does not alter the deck permutation;
- remains reconstructible from the committed deck and consumption history;
- is represented in auditable execution history.

Whether the identity of a burned card is publicly revealed is a protocol visibility rule, not a Dealer Engine semantic rule.

---

# 9. Consumption Model

The Dealer Engine maintains the canonical consumption sequence.

    START
      ↓
    OPTIONAL CUT
      ↓
    BURN, if required
      ↓
    CARD CONSUMPTION
      ↓
    BURN, if required
      ↓
    CARD CONSUMPTION
      ↓
    HAND COMPLETION

The Dealer Engine does not decide why a card is being consumed.

The applicable hand lifecycle classifies consumption as, for example:

    PLAYER_CARD
    BURN
    FLOP_CARD
    TURN_CARD
    RIVER_CARD
    OTHER_PROTOCOL_DEFINED_CARD

The Dealer Engine executes the authorized access operation and records its classification.

---

# 10. Hand Lifecycle Integration

The historical source identifies possible activation points at pre-flop, pre-flop reveal, pre-turn, and pre-river.

The corrected architectural boundary is:

> The Dealer Engine is invoked only when the canonical poker-rule specification requires a cut or burn.

For a Texas Hold'em-compatible lifecycle, a typical model is:

    HAND PREPARATION
          ↓
    DECK ACCESS INITIALIZATION
          ↓
    PLAYER CARD CONSUMPTION
          ↓
    PRE-FLOP BURN
          ↓
    FLOP CONSUMPTION
          ↓
    PRE-TURN BURN
          ↓
    TURN CONSUMPTION
          ↓
    PRE-RIVER BURN
          ↓
    RIVER CONSUMPTION

The definitive lifecycle remains under the canonical poker-rules specification.

---

# 11. Authority Boundary

The Dealer Engine MUST NOT independently decide:

- whether a hand has started;
- whether a burn is required;
- which players receive cards;
- which cards form a poker hand;
- who wins;
- how much a player wins;
- whether a bet is valid;
- whether settlement is authorized.

Its function is execution of an already-authorized card-consumption transition.

---

# 12. Relationship to Shuffle / Deck Commitment

The upstream card subsystem provides the committed deck D.

    ENTROPY / COMMIT-REVEAL / SHUFFLE
                    ↓
              COMMITTED DECK D
                    ↓
              DEALER ENGINE
                    ↓
             ACCESS / BURN
                    ↓
             HAND EXECUTION

The Dealer Engine does not replace the shuffle subsystem and does not create a competing randomness source.

---

# 13. Relationship to Poker Rules

The Poker Rules Engine defines the semantic game lifecycle.

It determines, according to the selected poker format:

- when cards must be consumed;
- when burns occur;
- how many cards are burned;
- when community cards are exposed;
- when the hand advances between streets.

The Dealer Engine executes the access mechanics required by those rules.

Therefore:

    POKER RULES ENGINE
        = defines required card-consumption transition

    DEALER ENGINE
        = executes the authorized transition

Neither component should silently absorb the authority of the other.

---

# 14. Relationship to Consensus

The consensus layer verifies that Dealer Engine transitions conform to the canonical protocol.

Verification may include:

    deck commitment/reference
    hand identity
    prior consumption state
    operation type
    cut parameters
    burn count
    resulting consumption state
    event ordering
    engine/version compatibility
    event integrity

Consensus verifies the transition. It does not delegate poker semantics to the Dealer Engine.

---

# 15. Formal Operation Types

The Dealer Engine SHOULD expose a canonical logical vocabulary:

    DEALER_INITIALIZE
    DEALER_CUT
    DEALER_BURN
    DEALER_CONSUME
    DEALER_FINALIZE

The externally exposed event registry remains governed by the canonical protocol event specification.

The Dealer Engine must not create a competing event-persistence model.

---

# 16. Dealer Operation Record

A canonical Dealer operation should contain, at minimum:

    dealer_operation_id
    table_id
    hand_id
    deck_commitment_id
    operation_type
    previous_consumption_state
    cut_reference
    burn_count
    consumption_start
    consumption_end
    protocol_version
    engine_version
    timestamp
    operation_hash
    authorization_reference

Additional fields may be required by the canonical event and ledger specifications.

---

# 17. Determinism

For identical canonical inputs, compatible implementations must produce equivalent Dealer Engine results.

Relevant inputs include:

    deck commitment
    hand identity
    prior consumption state
    authorized operation
    cut parameter
    burn count
    protocol version
    engine version

The Dealer Engine must not introduce hidden randomness.

If a cut parameter originates from an entropy subsystem, that value becomes an explicit protocol input.

---

# 18. Determinism vs. Unpredictability

The historical source states that the design provides no predictability of exact consumption points.

That claim requires qualification.

A deterministic replay system must allow a valid verifier to reproduce the consumption position after the required inputs and evidence become available.

The correct distinction is:

    BEFORE REQUIRED INPUTS ARE AVAILABLE
            ↓
    consumption may be unpredictable to an observer

    AFTER REQUIRED INPUTS / REVEALS / EVIDENCE ARE AVAILABLE
            ↓
    consumption must be reproducible

Normative security property:

> Consumption positions may remain unpredictable to unauthorized observers during execution while remaining deterministically reproducible to authorized verifiers after the protocol's required inputs become available.

---

# 19. Security Restrictions

The Dealer Engine MUST NOT:

1. modify the committed deck;
2. generate an undisclosed replacement randomness source;
3. change burn counts outside canonical rules;
4. consume cards without a valid lifecycle transition;
5. assign semantic meaning to cards;
6. determine winners;
7. determine betting outcomes;
8. authorize monetary settlement;
9. access strategic player information unnecessarily;
10. rewrite historical Dealer events.

---

# 20. Security Invariants

### Invariant 1 — Deck Integrity

    D remains the same committed permutation.

### Invariant 2 — Unique Deck Elements

    |D| = 52

and every deck element is unique.

### Invariant 3 — Consumption Integrity

No card position may be consumed twice within the same canonical consumption sequence.

### Invariant 4 — No Unauthorized Skip

The consumption state may advance only through a valid protocol operation.

### Invariant 5 — Burn Integrity

A burn must correspond to a valid burn transition and canonical burn count.

### Invariant 6 — Replayability

A valid verifier must reconstruct Dealer state from canonical inputs and recorded events.

### Invariant 7 — Semantic Separation

Dealer execution does not determine card meaning or game outcome.

### Invariant 8 — Event Integrity

Dealer operations remain cryptographically traceable through the protocol event and ledger system.

### Invariant 9 — Lifecycle Authority

The Dealer Engine cannot invent poker lifecycle transitions.

### Invariant 10 — Settlement Separation

Dealer state cannot authorize or execute monetary settlement.

---

# 21. Consumption Bounds

For a 52-card deck, the Dealer Engine must reject a transition that exceeds the valid deck-access domain.

The protocol must explicitly define whether an implementation permits:

    NO WRAP

or:

    CONTROLLED WRAP / MODULAR ACCESS

A simple monotonically consumed hand should satisfy:

    0 ≤ consumed_cards ≤ 52

A cut must never be implemented as an uncontrolled wrap that makes already-consumed cards available again.

---

# 22. Cut and Consumption State Model

To avoid ambiguity, the protocol should distinguish:

    deck_index
    access_origin
    consumed_count
    consumption_cursor

Recommended conceptual model:

    access_origin
          +
    relative_consumption_offset
          =
    current_access_position

The consumed count remains monotonic even when the initial access origin is changed by a valid cut.

This prevents a cut from appearing to reverse consumption history.

---

# 23. Burn Evidence

Each burn should establish, at minimum:

    hand identity
    deck commitment
    prior state
    burn operation
    burn count
    resulting state
    authorizing rule/reference

The exact burned-card identity may be retained privately or revealed according to protocol disclosure policy.

A burn event proves consumption; it does not necessarily imply public disclosure.

---

# 24. Event Ordering

Dealer events form part of the canonical hand event sequence.

    PREVIOUS HAND EVENT
            ↓
    DEALER OPERATION
            ↓
    RESULTING DEALER STATE
            ↓
    NEXT HAND EVENT

The Dealer Engine must reject or flag an operation whose predecessor state does not match the canonical state expected by the protocol.

This protects against insertion, deletion, or reordering of Dealer operations during replay.

---

# 25. Idempotency and Replay Protection

Every Dealer operation must have a unique operation identity.

Repeated delivery of the same logical operation must not cause an additional burn or additional consumption.

    SAME OPERATION ID
          +
        RETRY
          ↓
      SAME RESULT

not:

    RETRY
      ↓
SECOND CONSUMPTION

This is required for safe distributed event delivery.

---

# 26. Failure Handling

The engine should distinguish at least:

    INVALID_OPERATION
    INVALID_PREVIOUS_STATE
    INVALID_DECK_COMMITMENT
    INVALID_CUT
    INVALID_BURN_COUNT
    CONSUMPTION_OUT_OF_BOUNDS
    DUPLICATE_OPERATION
    REPLAY_DETECTED
    ENGINE_VERSION_INCOMPATIBLE
    PROTOCOL_STATE_INCOMPATIBLE

A failed operation must not advance canonical consumption state.

---

# 27. Canonical Processing Sequence

    1. RECEIVE AUTHORIZED DEALER OPERATION
              ↓
    2. IDENTIFY TABLE / HAND
              ↓
    3. VERIFY DECK COMMITMENT
              ↓
    4. VERIFY PREVIOUS CONSUMPTION STATE
              ↓
    5. VERIFY OPERATION TYPE
              ↓
    6. VERIFY CUT / BURN PARAMETERS
              ↓
    7. VERIFY CONSUMPTION BOUNDS
              ↓
    8. EXECUTE TRANSITION
              ↓
    9. PRODUCE NEW CONSUMPTION STATE
              ↓
    10. PRODUCE DEALER EVENT
              ↓
    11. SUBMIT EVENT TO PROTOCOL LEDGER
              ↓
    12. RETURN DETERMINISTIC RESULT

---

# 28. Formal Responsibility Flow

    CARD / SHUFFLE SUBSYSTEM
              │
              │ committed deck
              ▼
        DEALER ENGINE
              │
              ├── CUT
              │
              ├── BURN
              │
              └── CONSUMPTION STATE
              │
              ▼
       POKER / HAND EXECUTION
              │
              ▼
       CONSENSUS / VERIFICATION
              │
              ▼
       PRIVATE OFF-CHAIN LEDGER

The arrows represent protocol dependencies and evidence flow, not ownership by the Dealer Engine.

---

# 29. Non-Responsibilities

The Dealer Engine does not:

    generate the committed deck
    shuffle the deck
    create entropy
    interpret card values
    evaluate poker hands
    determine winners
    calculate pots
    authorize bets
    manage player seats
    manage player sessions
    authorize settlement
    execute Bitcoin transactions
    operate the permanent Ledger
    construct Merkle trees
    perform Bitcoin anchoring

These responsibilities remain with their respective protocol components.

---

# 30. Implementation Independence

Compatible implementations may use different internal data structures provided that they produce equivalent protocol results for equivalent canonical inputs.

The protocol contract is defined by:

    input state
    +
    authorized Dealer operation
    +
    canonical rules
    +
    result state
    +
    verifiable evidence

An implementation-specific pointer representation must not become a second protocol definition.

---

# 31. Versioning

The Dealer Engine is versionable only to the extent permitted by the protocol's engine-version and compatibility rules.

A new Dealer Engine version must not silently change:

- committed deck semantics;
- historical event interpretation;
- canonical poker rules;
- the meaning of a burn;
- the identity of previously recorded operations.

Changes affecting interoperability must be explicitly versioned and admitted according to the applicable protocol compatibility mechanism.

---

# 32. Canonical Nomenclature

**Committed Deck**  
Immutable canonical deck permutation supplied to the hand.

**Deck Access Position**  
Position from which the next card is consumed.

**Consumption Cursor**  
Protocol state representing sequential consumption.

**Cut**  
Operation establishing the permitted initial access origin.

**Burn**  
Consumption of cards without player or board assignment.

**Dealer Operation**  
One authorized cut, burn, consumption, or lifecycle operation.

**Dealer Event**  
Auditable protocol record of a Dealer operation.

A burned card must not be described as a deleted card. It is consumed while remaining part of the historical committed deck.

---

# 33. Integration Status

This revision consolidates the historical v1.0 Dealer Engine definition and resolves the principal ambiguities required for integration with the deterministic protocol architecture:

    ✓ Deck immutability clarified
    ✓ Cut semantics separated from monotonic consumption
    ✓ Burn defined as consumption rather than deck mutation
    ✓ Poker-rule authority separated from Dealer execution
    ✓ Randomness authority separated from Dealer execution
    ✓ Determinism distinguished from runtime unpredictability
    ✓ Burn visibility separated from burn execution
    ✓ Consumption bounds defined
    ✓ Idempotency and replay protection added
    ✓ Failure states defined
    ✓ Event ordering defined
    ✓ Consensus verification boundary defined
    ✓ Ledger persistence boundary defined
    ✓ Settlement separation preserved
    ✓ Canonical nomenclature established

**Status: CONSOLIDATED / CORRECTED**

---

# 34. Final Architectural Definition

The **Dealer Engine** is the Chain Poker Genesis protocol component responsible for executing authorized deck-access operations, principally cut and burn, against an immutable committed deck while preserving deterministic consumption state, replayability, cryptographic traceability, and strict separation from poker semantics, randomness generation, consensus authority, and monetary settlement.

Its central rule is:

    THE DEALER MAY CONTROL HOW THE COMMITTED DECK IS CONSUMED.
    THE DEALER MAY NOT CHANGE WHAT THE COMMITTED DECK IS.

And:

    DECK ORDER
        ≠
    DECK ACCESS
        ≠
    GAME SEMANTICS
        ≠
    MONETARY SETTLEMENT

---

© 2026 Lerry Alexander Elizondo Villalobos (LAEV).  
Chain Poker Genesis by LAEV.
