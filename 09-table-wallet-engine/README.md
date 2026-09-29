# CHAIN POKER GENESIS BY LAEV

# 09 — Table Wallet Engine

## Official Technical Specification v1.1

**Document Class:** CORE ENGINE  
**Document Status:** CONSOLIDATED / CORRECTED  
**Architecture Role:** Temporary Shared-Custody Table Wallet and Hand Settlement Infrastructure  
**Previous Specification:** v1.0  
**Revision:** v1.1  
**Protocol:** Chain Poker Genesis by LAEV

***

## 0. Document Control

```text
[LCCP]
SEQ: 9
PREV: 8
SELF: 9
NEXT: 10
CLASS: CORE ENGINE
STATUS: CONSOLIDATED
[/LCCP]
```

This specification defines the **Table Wallet Engine**, the protocol component responsible for the creation, authorization, operation, funding, settlement and closure of the temporary shared-custody wallet associated with an active Chain Poker Genesis table and its monetary settlement cycles.

The Table Wallet is not a player wallet.

It is not a permanent protocol treasury.

It is not a company-controlled custodial wallet.

It is not itself a Lightning Network channel.

It is a temporary shared-custody monetary component jointly authorized by the participants of the table according to the active table consensus and cryptographic configuration.

***

# 1. Purpose

The Table Wallet Engine provides the monetary custody boundary between:

```text
PLAYER EXTERNAL HD WALLETS
        ↓
TABLE CONSENSUS
        ↓
TABLE WALLET
        ↓
LIGHTNING / L2 PAYMENT RAIL
        ↓
POKER SETTLEMENT
```

Its responsibilities are:

- establish a Table Wallet instance;
- bind the wallet to an authorized table participant composition;
- maintain the cryptographic authorization configuration;
- receive valid wager value;
- represent the active table pot;
- coordinate real-time monetary movement through an approved Lightning/L2 adapter;
- receive authorized settlement instructions;
- execute or coordinate settlement authorization;
- distribute funds to winner wallet(s);
- distribute configured rake to rake wallet(s);
- execute authorized refunds where applicable;
- verify final balance;
- close the wallet instance;
- emit complete historical evidence to the Private Off-Chain Ledger Engine.

The Table Wallet Engine does not determine poker winners and does not calculate rake.

***

# 2. Fundamental Architectural Principle

Chain Poker Genesis does not require a central company-controlled wallet to custody player funds.

The monetary architecture is:

```text
PLAYER A EXTERNAL HD WALLET
PLAYER B EXTERNAL HD WALLET
PLAYER C EXTERNAL HD WALLET
            │
            │ authorized payment
            ▼
     LIGHTNING / L2
            │
            ▼
   TABLE WALLET INSTANCE
            │
            │ settlement
            ▼
WINNER WALLET(S) + RAKE WALLET(S)
```

The Table Wallet is jointly controlled according to the cryptographic configuration established by the table participants and authorized by the table protocol.

The protocol itself does not require possession of players' private keys.

***

# 3. Separation of Wallet Domains

The protocol distinguishes at least three wallet roles.

## 3.1 Player External HD Wallet

The Player Wallet:
- belongs to the player;
- retains the player's private keys;
- may be an external hardware/HD wallet;
- authorizes player-originated cryptographic operations;
- supplies wager value through the selected monetary rail;
- receives winnings;
- may receive refunds;
- is not controlled by the Table Wallet Engine.

The private key must not be transferred to the Table Wallet Engine.

***

## 3.2 Table Wallet

The Table Wallet:
- belongs to the active table context;
- is jointly authorized by the participating players;
- exists only for the defined table monetary lifecycle;
- receives wager value;
- represents temporary shared custody;
- authorizes settlement according to the active table composition;
- must not become a permanent player balance;
- must reach the required final settlement condition before closure.

***

## 3.3 Rake Wallet

A Rake Wallet is an externally defined settlement destination configured by the applicable protocol/rake policy.

The Table Wallet Engine may transfer an authorized rake obligation to the configured rake destination.

It does not calculate the rake amount.

***

# 4. Table Wallet Is Not the Lightning Network

The architecture explicitly separates:

```text
TABLE WALLET
```

