# CHAIN POKER GENESIS BY LAEV

# 10 — Player Node Disconnection Management Engine

## Official Technical Specification v1.1

**Document Class:** CORE ENGINE  
**Document Status:** CONSOLIDATED / CORRECTED / INTEGRATION-READY  
**Architecture Role:** Player Node Connection, Reconnection, Absence and Disconnection Management  
**Previous Specification:** v1.0  
**Revision:** v1.1  
**Protocol:** Chain Poker Genesis by LAEV

---

# 0. Document Control

~~~text
[LCCP]
SEQ: 10
PREV: 9
SELF: 10
NEXT: 11
CLASS: CORE ENGINE
STATUS: CONSOLIDATED
[/LCCP]
~~~

This specification governs communication loss, reconnection, synchronization, temporary absence, abandonment processing and participant-removal workflow.

The engine preserves separation between connection state, participant membership, poker/game state, table consensus, Table Wallet authorization, monetary settlement and historical evidence.

Engine 10 does not replace any of those authorities.

---

# 1. Purpose

The Player Node Disconnection Management Engine manages the protocol response when a player node temporarily or persistently loses communication with a poker table.

Its responsibilities are:

- detect or receive node-disconnection conditions;
- maintain connection-state transitions;
- start and enforce the configured reconnection timeout;
- coordinate reconnection attempts;
- coordinate state synchronization;
- track participant absence;
- determine when the configured abandonment condition is satisfied;
- initiate the participant-removal workflow;
- preserve the active-hand lifecycle;
- generate canonical disconnection and absence events;
- provide sufficient evidence for historical reconstruction.

A disconnection is initially a communication event, not a financial event and not an automatic membership-removal event.

---

# 2. Architectural Boundary

Engine 10 is a disconnection and absence-management component.

It is not:

- the Poker Rules Engine;
- the Table Join Engine;
- the Table Wallet Engine;
- the Monetary Settlement Engine;
- the Table Consensus authority;
- the Cryptographic Engine;
- the Private Off-Chain Ledger Engine;
- the payment or settlement rail.

~~~text
COMMUNICATIONS / SESSION
        ↓
ENGINE 10
        ↓
CONNECTION / ABSENCE MANAGEMENT
        ↓
POKER RULES / TABLE STATE
        ↓
TABLE MEMBERSHIP
        ↓
TABLE CONSENSUS / AUTHORIZATION
        ↓
TABLE WALLET ENGINE
        ↓
MONETARY SETTLEMENT
        ↓
PRIVATE OFF-CHAIN LEDGER EVIDENCE
~~~

Engine 10 generates protocol events and state-transition requests. The authoritative receiving engines retain their respective decision and execution authority.

---

# 3. Fundamental Principle

A temporary communication failure does not by itself mean that a player has abandoned the table.

The protocol therefore separates:

~~~text
CONNECTION STATE
~~~

from:

~~~text
PARTICIPANT STATE
~~~

A participant may remain an official table participant while its node is disconnected.

Example:

~~~text
table_participant_state = JOINED
connection_state = DISCONNECTED
~~~

No participant removal occurs merely because a connection was lost.

---

# 4. Connection State Machine

Canonical connection states:

~~~text
CONNECTED
DISCONNECTED
RECONNECTING
SYNCHRONIZING
RECONNECTED
~~~

Canonical recovery path:

~~~text
CONNECTED
    ↓
DISCONNECTED
    ↓
RECONNECTING
    ↓
SYNCHRONIZING
    ↓
RECONNECTED
    ↓
CONNECTED
~~~

RECONNECTED identifies successful protocol recovery. Normal operation resumes only after required synchronization and state verification.

---

# 5. Participant State Machine

Participant membership is independent from connection state.

Canonical participant states:

~~~text
JOINED
ACTIVE
ABSENT
ABANDONED
REMOVED
~~~

A temporary communication failure may produce:

~~~text
JOINED + DISCONNECTED
~~~

