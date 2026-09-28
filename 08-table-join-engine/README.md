# CHAIN POKER GENESIS BY LAEV

## 08 — Table Join Engine

### Consolidated Official Technical Specification v1.1

**Document Class:** CORE ENGINE  
**Document Status:** CONSOLIDATED / CORRECTED  
**Architecture Role:** Player Admission and Table Participation  
**Previous Specification:** v1.0  
**Revision:** v1.1  
**Protocol:** Chain Poker Genesis by LAEV

***

## 0. Document Control

```text
[LCCP]
SEQ: 8
PREV: 7
SELF: 8
NEXT: 9
CLASS: CORE ENGINE
STATUS: CONSOLIDATED
[/LCCP]
```

This specification defines the **Table Join Engine**, the protocol component responsible for admitting a player node into an already-created and configured poker table.

This revision consolidates the architectural corrections identified during the review of documents 01–07 and establishes the interfaces required by subsequent protocol components.

***

# 1. Purpose

The **Table Join Engine (TJE)** manages the controlled admission of a player node into a previously created Chain Poker Genesis table.

Its responsibility is to determine whether a player can become an official participant of the table by coordinating:

- table admission validation;
- player identity and node validation;
- cryptographic authorization;
- financial authorization;
- seat availability;
- atomic seat reservation;
- participant creation;
- admission event generation;
- table-state update;
- persistence of the resulting protocol events through the Private Off-Chain Ledger Engine.

The Table Join Engine is an **admission orchestrator**.

It is not:

- the table-creation engine;
- the cryptographic engine;
- the monetary settlement engine;
- the session/connection engine;
- the poker rules engine;
- the Private Off-Chain Ledger Engine.

Those components remain independently responsible for their own domains.

***

# 2. Architectural Principle

A table is created first and receives a fixed configuration.

The Table Join Engine consumes that configuration.

It does not redefine the table's fundamental rules during player admission.

The architectural sequence is:

```text
TABLE CREATION
      ↓
TABLE CONFIGURATION
      ↓
TABLE OPEN FOR ADMISSION
      ↓
TABLE JOIN ENGINE
      ↓
PARTICIPANT ADMISSION
      ↓
READY TO START
      ↓
HAND PREPARATION
```

The Join Engine therefore operates against an existing:

```text
table_id
table_configuration
admission_policy
selected_crypto_engine
settlement_configuration
seat_configuration
```

***

# 3. Scope

The Table Join Engine controls the following lifecycle:

1. Join request reception.
2. Join request identification.
3. Initial table validation.
4. Player-node validation.
5. Cryptographic validation through the engine selected by the table.
6. Financial authorization through the Monetary Settlement Engine.
7. Seat availability verification.
8. Atomic seat reservation.
9. Participant admission.
10. Table-state update.
11. Admission-event generation.
12. Ledger-event submission.
13. Transition of the table toward `READY_TO_START` when configured conditions are satisfied.

The engine also defines rejection, cancellation, timeout, and failure handling for the admission workflow.

***

# 4. Responsibility Boundaries

## 4.1 Table Join Engine

Responsible for:

```text
JOIN orchestration
ADMISSION validation
SEAT assignment
PARTICIPANT creation
JOIN state machine
ADMISSION event generation
TABLE admission state
```

## 4.2 Cryptographic Engine

Responsible for:

```text
cryptographic verification
signature verification
cryptographic authorization
engine-specific cryptographic operations
```

The exact cryptographic engine is selected when the table is created.

A player does not select a second cryptographic engine during Join.

***

## 4.3 Monetary Settlement Engine

Responsible for:

```text
buy-in authorization
available-funds verification
currency/network compatibility
settlement readiness
financial authorization
```

The Table Join Engine consumes the authorization result.

It does not become a duplicate financial ledger or settlement engine.

***

## 4.4 Communications / Session Layer

Responsible for:

```text
node connectivity
transport/session availability
connection state
reconnection
communication health
```

A temporary disconnection after successful Join does not automatically invalidate the participant.

***

## 4.5 Poker Rules Engine

Responsible for:

```text
game rules
blind configuration
turn order
betting rules
hand rules
game-state rules
```

The Join Engine must not become responsible for poker-rule execution.

***

## 4.6 Private Off-Chain Ledger Engine

Responsible for:

```text
event normalization
append-only persistence
cryptographic record integrity
Merkle consolidation
audit history
anchoring preparation
```