from:

```text
LIGHTNING / L2
```

The Table Wallet is the custody and authorization domain.

Lightning/L2 is a payment and settlement rail.

Conceptually:

```text
PLAYER WALLET
      ↓
PAYMENT ADAPTER
      ↓
LIGHTNING / L2
      ↓
TABLE WALLET
```

and:

```text
TABLE WALLET
      ↓
SETTLEMENT ADAPTER
      ↓
LIGHTNING / L2
      ↓
DESTINATION WALLET
```

The Table Wallet Engine must therefore remain independent from any single payment-network implementation.

***

# 5. Relationship with Table Join Engine

The Table Join Engine is responsible for participant admission.

It does not create the Table Wallet's final authorization state by itself.

The canonical relationship is:

```text
JOIN REQUEST
     ↓
TABLE JOIN ENGINE
     ↓
PLAYER JOINED
     ↓
TABLE STATE UPDATE
     ↓
TABLE CONSENSUS
     ↓
AUTHORIZED PARTICIPANT COMPOSITION
     ↓
TABLE WALLET CRYPTOGRAPHIC CONFIGURATION
```

A successful `PLAYER_JOINED` event therefore does not by itself authorize the new participant to spend from the existing Table Wallet.

The new participant must become part of the authorized table composition through the applicable consensus transition.

***

# 6. Table Consensus Boundary

Table Consensus is the authority responsible for accepting changes to the table's authoritative participant and cryptographic composition.

The Table Wallet Engine consumes the result.

It does not define the consensus threshold.

The exact consensus algorithm, threshold and quorum rules remain governed by the dedicated consensus specification.

Conceptually:

```text
PARTICIPANT CHANGE
        ↓
TABLE CONSENSUS
        ↓
APPROVED
        ↓
TABLE WALLET CONFIGURATION UPDATE
```

or:

```text
PARTICIPANT CHANGE
        ↓
TABLE CONSENSUS
        ↓
REJECTED / NO CONSENSUS
        ↓
CURRENT TABLE WALLET CONFIGURATION REMAINS
```

The Table Wallet Engine must never silently modify its authorized signer composition.

***

# 7. Table Wallet Instance vs Cryptographic Configuration

The protocol distinguishes:

```text
TABLE_WALLET_INSTANCE
```

from:

```text
TABLE_WALLET_CRYPTOGRAPHIC_CONFIGURATION
```

The instance identifies a specific temporary custody lifecycle.

The cryptographic configuration identifies the participants and authorization rules governing that wallet.

A configuration may potentially be reused under an approved security policy when the participant composition is unchanged.

A composition change requires a new authorized cryptographic configuration.

A wallet instance may therefore be:

```text
INSTANCE-001
CONFIGURATION-001
```

and a subsequent hand may use:

```text
INSTANCE-002
CONFIGURATION-001
```

if the protocol explicitly permits configuration reuse.

If the participant composition changes:

```text
INSTANCE-003
CONFIGURATION-002
```

must be established before monetary operations requiring the new composition become authoritative.

***

# 8. Participant Composition

The Table Wallet authorization set is derived from the authoritative table participant composition.

It must contain, at minimum:

```text
table_id
table_state_version
participant_set
participant identifiers
authorized public keys
cryptographic configuration version
consensus authorization reference
```

The participant set must correspond to the authoritative table state.

The Table Wallet Engine must reject a configuration whose participant composition cannot be reconciled with the authorized table state.

***

# 9. External HD Wallet Boundary

The protocol supports external HD/hardware wallets as signing devices.

The boundary is:

```text
PLAYER NODE
     ↓
CRYPTOGRAPHIC CONNECTION ENGINE
     ↓
EXTERNAL HD WALLET
```

The private key remains under the player's wallet security boundary.

The Table Wallet Engine receives only the cryptographic authorization result required by the protocol.

It must not request or persist the player's private seed or private key as part of ordinary table operation.

***

# 10. Cryptographic Authorization

The implementation may use an appropriate shared-authorization construction supported by the selected Bitcoin/L2 infrastructure.

A possible construction is an aggregated-key scheme such as MuSig2/Taproot where technically compatible.