or, when the configured absence policy applies:

~~~text
ABSENT + DISCONNECTED
~~~

Only after the abandonment condition is satisfied may the participant enter:

~~~text
ABANDONED
~~~

REMOVED is a separate state indicating that the authorized membership-removal operation has actually been applied.

---

# 6. Identity Model

Disconnection events must distinguish:

~~~text
table_id
table_participant_id
player_id
player_node_id
~~~

player_id identifies the player across the protocol.

table_participant_id identifies that player's participation in one specific table.

player_node_id identifies the node whose communication state is being managed.

A player may participate in multiple tables without sharing table-participant identities.

---

# 7. Disconnection Detection

When communication loss is detected or reported:

1. The Communications / Session Layer identifies the loss.
2. Engine 10 receives or records the condition.
3. Connection state transitions to DISCONNECTED.
4. The configured reconnection policy is loaded.
5. A reconnection timer is started when applicable.
6. A canonical disconnection event is generated.

~~~text
CONNECTION LOSS
      ↓
NODE_DISCONNECTION_DETECTED
      ↓
CONNECTION_STATE = DISCONNECTED
      ↓
RECONNECTION TIMER
~~~

Engine 10 does not infer financial loss from the communication failure.

---

# 8. Timeout Policies

The protocol distinguishes:

~~~text
reconnection_timeout
~~~

from:

~~~text
consecutive_absence_limit
~~~

reconnection_timeout controls the maximum configured period for restoring communication and completing required synchronization for the current disconnection episode.

consecutive_absence_limit controls the configured number of consecutive hands or other table-defined absence units after which the participant may be classified as abandoned.

These are separate parameters.

---

# 9. Disconnection During an Active Hand

A disconnection during an active hand does not automatically terminate the hand.

The hand remains governed by the Poker Rules Engine.

~~~text
PLAYER DISCONNECTED
        ↓
HAND CONTINUES
        ↓
POKER RULES APPLY ABSENT-PLAYER BEHAVIOR
        ↓
HAND_COMPLETED
        ↓
MONETARY SETTLEMENT
        ↓
PARTICIPANT REMOVAL PROCESS, IF REQUIRED
~~~

The active hand's authoritative participant and monetary context must not be retroactively changed solely because a node disconnected.

A participant-removal operation must not invalidate or rewrite an already-started hand.

---

# 10. Absent-Player Behavior

Engine 10 does not define poker action legality.

When a disconnected player reaches a point where the Poker Rules Engine requires a game-state consequence, the Poker Rules Engine applies the configured rules for an absent player.

Engine 10 supplies communication and absence state as protocol input.

It does not independently determine check, fold, call, bet, timeout action, winner, pot allocation or side-pot outcome.

---

# 11. Reconnection Attempt

When the player node attempts to reconnect:

~~~text
DISCONNECTED
      ↓
RECONNECTING
      ↓
RECONNECTION_ATTEMPTED
~~~

A successful transport-level reconnection does not immediately authorize normal operation. The node must proceed through synchronization.

---

# 12. Synchronization Lifecycle

~~~text
RECONNECTING
      ↓
SYNCHRONIZING
      ↓
STATE VERIFIED
      ↓
RECONNECTED
~~~

Synchronization reconciles, as applicable:

- authoritative table state;
- table participant state;
- current hand state;
- action history;
- participant-visible monetary state;
- table position;
- protocol configuration;
- required engine state;
- applicable authorization state.

Private data remains subject to its own privacy and cryptographic boundaries.

---

# 13. Versioned Table-State Synchronization

Engine 10 uses the authoritative table-state versioning established by the Table Join Engine.

The synchronization process uses at least:

~~~text
table_state_version
table_state_hash
~~~

~~~text
NODE RECONNECT
      ↓
LAST KNOWN TABLE STATE VERSION
      ↓
COMPARE WITH AUTHORITATIVE VERSION
      ↓
SYNCHRONIZATION
      ↓