The Table Join Engine generates protocol events and submits them to the Ledger Engine.

It does not directly implement the Ledger.

***

# 5. Join Request

Each admission attempt begins with a digitally authenticated Join Request.

Minimum request structure:

```json
{
  "join_request_id": "...",
  "table_id": "...",
  "player_id": "...",
  "player_node_id": "...",
  "wallet_id": "...",
  "wallet_address": "...",
  "signature": "...",
  "request_timestamp": "...",
  "protocol_version": "..."
}
```

A table may require additional parameters according to its configuration.

Each request receives one unique `join_request_id`.

The identifier must remain stable across retries of the same logical request.

***

# 6. Required Inputs

The Table Join Engine requires the following protocol inputs.

## 6.1 Table Inputs

```text
table_id
table_status
table_admission_status
table_configuration_hash
minimum_players
maximum_players
seat_configuration
buy_in_configuration
currency_configuration
network_configuration
selected_crypto_engine_id
admission_policy
```

## 6.2 Player Inputs

```text
player_id
player_node_id
wallet_id
wallet_address
player_protocol_version
node_capabilities
signature
```

## 6.3 External Authorization Inputs

The engine consumes responses from:

```text
Cryptographic Engine
Monetary Settlement Engine
Communications / Session Layer
Requests and Permissions Engine
```

***

# 7. Table Preconditions

The Table Join Engine may process a Join Request only when the target table:

1. exists;
2. has a valid table configuration;
3. is open for player admission;
4. has not crossed its admission cutoff;
5. contains an available seat;
6. has a valid selected cryptographic engine;
7. has a valid settlement configuration.

A table that has reached a state where new admission is no longer permitted must reject new Join Requests.

For deterministic protocol behavior, admission should be governed by the table's configured **admission policy**, rather than by a generic `game_started` boolean alone.

***

# 8. Player Preconditions

The Join Engine must verify that:

```text
player exists
player identity is structurally valid
player node is protocol-compatible
player has not already joined this table
join request is valid and unique
required permissions exist
required communication path is available
```

A player may participate in multiple tables, but each table must maintain its own participant identity.

***

# 9. Table Participant Identity

The protocol distinguishes between:

```text
player_id
```

and:

```text
table_participant_id
```

`player_id` identifies the player across the protocol.

`table_participant_id` identifies that player's participation in one specific table.

Example:

```text
player_id:
PLAYER-001

table A:
TABLE-A-PARTICIPANT-003

table B:
TABLE-B-PARTICIPANT-001
```

This distinction is required for clean Ledger history and independent table state.

***

# 10. Wallet Identity

The protocol distinguishes between:

```text
wallet_id
wallet_address
wallet_network
wallet_currency
```

`wallet_id` is the protocol-level wallet reference.

`wallet_address` is the public settlement address used by the relevant monetary subsystem.

The Join Engine must not assume that `wallet_id` and `wallet_address` are interchangeable.

***

# 11. Cryptographic Engine Selection

Every table has a cryptographic engine selected during table creation.

Conceptually:

```text
TABLE
  └── selected_crypto_engine_id
```

The Table Join Engine must use the cryptographic configuration already assigned to the table.

A player cannot replace or dynamically select another cryptographic engine during the Join process.

The Join Engine requests cryptographic validation from the selected engine.

Example:

```text
Table Creation
      ↓
selected_crypto_engine_id = ENGINE-A
      ↓
Player Join
      ↓
Cryptographic validation through ENGINE-A
```

If the player does not satisfy the requirements of the table's selected cryptographic engine, admission fails.

***

# 12. Initial Validation

The initial validation stage verifies:

```text
table exists
table admission is open
join request is well formed
join request has valid identity
player is not already joined
seat capacity exists
required permissions are present
player node is compatible
communication path is available
request is not expired
```

The result is either:

```text
VALIDATION_PASSED
```

or:

```text
VALIDATION_FAILED
```

***

# 13. Cryptographic Validation

After initial validation, the Join Engine requests verification from the table's selected cryptographic engine.

The cryptographic subsystem verifies, as applicable:

```text
signature authenticity
message integrity
key validity
engine compatibility
cryptographic authorization
```

The Table Join Engine records the result but does not implement the cryptographic primitive itself.

Possible result:

```text
CRYPTOGRAPHICALLY_AUTHORIZED
```

