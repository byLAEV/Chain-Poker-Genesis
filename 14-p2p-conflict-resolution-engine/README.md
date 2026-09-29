# CHAIN POKER GENESIS BY LAEV

## P2P Conflict Resolution Engine

### Official Technical Specification v1.1

**Engine ID:** 14  
**Component:** P2P Conflict Resolution Engine (PCRE)  
**Status:** REVISION 14.1 — AUDIT PENDING  
**Classification:** Core Protocol Engine

---

## 1. Purpose

The P2P Conflict Resolution Engine (PCRE) is an independent protocol subsystem responsible for detecting, classifying, analyzing, and deterministically resolving divergences between nodes concerning the canonical state of a CHAIN POKER GENESIS game.

The PCRE operates without modifying the immutable event history.

Its purpose is to ensure that, within the protocol's defined consensus and Byzantine-fault assumptions, participating nodes can converge on the same canonical game state despite:

- network latency;
- packet loss;
- retransmission;
- temporary disconnection;
- out-of-order delivery;
- duplicate submissions;
- conflicting valid observations;
- state-hash divergence;
- temporary event-ledger forks;
- protocol violations;
- malicious attempts to manipulate protocol state.

The PCRE does not replace the Validator Consensus mechanism, the Request & Permission Engine, the Player/Node Disconnection Management Engine, or the Monetary Settlement Engine.

---

## 2. Architectural Authority Boundary

The PCRE is a resolution engine, not a sovereign authority over the protocol.

Its responsibilities are limited to:

1. detecting divergence;
2. classifying the divergence;
3. validating available evidence;
4. performing deterministic replay;
5. determining whether the conflict can be resolved deterministically;
6. requesting validator consensus when deterministic resolution is insufficient;
7. constructing the canonical resolution result;
8. initiating deterministic state reconstruction;
9. producing auditable conflict evidence.

The PCRE does NOT independently:

- grant protocol permissions;
- authorize operations belonging to Engine 13;
- define player/node lifecycle;
- execute monetary settlement;
- alter the immutable event ledger;
- unilaterally override validator consensus;
- directly impose reputation or economic penalties.

---

## 3. Separation from Validator Consensus

Validator Consensus is an external protocol mechanism invoked by the PCRE only when deterministic evidence is insufficient to establish a canonical result.

The relationship is:

```text
PCRE
  ↓
Conflict Detection
  ↓
Evidence Validation
  ↓
Deterministic Replay
  ↓
Deterministically Resolvable?
     ├── YES → Canonical Resolution
     │
     └── NO
          ↓
     Validator Consensus
          ↓
     Consensus Result
          ↓
     PCRE Resolution Record
```

The PCRE therefore does not become the validator authority.

Validator Consensus determines the distributed consensus result according to the protocol's consensus rules.

The PCRE consumes that result and incorporates it into the final conflict-resolution record.

---

## 4. Core Responsibilities

### 4.1 Conflict Detection

The PCRE detects:

- out-of-order events;
- duplicate event submissions;
- conflicting events;
- invalid sequence numbers;
- invalid state references;
- invalid timestamps where timestamps are protocol-relevant;
- state-hash mismatches;
- invalid event-chain relationships;
- temporary event-ledger forks;
- deterministic replay divergence;
- cryptographic inconsistencies;
- protocol-rule inconsistencies.

---

## 5. Conflict Classification

Each detected conflict receives a deterministic classification.

Possible classifications include:

- Synchronization Conflict;
- Latency Conflict;
- Retransmission/Duplicate Conflict;
- Sequence Conflict;
- State Conflict;
- Cryptographic Conflict;
- Event-Chain Conflict;
- Consensus Conflict;
- Protocol Rule Conflict;
- Malicious Behavior Conflict.

Classification does not itself establish malicious intent.

A duplicate or retransmitted event MUST NOT automatically be classified as malicious.

---

## 6. Evidence Validation Chain