VERIFY TABLE STATE HASH
      ↓
SYNCHRONIZED
~~~

A stale or divergent state must not be treated as synchronized.

---

# 14. Successful Reconnection

A node may transition to RECONNECTED only after:

- communication is available;
- node identity is authenticated as required;
- required table state is synchronized;
- table_state_version is reconciled;
- table_state_hash is verified;
- required protocol authorization is restored.

~~~text
NODE_SYNCHRONIZED
      ↓
RECONNECTED
~~~

The participant does not lose membership merely because synchronization took time.

---

# 15. Reconnection Failure

If the node cannot successfully reconnect before reconnection_timeout:

~~~text
RECONNECTION_TIMEOUT
      ↓
ABSENCE POLICY
      ↓
PLAYER_MARKED_ABSENT
~~~

The participant remains distinct from REMOVED.

If the configured consecutive absence condition is not yet satisfied, the participant may remain associated with the table while absent.

---

# 16. Abandonment

Abandonment is a participant-state conclusion, not a connection-state synonym.

~~~text
DISCONNECTED
      ↓
ABSENT
      ↓
absence policy satisfied
      ↓
ABANDONED
~~~

The abandonment condition must be deterministic and based on the table's configured policy.

Engine 10 may determine that the configured abandonment condition has been satisfied and generate the corresponding protocol event, but final membership removal remains subject to table-state and authorization boundaries.

---

# 17. Participant Removal

~~~text
ABANDONMENT DECLARED
        ↓
PLAYER_REMOVAL_REQUESTED
        ↓
MEMBERSHIP UPDATE
        ↓
TABLE STATE UPDATE
        ↓
CONSENSUS / AUTHORIZATION
        ↓
REMOVED
~~~

REMOVED means that the participant is no longer part of the authoritative table participant set.

The seat becomes available only after the removal state has been validly applied.

A temporary disconnection never directly releases a seat.

---

# 18. Table Join Engine Relationship

The canonical component name is:

~~~text
Table Join Engine
~~~

Engine 10 does not replace the Table Join Engine.

The Table Join Engine owns initial participant admission and later re-entry.

After a valid removal operation, a subsequent return must follow the Table Join Engine admission protocol.

---

# 19. Table-State Change

Participant removal produces a table-state transition.

~~~text
PLAYER_ABANDONED
        ↓
PLAYER_REMOVAL_REQUESTED
        ↓
TABLE MEMBERSHIP UPDATE
        ↓
TABLE_STATE_UPDATED
        ↓
TABLE_COMPOSITION_CHANGED
~~~

The resulting authoritative state contains the current participant set and corresponding version/hash representation.

Engine 10 does not independently rewrite historical table state.

---

# 20. Table Consensus Boundary

Changes to authoritative table participant composition must pass through the applicable Table Consensus / authorization mechanism.

Engine 10 may initiate the removal workflow but does not unilaterally establish a new cryptographic participant composition.

~~~text
ENGINE 10
      ↓
REMOVAL REQUEST
      ↓
TABLE STATE / MEMBERSHIP AUTHORITY
      ↓
TABLE CONSENSUS / AUTHORIZATION
      ↓
AUTHORIZED PARTICIPANT COMPOSITION
~~~

The exact consensus threshold and algorithm are defined by dedicated specifications.

---

# 21. Table Wallet Boundary

Engine 10 does not create, modify or regenerate a Table Wallet configuration unilaterally.

When the authoritative participant composition changes:

~~~text
PARTICIPANT COMPOSITION CHANGED
        ↓
TABLE CONSENSUS / AUTHORIZATION
        ↓
AUTHORIZED PARTICIPANT COMPOSITION
        ↓
TABLE WALLET ENGINE
        ↓
NEW CRYPTOGRAPHIC CONFIGURATION IF REQUIRED
~~~

The Table Wallet Engine remains the authority for wallet cryptographic configuration and lifecycle.

Engine 10 supplies the participant-state transition that may require downstream reconfiguration.