or:

```text
CRYPTOGRAPHICALLY_REJECTED
```

***

# 14. Financial Authorization

Once technical and cryptographic validation succeeds, the Join Engine requests financial authorization from the Monetary Settlement Engine.

The Settlement Engine evaluates the table-defined requirements, including:

```text
minimum_buy_in
maximum_buy_in
available_authorized_funds
currency
network
settlement readiness
```

The Table Join Engine consumes the result:

```text
FINANCIAL_AUTHORIZED
```

or:

```text
FINANCIAL_REJECTED
```

The Join Engine does not perform an independent duplicate balance system.

***

# 15. Buy-In and Blinds Separation

The Join Engine validates whether the player satisfies the table's admission and buy-in requirements.

The actual poker blind rules remain under the Poker Rules Engine.

Therefore:

```text
Join Engine
    ↓
buy-in authorization
```

and:

```text
Poker Rules Engine
    ↓
blind calculation and enforcement
```

The Join Engine must not implement blind scheduling.

***

# 16. Seat Availability

A seat may be:

```text
AVAILABLE
RESERVED
OCCUPIED
```

The Join Engine must never assign a seat already reserved or occupied by another participant.

Seat state is table-specific.

Each seat contains at minimum:

```json
{
  "seat_id": "...",
  "status": "AVAILABLE | RESERVED | OCCUPIED",
  "table_participant_id": "...",
  "reservation_id": "...",
  "reservation_timestamp": "...",
  "reservation_expiry": "...",
  "occupancy_timestamp": "..."
}
```

***

# 17. Atomic Seat Reservation

Seat reservation must be atomic.

The protocol must guarantee that two concurrent Join Requests cannot both successfully reserve the same seat.

Conceptually:

```text
CHECK AVAILABLE
       +
ATOMIC RESERVE
       =
ONE VALID RESERVATION
```

Only one reservation may succeed.

***

# 18. Seat Reservation Expiration

A `SEAT_RESERVED` state must not be indefinite.

Every reservation must have:

```text
reservation_id
reservation_timestamp
reservation_expiry
```

If admission is not completed before expiration, the reservation may be released according to the table's admission policy.

The release itself is a protocol event.

Example:

```text
SEAT_RESERVED
      ↓
reservation expired
      ↓
SEAT_RELEASED
      ↓
seat = AVAILABLE
```

***

# 19. Participant Admission

After successful:

```text
initial validation
+
cryptographic authorization
+
financial authorization
+
seat reservation
```

the Join Engine creates the table participant.

At this point `table_participant_id` is assigned and the participant becomes officially associated with the table.

The resulting participant state becomes:

```text
JOINED
```

***

# 20. Player Admission State Machine

The canonical admission states are:

```text
REQUESTED
VALIDATING
CRYPTOGRAPHICALLY_VERIFIED
FINANCIALLY_VERIFIED
SEAT_RESERVED
JOINED
REJECTED
CANCELLED
```

`DISCONNECTED` is not treated as a replacement for `JOINED`.

It belongs to the connection/session lifecycle.

A participant may therefore exist as:

```text
JOINED + DISCONNECTED
```

without losing its membership in the table.

***

# 21. Canonical State Transitions

```text
REQUESTED
    ↓
VALIDATING
    ↓
CRYPTOGRAPHICALLY_VERIFIED
    ↓
FINANCIALLY_VERIFIED
    ↓
SEAT_RESERVED
    ↓
JOINED
```

Failure branches:

```text
REQUESTED → REJECTED
VALIDATING → REJECTED
CRYPTOGRAPHICALLY_VERIFIED → REJECTED
FINANCIALLY_VERIFIED → REJECTED
SEAT_RESERVED → CANCELLED
```

Reservation timeout:

```text
SEAT_RESERVED
    ↓
reservation_expired
    ↓
CANCELLED
```

A successful `JOINED` state is not reverted merely because communication is temporarily lost.

***

# 22. Transition Rules

## 22.1 REQUESTED → VALIDATING

Allowed when:

```text
request received
request structurally valid
join_request_id unique
```

## 22.2 VALIDATING → CRYPTOGRAPHICALLY_VERIFIED

Allowed only when:

```text
table admission valid
player valid
signature valid
selected crypto engine accepts request
```

## 22.3 CRYPTOGRAPHICALLY_VERIFIED → FINANCIALLY_VERIFIED

