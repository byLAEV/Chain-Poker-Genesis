# CHAIN POKER GENESIS BY LAEV

# 15 — Poker Rules Engine

## Official Technical Specification v2.2

**Document Class:** CORE ENGINE  
**Document Status:** INTEGRATION-READY — POST-AUDIT REVISION  
**Architecture Role:** Deterministic Poker Rule Authority  
**Protocol:** Chain Poker Genesis by LAEV  
**Game:** No-Limit Texas Hold'em Cash Game  
**Previous Specification:** v2.0  
**Revision:** v2.2

---

## 0. Document Control

~~~text
[LCCP]
SEQ: 15
PREV: 14
SELF: 15
NEXT: 16
CLASS: CORE ENGINE
STATUS: INTEGRATION-READY
[/LCCP]
~~~

This specification consolidates Engine 15 after normative review of the v2.0 candidate. It is the authoritative poker-rule specification for a No-Limit Texas Hold'em Cash Game hand.

## 1. Purpose

This specification incorporates the three residual integration corrections identified by the Engine 15 linear audit:

1. normative treatment of uncalled/excess wagers;
2. explicit Poker Rule Transition Result boundary before event encoding;
3. explicit Card/Dealer State input contract.

The Poker Rules Engine determines the normative truth of a poker hand:

- legal and invalid actions;
- authorized actor and action eligibility;
- betting obligations;
- minimum bets and raises;
- all-in and short-all-in classification;
- reopening of action;
- betting-round closure and street transitions;
- runout readiness;
- main and side pots;
- pot eligibility;
- hand evaluation;
- ties and deterministic pot division;
- terminal hand state.

For the same valid normative state, ruleset, authoritative Card/Dealer State where the transition depends on card state, and proposed action, the result MUST be deterministic.

## 2. Scope

This engine covers only No-Limit Texas Hold'em Cash Game rules. It does not own network, consensus, ledger persistence, request authorization, lifecycle, card randomness/dealing, wallet operations, monetary settlement, governance or UI.

An external layer may reject an operation for a reason belonging to its own domain, but MUST NOT redefine poker legality.

## 3. Fundamental Rules

### 3.1 Determinism

~~~text
Same Valid Normative State
+ Same Ruleset
+ Same Authoritative Card/Dealer State (when card-dependent)
+ Same Proposed Action
= Same Rule Result
~~~

### 3.2 Immutable Ruleset

A hand is bound to one ruleset identity and version. A rules change creates a new ruleset version.

### 3.3 Validation Before Transition

~~~text
GameState + ProposedAction
        ↓
ValidateAction
        ↓
LEGAL / INVALID
        ↓
LEGAL → normative transition
~~~

### 3.4 Invalid Action

An invalid action MUST NOT mutate player state, turn, street, cards, contributions, pots or hand result.

Formally: INVALID ACTION → GameState(t+1) = GameState(t).

## 4. Ruleset Identity

Every hand MUST identify:

~~~text
ruleset_id
ruleset_version
~~~

The applicable ruleset defines blind structure, minimum-bet policy, betting semantics, hand-ranking rules and odd-chip policy. Ruleset identity is part of replay input.

## 5. Normative Game State

The state MUST contain or deterministically derive:

~~~text
hand_id
ruleset_id / ruleset_version
participants
dealer_button
blind_structure
street
authorized_actor
player_participation_state
player_action_eligibility
available_stack
total_hand_contribution
current_street_contribution
current_bet
minimum_bet
minimum_raise_increment
last_full_raise_amount
betting_round_state
hole_card_state
community_cards
board_completion_state
all_in_state
pot_structure
pot_eligibility
hole_card_state_reference
community_card_state_reference
card_state_reference
board_completion_state
all_in_state
pot_structure
pot_eligibility
hand_result
~~~

Fields may be derived from authoritative state if the derivation is deterministic.

## 6. Player State Model

Participation state and action eligibility are separate.

Participation:

~~~text
ACTIVE
FOLDED
ALL_IN
~~~

Action eligibility:

~~~text
CAN_ACT
CANNOT_ACT
~~~

ALL_IN means the player has committed the entire available stack and cannot make another betting action. FOLDED players cannot win any pot.

## 7. Hand Lifecycle

~~~text
HAND_START → PREFLOP → FLOP → TURN → RIVER → SHOWDOWN → HAND_END
~~~

