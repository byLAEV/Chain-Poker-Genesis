# CHAIN POKER GENESIS BY LAEV

# 12 — Monetary Settlement Engine

## Official Technical Specification v1.2

**Document Class:** CORE ENGINE  
**Document Status:** INTEGRATION-READY  
**Architecture Role:** Authorized Monetary Settlement Execution  
**Previous Specification:** v1.1  
**Revision:** v1.2  
**Protocol:** Chain Poker Genesis by LAEV

---

## 0. Document Control

~~~text
[LCCP]
SEQ: 12
PREV: 11
SELF: 12
NEXT: 13
CLASS: CORE ENGINE
STATUS: INTEGRATION-READY
[/LCCP]
~~~

This specification defines the Monetary Settlement Engine.

The engine executes authorized monetary settlement resulting from completed poker operations. It does not determine poker outcomes, create tables, admit players, manage player connection state or control the lifecycle of the Table Wallet instance.

---

# 1. Purpose

The Monetary Settlement Engine is responsible for executing valid and authorized settlement instructions.

~~~text
AUTHORIZED SETTLEMENT INSTRUCTION
             ↓
MONETARY SETTLEMENT ENGINE
             ↓
SETTLEMENT EXECUTION
             ↓
SETTLEMENT RESULT
             ↓
SETTLEMENT EVIDENCE
~~~

The engine may move or distribute funds only according to a valid authorization produced by the applicable protocol authority.

It does not independently decide who won, how much each player should receive, whether a hand is complete or whether a player is entitled to funds.

---

# 2. Non-Responsibilities

The Monetary Settlement Engine does not determine:

- poker hand outcomes;
- winners or losers;
- poker actions;
- card generation or dealing;
- table creation;
- table admission;
- participant membership;
- connection or disconnection lifecycle;
- Table Wallet lifecycle;
- Requests and Permissions policy;
- table consensus decisions.

These responsibilities belong to their respective engines and authorities.

---

# 3. Authority Model

Settlement separates authorization from execution.

Canonical relationship:

~~~text
POKER / TABLE LOGIC
        ↓
SETTLEMENT REQUEST
        ↓
REQUESTS & PERMISSIONS / AUTHORIZATION
        ↓
AUTHORIZED SETTLEMENT INSTRUCTION
        ↓
MONETARY SETTLEMENT ENGINE
        ↓
TABLE WALLET / APPROVED PAYMENT RAIL
        ↓
SETTLEMENT RESULT
~~~

The Monetary Settlement Engine is an executor of authorized financial instructions.

It must not become a second authorization authority by silently changing amount, recipient, asset, network, destination or settlement conditions.

---

# 4. Table Wallet Boundary

The canonical monetary storage/custody object is:

~~~text
TABLE_WALLET_INSTANCE
~~~

Engine 12 may execute an authorized settlement operation against the applicable Table Wallet instance.

Engine 12 does not:

- create the Table Wallet instance;
- select its lifecycle;
- open or close it;
- replace it;
- change its cryptographic signer configuration;
- unilaterally reconfigure it.

Those responsibilities remain with the Table Wallet Engine.

---

# 5. Settlement Instruction

A settlement instruction should contain, at minimum:

~~~text
settlement_id
table_id
hand_id
authorization_reference
asset
network
settlement_rail
source_reference
destination_reference
amount
authorization_timestamp
instruction_version
idempotency_key
~~~

The exact field set may be extended by the applicable engine version.

The instruction must identify the authorized financial operation without requiring Engine 12 to infer missing business logic.

---

# 6. Input Validation

Before execution, Engine 12 verifies, as applicable:

~~~text
instruction identity
authorization authenticity
instruction integrity
table identity
hand identity
asset
network
settlement rail
amount
destination
engine compatibility
authorization status
expiry / validity window
idempotency state
~~~

An invalid or unauthorized instruction must not be executed.

---

# 7. Settlement Lifecycle