The PCRE does not resolve conflicts merely according to message arrival time.

Evidence is processed through the following deterministic validation chain before consensus escalation:

```text
1. Cryptographic Validity
        ↓
2. Event Identity and Uniqueness
        ↓
3. Sequence Validity
        ↓
4. Previous Verified State
        ↓
5. Event-Chain / Hash Validity
        ↓
6. Protocol-Rule Validity
        ↓
7. Deterministic Replay
        ↓
8. State-Hash Verification
        ↓
9. Logical Timestamp, only where explicitly protocol-defined
        ↓
10. Physical Timestamp, informational only
        ↓
Deterministically Resolvable?
        ├── YES → Canonical Resolution
        │
        └── NO → Validator Consensus
```

Logical and physical timestamps MUST NOT override stronger cryptographic, sequence, state, event-chain, rule, replay, or state-hash evidence. A timestamp may participate in deterministic resolution only where an authoritative protocol rule explicitly defines it as a valid criterion. Validator Consensus is an escalation mechanism after deterministic evidence has been evaluated; it is not another evidence priority level within the deterministic chain.

### 6.1 Cryptographic Validity

The event MUST contain valid cryptographic evidence according to the applicable protocol requirements.

A valid signature proves authorization of the signed message by its signing identity.

A valid signature alone does NOT establish that the event is valid within the current game state.

### 6.2 Event Identity

The PCRE MUST determine whether the event is:

- new;
- an exact retransmission;
- a duplicate with conflicting contents;
- or an independently conflicting event.

### 6.3 Sequence Validity

The event sequence MUST be compatible with the canonical predecessor state.

### 6.4 Previous Verified State

The event MUST reference a valid predecessor state or event according to the applicable protocol structure.

### 6.5 Event-Chain / Hash Validity

The event's cryptographic relationship with its predecessor and applicable event chain MUST be valid.

### 6.6 Protocol-Rule Validity

The event MUST be compatible with the applicable game and protocol rules.

### 6.7 Deterministic Replay

The PCRE MUST be capable of replaying the applicable event sequence using only protocol-defined deterministic inputs.

### 6.8 State-Hash Verification

The resulting state MUST produce the expected canonical state hash.

---

## 7. Latest Valid Checkpoint

A `LATEST_VALID_CHECKPOINT` is the protocol-valid checkpoint with the greatest protocol-defined checkpoint sequence within the same canonical verified state lineage.

A checkpoint is valid only when all applicable conditions are satisfied:

```text
CHECKPOINT_VALID =
    valid checkpoint identity
    AND valid cryptographic evidence
    AND valid predecessor reference
    AND valid sequence
    AND valid event-chain relationship
    AND valid event/state root
    AND deterministic replay compatibility
    AND resulting state hash matches checkpoint state hash
```

Checkpoint ordering MUST be determined by the authoritative checkpoint sequence and state-lineage rules of the protocol.

A checkpoint MUST NOT become the latest valid checkpoint merely because it is:

- received first;
- physically newer;
- broadcast by a particular node;
- stored by a majority of nodes;
- or locally considered current.

If two or more checkpoints are valid and belong to incompatible state lineages at the same applicable sequence position, the PCRE MUST classify the condition as unresolved and invoke the applicable Validator Consensus procedure.

A physically newer checkpoint MUST NOT override an earlier checkpoint from the canonical lineage unless the protocol-defined checkpoint sequence and lineage rules establish that the newer checkpoint is the valid successor.

---

## 8. Deterministic Game Consensus

When nodes disagree regarding the game state, the PCRE first attempts deterministic reconstruction.

Each participating node:

1. identifies the latest valid checkpoint;
2. loads the immutable event history after that checkpoint;
3. validates the applicable events;
4. executes deterministic replay;
5. calculates the resulting state hash.

If the applicable protocol conditions establish the same resulting canonical state:

```text
STATE ACCEPTED
```

