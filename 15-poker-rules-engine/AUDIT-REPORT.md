# ENGINE 15 — LINEAR INTEGRATION AUDIT

## Poker Rules Engine v2.1

**Protocol:** Chain Poker Genesis by LAEV  
**Engine:** 15 — Poker Rules Engine  
**Audit scope:** Engine 15 against repository-facing Engine 04 → Engine 14 integration contracts, with explicit review of Engine 12, Engine 13 and Engine 14 boundaries, plus available card-engine specifications.  
**Audit date:** 2026-09-28  
**Audit status:** CONDITIONAL PASS — INTEGRATION ITEMS REMAIN  
**Recommendation:** Do not mark Engine 15 FROZEN yet.

---

## 1. Executive Result

Engine 15 v2.1 is structurally consistent with the documented architecture and correctly establishes Poker Rules as the domain authority for poker legality and hand-state transitions.

The audit found **no authority inversion** between Engine 15 and Engines 04, 12, 13 or 14.

The audit also found **three residual specification items** that should be closed before freezing Engine 15:

1. **Uncalled/excess bet handling is not explicitly normative.**
2. **The boundary between the Poker Rules hand result and the canonical protocol event registry remains implicit.**
3. **Card/dealer state verification is referenced by Engine 15 but the exact authoritative input/result contract is not named.**

These are integration/specification gaps, not evidence that another engine currently owns poker rules.

---

## 2. Authority Audit

### 2.1 Engine 15 vs Engine 13

**Result: PASS**

Engine 13 owns request validation, permission and request-workflow authorization.

Engine 15 owns poker legality.

The critical separation is:

~~~text
REQUEST_AUTHORIZED
        ≠
POKER_ACTION_LEGAL
~~~

A request authorized by Engine 13 still requires Engine 15 validation.

No authority inversion was found.

---

## 3. Engine 15 vs Engine 14 — PCRE

**Result: PASS**

Engine 14 performs deterministic replay, conflict analysis, canonical-state reconstruction and escalation to validator consensus when deterministic evidence is insufficient.

Engine 15 supplies the poker-rule transition used during deterministic replay.

Engine 14 does not acquire poker-rule authority.

Correct relationship:

~~~text
Accepted / Candidate Game Event
        ↓
Poker Rules Validation
        ↓
Normative Transition
        ↓
Deterministic Replay
        ↓
PCRE Canonical-State Analysis
~~~

The PCRE's documented requirement that replay use Texas Hold'em rules is compatible with Engine 15.

No contradiction was found.

---

## 4. Engine 15 vs Engine 12 — Monetary Settlement

**Result: PASS**

Engine 12 executes authorized monetary settlement.

Engine 15 determines poker outcome and pot distribution.

Therefore:

~~~text
ENGINE 15
Poker Result
    ↓
ENGINE 05
Monetary Obligation
    ↓
ENGINE 13 / Authorization Boundary
    ↓
ENGINE 12
Settlement Execution
~~~

Engine 15 does not debit, credit, transfer or settle funds.

No settlement authority is incorrectly assigned to Engine 15.

---

## 5. Engine 15 vs Engine 04 — Private Off-Chain Ledger

**Result: PASS**

Engine 04 records historical protocol evidence.

It does not determine poker legality.

Engine 15 can therefore produce a normative transition/result that Engine 04 records as an event.

The ledger cannot reinterpret a stored event to change poker legality.

No contradiction was found.

---

## 6. Engine 15 vs Engine 06 / 07 — Card Systems

**Result: PASS WITH INTEGRATION ITEM**

Engine 06 protects and verifies private-card commitments/reveals.

Engine 07 establishes the dual-shuffle/card-distribution architecture and requires one selected authoritative card-assignment path.

Engine 15 correctly states that it does not generate, shuffle or deal cards.

However, Engine 15 currently says it validates:

- deck/card uniqueness;
- private-card count;
- community-card counts;
- board completion.

The specification does not yet name the exact canonical **Card Assignment / Dealer State Result** consumed by Engine 15.

This is not an authority contradiction, but the interface should be made explicit before implementation freeze.

Required closure:

~~~text
CARD / DEALER AUTHORITY
        ↓
Canonical Card State / Assignment Result
        ↓
ENGINE 15
Poker-rule validation using that state
~~~

Engine 15 must not independently select between competing card assignments.

---

# 7. Residual Issue A — Uncalled Bets

**Severity: HIGH — normative poker rule completeness**

Engine 15 defines contribution-based pot construction but does not explicitly define the normative treatment of an **uncalled excess wager**.

Example:

~~~text
Player A: 100
Player B: 40
Player A bets 60 more
Player B can only call 40
~~~

The uncalled portion must not remain as a contested pot contribution merely because it was temporarily committed as an action amount.

The rules specification needs an explicit invariant separating:

~~~text
PROPOSED WAGER
COMMITTED CONTRIBUTION
UNCALLED RETURN
FINAL HAND CONTRIBUTION
~~~

Pot construction must use the final valid contribution after any required uncalled amount is returned.

### Required closure

Add an explicit normative rule:

~~~text
UncalledAmount
    ↓
returned to originating player
    ↓
final contribution state
    ↓
pot construction
~~~

Without this clarification, the pot-layer algorithm is deterministic but incomplete for a class of legal betting states.

---

# 8. Residual Issue B — Canonical Event Boundary

**Severity: MEDIUM — integration contract**

Engine 15 correctly states:

~~~text
Proposed Action
    ↓
Poker Rules Engine
    ↓
LEGAL
    ↓
Accepted Game Event
~~~

However, the README does not define the canonical semantic identity of the accepted poker transition/event.

It should not invent a new global event registry inside Engine 15.