---

# 22. Table Wallet Instance vs Configuration

The protocol distinguishes:

~~~text
TABLE_WALLET_INSTANCE
~~~

from:

~~~text
TABLE_WALLET_CRYPTOGRAPHIC_CONFIGURATION
~~~

A participant-state change does not automatically imply creation of a new wallet instance.

~~~text
composition unchanged
      ↓
no cryptographic reconfiguration required
~~~

When the authoritative composition changes:

~~~text
composition changed
      ↓
new authorized cryptographic configuration required
~~~

Whether a new wallet instance is created is governed by the Table Wallet lifecycle and applicable policy.

Engine 10 must never silently change authorized signers.

---

# 23. Protection of an Active Monetary Context

A participant removal must not retroactively alter the cryptographic authorization or monetary context of an already-started hand.

The active hand reaches:

~~~text
HAND_COMPLETED
~~~

before a participant-composition change becomes authoritative for subsequent table operations, except where a dedicated protocol rule explicitly defines another safe boundary.

The Table Wallet Engine and Monetary Settlement Engine retain their respective monetary authorities.

---

# 24. Monetary Boundary

A communication failure is not itself a monetary settlement event.

Engine 10 does not calculate:

- wager amounts;
- pot amounts;
- rake;
- winners;
- refunds;
- settlement outputs.

The distinction is:

~~~text
AUTHORIZED WAGER
      ↓
TABLE WALLET / PAYMENT RAIL
      ↓
HAND_COMPLETED
      ↓
ENGINE 05
      ↓
SETTLEMENT PLAN
      ↓
MONETARY SETTLEMENT
~~~

Engine 10 uses WAGER VALUE TRANSFER / FUNDING for wager movement and FINAL MONETARY SETTLEMENT for final hand settlement.

---

# 25. Monetary Safety Principle

A disconnection alone does not create a new monetary obligation.

Any unresolved monetary condition remains governed by the applicable:

- Table Wallet procedures;
- Monetary Settlement procedures;
- payment/settlement adapter;
- recovery procedures;
- reconciliation procedures.

Engine 10 does not promise that every possible external payment or recovery condition is instantaneously resolved.

It ensures that communication loss does not itself become an unauthorized settlement instruction.

---

# 26. Engine 05 Integration

Engine 05 owns the rake obligation and settlement-request boundary defined by its specification.

~~~text
DISCONNECTION
      ↓
ABSENCE / ACTION CONSEQUENCE
      ↓
POKER RULES
      ↓
HAND_COMPLETED
      ↓
ENGINE 05
      ↓
RAKE / SETTLEMENT OBLIGATION
      ↓
MONETARY SETTLEMENT
~~~

Engine 10 does not determine winner, rake eligibility, rake amount, settlement obligation or final settlement outputs.

---

# 27. Audit Event Model

Engine 10 generates protocol events. It does not replace the Private Off-Chain Ledger Engine.

Minimum canonical events:

~~~text
NODE_DISCONNECTION_DETECTED
RECONNECTION_TIMER_STARTED
RECONNECTION_ATTEMPTED
NODE_RECONNECTED
NODE_SYNCHRONIZATION_STARTED
NODE_SYNCHRONIZED
RECONNECTION_TIMEOUT
PLAYER_MARKED_ABSENT
PLAYER_ABANDONED
PLAYER_REMOVAL_REQUESTED
PLAYER_REMOVED
TABLE_STATE_UPDATED
TABLE_COMPOSITION_CHANGED
~~~

Table Wallet events remain under the Table Wallet domain, including where applicable:

~~~text
TABLE_WALLET_RECONFIGURATION_REQUESTED
TABLE_WALLET_RECONFIGURATION_AUTHORIZED
~~~

Engine 10 may reference those events but does not manufacture wallet authorization.

---

# 28. Event Record Requirements

A disconnection-related event should contain, when applicable:

~~~text
event_id
event_type
event_version
event_timestamp
table_id
table_participant_id
player_id
player_node_id
hand_id
connection_state
participant_state
table_state_version
table_state_hash
authorization_reference
event_hash
~~~

hand_id may be absent when the event occurs outside an active hand.

The Private Off-Chain Ledger Engine remains responsible for event normalization, persistence, cryptographic evidence and historical reconstruction.

---

# 29. Auditability

The event model must permit reconstruction of:

- when the node disconnected;
- which table participant was affected;
- which hand, if any, was active;
- how long the node remained unavailable;
- when reconnection was attempted;
- whether synchronization succeeded;
- when the participant became absent;
- when abandonment was declared;
- when removal was requested;
- when removal became authoritative;
- which table-state version resulted;
- which authorization reference supported the membership change.

The audit record must distinguish observed events from authoritative state transitions.

---

# 30. Table Continuity

Participant removal does not automatically close the table.

~~~text
PLAYER_REMOVED
      ↓
RECALCULATE ACTIVE PARTICIPANT COUNT
      ↓
      ├── active participants >= minimum_players
      │          ↓
      │       CONTINUE
      │
      └── active participants < minimum_players
                 ↓
          WAITING_FOR_PLAYERS
~~~

The exact transition is governed by the table/game lifecycle.

PLAYER_REMOVED and TABLE_CLOSED are independent states.

---

# 31. Seat Availability

A seat becomes available only after participant removal has become authoritative.

~~~text
ABANDONED
      ↓
REMOVAL REQUESTED
      ↓
MEMBERSHIP UPDATE
      ↓
REMOVED
      ↓
SEAT AVAILABLE
~~~

A disconnected or merely absent participant continues to occupy its seat unless the authorized membership process explicitly removes it.

---

# 32. Re-entry After Removal

A player whose participant state is REMOVED is no longer a participant of the table.

A subsequent return must use the Table Join Engine.

~~~text
REMOVED
      ↓
NEW JOIN REQUEST
      ↓
TABLE JOIN ENGINE
      ↓
NEW TABLE PARTICIPANT ID
~~~

Engine 10 does not bypass admission controls.

---

# 33. Security Invariants

1. DISCONNECTED does not imply REMOVED.
2. Connection state and participant state are independent.
3. A disconnected player does not automatically lose table membership.
4. An active hand is not retroactively invalidated by communication loss.
5. Engine 10 does not determine poker outcomes.
6. Engine 10 does not calculate rake.
7. Engine 10 does not execute final monetary settlement.
8. Engine 10 does not change Table Wallet authorized signers unilaterally.
9. Participant composition changes require the applicable table-state and authorization process.
10. A seat is not released merely because a node disconnected.
11. Reconnection requires state synchronization and verification.
12. Stale or divergent table state must not be accepted as synchronized.
13. Every material disconnection transition must be auditable.
14. Table Wallet instance and cryptographic configuration remain distinct.
15. Removal of a player does not by itself close the table.

---

# 34. Determinism

For identical canonical inputs and identical configured policies, Engine 10 must produce deterministic state-transition results.

Relevant inputs include:

~~~text
table_id
table_participant_id
connection event
authoritative table state
reconnection_timeout
consecutive_absence_limit
protocol version
table-state version
applicable authorization state
~~~

Time-dependent decisions must use protocol-defined timestamps and policy boundaries rather than local UI interpretation.

---

# 35. Failure and Recovery

Engine 10 distinguishes at least:

~~~text
CONNECTION_FAILURE
RECONNECTION_FAILURE
SYNCHRONIZATION_FAILURE
STATE_DIVERGENCE
RECONNECTION_TIMEOUT
REMOVAL_PROCESS_FAILURE
~~~

A synchronization failure must not be represented as successful reconnection.

A table-state divergence must not be silently overwritten by the reconnecting node's local state.

A participant-removal failure must not be represented as REMOVED until the authoritative membership transition has succeeded.

---

# 36. Configuration Parameters

At minimum, table policy must define:

~~~text
reconnection_timeout
consecutive_absence_limit
minimum_players
~~~

The protocol may define additional parameters for:

- synchronization retry policy;
- reconnection retry interval;
- maximum synchronization delay;
- removal retry policy;
- table-specific absence rules.

Operational defaults must be defined by the applicable table configuration.

---

# 37. End-to-End Lifecycle

~~~text
CONNECTED
    ↓
NODE_DISCONNECTION_DETECTED
    ↓
DISCONNECTED
    ↓
RECONNECTION_TIMER_STARTED
    ↓
┌──────────────────────────────┐
│                              │
│ reconnect succeeds           │ timeout / failure
│                              │
↓                              ↓
RECONNECTING               ABSENT
↓                              ↓
SYNCHRONIZING             absence policy
↓                              ↓
STATE VERIFIED             ABANDONED
↓                              ↓
RECONNECTED               REMOVAL REQUESTED
                               ↓
                         MEMBERSHIP UPDATE
                               ↓
                         TABLE CONSENSUS /
                         AUTHORIZATION
                               ↓
                            REMOVED
                               ↓
                    TABLE COMPOSITION CHANGED
                               ↓
                       TABLE WALLET ENGINE
                     CONFIGURATION IF REQUIRED
~~~

For an active hand, the game lifecycle remains independently:

~~~text
DISCONNECTION
      ↓
HAND CONTINUES
      ↓
HAND_COMPLETED
      ↓
MONETARY SETTLEMENT
~~~

The two lifecycles must not be conflated.

---

# 38. Engine Relationship Matrix

| Component | Engine 10 Relationship |
|---|---|
| Communications / Session | Supplies or detects connection events |
| Table Join Engine | Owns initial participant admission and later re-entry |
| Poker Rules Engine | Owns hand consequences and poker legality |
| Table Consensus / Authorization | Authorizes authoritative participant-composition changes |
| Table Wallet Engine | Owns Table Wallet configuration and lifecycle |
| Engine 05 — Rake / Settlement Flow | Owns rake obligation and settlement-request boundary |
| Monetary Settlement Engine | Owns final monetary settlement execution |
| Private Off-Chain Ledger Engine | Persists and verifies historical evidence |
| Cryptographic Engine | Provides cryptographic validation where required |

---

# 39. Final Architectural Rule

The Player Node Disconnection Management Engine has one primary authority domain:

~~~text
DISCONNECTION
+
RECONNECTION
+
SYNCHRONIZATION
+
ABSENCE
+
ABANDONMENT WORKFLOW
~~~

It does not become:

~~~text
TABLE WALLET AUTHORITY
POKER RULES AUTHORITY
MONETARY SETTLEMENT AUTHORITY
TABLE CONSENSUS AUTHORITY
PRIVATE LEDGER AUTHORITY
~~~

The central protocol rule is:

~~~text
CONNECTION FAILURE
        ≠
PLAYER ABANDONMENT
        ≠
PLAYER REMOVAL
        ≠
TABLE WALLET RECONFIGURATION
        ≠
MONETARY SETTLEMENT
~~~

Each transition is handled by its proper architectural authority.

---

# 40. Integration Status

This v1.1 revision incorporates the required corrections identified during architectural review against Engines 05, 08 and 09.

The specification is intended for the subsequent integrated audit of:

~~~text
01 → 10
~~~

It must not be marked FROZEN until that audit confirms:

- no remaining contradiction with Engine 08;
- no remaining contradiction with Engine 09;
- no remaining contradiction with Engine 05;
- consistent event naming;
- consistent identity naming;
- consistent authority boundaries;
- consistent table-state version/hash handling;
- consistent active-hand lifecycle;
- consistent Table Wallet configuration lifecycle.

**Status: CONSOLIDATED / CORRECTED / INTEGRATION-READY**

---

© 2026 Lerry Alexander Elizondo Villalobos (LAEV).  
Chain Poker Genesis by LAEV.
