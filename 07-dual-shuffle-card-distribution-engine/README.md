# Dual Shuffle & Card Distribution Architecture

**Chain Poker Genesis by LAEV**  
**Status:** Architectural specification v1.0  
**Role:** Supporting architecture; does not replace the repository's Engine 07 — Table Creation Engine.

## 1. Purpose

Chain Poker Genesis uses two independently defined card-shuffle/distribution mechanisms so that card generation is not architecturally dependent on a single implementation.

The two mechanisms are:

1. **Engine A — Native Chain Poker Genesis Shuffle & Distribution**
   - protocol-native mechanism;
   - based on the project's committed deck/state and defined transition model;
   - compatible with the protocol's UTXO-style execution model.

2. **Engine B — Independent Verifiable Shuffle / Mental-Poker Adapter**
   - independent cryptographic shuffle/dealing mechanism;
   - based on the established family of mental-poker / verifiable-shuffle constructions;
   - integrated through a protocol adapter rather than silently replacing the native mechanism.

## 2. Critical rule: two engines do not mean two different hands

The two engines must never independently produce competing card assignments for the same hand and then leave the protocol to choose between them after seeing the result.

For a given hand, the protocol establishes a **Shuffle Engine Selection** before execution:

SHUFFLE_ENGINE_SELECTED = A or SHUFFLE_ENGINE_SELECTED = B

The selected engine becomes authoritative for card assignment.

Where both engines can operate over the same canonical inputs, the non-authoritative engine may run as an **independent verifier**. A verifier mismatch is a protocol fault, not a reason to choose whichever result is favorable.

## 3. Why two engines exist

The dual architecture provides:
- implementation independence;
- reduced single-engine dependency;
- an alternate cryptographic construction;
- migration and compatibility capability;
- independent verification where compatible;
- a defined fallback path when one implementation is unavailable;
- clearer separation between protocol rules and shuffle implementation.

It does **not** imply that two independent random outputs should be combined after the hand has started.

## 4. Engine A — Native mechanism

Engine A owns the Chain Poker Genesis-native card-generation path.

Its exact responsibilities are defined by the Card Distribution, Dealer, randomness and UTXO specifications.

At a high level:

Randomness → committed deck/state → player commitments → finalized hand sequence → Dealer consumption → card assignment → Engine 06 commitment/reveal

Engine A must not delegate poker legality to the shuffle implementation.

## 5. Engine B — Independent verifiable-shuffle mechanism

Engine B is an adapter boundary for a cryptographic shuffle/deal construction based on mental-poker / verifiable-shuffle techniques.

The adapter must expose the same canonical output contract as Engine A:

DeckAssignmentResult

containing, conceptually:
- hand identifier;
- protocol version;
- shuffle-engine identifier;
- canonical deck/state commitment;
- player/card assignment commitments;
- proof or verification material;
- deterministic state-transition identifiers.

The implementation may use a different cryptographic construction internally, but the output must be normalized before Engine 06 consumes it.

## 6. Canonical boundary

Both engines must terminate at the same protocol boundary:

ShuffleResult → Card Distribution Contract → Engine 06

Engine 06 therefore does not need to know whether Engine A or Engine B produced the assignment.

## 7. Selection lifecycle

A hand should follow:

1. HAND_INITIALIZED
2. PLAYER_SET_FINALIZED
3. SHUFFLE_ENGINE_SELECTED
4. SHUFFLE_COMMITMENT_CREATED
5. DECK_STATE_FINALIZED
6. CARD_ASSIGNMENT_COMMITTED
7. DEAL_SEQUENCE_EXECUTED
8. CARD_COMMITMENTS_CREATED
9. gameplay
10. authorized reveals
11. hand close

The shuffle engine must be selected before the resulting card assignment becomes authoritative.

## 8. No post-result switching

The protocol must reject any attempt to:
- select Engine A after Engine B has produced an authoritative result;
- select Engine B after Engine A has produced an authoritative result;
- compare both outputs and select the more convenient result;
- alter the selected engine after commitment finalization.

The selected engine identifier must be included in the hand's canonical state.

## 9. Independent verification mode

If Engine A and Engine B are mathematically compatible for a given protocol version, the non-selected engine may independently verify:
- deck validity;
- permutation validity;
- assignment validity;
- commitment consistency;
- proof validity.

This produces:

PRIMARY_RESULT + INDEPENDENT_VERIFICATION

rather than:

RESULT_A versus RESULT_B.

## 10. Failure and fallback

Fallback is permitted only **before authoritative hand execution is finalized**.

Example:

Engine A unavailable → permission/state layer records failure → Engine B selected → new shuffle commitment → execution

Once the authoritative shuffle commitment has been finalized, failure must produce a defined hand-abort/recovery state rather than an invisible engine substitution.

## 11. Randomness boundary

Neither shuffle engine may secretly obtain additional unpredictable input after its commitment point unless that randomness is explicitly part of the protocol state transition.

Randomness ownership must be specified separately from the presentation of the shuffle engine.

The Dealer consumes the resulting committed state; it does not invent randomness.

## 12. Card distribution boundary

The selected shuffle engine establishes the cryptographic deck/order and assignment proof.

The Card Distribution layer maps the resulting assignment to protocol player identifiers.

Engine 06 then protects and verifies each player's private card state.

The Dealer remains responsible for its explicitly defined consumption operations such as cut and burn and must not become a hidden second shuffle engine.

## 13. Compatibility contract

Both engines must eventually support a common test-vector suite covering:
- same protocol version;
- same player set;
- same canonical hand context;
- valid deck;
- invalid deck;
- duplicate card;
- missing card;
- invalid proof;
- invalid commitment;
- wrong player assignment;
- wrong engine identifier;
- replayed result.

## 14. Security boundary

Two engines reduce implementation monoculture, but they do not automatically create security.

The protocol still depends on:
- secure cryptographic primitives;
- correct key custody;
- correct randomness;
- correct canonicalization;
- correct authorization;
- correct verification;
- correct implementation.

A second engine is useful only if its trust assumptions and implementation are sufficiently independent.

## 15. Relationship to Engine 06

The selected shuffle engine produces the card assignment input.

Engine 06 performs:

private card protection → commitment → authorized reveal → reveal verification

Engine 06 must not select the shuffle result after observing private cards.

## 16. Relationship to Engine 04

Engine 04 records:
- selected engine;
- engine version;
- shuffle commitment;
- assignment commitment;
- proof identifiers;
- transition results;
- verification result;
- failure/fallback events.

Private card plaintext must not be placed in the general event ledger solely because two shuffle engines exist.

## 17. Relationship to Request & Permission

All engine selection, fallback, verification and execution transitions that require authorization must use the Request & Permission layer.

The permission layer does not decide which cryptographic result is favorable.

## 18. Final architectural rule

The protocol has **two shuffle/distribution engines but one canonical hand state**.

Only one engine is authoritative for a hand.

The second engine is an independent implementation/verification path, not a second dealer that can silently overwrite the first.

---

© 2026 Lerry Alexander Elizondo Villalobos (LAEV).
Chain Poker Genesis by LAEV.