Instead, Engine 15 should explicitly state that its output is a **Poker Rule Transition Result**, which is then encoded into the protocol's canonical event schema by the event/ledger layer.

Recommended conceptual contract:

~~~text
PokerRuleTransitionResult {
    hand_id
    ruleset_id
    ruleset_version
    actor_id
    action
    previous_state_reference
    resulting_state_reference
    transition_result
}
~~~

The exact event identifier and wire schema should remain under the protocol event registry.

---

# 9. Residual Issue C — Card/Dealer Input Contract

**Severity: MEDIUM — interface precision**

Engine 15 currently contains sufficient poker-level card invariants, but the interface should explicitly identify the authoritative card/dealer output consumed by the Rules Engine.

Recommended conceptual distinction:

~~~text
Card / Dealer Engine
    =
card-state authority

Poker Rules Engine
    =
rules authority over the game using that card state
~~~

This avoids any interpretation that Engine 15 can independently generate or select cards during replay.

---

# 10. State / Identifier Audit

**Result: PASS**

The v2.1 specification explicitly binds:

~~~text
hand_id
ruleset_id
ruleset_version
pot_id
~~~

It also uses existing architectural identifiers such as:

~~~text
table_id
request_id
settlement_id
event_id
~~~

where applicable through external interfaces.

No contradictory identifier ownership was found.

A future canonical identifier registry should still define exact formats and namespaces globally.

---

# 11. Lifecycle Audit

**Result: PASS**

Engine 15 owns:

~~~text
HAND_START
PREFLOP
FLOP
TURN
RIVER
SHOWDOWN
HAND_END
~~~

It does not claim ownership of:

- table lifecycle;
- seat lifecycle;
- wallet lifecycle;
- node lifecycle;
- session lifecycle;
- disconnection lifecycle.

This matches the documented separation in Engines 09, 10 and 13.

No lifecycle authority inversion was found.

---

# 12. Invalid-Action Audit

**Result: PASS**

Engine 15 explicitly defines:

~~~text
INVALID ACTION
        ↓
NO NORMATIVE STATE MUTATION
~~~

This is compatible with event-sourced reconstruction and PCRE replay.

Invalid actions are therefore not silently converted into state transitions.

---

# 13. Replay Audit

**Result: PASS**

Engine 15 binds deterministic replay to:

~~~text
same state
+
same ruleset
+
same action
=
same normative result
~~~

Engine 14 requires deterministic replay and state-hash verification.

The two specifications are architecturally compatible.

The remaining integration requirement is to ensure the replay input includes the authoritative card/dealer state and all ruleset configuration required by Engine 15.

---

# 14. Pot / Settlement Boundary Audit

**Result: PASS**

Engine 15 determines:

~~~text
pot amount
eligible players
winning players
division
~~~

Engine 05 may then derive monetary obligations from the completed poker result.

Engine 12 executes the authorized settlement.

No monetary execution authority has leaked into Engine 15.

---

# 15. Consensus Boundary Audit

**Result: PASS**

Engine 15 explicitly does not determine:

- canonical history;
- checkpoint selection;
- validator consensus;
- node preference;
- network ordering.

Engine 14 handles conflict resolution and canonical-state reconstruction.

This is the correct authority separation.

---

# 16. Governance / Ruleset Audit

**Result: PASS WITH CONFIGURATION REQUIREMENT**

Engine 15 correctly makes the ruleset version part of the hand's deterministic input.

A rules change therefore produces a new ruleset rather than mutating the meaning of an existing hand.

The remaining global requirement is that the governance/configuration layer must provide an immutable, resolvable ruleset reference for the table/hand.

Engine 15 should consume that reference, not select it autonomously.

---

# 17. Audit Matrix

| Area | Result | Residual issue |
|---|---|---|
| Poker authority | PASS | None |
| Engine 13 boundary | PASS | None |
| Engine 14 / PCRE boundary | PASS | None |
| Engine 12 settlement boundary | PASS | None |
| Engine 04 ledger boundary | PASS | None |
| Engine 06 card privacy | PASS | Interface naming |
| Engine 07 card distribution | PASS | Interface naming |
| Player state | PASS | None |
| Turn authority | PASS | None |
| Betting semantics | PASS | Uncalled bet closure needed |
| Raise/reopen | PASS | Test vectors should cover implementation |
| Pot construction | CONDITIONAL | Uncalled excess must be explicit |
| Showdown | PASS | None |
| Hand ranking | PASS | None |
| Split/odd chip | PASS | Ruleset policy must be resolved |
| Lifecycle | PASS | None |
| Replay | PASS | Card-state input must be explicit |
| Event boundary | CONDITIONAL | Canonical transition/event interface needed |
| Settlement | PASS | None |
| Consensus | PASS | None |
| Ruleset identity | PASS | Global configuration registry required |

---

# 18. Audit Conclusion

Engine 15 v2.1 is **architecturally sound and substantially integration-ready**.

The audit found no residual contradiction in which another documented engine claims authority over poker legality, hand evaluation, pot eligibility or poker outcomes.

However, Engine 15 should **not yet be marked FROZEN**.

Before freezing, the following three items should be closed:

~~~text
1. UNCALLED BET / EXCESS WAGER RULE
2. POKER RULE TRANSITION → CANONICAL EVENT INTERFACE
3. CARD / DEALER STATE INPUT CONTRACT
~~~

Once these are explicitly resolved and the corresponding conformance tests are added, a final Engine 15 freeze audit can be performed.

**AUDIT STATUS: CONDITIONAL PASS**

**FROZEN: NO**

**NEXT REQUIRED STATE: FINAL INTEGRATION CORRECTION**