This is an implementation option, not a universal requirement of this specification.

The protocol requirement is:

> The Table Wallet must be spend-authorized only according to the active table cryptographic configuration.

The exact cryptographic algorithm, key aggregation method, signature format, domain separation and L2 compatibility rules require separate cryptographic specification.

***

# 11. Wallet Creation

A Table Wallet may be initialized only after:

```text
table exists
AND
table configuration is valid
AND
participant composition is authoritative
AND
table consensus requirements are satisfied
AND
cryptographic configuration is valid
AND
settlement configuration is valid
```

The resulting wallet context must include:

```text
table_wallet_instance_id
table_id
hand_id or settlement_cycle_id
participant_set
cryptographic_configuration_id
configuration_version
authorized_public_keys
payment_rail_id
payment_rail_version
creation_timestamp
initial_state
```

***

# 12. Wallet Lifecycle

The canonical lifecycle is:

```text
CREATED
    ↓
AUTHORIZED
    ↓
ACTIVE
    ↓
SETTLEMENT_PENDING
    ↓
SETTLING
    ↓
SETTLED
    ↓
BALANCE_VERIFIED
    ↓
CLOSED
```

Failure states include:

```text
FAILED
RECOVERY_REQUIRED
```

A failed settlement must not be represented as successful merely because a settlement request was created.

***

# 13. Wallet State Definitions

## CREATED

Wallet instance has been defined but is not yet authorized for monetary use.

## AUTHORIZED

The cryptographic configuration and participant authorization have been validated.

## ACTIVE

The wallet may receive authorized wager value.

## SETTLEMENT_PENDING

The poker hand has reached the settlement boundary and the wallet is awaiting an authorized settlement plan.

## SETTLING

Settlement execution is in progress.

## SETTLED

The authorized settlement outputs have been executed or otherwise cryptographically confirmed according to the selected payment rail.

## BALANCE_VERIFIED

The wallet's remaining balance satisfies the settlement invariant.

## CLOSED

The wallet instance is permanently closed for subsequent table settlement operations.

Historical evidence remains available through the Private Off-Chain Ledger.

## FAILED

The wallet operation failed.

## RECOVERY_REQUIRED

The wallet cannot safely continue normal lifecycle progression without a defined recovery procedure.

***

# 14. Real-Time Wager Flow

All monetary bets are represented in satoshis.

During an active hand:

```text
PLAYER ACTION
     ↓
POKER RULE VALIDATION
     ↓
AUTHORIZED WAGER
     ↓
PLAYER EXTERNAL WALLET
     ↓
LIGHTNING / L2 PAYMENT RAIL
     ↓
TABLE WALLET
     ↓
ACTIVE POT
```

Examples include:

```text
ANTE
BLIND
CALL
BET
RAISE
RE-RAISE
ALL-IN
```

The Table Wallet Engine does not decide whether a player is legally permitted to perform the action.

That determination belongs to the poker/game-state authority.

The Table Wallet Engine verifies the monetary movement against the authorized wager instruction.

***

# 15. Payment Rail Adapter

The Table Wallet Engine communicates with a payment abstraction rather than directly embedding one network implementation.

Conceptually:

```text
Table Wallet Engine
        ↓
Payment / Settlement Adapter
        ↓
Lightning or Selected L2
```

The adapter must provide sufficient information to establish:

```text
payment_request_id
source_reference
destination_reference
amount_sats
payment_rail
payment_rail_version
authorization_reference
execution_status
settlement_reference
```

The exact Lightning/L2 implementation is outside the Table Wallet Engine specification.

***

# 16. Wager Registration

Every accepted wager movement must be associated with:

```text
table_id
hand_id
table_wallet_instance_id
table_participant_id
wager_id
wager_type
amount_sats
payment_rail
payment_reference
authorization_reference
timestamp
```

The wager must not be counted toward the active pot merely because a payment was requested.

The monetary movement must satisfy the payment adapter's confirmation requirements.

***

# 17. Active Pot

The Table Wallet provides the custody boundary for the active monetary pot.

Conceptually:

```text
VALIDATED WAGER INPUTS
        ↓
TABLE WALLET
        ↓
ACTIVE POT
```