If deterministic evidence does not establish one canonical result:

```text
CONSENSUS REQUIRED
```

The PCRE cannot substitute its own unilateral preference for the consensus mechanism.

---

## 9. Deterministic Replay

The PCRE MUST be capable of reconstructing the applicable game state exclusively from:

- immutable events;
- event identifiers;
- event hashes;
- cryptographic signatures;
- valid checkpoints;
- protocol-defined state references;
- Texas Hold'em rules;
- Genesis Virtual Machine deterministic execution rules.

No external information is required to reconstruct the canonical game state.

Physical network arrival time MUST NOT become an input into deterministic game-state computation unless an explicit protocol rule defines it as such.

---

## 10. State Reconstruction Instead of Ledger Rollback

The PCRE does not roll back or rewrite the immutable event ledger.

The ledger remains historically immutable.

When an invalid or non-canonical event is identified, the PCRE performs:

```text
Identify latest valid checkpoint
        ↓
Identify applicable valid events
        ↓
Exclude invalid/non-canonical events from canonical replay
        ↓
Replay remaining valid events
        ↓
Calculate canonical state
        ↓
Produce canonical state hash
```

Therefore:

> The PCRE performs deterministic state reconstruction, not historical ledger deletion.

Invalid events remain auditable as historical observations or protocol-invalid records according to the ledger specification.

---

## 11. Duplicate and Retransmission Handling

The PCRE distinguishes between:

### 11.1 Exact Retransmission

Same event identity and same valid content.

Result:

```text
RETRANSMISSION
```

The event is not interpreted as a second game action.

### 11.2 Duplicate Submission

Same event identity submitted more than once.

Result:

```text
DUPLICATE_EVENT
```

The duplicate does not create an additional state transition.

### 11.3 Conflicting Duplicate

Same event identity but incompatible content.

Result:

```text
CONFLICTING_DUPLICATE
```

This requires evidence analysis.

### 11.4 Malicious Double Action

A protocol-defined violation in which an actor attempts to create incompatible state transitions through multiple actions.

Result:

```text
POTENTIAL_PROTOCOL_VIOLATION
```

Malicious classification MUST require evidence sufficient under the protocol's defined rules.

Network retransmission alone is not evidence of malicious behavior.

---

## 12. Malicious Behavior Detection

The PCRE may detect evidence consistent with:

- double signing;
- conflicting signed actions;
- state tampering;
- message manipulation;
- replay attacks;
- sequence manipulation;
- clock manipulation;
- invalid event-chain construction;
- unauthorized fork creation;
- event censorship attempts.

Detection produces an auditable finding.

Detection does not automatically imply a specific penalty.

---

## 13. Reputation and Penalty Boundary

The PCRE MUST NOT directly own the reputation or incentive policy.

Instead:

```text
PCRE
 ↓
Protocol Violation Evidence
 ↓
Violation Classification
 ↓
Applicable Reputation / Permission / Incentive System
 ↓
Policy-Defined Consequence
```

Possible consequences may include:

- warning;
- reputation reduction;
- reward reduction;
- temporary exclusion;
- validator-status removal;
- permanent reputation record.

The actual consequence MUST be determined by the protocol component responsible for reputation, permissions, incentives, or governance.

The PCRE supplies evidence and resolution data.

---

## 14. Formal Conflict Resolution Result

Every completed conflict-resolution procedure MUST produce a deterministic:

`CONFLICT_RESOLUTION_RESULT`

The conceptual structure is:

```text
CONFLICT_RESOLUTION_RESULT {

    conflict_id

    game_id

    table_id

    affected_sequence

    conflict_type

    candidate_event_ids

    evidence_set

    latest_valid_checkpoint

    canonical_parent_state

    resolution_method

    consensus_required

    consensus_result

    invalid_or_noncanonical_event_ids

    canonical_state_hash

    protocol_violation_detected

    resolution_status
}
```