Not every hand visits every state. A hand may end early when only one non-folded player remains eligible. An all-in hand may require board runout without further betting.

## 8. Position and Turn

Only one player is the authorized actor at a betting point.

### Standard multiway preflop

The first eligible player after the big blind acts first.

### Heads-up

~~~text
BUTTON = SMALL_BLIND
PRE_FLOP: BUTTON / SMALL_BLIND acts first
POST_FLOP: BIG_BLIND acts first
~~~

### Postflop multiway

The first eligible player after the dealer button acts first. Folded and all-in players are skipped.

## 9. Canonical Actions

~~~text
FOLD
CHECK
CALL
BET
RAISE
ALL_IN
~~~

RE_RAISE is not a separate action type. A further increase is RAISE.

## 10. Action Result

The canonical validation contract is:

~~~text
ValidateAction(GameState, PlayerID, ProposedAction)
→ ActionResult
~~~

ActionResult contains at least status and a deterministic validation code. Status is LEGAL or INVALID. A legal result includes the normative transition/resulting state. An invalid result preserves the input state.

Useful validation codes include:

~~~text
INVALID_ACTOR
OUT_OF_TURN
INVALID_STREET
PLAYER_CANNOT_ACT
CHECK_FACING_BET
CALL_NOT_REQUIRED
INSUFFICIENT_STACK
BET_BELOW_MINIMUM
RAISE_BELOW_MINIMUM
RAISE_NOT_REOPENED
HAND_ALREADY_ENDED
INVALID_ACTION
~~~

## 11. Fold / Check / Call

### FOLD

Legal only for the authorized actor. Previous contributions remain in the pots; the player can never win.

### CHECK

Legal only when amount_to_call = 0.

### CALL

CALL means fully satisfying amount_to_call. If available stack is insufficient, a partial CALL is not accepted as CALL; committing the entire available stack is represented as ALL_IN.

An all-in call produces a final contribution equal to the player's available stack and may create a side-pot boundary.

## 12. Bet / Raise

### BET

BET is an opening wager when current_bet = 0. It requires available stack > 0 and bet_amount ≥ minimum_bet, subject to the all-in exception.

### RAISE

RAISE increases an existing current bet. A full raise must satisfy:

~~~text
new_current_bet >= current_bet + minimum_raise_increment
~~~

Current bet and minimum raise increment are distinct state variables.

## 13. Minimum Bet and Minimum Raise

The engine MUST distinguish:

~~~text
MINIMUM_BET
MINIMUM_RAISE_INCREMENT
~~~

For standard No-Limit Hold'em, MINIMUM_BET is normally the applicable big-blind amount unless the active ruleset explicitly defines another supported value.

When a full raise increases the current bet by X, X becomes the minimum raise increment for subsequent full raises in that betting round, subject to the active ruleset.

## 14. All-In and Short All-In

ALL_IN commits the player's entire available stack. It may result in a call, bet, full raise or short all-in.

A short all-in is an all-in whose increase over the current wager is below the minimum full-raise increment. A short all-in is not automatically a full raise, does not automatically change minimum_raise_increment and does not automatically reopen action.

## 15. Reopening Action

A full raise may reopen raising rights for players who still have the right to act.

A short all-in below the full-raise increment does not automatically reopen raising rights for a player who already acted against the current wager.

The betting-round state MUST retain or deterministically derive enough history to answer:

~~~text
Has this player already acted against the current wager?
Has a full raise occurred since that player's action?
~~~

Equivalent representations may use action_sequence, last_full_raise_amount, last_full_raise_actor and reopened_players.

## 16. Uncalled and Excess Wagers

An amount wagered by a player that is not matched by any opposing contribution and is not required to form a contested pot MUST be classified as an uncalled amount.

The normative sequence is:

~~~text
Proposed / committed wager
        ↓
Determine opposing matched contribution
        ↓
Identify uncalled excess
        ↓
Return uncalled excess to originating player
        ↓
Finalize contribution state
        ↓
Construct pots
~~~

The returned amount MUST NOT remain in `TOTAL_HAND_CONTRIBUTION`, `CURRENT_STREET_CONTRIBUTION` or any pot.

Therefore pot construction MUST use **finalized contributions after uncalled amounts have been returned**.

An uncalled amount MUST NOT be resolved by network ordering, consensus preference or settlement policy.

## 17. Betting-Round Closure