The Table Wallet Engine must maintain sufficient references to reconcile the active pot with:

```text
wager events
payment references
table state
hand state
ledger evidence
```

The Table Wallet does not determine the poker meaning of those amounts.

***

# 18. Temporary Custody

The Table Wallet is temporary shared custody.

It must not become:

```text
permanent player balance
```

or:

```text
protocol treasury
```

or:

```text
company-controlled custody
```

Its expected purpose is:

```text
receive wager value
        ↓
hold active table value
        ↓
settle according to protocol
        ↓
return required remaining balance
        ↓
close
```

***

# 19. Hand Completion Boundary

The Table Wallet Engine must not independently determine that a poker hand has ended.

The authoritative game/poker state emits:

```text
HAND_COMPLETED
```

The Table Wallet Engine consumes that transition.

The transition then activates:

```text
SETTLEMENT_PENDING
```

***

# 20. Settlement Inputs

A valid settlement request must contain sufficient information to determine:

```text
table_id
hand_id
table_wallet_instance_id
winner_destination(s)
refund_destination(s), if applicable
rake obligation(s), if applicable
amount_sats per destination
settlement authorization context
```

The settlement request must reference the authoritative hand-completion state.

***

# 21. Poker Rules Responsibility

The Poker Rules Engine determines:

```text
winner(s)
split pot
side pots
return wagers
eligible players
hand completion
```

The Table Wallet Engine does not determine any of those outcomes.

The correct relationship is:

```text
POKER RULES
     ↓
AUTHORIZED OUTCOME
     ↓
MONETARY SETTLEMENT
     ↓
TABLE WALLET
```

***

# 22. Monetary Settlement Responsibility

The Monetary Settlement Engine owns final monetary settlement execution.

Engine 05 and the Table Wallet Engine provide required inputs.

The responsibility chain is:

```text
POKER RULES
     ↓
HAND_COMPLETED
     ↓
ENGINE 05
     ↓
RAKE OBLIGATION
     ↓
MONETARY SETTLEMENT ENGINE
     ↓
TABLE WALLET
     ↓
AUTHORIZED OUTPUTS
```

The Table Wallet Engine therefore does not replace the Monetary Settlement Engine.

It is the custody/authorization execution boundary used by that settlement process.

***

# 23. Rake Integration

Engine 05 owns:

```text
rake eligibility
rake calculation
rake obligation
```

The Table Wallet Engine consumes the resulting:

```text
rake_obligation_id
```

It must not independently recalculate:

```text
R = P × 0.03
```

or any future rake formula.

The current Engine 05 specification defines the conceptual allocation:

```text
R = P × 0.03
F = R × 0.11
A = R × 0.89
```

The final integer-satoshi precision and fee policy remain governed by the settlement/rake specifications.

***

# 24. Rake Settlement

Once a valid rake obligation exists:

```text
RAKE_OBLIGATION_CREATED
        ↓
SETTLEMENT_REQUESTED
        ↓
TABLE WALLET
        ↓
RAKE DESTINATION
```

The rake destination must be explicitly identified by the settlement configuration.

The Table Wallet Engine only executes the authorized obligation.

***

# 25. Settlement Distribution

A completed hand may produce:

```text
winner payout(s)
+
rake payout(s)
+
authorized refund(s)
```

The exact destination set is determined by the settlement plan.

The Table Wallet Engine must not create an unrequested payout.

***

# 26. Conservation of Funds

The following invariant is mandatory:

```text
TOTAL VALID WAGER INPUTS
=
TOTAL VALID SETTLEMENT OUTPUTS
+
AUTHORIZED REMAINING BALANCE
```

For a fully settled hand where no balance is intentionally carried forward:

```text
TOTAL VALID WAGER INPUTS
=
WINNER PAYOUTS
+
REFUNDS
+
RAKE
```

and:

```text
TABLE WALLET FINAL BALANCE = 0
```

subject to any explicitly defined network/settlement fee treatment.

Fees must not be silently absorbed into the invariant.

They must be explicitly represented by the applicable settlement policy.

***

# 27. Zero-Balance Closure

A Table Wallet must not enter `CLOSED` until its final monetary condition has been verified.