---

## 15. Resolution Status

The PCRE recognizes the following resolution states:

```text
UNRESOLVED
```

Conflict exists but no resolution has yet been established.

```text
DETERMINISTICALLY_RESOLVED
```

The canonical result was established entirely through deterministic protocol evidence.

```text
CONSENSUS_REQUIRED
```

Deterministic evidence was insufficient and validator consensus is required.

```text
CONSENSUS_RESOLVED
```

Validator consensus produced the applicable canonical result.

```text
REJECTED
```

The candidate event or state was rejected as invalid or non-canonical.

```text
ESCALATED
```

The conflict requires a higher-level protocol procedure because the applicable resolution conditions cannot yet be satisfied.

---

## 16. State Resolution

Once the canonical result is established:

```text
CONFLICT_RESOLUTION_RESULT
        ↓
CANONICAL STATE IDENTIFIED
        ↓
DETERMINISTIC STATE RECONSTRUCTION
        ↓
STATE HASH VERIFIED
        ↓
FINAL STATE PROPAGATION
```

The PCRE MUST NOT modify historical events.

---

## 17. Integration with Engine 10

### Player / Node Disconnection Management Engine

Engine 10 remains authoritative for player/node disconnection lifecycle behavior.

A disconnection event does not automatically constitute a conflict.

The relationship is:

```text
Engine 10
    ↓
Detects / manages disconnection
    ↓
Produces lifecycle consequence/event
    ↓
PCRE observes event
    ↓
Only intervenes if state divergence or event conflict exists
```

The PCRE MUST NOT independently redefine the lifecycle semantics established by Engine 10.

If a disconnection causes different nodes to construct different valid state histories, the PCRE may resolve the resulting state divergence according to this specification.

---

## 18. Integration with Engine 12

### Monetary Settlement Engine

Engine 12 remains responsible for monetary settlement.

The PCRE resolves the canonical game state that settlement depends upon.

The relationship is:

```text
Game Events
     ↓
PCRE
     ↓
Canonical Game State
     ↓
Monetary Settlement Engine
     ↓
Settlement Result
```

The PCRE MUST NOT directly modify, override, or execute monetary settlement merely because a game-state conflict exists.

If settlement-related state is disputed, the canonical game state MUST first be resolved according to the PCRE and applicable consensus rules.

Engine 12 then applies its own settlement specification to the canonical state.

---

## 19. Integration with Engine 13

### Request & Permission Engine

Engine 13 remains authoritative for request and permission semantics.

The PCRE MUST NOT grant, revoke, or redefine permissions that belong to Engine 13.

The relationship is:

```text
Engine 13
    ↓
Request / Permission Determination
    ↓
Protocol-authorized event
    ↓
PCRE
    ↓
Conflict Detection / State Resolution
```

If a disputed event depends upon a permission established by Engine 13, the PCRE validates the event against the applicable permission result.

The PCRE may reject an event from the canonical state when its permission evidence is invalid.

The PCRE does NOT create a new permission merely because a conflict exists.

This prevents duplicate authority between Engine 13 and Engine 14.

---

## 20. Integration with Validator Consensus

The Validator Consensus mechanism is invoked only when deterministic evidence cannot establish a unique canonical result.

The PCRE:

1. identifies the unresolved conflict;
2. packages the relevant evidence;
3. identifies candidate states/events;
4. invokes the applicable consensus procedure;
5. receives the consensus result;
6. verifies that the returned result is internally valid;
7. records the result in `CONFLICT_RESOLUTION_RESULT`;
8. reconstructs the canonical state.

The PCRE cannot override a valid consensus result through unilateral preference.

---

## 21. Simplified Workflow