A settlement operation is distinct from the lifecycle of the Table Wallet instance.

Canonical settlement-operation states:

~~~text
CREATED
    ↓
AUTHORIZED
    ↓
SUBMITTED
    ↓
CONFIRMED
~~~

Terminal or exceptional states may include:

~~~text
FAILED
UNKNOWN
~~~

The operation state must not be confused with the TABLE_WALLET_INSTANCE lifecycle.

An operation may fail without changing the wallet instance lifecycle.

---

# 8. Idempotency and Replay Protection

Every settlement operation must have a unique settlement identity.

At minimum:

~~~text
settlement_id
idempotency_key
~~~

The engine must reject or safely deduplicate an already executed logical operation.

The same authorized settlement must not be applied twice because a message was retried, duplicated or replayed.

Conceptually:

~~~text
SAME AUTHORIZED OPERATION
        +
RETRY
        ↓
SINGLE EFFECT
~~~

---

# 9. Monetary Integrity

The engine must preserve the integrity of:

~~~text
asset
amount
destination
network
settlement rail
authorization
~~~

It must not silently convert assets, networks, settlement mechanisms, destinations or amounts.

Any conversion or routing rule must be explicit in the authorized instruction and supported by the selected settlement implementation.

---

# 10. Bitcoin as Default Settlement Environment

The official/default monetary settlement environment is Bitcoin.

The architecture is designed to support Bitcoin technologies including, where compatible with the selected implementation:

- Bitcoin mainnet;
- Bitcoin test networks;
- payment channels;
- Bitcoin Layer 2 systems;
- UTXO-based settlement;
- Bitcoin-compatible micropayment mechanisms.

These concepts remain distinct:

~~~text
ASSET
≠
NETWORK
≠
SETTLEMENT RAIL
≠
LAYER
≠
CHANNEL
~~~

Bitcoin is the default monetary environment, while a channel, layer or payment rail represents a specific technical mechanism for moving or settling that asset.

---

# 11. Source and Destination Boundary

For a table settlement funded through the Table Wallet, Engine 12 may use the authorized TABLE_WALLET_INSTANCE as the source or destination context.

However, the phrase "sole source and destination of all funds" must not be interpreted as a universal statement about every external funding, withdrawal, channel or payment path.

External wallets, payment rails, adapters and settlement networks may exist outside the Table Wallet boundary.

The settlement instruction determines which source and destination references are valid for the specific operation.

---

# 12. Settlement Engine Selection

The settlement engine used by a table is selected through the applicable table-creation/governance process.

Conceptually:

~~~text
TABLE CREATION
      ↓
GOVERNANCE / CONFIGURATION
      ↓
SETTLEMENT ENGINE SELECTION
      ↓
TABLE CONFIGURATION
      ↓
TABLE CREATED
~~~

The selected settlement engine becomes the compatible settlement environment for the table according to the table's governing configuration.

Engine 12 does not independently change the selected engine.

---

# 13. Node Compatibility

The selected settlement engine establishes technical compatibility requirements that a node must satisfy before participating in the table.

Compatibility may include:

~~~text
asset support
network support
settlement rail support
wallet interface support
cryptographic requirements
protocol version
engine version
~~~

Compatibility is not the same as table membership authority.

The Table Join Engine remains responsible for player admission.

---

# 14. Settlement Execution

Once an instruction is validly authorized and validated:

~~~text
AUTHORIZED
    ↓
SUBMITTED
    ↓
EXECUTION
    ↓
CONFIRMED
~~~

The engine must return an execution result that identifies the outcome.

A successful result should contain, where applicable:

~~~text
settlement_id
execution_status
asset
amount
destination
network
settlement_rail
transaction_reference
confirmation_reference
evidence_reference
timestamp
~~~

---

# 15. Failure Handling

The engine distinguishes at least:

~~~text
INVALID_INSTRUCTION
UNAUTHORIZED
INSUFFICIENT_FUNDS
INCOMPATIBLE_ASSET
INCOMPATIBLE_NETWORK
INCOMPATIBLE_RAIL
INVALID_DESTINATION
DUPLICATE_SETTLEMENT
REPLAY_DETECTED
SUBMISSION_FAILED
CONFIRMATION_TIMEOUT
UNKNOWN
~~~

A failure must not be represented as confirmation.

An unknown external result must not be silently converted into success or failure without reconciliation.

---

# 16. Evidence

Every executed settlement should produce sufficient evidence for later verification.

Evidence may include:

~~~text
settlement_id
authorization_reference
transaction_reference
network
asset
amount
destination
submission_timestamp
confirmation_timestamp
confirmation_reference
adapter_reference
result_hash
~~~

The exact evidence format depends on the selected settlement implementation.

Evidence is a record of execution; it does not replace the source authorization.

---

# 17. Security Invariants

Engine 12 must preserve at least the following invariants:

1. No settlement without valid authorization.
2. No silent modification of authorized amount.
3. No silent modification of destination.
4. No silent asset substitution.
5. No silent network substitution.
6. No duplicate settlement for the same logical operation.
7. Replay must not produce a second monetary effect.
8. Failed settlement must not be reported as confirmed.
9. Unknown external status must remain distinguishable from success.
10. Table Wallet lifecycle is controlled by Engine 09.
11. Player membership is controlled by the table admission/membership authorities.
12. Disconnection is not settlement authorization.
13. Documentation is not settlement authorization.
14. Settlement evidence must remain linked to its authorization reference.

---

# 18. Relationship to Engine 08

Engine 08 controls table admission and participant identity.

Engine 12 may consume financial requirements of an authorized join or settlement workflow where the protocol requires them, but it does not become the membership authority.

The boundary is:

~~~text
08 TABLE JOIN
      ↓
participant admission
      ↓
financial authorization request
      ↓
12 / monetary subsystem
~~~

Engine 12 does not create or remove participants.

---

# 19. Relationship to Engine 09

Engine 09 retains authority over:

- Table Wallet instance lifecycle;
- wallet cryptographic configuration;
- authorized signer configuration;
- wallet operational state.

Engine 12 executes authorized settlement actions using the relevant wallet or rail interface.

Therefore:

~~~text
09 = TABLE_WALLET authority
12 = SETTLEMENT execution
~~~

These authorities are complementary and must not be merged.

---

# 20. Relationship to Engine 10

Engine 10 controls:

- disconnection;
- reconnection;
- synchronization;
- absence;
- abandonment workflow;
- removal workflow.

Engine 12 does not treat:

~~~text
DISCONNECTED
ABSENT
ABANDONED
REMOVED
~~~

as automatic financial settlement authorization.

Where a participant removal changes a later settlement context, the applicable authorization and Table Wallet procedures must explicitly establish that consequence.

---

# 21. Relationship to Engine 11

Engine 11 documents, versions, publishes and preserves the specification and audit trail.

It does not authorize or execute monetary operations.

The relationship is:

~~~text
12
operational settlement execution
        ↓
11
documentation / traceability
~~~

A published Engine 12 specification does not itself authorize a settlement.

---

# 22. Events

Settlement events should be uniquely identifiable and traceable.

Canonical events include:

~~~text
SETTLEMENT_CREATED
SETTLEMENT_AUTHORIZED
SETTLEMENT_SUBMITTED
SETTLEMENT_CONFIRMED
SETTLEMENT_FAILED
SETTLEMENT_UNKNOWN
~~~

The exact externally exposed event set must remain consistent with the protocol's canonical event registry.

Each event should preserve, where applicable:

~~~text
event_id
event_type
settlement_id
table_id
hand_id
authorization_reference
timestamp
event_hash
~~~

The Private Off-Chain Ledger Engine remains the historical persistence authority for protocol events.

---

# 23. Operation vs Wallet Lifecycle

The following are intentionally independent:

~~~text
SETTLEMENT_OPERATION
~~~

and:

~~~text
TABLE_WALLET_INSTANCE
~~~

Therefore:

~~~text
SETTLEMENT_FAILED
    ≠
WALLET_CLOSED
~~~

and:

~~~text
SETTLEMENT_CONFIRMED
    ≠
CREATE_NEW_WALLET
~~~

Wallet lifecycle transitions must be authorized through Engine 09 and the applicable table lifecycle.

---

# 24. Engine Modularity

The protocol supports multiple compatible settlement implementations.

A settlement implementation should provide a common logical interface able to:

1. receive a valid settlement instruction;
2. validate instruction compatibility;
3. execute through the selected asset, network and rail;
4. return a deterministic protocol status;
5. provide execution evidence;
6. expose failure and unknown results;
7. enforce idempotency and replay protection.

This allows future settlement implementations without changing poker logic.

Possible environments may include:

~~~text
Bitcoin mainnet
Bitcoin test networks
Bitcoin Layer 2
payment channels
other compatible digital assets
stablecoin systems
traditional electronic-money rails
play-money / virtual currencies
~~~

Any additional environment must satisfy protocol compatibility, authorization, security and evidence requirements before being admitted into the ecosystem.

---

# 25. Change of Settlement Engine

The selected settlement engine should be treated as a table configuration parameter.

A change during an active table requires explicit governance and migration rules.

Before such a migration can be considered valid, the protocol must account for:

- outstanding settlement operations;
- funds already held in the current wallet context;
- asset and network compatibility;
- pending channel or rail operations;
- evidence reconciliation;
- node compatibility;
- prevention of mixed or ambiguous settlement authority.

Until a migration procedure is explicitly defined and authorized, the selected settlement engine should not be changed silently during the table lifetime.

---

# 26. Determinism

For identical authorized settlement instructions and identical external execution conditions, compatible implementations should produce equivalent protocol results.

Deterministic protocol inputs include:

~~~text
settlement_id
authorization_reference
asset
network
rail
amount
destination
instruction_version
~~~

External confirmation timing may be nondeterministic; the protocol must therefore distinguish deterministic instruction processing from external settlement confirmation.

---

# 27. Auditability

A completed settlement must permit reconstruction of:

- what instruction was authorized;
- who or what authorized it;
- which table and hand it belonged to;
- which asset and amount were specified;
- which destination was specified;
- which network and rail were selected;
- when submission occurred;
- when confirmation occurred;
- what evidence was produced;
- whether the operation was retried or deduplicated.

The audit record must distinguish:

~~~text
AUTHORIZED
≠
SUBMITTED
≠
CONFIRMED
~~~

---

# 28. Final Architectural Boundary

The Monetary Settlement Engine is the execution component for authorized monetary settlement.

Its central rule is:

~~~text
POKER LOGIC
    ↓
AUTHORIZATION
    ↓
SETTLEMENT ENGINE
    ↓
MONETARY EXECUTION
~~~

And explicitly:

~~~text
SETTLEMENT ENGINE
    ≠
POKER RULES
    ≠
TABLE JOIN
    ≠
TABLE WALLET LIFECYCLE
    ≠
DISCONNECTION MANAGEMENT
    ≠
DOCUMENTATION
~~~

---

# 29. Integration Status

This revision incorporates the architectural boundaries established during the review of Engines 08, 09, 10 and 11.

Integration requirements for the current revision include:

- authorization separated from execution;
- Table Wallet lifecycle retained by Engine 09;
- disconnection and removal retained by Engine 10;
- documentation authority retained by Engine 11;
- table admission retained by Engine 08;
- settlement idempotency and replay protection;
- settlement operation states separated from wallet lifecycle;
- settlement evidence separated from authorization.

**Status: INTEGRATION-READY**

---

© 2026 Lerry Alexander Elizondo Villalobos (LAEV).  
Chain Poker Genesis by LAEV.