Required condition:

```text
SETTLEMENT_COMPLETE
AND
BALANCE_RECONCILED
AND
NO_PENDING_AUTHORIZED_OUTPUTS
```

Then:

```text
BALANCE_VERIFIED
      ↓
CLOSED
```

A wallet that still contains an unexplained balance must enter:

```text
RECOVERY_REQUIRED
```

rather than being silently closed.

***

# 28. Table Wallet Renewal

A new wallet instance or cryptographic configuration is required when the applicable table protocol changes the authorized custody composition.

Examples include:

```text
new player admitted
player permanently leaves
player removed
seat composition changes
authorized signer composition changes
cryptographic configuration changes
```

A temporary communication interruption does not automatically constitute a composition change.

***

# 29. Connection Failure

The Table Wallet Engine must distinguish:

```text
temporary communication failure
```

from:

```text
participant removal
```

and:

```text
authorized composition change
```

A player being temporarily:

```text
DISCONNECTED
```

does not by itself authorize removal from the Table Wallet configuration.

The applicable disconnection-management and consensus rules determine whether the participant remains authorized.

***

# 30. Permanent Participant Change

When a participant permanently leaves or is removed:

```text
PARTICIPANT CHANGE
       ↓
TABLE STATE UPDATE
       ↓
TABLE CONSENSUS
       ↓
NEW AUTHORIZED COMPOSITION
       ↓
NEW TABLE WALLET CONFIGURATION
```

No unauthorized participant may remain a signer after the new configuration becomes active.

***

# 31. Hand Boundary

The protocol should not modify the active Table Wallet cryptographic composition in the middle of an already authorized monetary execution cycle unless an explicit recovery/security rule requires it.

Normal participant-composition changes should therefore become effective at an authorized table boundary.

The exact activation boundary is governed by table consensus and game-state rules.

***

# 32. Settlement Authorization

A settlement must contain sufficient authorization evidence to prove:

```text
settlement request valid
AND
hand outcome authoritative
AND
rake obligation valid, if applicable
AND
destinations valid
AND
amounts valid
AND
Table Wallet authorization valid
```

Only then may the wallet proceed to execution.

***

# 33. External Signing

Where the selected cryptographic implementation requires signatures from external player-controlled HD wallets, the signing operation must be requested through the approved cryptographic interface.

Conceptually:

```text
SETTLEMENT PLAN
      ↓
SIGNING REQUEST
      ↓
PLAYER EXTERNAL HD WALLET(S)
      ↓
SIGNATURE(S)
      ↓
TABLE WALLET AUTHORIZATION
      ↓
SETTLEMENT EXECUTION
```

Private keys never become part of the Table Wallet Engine's ordinary data model.

***

# 34. Failed Settlement

If settlement fails:

```text
SETTLEMENT_REQUESTED
      ↓
SETTLEMENT_FAILED
```

The Table Wallet must not be declared successfully settled.

The associated settlement obligation remains identifiable.

Recovery must preserve:

```text
original settlement request
authorization context
payment references
failure reason
current wallet state
ledger evidence
```

Retry operations must be idempotent.

***

# 35. Idempotency

The following identifiers must be stable across retries:

```text
table_wallet_instance_id
settlement_request_id
wager_id
rake_obligation_id
payment_request_id
```

A repeated settlement request must not create duplicate payouts.

The implementation must be able to distinguish:

```text
NEW SETTLEMENT
```

from:

```text
RETRY OF EXISTING SETTLEMENT
```

***

# 36. Ledger Integration

The Table Wallet Engine does not maintain a parallel historical ledger.

It emits protocol events to:

```text
04 — Private Off-Chain Ledger Engine
```

The Ledger records historical evidence.

It does not become the live monetary authority.

***

# 37. Required Table Wallet Events

At minimum, the following events should be supported:

```text
TABLE_WALLET_CREATED
TABLE_WALLET_AUTHORIZATION_PENDING
TABLE_WALLET_AUTHORIZED
TABLE_WALLET_ACTIVATED

TABLE_WALLET_CONFIGURATION_CREATED
TABLE_WALLET_CONFIGURATION_CHANGED
TABLE_WALLET_CONFIGURATION_ACTIVATED

TABLE_WALLET_WAGER_REQUESTED
TABLE_WALLET_WAGER_AUTHORIZED
TABLE_WALLET_FUNDED
TABLE_WALLET_INPUT_REGISTERED

TABLE_WALLET_SETTLEMENT_REQUESTED
TABLE_WALLET_SETTLEMENT_AUTHORIZED
TABLE_WALLET_PAYOUT_EXECUTED
TABLE_WALLET_RAKE_EXECUTED
TABLE_WALLET_REFUND_EXECUTED

TABLE_WALLET_SETTLEMENT_FAILED
TABLE_WALLET_RECOVERY_REQUIRED

TABLE_WALLET_BALANCE_VERIFIED
TABLE_WALLET_CLOSED
```

Event names remain subject to the canonical event-schema specification.

***

# 38. Event Evidence

Each event submitted to Engine 04 must be compatible with the ledger's canonical event model.

At minimum, the event should be attributable to:

```text
table_id
hand_id
table_wallet_instance_id
engine_id
event_type
event_version
payload
timestamp
```

The Ledger Engine then performs canonicalization, hashing, persistence and later Merkle processing according to its own specification.

***

# 39. Privacy

The Table Wallet Engine must not expose private cryptographic material.

The ledger should record sufficient evidence to verify:

```text
who authorized
what was authorized
which wallet instance was used
which settlement was requested
which payment rail was used
what amount was involved
what result occurred
```

without automatically publishing:

```text
private keys
seed phrases
private wallet credentials
```

***

# 40. State Machine

The canonical normal flow is:

```text
CREATED
   ↓
AUTHORIZED
   ↓
ACTIVE
   ↓
SETTLEMENT_PENDING
   ↓
SETTLING
   ↓
SETTLED
   ↓
BALANCE_VERIFIED
   ↓
CLOSED
```

Failure paths:

```text
ACTIVE
   ↓
FAILED
   ↓
RECOVERY_REQUIRED
```

and:

```text
SETTLING
   ↓
SETTLEMENT_FAILED
   ↓
RECOVERY_REQUIRED
```

***

# 41. Integrated Economic Flow

The complete monetary sequence is:

```text
TABLE JOIN
     ↓
TABLE STATE UPDATE
     ↓
TABLE CONSENSUS
     ↓
AUTHORIZED PARTICIPANT COMPOSITION
     ↓
TABLE WALLET CONFIGURATION
     ↓
TABLE WALLET ACTIVATION
     ↓
PLAYER EXTERNAL HD WALLET
     ↓
LIGHTNING / L2
     ↓
TABLE WALLET
     ↓
ACTIVE POT
     ↓
POKER RULES
     ↓
HAND_COMPLETED
     ↓
RAKE ENGINE
     ↓
RAKE OBLIGATION
     ↓
MONETARY SETTLEMENT ENGINE
     ↓
TABLE WALLET AUTHORIZED SETTLEMENT
     ↓
WINNER WALLET(S)
     +
RAKE WALLET(S)
     +
AUTHORIZED REFUNDS
     ↓
BALANCE VERIFICATION
     ↓
TABLE WALLET CLOSED
     ↓
PRIVATE OFF-CHAIN LEDGER
```

The Ledger records evidence throughout the lifecycle rather than acting only at the end.

***

# 42. Relationship with Documents 01–08

The Table Wallet Engine preserves the following established boundaries.

### 01 — Installation

Prepares the node.

It does not own Table Wallet state.

### 02 — Graphical Interface

Displays wallet/table information and requests operations.

It does not authorize monetary state merely because a user initiated an action through the GUI.

### 03 — Cryptographic Connection

Provides cryptographic identity and external HD-wallet interaction.

It does not own the Table Wallet.

### 04 — Private Off-Chain Ledger

Records historical evidence.

It does not own live wallet state.

### 05 — Rake & Settlement Flow

Calculates the rake obligation and hands settlement to the Monetary Settlement Engine.

It does not become the Table Wallet.

### 06 — Commitment & Reveal

Handles card commitment, protected private-card state and reveal verification.

It does not control monetary custody.

### 07 — Table Creation