```text
EVENT RECEIVED
      ↓
CRYPTOGRAPHIC VALIDATION
      ↓
EVENT ID / DUPLICATE CHECK
      ↓
SEQUENCE VALIDATION
      ↓
PREVIOUS STATE VALIDATION
      ↓
EVENT-CHAIN / HASH VALIDATION
      ↓
PROTOCOL-RULE VALIDATION
      ↓
DETERMINISTIC REPLAY
      ↓
STATE-HASH COMPARISON
      ↓
CONFLICT?
   /        \
 NO          YES
 ↓            ↓
ACCEPT     CLASSIFY
              ↓
        EVIDENCE EVALUATION
              ↓
     DETERMINISTICALLY RESOLVABLE?
          /             \
        YES              NO
        ↓                 ↓
  RESOLUTION        CONSENSUS REQUIRED
        │                 │
        │          VALIDATOR CONSENSUS
        │                 ↓
        └────────── CANONICAL RESULT
                         ↓
                STATE RECONSTRUCTION
                         ↓
                STATE HASH VERIFIED
                         ↓
                RESOLUTION RECORD
                         ↓
                PROPAGATE FINAL STATE
                         ↓
              VIOLATION EVIDENCE
                         ↓
       REPUTATION / PERMISSION / INCENTIVE
              IF APPLICABLE
```

---

## 22. Fundamental Principles

The PCRE operates according to the following principles:

1. Deterministic state reconstruction.
2. Immutable event history.
3. Cryptographic evidence over message-arrival order.
4. Deterministic replay before consensus escalation.
5. Consensus without unilateral central authority.
6. Separation of conflict resolution from permission authority.
7. Separation of conflict resolution from player/node lifecycle authority.
8. Separation of conflict resolution from monetary settlement.
9. Retransmission is not automatically malicious behavior.
10. Evidence of misconduct is distinct from application of penalties.
11. Complete auditability of conflict-resolution procedures.
12. Byzantine fault tolerance only within the protocol-defined assumptions.

---

## 23. Non-Authority Rules

For avoidance of ambiguity:

```text
PCRE DOES NOT:

- define player permissions;
- define player/node lifecycle;
- execute monetary settlement;
- rewrite immutable history;
- delete historical events;
- replace validator consensus;
- impose reputation policy;
- unilaterally punish nodes;
- determine validity from physical arrival time alone.
```

---

## 24. Canonical Architecture Relationship

The PCRE occupies the following architectural position:

```text
                 ┌─────────────────────────┐
                 │  Immutable Event Ledger │
                 └────────────┬────────────┘
                              ↓
                 ┌─────────────────────────┐
                 │          PCRE           │
                 │ Conflict Resolution     │
                 └────────────┬────────────┘
                              │
            ┌─────────────────┼──────────────────┐
            ↓                 ↓                  ↓
       Engine 10          Engine 13          Engine 12
     Lifecycle /        Requests /          Monetary
    Disconnection       Permissions         Settlement
                              │
                              ↓
                    Validator Consensus
                              │
                              ↓
                    Canonical Game State
```

The PCRE is therefore a coordination and deterministic resolution layer, not a replacement for the specialized authorities of the other engines.

---

## 25. Final Architectural Definition

The P2P Conflict Resolution Engine is the subsystem responsible for transforming conflicting observations of a game into a single protocol-valid canonical state through deterministic evidence evaluation and, only where necessary, distributed validator consensus.

It preserves the immutable history of events while reconstructing the canonical state.

It does not possess independent authority over permissions, lifecycle, monetary settlement, reputation, or governance.

Its fundamental output is the auditable:

`CONFLICT_RESOLUTION_RESULT`

which identifies how the conflict was evaluated, whether consensus was required, which state became canonical, and which events were excluded from canonical state reconstruction.

The PCRE therefore provides the conflict-resolution layer required for CHAIN POKER GENESIS to maintain deterministic, cryptographically verifiable game-state convergence across its peer-to-peer network within the protocol's defined fault and consensus assumptions.

---

# 26. Final Integration Audit — 04 → 14

## 26.1 Audit Scope

