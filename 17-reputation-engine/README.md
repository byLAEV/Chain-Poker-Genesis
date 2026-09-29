# Chain Poker Genesis — Reputation Engine

**Module:** 17.0 Reputation Engine  
**Repository:** Chain Poker Genesis by LAEV  
**Status:** Consolidated technical specification — repository-aligned revision  
**Purpose:** Reputation-based table governance and deterministic access control

## 1. Scope

The Reputation Engine is the subsystem responsible for deriving a verifiable player reputation state from protocol-observable events and for evaluating that state against the admission policy of a table.

It is a governance and eligibility engine, not a general-purpose identity system and not a mechanism for assigning moral value to players.

The engine defines:
- how reputation state is represented;
- which protocol events may contribute to that state;
- how activity and inactivity are represented;
- how a table declares its admission profile;
- how player/table compatibility is evaluated;
- how a reputation state may be exported and independently verified;
- how optional display aliases remain separated from real-world identity.

## 2. Normative Principles

1. **Rule-based admission:** table access is determined by the table's declared policy and the player's verifiable state, not by discretionary operator approval.
2. **Deterministic evaluation:** identical input state and identical table policy MUST produce the same admission result.
3. **Separation of concerns:** reputation, identity, wallet ownership, gameplay rules, settlement, and conflict resolution remain distinct protocol layers.
4. **Evidence-based state:** reputation components MUST be derived from defined protocol events or explicitly defined external attestations.
5. **Non-punitive inactivity:** inactivity is an activity-state dimension and MUST NOT automatically be interpreted as misconduct.
6. **Privacy by default:** the engine MUST NOT require disclosure of real-world identity merely to calculate or verify reputation.
7. **Verifiability:** exported reputation states MUST contain sufficient cryptographic evidence for independent validation, subject to the privacy model of the protocol.
8. **Versioning:** reputation algorithms, policy schemas, and export formats MUST be versioned so that historical states remain interpretable.

## 3. Reputation State Model

The conceptual reputation state is:

R = (A, C, T, S, M, I)

Where:

| Component | Meaning | Required interpretation |
|---|---|---|
| **A** | Strategic activity/aggression profile | Describes observed gameplay tendencies; it is not intrinsically positive or negative. |
| **C** | Gameplay consistency | Measures consistency according to protocol-defined observations. |
| **T** | Behavioral traceability | Measures the completeness/verifiability of protocol-observable behavioral history. |
| **S** | Suspicion/risk signals | Represents defined integrity-risk signals detected by the protocol. |
| **M** | Multi-account risk indicator | Represents protocol evidence associated with possible linked or duplicate accounts. |
| **I** | Activity/inactivity state | Represents session, absence, and historical activity state. |

### 3.1 Important distinction

The vector is **not inherently a single scalar score**.

A table policy MUST therefore specify the dimensions and thresholds it requires. A notation such as R >= 0.75 is permitted only if a separately versioned aggregation function defines exactly how the vector is normalized into that scalar.

Until such an aggregation function exists, admission MUST use explicit component predicates.

Example:

C >= C_min AND T >= T_min AND S <= S_max AND M <= M_max

## 4. Component Semantics

### 4.1 Strategic profile — A

A describes observable strategic tendencies such as aggression or passivity.

It MUST NOT be treated as a universal quality score. Different table policies may legitimately permit different strategic profiles.

### 4.2 Consistency — C

C represents consistency of protocol-observable participation and gameplay behavior over a defined observation window.

The calculation MUST specify:
- observation window;
- eligible events;
- missing-data treatment;
- normalization;
- version of the calculation algorithm.

### 4.3 Traceability — T

T measures how much of the relevant protocol history can be cryptographically reconstructed or verified.

Traceability MUST NOT mean disclosure of a player's civil identity.

### 4.4 Suspicion signals — S

S represents defined integrity or anomaly signals.

The engine MUST distinguish:
- observed protocol facts;
- derived risk indicators;
- unresolved allegations.

A suspicion signal MUST NOT by itself be represented as proof of misconduct.

### 4.5 Multi-account risk — M

M represents evidence associated with possible account linkage.

The implementation MUST define:
- permitted evidence sources;
- confidence representation;
- false-positive handling;
- privacy constraints;
- whether the value is advisory or admission-critical.

### 4.6 Activity / inactivity — I

I is an activity-state vector rather than a single moral score.