Creates the table context and initial configuration.

It does not become the wallet custodian.

### 08 — Table Join

Admits players and updates the table participant state.

It does not directly modify wallet authorization without the required consensus transition.

***

# 43. Core Security Invariants

The following conditions must hold.

### Invariant 1

A player private key is never required to be transferred to the Table Wallet Engine.

### Invariant 2

A player cannot become an authorized Table Wallet participant without the applicable table authorization/consensus transition.

### Invariant 3

A temporary network disconnection does not automatically remove a participant from the wallet configuration.

### Invariant 4

The Table Wallet cannot independently determine poker winners.

### Invariant 5

The Table Wallet cannot independently calculate rake.

### Invariant 6

The Table Wallet cannot execute an unauthorized destination.

### Invariant 7

A failed settlement cannot be represented as a successful settlement.

### Invariant 8

A settlement retry cannot create a duplicate payout.

### Invariant 9

A Table Wallet cannot be closed while an unexplained balance remains.

### Invariant 10

Every monetary movement must be attributable to a table, hand or authorized settlement cycle.

### Invariant 11

The Ledger remains evidence infrastructure and does not become a second live-state authority.

### Invariant 12

Lightning/L2 remains an interchangeable payment/settlement rail abstraction rather than the definition of Table Wallet itself.

***

# 44. Required Reconciliation

A completed monetary cycle must be independently reconcilable across:

```text
TABLE PARTICIPANT STATE
        ↓
TABLE CONSENSUS
        ↓
TABLE WALLET CONFIGURATION
        ↓
WAGER INPUTS
        ↓
ACTIVE POT
        ↓
HAND_COMPLETED
        ↓
RAKE OBLIGATION
        ↓
SETTLEMENT REQUEST
        ↓
PAYMENT / SETTLEMENT REFERENCES
        ↓
WINNER / REFUND / RAKE OUTPUTS
        ↓
FINAL BALANCE
        ↓
LEDGER EVIDENCE
```

Any unresolved break in this chain is an audit exception.

***

# 45. Canonical Financial Invariant

For every fully settled hand:

```text
VALID WAGER INPUTS
=
VALID WINNER OUTPUTS
+
VALID REFUND OUTPUTS
+
VALID RAKE OUTPUTS
+
EXPLICITLY ACCOUNTED FEES
```

and, when no balance is intentionally carried:

```text
FINAL TABLE WALLET BALANCE = 0
```

No amount may disappear because it was not assigned to a known output category.

***

# 46. Non-Responsibilities

The Table Wallet Engine does not:

```text
create poker tables
admit players
define poker rules
determine winners
generate card randomness
deal cards
calculate rake
define the rake percentage
own player private keys
manage player seed phrases
become a permanent treasury
operate as the Lightning Network itself
replace the Monetary Settlement Engine
replace Table Consensus
replace the Private Off-Chain Ledger
define consensus thresholds
```

***

# 47. Implementation Abstraction

The implementation should expose conceptual interfaces equivalent to:

```text
createTableWallet()
authorizeTableWallet()
activateTableWallet()
registerWager()
receivePayment()
registerInput()
requestSettlement()
authorizeSettlement()
executePayout()
executeRake()
executeRefund()
verifyBalance()
closeTableWallet()
recoverTableWallet()
```

Exact API names are implementation details and are not normative.

***

# 48. Required Identifiers

At minimum, the implementation should distinguish:

```text
table_id
table_participant_id
player_wallet_id
table_wallet_instance_id
table_wallet_configuration_id
hand_id
wager_id
payment_request_id
settlement_request_id
rake_obligation_id
payment_reference
settlement_reference
ledger_event_id
```

No single identifier should be overloaded to represent multiple protocol objects.

***

# 49. Protocol Boundary for Lightning/L2

The selected payment rail must expose enough information to permit:

```text
authorization
payment execution
confirmation
failure reporting
reconciliation
retry/idempotency
```

The Table Wallet Engine must remain capable of representing the table's custody lifecycle independently of the implementation details of the selected rail.

This allows future compatibility with:

```text
Lightning
Bitcoin L2
other approved Bitcoin-compatible fast-settlement mechanisms
```