This closure audit verifies the integration path from Engine 04 through Engine 14, with particular attention to:

- authority boundaries;
- lifecycle ownership;
- event production and observation;
- event identity and sequencing;
- hash and state verification;
- checkpoint and canonical-state semantics;
- request and permission authority;
- table-wallet authority;
- disconnection lifecycle authority;
- monetary settlement authority;
- validator-consensus boundaries;
- conflict-resolution authority;
- historical immutability;
- reputation and penalty boundaries.

## 26.2 Linear Integration Result

The final linear review establishes the following authority chain:

```text
Engine 04
Private Event Ledger
    ↓ historical event evidence
Engine 05–09
Specialized game / table / wallet processing
    ↓ protocol-defined events and state transitions
Engine 10
Player / Node Disconnection Lifecycle Authority
    ↓ lifecycle consequences/events
Engine 11
Protocol Documentation / Specification Authority
    ↓ documented protocol contracts
Engine 12
Monetary Settlement Authority
    ↓ settlement result
Engine 13
Request & Permission Authority
    ↓ protocol-authorized events
Engine 14
P2P Conflict Resolution
    ↓ canonical game-state reconstruction
Validator Consensus
    ↓ only when deterministic resolution is insufficient
Canonical Game State
```

This chain does not transfer specialized authority to Engine 14. The PCRE consumes evidence and authority results produced by the applicable engines and resolves state divergence without redefining those engines' responsibilities.

## 26.3 Residual Contradiction Check

The closure audit found no remaining contradiction requiring a change to Engine 14.1 in the following areas:

- **Authority:** PCRE does not replace Engine 10, Engine 12, Engine 13, or Validator Consensus.
- **Lifecycle:** Engine 10 remains authoritative for player/node disconnection lifecycle behavior.
- **Permissions:** Engine 13 remains authoritative for request and permission semantics.
- **Table wallet:** PCRE does not assume lifecycle authority over `TABLE_WALLET_INSTANCE`.
- **Settlement:** Engine 12 remains authoritative for monetary settlement.
- **Ledger:** Engine 04 remains the historical event record; PCRE performs state reconstruction and does not rewrite history.
- **Evidence:** deterministic evidence is evaluated before consensus escalation; Validator Consensus is not an evidence-priority level.
- **Checkpoint ordering:** `LATEST_VALID_CHECKPOINT` is selected by protocol-defined sequence and verified state lineage, not arrival time.
- **Retransmission:** retransmission and duplicate submission are not automatically treated as malicious behavior.
- **Penalties:** PCRE produces auditable violation evidence but does not directly impose reputation or economic consequences.
- **Canonical state:** PCRE reconstructs and verifies the canonical state rather than independently creating a competing authority.

## 26.4 Closure Determination

```text
AUDIT 04 → 14

AUTHORITY            PASS
LIFECYCLE             PASS
EVENT FLOW            PASS
IDENTIFIERS           PASS
HASH / STATE          PASS
CHECKPOINT            PASS
PERMISSIONS           PASS
TABLE WALLET          PASS
SETTLEMENT            PASS
CONSENSUS BOUNDARY    PASS
LEDGER IMMUTABILITY   PASS
PENALTY BOUNDARY      PASS

RESIDUAL CONTRADICTIONS: NONE IDENTIFIED

AUDIT RESULT: PASS
ENGINE 14.1: FROZEN
```

This audit result applies to the documented integration contracts available in Engines 04–14. It does not claim that implementation code, cryptographic primitives, network transport, or runtime behavior have been independently security-audited.

---

**Document Status:** REVISION 14.1 — FROZEN
**Next Required Procedure:** Implementation-level verification and subsequent protocol-wide audit when the remaining engine specifications are formally extended.
**FROZEN:** YES  
**Next Required Procedure:** Integration Audit 10 → 14 → 12 → 13, followed by complete Audit 01 → 14.  
**FROZEN:** NO