A betting round closes when no required betting action remains among players capable of acting. This includes cases where all required players matched the wager, all remaining players are all-in, or only one non-folded player remains.

## 18. Streets and Runout

Valid street transitions:

~~~text
PREFLOP → FLOP
FLOP → TURN
TURN → RIVER
RIVER → SHOWDOWN
~~~

A transition requires the current betting round to be closed, no early termination condition, and the applicable board/runout condition.

An all-in hand may follow:

~~~text
BETTING_CLOSED → RUNOUT → BOARD_COMPLETE → SHOWDOWN_READY
~~~

The card/dealer subsystem controls actual card generation, shuffle, deal and reveal. Engine 15 validates the normative transition and card-state invariants; it does not replace the card engine.

## 20. Board and Card Invariants

### Card / Dealer State Contract

Engine 15 consumes an authoritative **CardDealerStateResult** produced by the applicable card/dealer subsystem.

~~~text
CARD / DEALER ENGINE
        ↓
CardDealerStateResult
        ↓
POKER RULES ENGINE
~~~

The result MUST identify or deterministically derive `card_state_reference`, `hand_id`, private-card state reference, community-card state, board stage, card integrity status and deal/reveal status. `CardDealerStateResult` is the normalized semantic input contract of Engine 15; it does not create a second card engine or replace the authoritative card/distribution engine.

Engine 15 MUST NOT generate, shuffle or choose among competing card assignments. If incompatible card/dealer results exist, their resolution belongs to the applicable card/dealer conflict or canonicality layer before Engine 15 receives the authoritative state.

Engine 15 validates the supplied card state against poker-rule invariants.

## 19. Board and Card Invariants

- flop = exactly 3 community cards;
- turn = exactly 4;
- river = exactly 5;
- a valid deck state cannot contain duplicate physical card identities;
- each player has the applicable private-card count;
- showdown uses the available hole and community cards;
- the best valid five-card Hold'em hand is used.

## 19. Early Completion

When exactly one non-folded player remains eligible for the unresolved pots, the hand may terminate without showdown. No hand comparison is required for those pots.

## 22. Pot Construction

Pot construction MUST use finalized contribution state after all required uncalled amounts have been returned.

Let C_i = FINAL_TOTAL_HAND_CONTRIBUTION(player_i). Let L be the sorted set of distinct positive contribution levels.

For each current_level:

~~~text
previous_level = previous contribution level, or 0
layer_amount = current_level - previous_level
pot_layer_amount = layer_amount × count(players with C_i >= current_level)
~~~

Each contribution layer becomes a deterministic pot layer.

## 21. Pot Contributors and Eligibility

For a pot layer:

~~~text
CONTRIBUTORS = players with C_i >= current_level
ELIGIBLE_WINNERS = contributors whose state != FOLDED
~~~

Folded contributions remain in the pot. ALL_IN players may remain eligible to win.

## 22. Main and Side Pots

The first contribution layer is the main pot. Higher layers are side pots. Each pot has a unique pot_id, amount, contributors and eligible_winners.

## 23. Showdown

Showdown is ready when betting is closed, the required board is complete and at least two players are eligible for a pot requiring comparison. If only one player is eligible for all unresolved pots, early completion applies.

## 24. Hand Evaluation

Each eligible player is evaluated using the best valid five-card hand available from the player's hole cards and community cards.

The comparison hierarchy is:

~~~text
STRAIGHT_FLUSH
FOUR_OF_A_KIND
FULL_HOUSE
FLUSH
STRAIGHT
THREE_OF_A_KIND
TWO_PAIR
ONE_PAIR
HIGH_CARD
~~~

ROYAL_FLUSH is a presentation label for the highest STRAIGHT_FLUSH, not a separate comparison category.

## 25. Deterministic Hand Rank

Each evaluated hand produces a comparison vector such as:

~~~text
(category_rank, primary_rank, secondary_rank, kicker_1, kicker_2, ...)
~~~

Examples:

~~~text
FOUR_OF_A_KIND = category + quad_rank + kicker
FULL_HOUSE = category + trip_rank + pair_rank
TWO_PAIR = category + high_pair + low_pair + kicker
ONE_PAIR = category + pair_rank + kicker_1 + kicker_2 + kicker_3
~~~

Two hands tie when their complete comparison vectors are equal.

## 26. Straight, Flush and Suit Rules