without redefining the Table Wallet concept.

***

# 50. Final Architectural Definition

The **Table Wallet Engine** is the Chain Poker Genesis component responsible for temporary shared custody and authorized monetary settlement at the table level.

Its canonical role is:

```text
TABLE PARTICIPANTS
       ↓
TABLE CONSENSUS
       ↓
SHARED CRYPTOGRAPHIC AUTHORIZATION
       ↓
TABLE WALLET
       ↓
LIGHTNING / L2
       ↓
ACTIVE TABLE VALUE
       ↓
AUTHORIZED SETTLEMENT
       ↓
WINNERS / REFUNDS / RAKE
       ↓
ZERO-BALANCE VERIFICATION
       ↓
CLOSED
```

The Table Wallet is jointly controlled by the authorized table participants according to the applicable cryptographic configuration.

The protocol does not require a central company to custody player funds.

The Player Wallet remains external.

The Table Wallet is temporary.

The Lightning/L2 layer is the payment rail.

The Poker Rules Engine determines the game result.

Engine 05 determines the rake obligation.

The Monetary Settlement Engine executes monetary settlement.

Engine 04 preserves the historical evidence.

***

# 51. Integration Gate

The following relationship is normative for the 09 boundary:

```text
08 TABLE JOIN
      ↓
TABLE PARTICIPANT STATE
      ↓
TABLE CONSENSUS
      ↓
TABLE WALLET AUTHORIZATION
      ↓
LIGHTNING / L2 PAYMENT RAIL
      ↓
TABLE WALLET
      ↓
HAND SETTLEMENT
      ↓
RAKE OBLIGATION
      ↓
MONETARY SETTLEMENT
      ↓
TABLE WALLET BALANCE VERIFICATION
      ↓
04 PRIVATE OFF-CHAIN LEDGER
```

No component may silently absorb another component's authority.

The governing principle is:

> **The player owns the player wallet. The participating players jointly authorize the temporary Table Wallet. The payment network moves value. Poker Rules determine the game result. Engine 05 determines the rake obligation. Monetary Settlement executes the authorized monetary distribution. Engine 04 preserves the evidence.**

***

# 52. Open Technical Items

The following remain intentionally open and must be specified elsewhere before production implementation:

1. Exact Table Consensus algorithm and quorum.
2. Exact Table Wallet cryptographic construction.
3. MuSig2/Taproot applicability to the selected payment infrastructure.
4. External HD Wallet signing protocol.
5. Exact Lightning/L2 adapter contract.
6. Payment confirmation requirements.
7. Settlement finality requirements.
8. Integer-satoshi rake calculation and rounding.
9. Dust and minimum-output rules.
10. Network-fee accounting.
11. Settlement failure/recovery protocol.
12. Wallet configuration activation boundary.
13. Cryptographic key rotation/revocation.
14. Canonical monetary event serialization.
15. Formal test vectors for wallet creation, funding and settlement.

These are specification tasks, not reasons to collapse the architectural separation established by this document.

***

# 53. Normative Closing Statement

A Chain Poker Genesis Table Wallet is a **temporary, jointly authorized shared-custody component created for table-level monetary operation and settlement**.

It does not replace the Player Wallet.

It does not require central company custody.

It does not define poker outcomes.

It does not calculate rake.

It does not become the Ledger.

It does not become Lightning.

Its purpose is to provide the cryptographic and economic boundary through which authorized player value enters the active table, remains temporarily under shared custody, and is deterministically distributed according to the authoritative settlement result.

The lifecycle is complete only when:

```text
AUTHORIZED INPUTS
        ↓
AUTHORIZED TABLE CUSTODY
        ↓
AUTHORIZED SETTLEMENT
        ↓
ALL REQUIRED OUTPUTS
        ↓
BALANCE VERIFIED
        ↓
CLOSED
        ↓
HISTORICAL EVIDENCE PRESERVED
```

**Document 09 — Table Wallet Engine v1.1 — Consolidated Corrected Specification**

**Status: READY FOR TECHNICAL INTEGRATION REVIEW**

© 2026 Lerry Alexander Elizondo Villalobos (LAEV)  
Chain Poker Genesis by LAEV