Allowed only when:

```text
Monetary Settlement Engine = FINANCIAL_AUTHORIZED
```

## 22.4 FINANCIALLY_VERIFIED → SEAT_RESERVED

Allowed only when:

```text
seat available
atomic reservation successful
reservation_id created
reservation expiry established
```

## 22.5 SEAT_RESERVED → JOINED

Allowed only when:

```text
reservation remains valid
participant record created
admission event generated
```

## 22.6 Any Pre-Join State → REJECTED

Allowed when an unrecoverable validation condition fails.

Examples:

```text
invalid signature
unknown table
table closed
permission failure
crypto incompatibility
financial rejection
protocol incompatibility
```

## 22.7 SEAT_RESERVED → CANCELLED

Allowed when:

```text
player cancels
reservation expires
required admission confirmation is not completed
protocol aborts the reservation
```

***

# 23. Table Admission Policy

The Join Engine must use the table's admission policy to determine whether new participants may enter.

A valid policy must define at minimum:

```text
admission_open_state
admission_close_condition
maximum_players
minimum_players
reservation_timeout
```

The exact policy is established during table creation/configuration.

***

# 24. Table State

The table maintains a separate lifecycle state from player admission state.

Relevant states include:

```text
WAITING_FOR_PLAYERS
READY_TO_START
STARTING
IN_HAND
```

This document defines only the Join Engine's interaction with those states.

***

# 25. WAITING_FOR_PLAYERS → READY_TO_START

The table may transition from `WAITING_FOR_PLAYERS` to `READY_TO_START` when the configured readiness conditions are satisfied.

Minimum condition:

```text
active participants >= minimum_players
```

and:

```text
all required admission operations are complete
```

The transition does not itself begin a hand.

***

# 26. READY_TO_START

`READY_TO_START` means:

```text
the table has enough admitted participants
and
the table is authorized to begin hand preparation
```

It does not mean that the first hand has already started.

The subsequent transition toward hand preparation belongs to the table/game lifecycle.

***

# 27. Table State Update

After successful admission, the Join Engine requests or performs the table-state update.

The resulting state must include:

```text
participant_count
occupied_seats
available_seats
table_admission_state
operational_state
official_participant_list
table_state_version
```

Each committed state change must receive a deterministic state representation.

A state hash may be produced:

```text
table_state_hash
```

This hash represents the canonical serialized table state at that point in the protocol.

***

# 28. Versioned Table State

Table state must be versioned to prevent ambiguous concurrent updates.

Example:

```text
table_state_version = 41
```

Next successful state:

```text
table_state_version = 42
```

Concurrent updates must fail or retry when their base state is stale.

This allows deterministic synchronization and conflict detection.

***

# 29. Admission Events

The Join Engine emits protocol events rather than directly maintaining the historical Ledger.

Minimum events include:

```text
JOIN_REQUESTED
PLAYER_VALIDATION_STARTED
CRYPTOGRAPHIC_VALIDATION_COMPLETED
FINANCIAL_VALIDATION_COMPLETED
SEAT_RESERVED
PLAYER_JOINED
SEAT_RELEASED
JOIN_CANCELLED
JOIN_REJECTED
TABLE_STATE_UPDATED
TABLE_READY_TO_START
```

Not every implementation must expose all events externally, but the internal event model must preserve sufficient history for reconstruction and audit.

***

# 30. Admission Event Structure

A successful `PLAYER_JOINED` event should contain at minimum:

```json
{
  "event_type": "PLAYER_JOINED",
  "join_request_id": "...",
  "table_id": "...",
  "table_participant_id": "...",
  "player_id": "...",
  "player_node_id": "...",
  "wallet_id": "...",
  "wallet_address": "...",
  "seat_id": "...",
  "reservation_id": "...",
  "selected_crypto_engine_id": "...",
  "timestamp": "...",
  "table_state_version": 42,
  "table_state_hash": "...",
  "event_hash": "...",
  "signature": "..."
}
```

Additional fields may be introduced through protocol versioning.

***

# 31. Event Integrity

Every generated protocol event must be uniquely identifiable and cryptographically verifiable.

At minimum:

```text
event_id
event_type
event_timestamp
event_payload
event_hash
event_signature
```

The event hash must be derived from the canonical event representation.

***

# 32. Off-Chain Private Ledger Integration

The Table Join Engine submits resulting protocol events to the:

```text
Private Off-Chain Ledger Engine
```

The Ledger Engine is responsible for:

```text
normalization
persistence
hash-chain / integrity processing
Merkle consolidation
audit records
future anchoring workflow
```

The Join Engine must not create a parallel historical record system.

***

# 33. Merkle Consolidation and Bitcoin Anchoring

Admission events may subsequently become part of the corresponding Merkle structure.

Conceptually:

```text
PLAYER_JOINED
      ↓
PRIVATE OFF-CHAIN LEDGER
      ↓
MERKLE TREE
      ↓
MERKLE ROOT
      ↓
BITCOIN ANCHOR
```

Anchoring follows the protocol's independent anchoring policy.

An event is not considered directly written to Bitcoin merely because it has been written to the Private Off-Chain Ledger.

***

# 34. Requests and Permissions Integration

The Requests and Permissions Engine may determine whether the requesting node has the protocol-level authority to perform the Join operation.

The Table Join Engine consumes that result.

Example:

```text
PERMISSION_AUTHORIZED
PERMISSION_DENIED
```

The Join Engine must reject a Join when the required permission is denied.

***

# 35. Communications Integration

Before admission, the Join Engine requires sufficient communication capability to complete the admission workflow.

However:

```text
temporary post-admission disconnection
```

does not automatically invalidate:

```text
table_participant_id
JOINED
seat ownership
```

Connection lifecycle is handled by the Communications / Session subsystem.

***

# 36. Failure Handling

The Join Engine must fail deterministically.

Examples:

### Table closed

```text
JOIN_REQUESTED
    ↓
REJECTED
reason = TABLE_ADMISSION_CLOSED
```

### Cryptographic failure

```text
CRYPTOGRAPHIC_VALIDATION
    ↓
REJECTED
reason = CRYPTOGRAPHIC_AUTHORIZATION_FAILED
```

### Financial failure

```text
FINANCIAL_VALIDATION
    ↓
REJECTED
reason = FINANCIAL_AUTHORIZATION_FAILED
```

### No seat

```text
VALIDATING
    ↓
REJECTED
reason = NO_SEAT_AVAILABLE
```

### Reservation timeout

```text
SEAT_RESERVED
    ↓
CANCELLED
reason = RESERVATION_EXPIRED
```

***

# 37. Idempotency

Join processing must be idempotent.

Submitting the same valid `join_request_id` repeatedly must not create multiple participants.

For example:

```text
JOIN_REQUEST_ID = JR-001
```

First processing:

```text
JR-001 → PLAYER_JOINED
```

Repeated processing:

```text
JR-001 → existing result returned
```

It must not produce:

```text
two participants
two seats
two financial authorizations
```

for the same logical admission request.

***

# 38. Duplicate Join Prevention

The engine must prevent:

```text
same player
+
same table
+
multiple active participant records
```

unless the table protocol explicitly defines a later re-entry mechanism.

A successful participant record must be uniquely constrained at the table level.

Conceptually:

```text
UNIQUE(table_id, player_id, active_participation)
```

***

# 39. Concurrency Requirements

The Join Engine must be safe under concurrent requests.

The following operations require atomic or conflict-safe handling:

```text
seat reservation
participant creation
table state version update
join request finalization
```

The system must prevent:

```text
double seat assignment
double participant creation
double admission event
inconsistent participant count
```

***

# 40. Deterministic Seat Assignment

The seat-assignment mechanism must follow the table's configured seat policy.

The Join Engine executes the policy.

It does not redefine it.

At minimum, the policy must produce:

```text
selected_seat_id
```

deterministically for a given valid allocation state.

Possible policies may include:

```text
FIRST_AVAILABLE
CONFIGURED_ORDER
DETERMINISTIC_SELECTION
```

The definitive algorithm is part of the table configuration or the protocol component responsible for seat policy.

***

# 41. Security Invariants

The following invariants must always hold:

### Invariant 1

A player cannot become `JOINED` without successful required validation.

### Invariant 2

A player cannot become `JOINED` without financial authorization where the table requires it.

### Invariant 3

A seat cannot be assigned to two simultaneous participants.

### Invariant 4

A duplicate Join Request cannot create duplicate participation.

### Invariant 5

A participant cannot replace the table's selected cryptographic engine.

### Invariant 6

A temporary connection loss does not automatically erase a valid participant.

### Invariant 7