A straight consists of five consecutive ranks. A-2-3-4-5 is valid and has high rank 5.

A flush is five cards of the same suit and is compared by descending ranks.

Suit MUST NOT be used as a tie-breaker.

## 27. Pot Resolution

Each pot is resolved independently:

~~~text
pot → eligible players → hand comparison → best rank → tied winners → deterministic division
~~~

A player may win one pot and lose another.

## 28. Split Pots and Odd Chips

For N tied winners:

~~~text
base_share = floor(pot_amount / N)
remainder = pot_amount mod N
~~~

The applicable table ruleset MUST provide odd_chip_policy_id and define the deterministic recipient order. Network arrival order, node preference or ad-hoc consensus MUST NOT decide odd-chip distribution.

## 31. Poker Rule Transition Result

Engine 15 exposes a semantic result distinct from the protocol's global event representation.

~~~text
ProposedAction
      ↓
ValidateAction
      ↓
PokerRuleTransitionResult
~~~

The result MUST contain at minimum `hand_id`, `ruleset_id`, `ruleset_version`, `actor_id`, `action`, `validation_status`, `previous_state_reference`, `resulting_state_reference` and `transition_type`.

When a hand completes it MUST additionally expose or reference the hand result, pot results and termination reason.

`PokerRuleTransitionResult` is a domain result of Engine 15, not a new protocol-wide event registry. The Event/Ledger layer is responsible for encoding an accepted transition into the canonical protocol event schema without changing its semantics.

## 32. Hand Result

The completed result MUST identify:

~~~text
hand_id
ruleset_id
ruleset_version
termination_reason
final_board
pots[]
winners[]
~~~

Each pot result MUST identify pot_id, type, amount, contributors, eligible_winners, winning_players, winning_rank, tie status, division and odd_chip_policy_id.

The result must be independently reproducible.

## 33. HAND_END

HAND_END requires all required pots resolved, all winners and divisions determined, no betting action pending and no board/runout step pending.

HAND_END is terminal for ordinary player actions.

## 34. Engine 13 Boundary

Engine 13 controls inter-engine request authorization and workflow.

~~~text
REQUEST_AUTHORIZED ≠ POKER_ACTION_LEGAL
~~~

An authorized request must still pass Engine 15 validation before it becomes a legal poker transition.

## 35. Event / Ledger Boundary

~~~text
Proposed Action
      ↓
Poker Rules Engine
      ↓
PokerRuleTransitionResult
      ↓
Canonical Event Encoding
      ↓
Event / Ledger
~~~

Engine 15 determines poker legality. The Event/Ledger layer preserves accepted history. History does not redefine the rules.

## 36. PCRE / Consensus Boundary

Engine 15 does not determine event canonicality, node consensus, checkpoints or conflict resolution.

~~~text
Poker Rules Engine → deterministic normative transition → event/state evidence → PCRE / canonicality layer
~~~

During replay, identical valid inputs and the same ruleset MUST reproduce the same normative result.

## 37. Lifecycle, Card and Settlement Boundaries

Table, seat, player/node and wallet lifecycle belong to their respective engines.

Card generation, shuffle, dealing and reveal belong to the applicable card/dealer engines.

Engine 12 performs monetary settlement. Engine 15 may produce a result such as PLAYER_A → MAIN_POT and PLAYER_B → SIDE_POT_1, but does not debit, credit, transfer or settle funds.

## 38. Normative Reproducibility

The state MUST contain or deterministically derive everything necessary to reproduce:

~~~text
legal action set
authorized actor
betting obligation
next normative state
pot structure
eligibility
showdown result
hand result
~~~

A canonical semantic state SHOULD expose ruleset identity, hand identity, street, button, participants, player states, stacks, contributions, betting state, board, pots, eligibility and authorized actor.

## 39. Conformance Requirements

A conforming implementation MUST be able to:

1. reject out-of-turn actions;
2. reject invalid street actions;
3. distinguish participation state from action eligibility;
4. validate check/call/bet/raise/fold/all-in;
5. distinguish minimum bet from minimum raise;
6. distinguish full raise from short all-in;
7. enforce reopening rules;
8. implement heads-up action order;
9. close betting rounds correctly;
10. advance streets correctly;
11. perform all-in runouts correctly;
12. construct main and side pots;
13. preserve folded contributions;
14. calculate pot eligibility;
15. evaluate Hold'em hands;
16. handle A-2-3-4-5;
17. ignore suit as a tie-breaker;
18. resolve split pots deterministically;
19. apply the configured odd-chip policy;
20. produce a deterministic terminal result;
21. leave state unchanged after invalid actions;
22. preserve ruleset identity;
23. remain independent from network, consensus and settlement authority.