At minimum it distinguishes:
- **session inactivity:** AFK, pause, or short disconnection;
- **absence inactivity:** extended period without participation;
- **historical inactivity:** long-term activity cycles and returning-player status.

A recommended conceptual representation is:

I = (I_session, I_absence, I_historical)

The exact units and thresholds MUST be defined by the implementation specification.

## 5. Table Reputation Policy

Every reputation-governed table MAY define a policy object containing:
- minimum and/or maximum component thresholds;
- permitted activity/inactivity ranges;
- suspicion tolerance;
- multi-account risk tolerance;
- required integrity profile;
- accepted risk profile;
- observation-window requirements;
- reputation algorithm version;
- export/attestation requirements.

A table policy is itself protocol data and MUST be versioned.

### 5.1 Admission predicate

Conceptually:

Eligible(player, table) = Policy(table) AND ReputationState(player) AND ValidEvidence(player)

The result MUST be deterministic.

A failed predicate SHOULD return a machine-readable reason code rather than an opaque rejection.

## 6. Table Classes

The following are reference policy classes, not mandatory economic categories.

### 6.1 High-integrity table

Uses stricter integrity, traceability, risk, and activity requirements.

### 6.2 Return-player table

Designed for players whose historical activity state identifies them as returning participants.

### 6.3 Open table

Uses limited reputation restrictions while preserving protocol integrity requirements.

### 6.4 Experimental / research table

Permits explicitly declared experimental admission policies.

Experimental policies MUST NOT silently modify the global reputation state.

## 7. Relationship to Table Creation and Table Join

The Reputation Engine does not replace the Table Creation Engine or Table Join Engine.

The separation is:

**Table Creation Engine**
- creates the table;
- establishes its configuration;
- stores or references its admission policy.

**Reputation Engine**
- computes/maintains the player reputation state;
- evaluates the player's state against the table policy.

**Table Join Engine**
- executes the actual join request;
- invokes the reputation eligibility result where required;
- records the resulting admission decision.

Therefore:

Create Table → Declare Policy → Evaluate Player → Join Authorization → Table Entry

This prevents the reputation layer from becoming an implicit replacement for the join protocol.

## 8. Optional Wallet Display Alias

The protocol MAY support an optional wallet-linked display alias.

Properties:
- user-controlled;
- optional;
- revocable;
- publicly visible only where the table/UI policy permits;
- cryptographically associated with a wallet or protocol identity;
- not equivalent to civil identity;
- independent from the reputation calculation.

The protocol MUST preserve:

Wallet != RealIdentity

DisplayAlias != RealIdentity

ReputationState != Identity

A display alias MUST NOT automatically alter reputation.

## 9. Reputation State Lifecycle

A reputation state follows a versioned lifecycle:

1. **Observe** — protocol events are collected.
2. **Normalize** — eligible events are normalized according to the active algorithm.
3. **Compute** — reputation components are derived.
4. **Validate** — evidence and state integrity are checked.
5. **Commit** — a state identifier/version is established.
6. **Export** — an attestable representation MAY be produced.
7. **Supersede** — a later valid state replaces the active state for future evaluations.

Historical states SHOULD remain auditable where protocol privacy rules permit.

## 10. REP-EXPORT

The REP-EXPORT format is the interoperability representation for a reputation state.

A conceptual export contains:
- protocol identifier;
- player pseudonymous identifier/hash;
- reputation vector;
- activity vector;
- reputation algorithm version;
- policy/schema version;
- state timestamp;
- observation-window identifier;
- validator attestations/signatures;
- state hash;
- optional predecessor-state reference.

### 10.1 Privacy requirement

The export SHOULD minimize information disclosure.

A verifier should be able to verify the claims required for the relevant table policy without receiving unrelated behavioral history.

## 11. Consensus Validation

A reputation export MAY be validated by a distributed validator set.

For a validator set of N nodes, a two-thirds threshold is conceptually:

validity = approvals >= ceil(2N/3)

The implementation MUST define:
- validator-set membership;
- validator identity/key format;
- epoch or validator-set version;
- signature algorithm;
- quorum calculation;
- handling of unavailable validators;
- conflicting attestations;
- validator-set rotation.

A two-thirds threshold alone does not define a complete consensus protocol.

## 12. Conflict and Inconsistency Handling

A reputation state MUST NOT be accepted merely because it has signatures if the signed contents are inconsistent.