The Ledger history is append-only from the perspective of the Join Engine.

### Invariant 8

A table cannot become `READY_TO_START` until its configured readiness conditions are satisfied.

### Invariant 9

The Join Engine cannot independently redefine poker rules.

### Invariant 10

The Join Engine cannot independently redefine monetary settlement policy.

***

# 42. Outputs

A successful Join operation returns at minimum:

```json
{
  "status": "JOINED",
  "join_request_id": "...",
  "table_id": "...",
  "table_participant_id": "...",
  "player_id": "...",
  "seat_id": "...",
  "wallet_id": "...",
  "selected_crypto_engine_id": "...",
  "table_state_version": 42,
  "table_state_hash": "...",
  "event_id": "..."
}
```

A rejected operation returns:

```json
{
  "status": "REJECTED",
  "join_request_id": "...",
  "table_id": "...",
  "reason_code": "...",
  "event_id": "..."
}
```

A cancelled reservation returns:

```json
{
  "status": "CANCELLED",
  "join_request_id": "...",
  "reservation_id": "...",
  "reason_code": "...",
  "event_id": "..."
}
```

***

# 43. Conceptual Processing Sequence

```text
1. RECEIVE JOIN REQUEST
          ↓
2. VALIDATE REQUEST
          ↓
3. VALIDATE TABLE ADMISSION
          ↓
4. VALIDATE PLAYER
          ↓
5. VERIFY CRYPTOGRAPHY
          ↓
6. REQUEST FINANCIAL AUTHORIZATION
          ↓
7. SELECT AVAILABLE SEAT
          ↓
8. ATOMICALLY RESERVE SEAT
          ↓
9. CREATE TABLE PARTICIPANT
          ↓
10. GENERATE PLAYER_JOINED EVENT
          ↓
11. UPDATE TABLE STATE
          ↓
12. SUBMIT EVENTS TO PRIVATE LEDGER
          ↓
13. EVALUATE TABLE READINESS
          ↓
14. RETURN JOIN RESULT
```

***

# 44. Formal Responsibility Flow

```text
PLAYER NODE
    │
    │ Join Request
    ▼
TABLE JOIN ENGINE
    │
    ├──────────────► REQUESTS & PERMISSIONS
    │
    ├──────────────► SELECTED CRYPTOGRAPHIC ENGINE
    │
    ├──────────────► MONETARY SETTLEMENT ENGINE
    │
    ├──────────────► COMMUNICATIONS / SESSION
    │
    ▼
SEAT RESERVATION
    │
    ▼
TABLE PARTICIPANT
    │
    ├──────────────► PRIVATE OFF-CHAIN LEDGER
    │
    ▼
TABLE STATE
    │
    ▼
READY_TO_START
```

***

# 45. Interface Summary

## Input Interface

```text
JoinRequest
TableConfiguration
PlayerIdentity
WalletReference
CryptographicAuthorizationResult
FinancialAuthorizationResult
PermissionResult
CommunicationStatus
```

## Output Interface

```text
JoinResult
ParticipantRecord
SeatAssignment
AdmissionEvents
TableStateUpdate
ReadinessTransition
```

***

# 46. Protocol Compatibility

The Table Join Engine must remain compatible with the modular architecture of:

```text
Chain Poker Genesis by LAEV
```

Its interface must therefore avoid direct dependence on implementation-specific details belonging to other engines.

The engine communicates through defined protocol contracts rather than duplicating the internal logic of other components.

***

# 47. Non-Responsibilities

The Table Join Engine does not:

```text
create tables
define poker rules
select a new cryptographic engine for an existing table
settle monetary transactions itself
maintain the permanent historical Ledger
construct Merkle trees itself
perform Bitcoin anchoring itself
manage long-term player sessions
execute hands
deal cards
determine winners
calculate blinds
```

Those responsibilities belong to their respective protocol components.

***

# 48. Canonical Architectural Invariant

The following statement is normative for Chain Poker Genesis:

> A player joins a previously configured table. The player does not redefine the table.

Consequently:

```text
TABLE CONFIGURATION
        ↓
PLAYER COMPATIBILITY
```

not:

```text
PLAYER JOIN
        ↓
TABLE RECONFIGURATION
```

***

# 49. Completion Condition

A Join Request is considered **successfully completed** only when all required conditions are true:

```text
request valid
AND
table admission open
AND
player valid
AND
cryptographic authorization valid
AND
financial authorization valid
AND
seat reservation successful
AND
participant record committed
AND
PLAYER_JOINED event generated
```

Only then may the participant state become:

```text
JOINED
```

***

# 50. Table Readiness Condition

The table may become:

```text
READY_TO_START
```

only when:

```text
minimum_players reached
AND
all required participants are in valid admitted state
AND
no blocking admission process remains
AND
table configuration remains valid
```

`READY_TO_START` authorizes the next stage of the protocol.

It does not itself initiate a poker hand.

***

# 51. Canonical State Model

### Player admission

```text
REQUESTED
    ↓
VALIDATING
    ↓
CRYPTOGRAPHICALLY_VERIFIED
    ↓
FINANCIALLY_VERIFIED
    ↓
SEAT_RESERVED
    ↓
JOINED
```

### Failure

```text
REQUESTED ───────────────► REJECTED
VALIDATING ──────────────► REJECTED
CRYPTOGRAPHICALLY_VERIFIED ─► REJECTED
FINANCIALLY_VERIFIED ───────► REJECTED
SEAT_RESERVED ─────────────► CANCELLED
```

### Connection lifecycle

```text
JOINED
  │
  ├── CONNECTED
  │
  └── DISCONNECTED
          │
          └── RECONNECTED
```

The connection lifecycle is separate from the admission lifecycle.

***

# 52. Final Architectural Definition

The **Table Join Engine** is the Chain Poker Genesis component that converts a valid player request into an officially recognized table participant through a deterministic, cryptographically verifiable, financially authorized and auditable admission process.

Its core function is:

```text
REQUEST
   ↓
VALIDATE
   ↓
AUTHORIZE
   ↓
RESERVE
   ↓
JOIN
   ↓
RECORD
   ↓
UPDATE TABLE
```

The engine preserves the separation between:

```text
ADMISSION
CRYPTOGRAPHY
SETTLEMENT
SESSION
GAME RULES
LEDGER
```

while providing the orchestration required to connect those subsystems into a single valid table-participation event.

***

# 53. Canonical Dependency Set

The consolidated Table Join Engine recognizes the following dependencies:

```text
01. Table Creation / Table Configuration
02. Requests and Permissions Engine
03. Communications / Session Layer
04. Selected Cryptographic Engine
05. Monetary Settlement Engine
06. Private Off-Chain Ledger Engine
07. Table / Game State Manager
08. Poker Rules Engine (read-only configuration dependency)
```

The:

```text
Installation Engine
```

is treated as a **precondition provider** for node readiness rather than as a permanent runtime dependency of the Join Engine.

The:

```text
Card Commitment and Reveal Engine
```

is a **downstream consumer** activated after table readiness and is therefore not required to complete ordinary player admission.

***

# 54. v1.1 Consolidation Result

This revision resolves the principal architectural ambiguities identified in the previous v1.0 specification:

```text
✓ Selected cryptographic engine explicitly bound to the table
✓ Financial logic delegated to Monetary Settlement Engine
✓ Buy-in separated from poker blind execution
✓ Atomic seat reservation defined
✓ Reservation expiration defined
✓ Join and session state separated
✓ Player ID separated from Table Participant ID
✓ Wallet ID separated from Wallet Address
✓ Join Request ID propagated into admission events
✓ Table state versioning defined
✓ Event-driven Ledger integration clarified
✓ Merkle / Bitcoin anchoring responsibility separated
✓ Idempotency defined
✓ Duplicate admission prevention defined
✓ Concurrency requirements defined
✓ Deterministic seat-policy interface defined
✓ READY_TO_START separated from hand initiation
✓ Engine boundaries explicitly defined
```

***

# 55. Normative Closing Statement

The Table Join Engine must admit only participants who satisfy the table's predefined protocol conditions.

No admission event may bypass:

```text
validation
cryptographic authorization
financial authorization
seat reservation
participant commitment
```

and no Join operation may modify the fundamental cryptographic, financial, or poker configuration of an already-created table.

The resulting participant admission becomes a protocol event that can be independently verified, persisted in the Private Off-Chain Ledger, incorporated into Merkle consolidation, and subsequently included in the protocol's Bitcoin anchoring process.

**Document 08 — Table Join Engine v1.1 — Consolidated Corrected Specification**

**Status: READY FOR DOWNSTREAM INTEGRATION**