## 40. Normative Test Set

The implementation MUST contain executable tests for at least:

~~~text
TEST-001 CHECK WITH NO BET
TEST-002 CHECK FACING BET
TEST-003 PREFLOP OPEN
TEST-004 MINIMUM RAISE
TEST-005 FULL RAISE REOPEN
TEST-006 SHORT ALL-IN
TEST-007 SHORT ALL-IN DOES NOT REOPEN PRIOR ACTOR
TEST-008 HEADS-UP PREFLOP ORDER
TEST-009 HEADS-UP POSTFLOP ORDER
TEST-010 MULTIPLE SIDE POTS
TEST-011 FOLDED CONTRIBUTOR
TEST-012 A-2-3-4-5 STRAIGHT
TEST-013 EXACT HAND TIE
TEST-014 SUIT DOES NOT BREAK TIE
TEST-015 ODD CHIP
TEST-016 PREFLOP ALL-IN RUNOUT
TEST-017 INVALID ACTION STATE IMMUTABILITY
TEST-018 HAND_END IMMUTABILITY
TEST-019 RULESET VERSION BINDING
TEST-020 REPLAY DETERMINISM
TEST-021 UNCALLED EXCESS RETURN
TEST-022 UNCALLED EXCESS EXCLUDED FROM POT
TEST-023 CARD/DEALER STATE ACCEPTANCE
TEST-024 CARD/DEALER STATE INCONSISTENCY REJECTION
TEST-025 POKER RULE TRANSITION RESULT DETERMINISM
TEST-026 EVENT ENCODING PRESERVES RULE RESULT
~~~

### TEST-021 — Uncalled Excess Return

The engine MUST return any uncalled excess to the originating player before final contribution state and pot construction.

### TEST-022 — Uncalled Excess Excluded From Pot

Final contribution, street contribution and pot amounts MUST exclude returned uncalled excess.

### TEST-023 — Card/Dealer State Acceptance

A valid authoritative CardDealerStateResult MUST be accepted for the applicable transition.

### TEST-024 — Card/Dealer State Inconsistency Rejection

Duplicate cards, invalid board counts, invalid hand references or impossible deal/reveal states MUST reject the dependent transition without state mutation.

### TEST-025 — Poker Rule Transition Result Determinism

Identical GameState + Ruleset + CardDealerStateResult + PlayerID + ProposedAction MUST produce an identical semantic PokerRuleTransitionResult.

### TEST-026 — Event Encoding Preserves Rule Result

Canonical event encoding MUST preserve action legality, resulting state, contributions, pots, eligibility, winners and termination reason.
~~~

## 41. Architectural Summary

~~~text
ENGINE 13
    = REQUEST / PERMISSION WORKFLOW

ENGINE 15
    = POKER LEGALITY + NORMATIVE HAND STATE

CARD / DEALER ENGINES
    = CARD GENERATION / SHUFFLE / DEAL / REVEAL

EVENT / LEDGER
    = RECORDED HISTORY

PCRE / CANONICALITY
    = CONFLICT RESOLUTION / CANONICAL HISTORY

LIFECYCLE ENGINES
    = OPERATIONAL LIFECYCLE

ENGINE 12
    = MONETARY SETTLEMENT EXECUTION
~~~

## 42. Final Normative Declaration

The Poker Rules Engine of Chain Poker Genesis is the deterministic normative authority for No-Limit Texas Hold'em Cash Game rules.

It defines what a player may do, when the player may do it, whether the action is legal, what normative transition follows, how betting obligations evolve, how pots are constructed, who is eligible, how hands are compared, how ties and pot divisions are resolved, and when the hand ends.

It is not a network engine, consensus engine, ledger, request/permission engine, lifecycle engine, card-dealing engine, wallet engine, settlement engine, cloud infrastructure engine or user interface.

**Current status: INTEGRATION-READY — AUDIT CORRECTIONS APPLIED**

---

© 2026 Lerry Alexander Elizondo Villalobos (LAEV).  
Chain Poker Genesis by LAEV.