The validator layer SHOULD detect:
- different vector values for the same state identifier;
- invalid predecessor references;
- invalid timestamps;
- malformed state hashes;
- incompatible algorithm versions;
- conflicting validator attestations.

When a conflict exists, the state SHOULD enter an explicitly defined **UNRESOLVED** or equivalent status until the applicable conflict-resolution mechanism determines the canonical state.

The Reputation Engine MUST NOT silently choose a value.

## 13. Security Model

The engine is intended to mitigate:
- arbitrary table admission;
- opaque reputation manipulation;
- single-node reputation control;
- forged reputation exports;
- ambiguous historical state;
- unnecessary identity disclosure.

It does **not**, by itself, guarantee:
- Sybil resistance;
- detection of every multi-account relationship;
- truthful off-protocol behavior;
- absence of colluding validators;
- economic solvency;
- fair gameplay.

Those properties belong to other protocol mechanisms or require additional assumptions.

## 14. Data Minimization

The engine SHOULD avoid storing raw behavioral data when a cryptographically derived state is sufficient.

Where raw evidence is required, the implementation MUST define:
- retention period;
- access permissions;
- integrity protection;
- derivation method;
- deletion/expiration behavior;
- relationship between evidence and exported state.

## 15. Determinism Requirements

For a given:
- player state;
- observation window;
- algorithm version;
- table policy version;
- validator-set version;

the same implementation inputs MUST produce the same reputation evaluation.

Floating-point ambiguity SHOULD be avoided in consensus-critical calculations.

Where numeric scores are consensus-critical, fixed-point or explicitly specified integer arithmetic SHOULD be used.

## 16. Versioning

The following MUST be versioned independently where applicable:
- reputation calculation algorithm;
- reputation vector schema;
- activity schema;
- table policy schema;
- REP-EXPORT schema;
- validator-set configuration.

A reputation state MUST identify the versions necessary to reproduce its interpretation.

## 17. Cross-Engine Dependencies

The Reputation Engine is expected to interact with:
- **Table Creation Engine** — table policy declaration;
- **Table Join Engine** — admission enforcement;
- **Poker Rules Engine** — gameplay event semantics;
- **Dealer Engine** — authoritative card-consumption/dealing events where relevant;
- **Player Node / Disconnection Management** — session activity and disconnection events;
- **P2P Conflict Resolution Engine** — resolution of inconsistent state;
- **Monetary Settlement Engine** — settlement-related events when explicitly included by policy;
- **Protocol Documentation Engine** — canonical specification and version records;
- **Consensus / cryptographic layers** — signatures, hashes, and validator attestations.

The Reputation Engine MUST NOT silently assume that another engine provides data unless the interface is explicitly specified.

## 18. Reference Admission Example

A table policy could declare:
- C >= 0.75
- T >= 0.80
- S <= 0.10
- M <= 0.05
- historical inactivity within the table's declared range;
- reputation algorithm version = v3.

A player is eligible only if every mandatory predicate is satisfied and the underlying reputation state is valid.

This example does not establish universal thresholds for the ecosystem.

## 19. Formal Result Codes

A reference implementation SHOULD expose deterministic result codes such as:
- REP_OK
- REP_STATE_MISSING
- REP_STATE_EXPIRED
- REP_POLICY_MISMATCH
- REP_THRESHOLD_FAILED
- REP_EVIDENCE_INVALID
- REP_CONSENSUS_PENDING
- REP_CONSENSUS_CONFLICT
- REP_ALGORITHM_UNSUPPORTED

The exact code registry belongs to the protocol-wide error-code specification.

## 20. Final Definition

The Chain Poker Genesis Reputation Engine is a deterministic, versioned reputation-state and table-governance subsystem.

It evaluates protocol-observable player state against explicitly declared table policies while preserving separation between reputation and real-world identity.

Its core rule is:

> A player is admitted to a reputation-governed table when the player's valid reputation state satisfies every mandatory predicate declared by that table's policy.

The engine therefore functions as a **verifiable table-admission layer**, rather than as an autonomous identity authority or an undifferentiated player-ranking system.

## 21. Source Document

Source material:

17.0 Reputation Engine_Chain Poker Genesis.pdf

This README is the repository-aligned consolidation of that source specification and records the normative clarifications required for deterministic implementation.

---

**Chain Poker Genesis by LAEV**  
**Reputation Engine — Module 17.0**
