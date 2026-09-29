
# CHAIN POKER GENESIS BY LAEV

# 18 — CID Engine

## Content Identity, Evidence, Chained Logs and Protocol Reference Engine

**Document Class:** CORE INFRASTRUCTURE ENGINE  
**Document Status:** CONSOLIDATED ARCHITECTURAL SPECIFICATION v1.0  
**Architecture Role:** Content Identity, Integrity, Evidence Reference, Log Fragmentation and Historical Object Linking  
**Protocol:** Chain Poker Genesis by LAEV  
**Revision:** v1.0

---

## 0. Document Control

~~~text
[LCCP]
SEQ: 18
PREV: 17
SELF: 18
NEXT: 19
CLASS: CORE INFRASTRUCTURE ENGINE
STATUS: CONSOLIDATED
[/LCCP]
~~~

This document establishes the **CID Engine** as a native infrastructure component of Chain Poker Genesis.

The CID Engine provides a canonical mechanism for identifying protocol objects by their content and for constructing verifiable references between events, records, evidence, logs, sessions, agreements, consensus records and historical structures.

The CID Engine does **not** decide truth, resolve conflicts, determine reputation, or independently establish the factual or legal validity of a claim.

Its fundamental responsibility is:

> **Identify what an object is, preserve a verifiable reference to its exact content, and provide the cryptographic linkage required to determine whether that content or its chain of references has changed.**

---

# 1. Purpose

The CID Engine provides the common content-identity layer for the CPG protocol.

It supports, subject to the applicable object policy:

- protocol object identification;
- content integrity;
- tamper detection;
- evidence references;
- individual node records;
- player declarations;
- session reports;
- hand reports;
- table records;
- consensus records;
- P2P agreements;
- conflict-resolution records;
- identity evidence;
- KYC evidence references;
- reputation evidence references;
- replay packages;
- state snapshots;
- event logs;
- fragmented logs;
- chained logs;
- historical roots;
- cross-node references;
- protocol-version references;
- document references;
- external storage references;
- optional external anchoring.

The CID Engine is therefore an infrastructure layer, not merely an IPFS adapter.

---

# 2. Fundamental Principle

The CID Engine answers:

> **Which exact content does this reference identify?**

It does not answer:

> **Is this content true?**

A player may publish a false declaration and still receive a valid CID for that declaration.

Therefore:

~~~text
CID
=
CONTENT IDENTITY / INTEGRITY REFERENCE

CID
≠
TRUTH DETERMINATION
~~~

A false statement can have a valid CID.

A true statement can have a valid CID.

A disputed statement can have a valid CID.

The CID identifies the object that was presented.

---

# 3. Truth and Protocol Recognition

CPG separates content integrity from protocol recognition.

~~~text
CONTENT
   ↓
CANONICALIZATION
   ↓
CID
   ↓
SIGNATURE / AUTHORIZATION
   ↓
PROTOCOL RECORD
   ↓
CONSENSUS
   ↓
RECOGNITION / REJECTION / DISPUTE
~~~

The Consensus and Conflict Resolution layers determine what the protocol recognizes when competing records exist.

Therefore:

- CID Engine identifies content.
- Signature layer identifies authorization or authorship.
- Consensus determines protocol recognition.
- Conflict Resolution determines how contradictions are processed.
- Reputation Engine may derive reputation events from resolved protocol outcomes.

No component should silently assume the authority of another.

---

# 4. Content Identity Model

A canonical CPG object is processed conceptually as:

~~~text
RAW OBJECT
    ↓
CANONICAL REPRESENTATION
    ↓
CONTENT DIGEST
    ↓
CONTENT IDENTIFIER
    ↓
CPG CONTENT REFERENCE
~~~

Canonicalization is mandatory whenever logically equivalent representations must produce the same protocol object identity.

The canonicalization profile MUST define:

- serialization format;
- field ordering;
- numeric representation;
- text encoding;
- treatment of optional fields;
- treatment of null values;
- normalization rules;
- protocol version;
- digest algorithm;
- CID generation profile.

An implementation MUST NOT silently create a second canonical representation.

---

# 5. CID and Change Detection

The central integrity property is:

~~~text
CONTENT-A
    ↓
CID-A

CONTENT-B
    ↓
CID-B
~~~

If canonical content changes in a way that changes its digest:

~~~text
CID-A ≠ CID-B
~~~

A verifier can therefore detect that the received object does not correspond to the previously registered content.

This establishes content difference. It does not independently establish why the content changed or who changed it.

---

# 6. CID Is Not a Truth Oracle

The following distinction is normative:

~~~text
INTEGRITY
    =
"Is this the same content?"

TRUTH / VALIDITY
    =
"Should the protocol recognize this content as valid?"
~~~

The first belongs to content identity.

The second belongs to protocol rules, evidence policy, consensus and conflict resolution.

---

# 7. CPG Content Reference

The protocol SHOULD use a wrapper around the raw CID for protocol context.

Recommended conceptual object:

~~~json
{
  "record_type": "CPG_CONTENT_REFERENCE",
  "cid": "bafy...",
  "artifact_type": "SESSION_REPORT",
  "protocol_version": "1.0",
  "creator_id": "PLAYER-001",
  "sequence": 42,
  "previous_cid": "bafy...",
  "created_at": "protocol-timestamp",
  "signatures": [],
  "context": {}
}
~~~

The exact canonical schema is governed by the CPG data-model specification.

The distinction is:

~~~text
CID
    =
identity of content

CPG Content Reference
    =
CID + protocol context + references + authorization
~~~

---

# 8. Signed Content Reference

A CPG content reference MAY be signed.

Recommended conceptual flow:

~~~text
Canonical Content Reference
        ↓
Digest / CID
        ↓
Canonical Signed Record
        ↓
Participant Signature(s)
        ↓
Consensus Signature(s), when applicable
~~~

Signatures MUST cover a canonical representation of the signed record.

A signature MUST NOT be described as proof that the content is factually true.

It proves that the signing identity authorized the signed representation under the applicable signature rules.

---

# 9. Individual Node CIDs

Every participating node may create independently identified records.

~~~text
NODE-001
   │
   ├── Event CID
   ├── Observation CID
   ├── State CID
   ├── Evidence CID
   └── Session CID
~~~

An individual CID means:

> This node produced or referenced this exact object.

It does not automatically mean that other nodes agree with it.

This allows CPG to preserve independent observations before consensus.

---

# 10. Group CIDs

Multiple participants may create a common object.

~~~text
PLAYER-A ─┐
PLAYER-B ─┼──→ GROUP CONTENT
PLAYER-C ─┘          ↓
                    CID
~~~

A group CID may represent:

- a jointly authored report;
- a jointly accepted state;
- a P2P agreement;
- a shared evidence package;
- a collaborative statement;
- a group session report.

The CID identifies the group object.

Participant signatures identify participants who authorized it.

---

# 11. Consensus CIDs

A consensus record may itself become a CID-identified object.

~~~text
Individual Records
      ↓
Evidence Set
      ↓
Consensus Process
      ↓
Consensus Record
      ↓
Consensus CID
~~~

A Consensus CID may identify:

- accepted state;
- rejected proposal;
- resolved conflict;
- table closure;
- settlement authorization record;
- evidence recognition result;
- protocol state confirmation.

The Consensus CID does not replace the underlying evidence.

It identifies the resulting consensus record.

---

# 12. Session Report CIDs

A player or table may request:

> "Create a CID containing the results of this session."

The CID Engine can create a canonical session report containing, according to policy:

- session identifier;
- player identities;
- table identifier;
- hands;
- actions;
- contributions;
- settlement references;
- disputes;
- resolutions;
- final state;
- protocol version;
- relevant evidence references;
- signatures.

Conceptually:

~~~text
SESSION
   │
   ├── HAND CIDs
   ├── EVENT CIDs
   ├── SETTLEMENT CIDs
   ├── DISPUTE CIDs
   └── RESOLUTION CIDs
            ↓
      SESSION REPORT
            ↓
       SESSION CID
~~~

A player may present this CID to another compatible application as a reference to the exact session report.

---

# 13. Event CIDs

Individual protocol events MAY receive their own content identifiers.

~~~text
EVENT
 ├── table_id
 ├── hand_id
 ├── event_id
 ├── actor
 ├── action
 ├── previous_state
 ├── resulting_state
 ├── sequence
 └── protocol version
          ↓
        CID
~~~

This permits precise referencing of individual events without requiring an entire session or hand to be transmitted.

---

# 14. Fragmented Logs

Large logs SHOULD be fragmentable.

Instead of one permanent object:

~~~text
FULL LOG
   ↓
ONE HUGE OBJECT
~~~

CPG may use:

~~~text
LOG
 ├── Fragment 001 → CID-001
 ├── Fragment 002 → CID-002
 ├── Fragment 003 → CID-003
 └── Fragment 004 → CID-004
~~~

Each fragment may contain:

- fragment sequence;
- previous fragment CID;
- event range;
- first sequence;
- last sequence;
- state reference;
- creator node;
- protocol version;
- creation metadata;
- signatures;
- optional next-fragment reference.

---

# 15. Chained Log Fragments

A fragment chain MAY be represented as:

~~~text
CID-001
   ↓
CID-002
   ↓
CID-003
   ↓
CID-004
~~~

A fragment can conceptually contain:

~~~json
{
  "record_type": "CPG_LOG_FRAGMENT",
  "sequence": 42,
  "previous_cid": "bafy...",
  "events": [],
  "first_event_sequence": 4001,
  "last_event_sequence": 4050,
  "creator_id": "NODE-001",
  "protocol_version": "1.0"
}
~~~

Because the next fragment references the previous CID, modification of an earlier fragment can cause chain verification to fail.

This creates a tamper-evident continuity structure.

---

# 16. Log Fragmentation Does Not Automatically Establish Truth

A perfectly chained log can still contain an incorrect observation.

Therefore:

~~~text
CHAIN INTEGRITY
    ≠
FACTUAL TRUTH
~~~

The chain proves continuity of the recorded objects.

Consensus and protocol verification determine whether those records are recognized.

---

# 17. Cross-Node Log Chains

Independent nodes may maintain separate chains.

~~~text
NODE A
A1 → A2 → A3

NODE B
B1 → B2 → B3

NODE C
C1 → C2 → C3
~~~

A consensus record can reference relevant terminal or selected CIDs:

~~~text
A3 ─┐
B3 ─┼──→ CONSENSUS CID
C3 ─┘
~~~

This preserves both:

- independent observations;
- collective recognition.

The protocol MUST NOT silently overwrite an individual node's original evidence merely because another record was accepted.

---

# 18. Historical Object Hierarchy

CPG may build hierarchical references:

~~~text
EVENT CID
    ↓
HAND CID
    ↓
SESSION CID
    ↓
TABLE CID
    ↓
DAILY ROOT
    ↓
PERIOD ROOT
    ↓
HISTORICAL ROOT
~~~

Each higher-level object references lower-level objects rather than duplicating their entire contents.

This provides efficient historical navigation and verification.

---

# 19. Merkle and Aggregate Structures

Multiple CIDs MAY be aggregated into a Merkle tree or equivalent authenticated data structure.

~~~text
CID-001 ─┐
CID-002 ─┤
CID-003 ─┼──→ MERKLE ROOT
CID-004 ─┘
~~~

The aggregate root can represent a set of records without storing every record inside the root object.

The aggregation mechanism MUST be separately specified if it becomes normative.

---

# 20. Temporal Records

CPG may create records representing:

- an event;
- a session;
- a day;
- an hour;
- a protocol period;
- a table interval;
- a historical checkpoint.

Example:

~~~text
DAY
 │
 ├── 10:00 → Event CIDs
 ├── 10:15 → Event CIDs
 ├── 10:30 → Event CIDs
 └── 11:00 → Event CIDs
~~~

A timestamp stored in a CID object is a declared protocol field.

A timestamp alone MUST NOT be treated as absolute proof that the object existed at that physical time.

Temporal assurance may additionally derive from:

- protocol sequence;
- signed observations;
- consensus ordering;
- predecessor references;
- external anchoring;
- other formally defined temporal mechanisms.

---

# 21. CID and Replay

Replay artifacts can be identified by CID.

~~~text
HAND
  ↓
EVENT LOG
  ↓
REPLAY PACKAGE
  ↓
CID
~~~

The replay package may reference:

- ruleset;
- Dealer state;
- card commitment;
- state transitions;
- actions;
- signatures;
- settlement references;
- final state;
- evidence;
- protocol versions.

A replay CID identifies the exact replay package used for verification.

---

# 22. CID and Identity

A cryptographic player identity may be associated with CIDs without making the CID itself an identity.

~~~text
PLAYER-001
    │
    ├── Identity Key Reference
    ├── Photo Evidence CID
    ├── Video Evidence CID
    ├── Document Evidence CID
    └── Certification CID
~~~

The CID identifies the evidence object.

The cryptographic identity identifies the participant associated with the signed record.

---

# 23. CID and KYC

The CID Engine can support KYC evidence without making the CID itself a KYC decision.

~~~text
Identity Document
      ↓
Encrypted Evidence Object
      ↓
CID
      ↓
KYC Evidence Reference
      ↓
Verifier / Policy
      ↓
KYC Resolution
~~~

A CID may preserve the exact evidence submitted during a KYC process.

If the underlying content is changed:

~~~text
Original CID ≠ New CID
~~~

The CID system can detect that the content is no longer identical.

The CID does not independently determine whether the document is authentic.

---

# 24. CID and Declarations

A player may voluntarily create a CID for a statement or report.

Example:

> "These are my results from this session."

CPG can generate:

~~~text
PLAYER DECLARATION
      ↓
CANONICAL OBJECT
      ↓
CID
      ↓
PLAYER SIGNATURE
~~~

Later, the declaration can be compared against protocol records.

The declaration may be:

- consistent;
- inconsistent;
- incomplete;
- disputed;
- accepted;
- rejected.

The CID remains the reference to what was actually declared.

---

# 25. CID and P2P Conflict Resolution

The P2P Conflict Resolution Engine can use CIDs as precise references to disputed objects.

~~~text
PLAYER A
  ↓
CID-A

PLAYER B
  ↓
CID-B

      ↓
P2P CONFLICT ENGINE
      ↓
NEGOTIATION
      ↓
AGREEMENT
      ↓
AGREEMENT CID
      ↓
SIGNATURE A + SIGNATURE B
~~~

The agreement itself can become a CID-identified object.

If no agreement is reached:

~~~text
P2P FAILURE
     ↓
TABLE CONSENSUS
     ↓
NETWORK ESCALATION
~~~

This preserves the evidence path.

---

# 26. CID and Conflict Resolution

A conflict record may reference:

- competing CIDs;
- parties;
- signatures;
- relevant protocol state;
- sequence;
- evidence;
- proposals;
- responses;
- final resolution.

Conceptually:

~~~text
CONFLICT
 ├── CID-A
 ├── CID-B
 ├── CID-C
 │
 └── Resolution CID
~~~

The resolution record can state which evidence the protocol recognizes without modifying the original evidence objects.

---

# 27. CID and Reputation

The Reputation Engine may consume resolved CID-linked events.

~~~text
PLAYER-001
     │
     ▼
DECLARATION CID
     │
     ▼
CONFLICT
     │
     ▼
CONSENSUS RESOLUTION
     │
     ▼
REPUTATION EVENT
     │
     ▼
PLAYER REPUTATION STATE
~~~

This enables reputation to be based on traceable protocol events rather than unsupported assertions.

The Reputation Engine remains responsible for reputation policy.

The CID Engine remains responsible for content identity.

---

# 28. CID and Table Wallet / Settlement

Economic records may reference CIDs for:

- settlement reports;
- payment evidence;
- table closure;
- contribution records;
- dispute records;
- settlement resolutions.

The CID does not become a monetary ledger.

The economic source remains the applicable Table Wallet / settlement and payment evidence subsystem.

The CID provides an integrity reference to the corresponding report or evidence object.

---

# 29. CID and Ledger

The CPG canonical ledger may reference CIDs rather than embedding every large artifact.

~~~text
LEDGER EVENT
   │
   ├── event_id
   ├── state transition
   ├── actor
   ├── sequence
   └── content_reference → CID
~~~

This permits the ledger to remain interoperable and compact while large evidence objects remain separately stored.

The Ledger and CID Engine have different responsibilities:

~~~text
LEDGER
=
canonical protocol representation

CID ENGINE
=
content identity and object reference
~~~

---

# 30. CID and Decentralized Storage

A CID can be used to retrieve or verify content from compatible content-addressed storage.

IPFS is one possible storage mechanism.

However:

~~~text
CID ≠ IPFS
~~~

The CID Engine MUST NOT depend conceptually on one storage provider.

Storage adapters may include:

- IPFS;
- local storage;
- distributed object storage;
- archival storage;
- other content-addressed systems.

A storage system stores or transports content.

The CID identifies the content.

---

# 31. CID and Encryption

Sensitive objects may be encrypted before storage.

~~~text
PRIVATE DATA
    ↓
ENCRYPTION
    ↓
ENCRYPTED OBJECT
    ↓
CID
~~~

The CID identifies the encrypted object.

This permits the protocol to preserve integrity without requiring sensitive plaintext to be publicly available.

Access control and key management remain outside the fundamental CID function.

---

# 32. CID and Evidence Preservation

The CID Engine can preserve references to:

- photos;
- videos;
- screenshots;
- documents;
- logs;
- replay packages;
- signed statements;
- external evidence;
- identity evidence;
- protocol reports.

The existence of a CID means that an object was identifiable by that content reference.

It does not independently establish the factual correctness of the object.

---

# 33. CID and Protocol Versioning

Protocol objects SHOULD reference the applicable protocol version.

Example:

~~~json
{
  "artifact_type": "HAND_REPLAY",
  "protocol_version": "1.0",
  "ruleset_id": "NLH-CASH",
  "ruleset_version": "2.2",
  "cid": "bafy..."
}
~~~

This prevents a historical object from becoming ambiguous when implementations evolve.

---

# 34. CID and Engine Versioning

Engine outputs may reference:

- engine name;
- engine version;
- configuration;
- protocol version.

This is important for:

- Dealer Engine;
- Poker Rules Engine;
- Replay Engine;
- Settlement Engine;
- Reputation Engine;
- Consensus Engine.

The CID does not replace version metadata.

It provides integrity for the object containing that metadata.

---

# 35. CID as an Internal Protocol Anchor

A CID may function as an internal anchor when embedded into a formally defined chain of references.

~~~text
CID-001
   ↓
CID-002
   ↓
CID-003
   ↓
CID-004
   ↓
Historical Root
~~~

The protocol can use this structure to detect discontinuities or unexpected content changes.

An internal CPG anchor may therefore be sufficient for many protocol integrity purposes without requiring an external blockchain anchor for every object.

---

# 36. Bitcoin Anchoring Is Optional

Bitcoin may be used as an additional external historical anchor.

~~~text
CPG Historical Root
        ↓
Bitcoin Anchor
~~~

However:

> **CPG MUST NOT depend on Bitcoin anchoring for the basic integrity of its CID chains.**

The CPG protocol should remain internally capable of:

- identifying objects;
- validating content integrity;
- checking chain continuity;
- verifying signatures;
- verifying consensus references;
- reconstructing historical structures.

Bitcoin anchoring, if adopted, provides an additional independent external commitment.

---

# 37. CID Chain Verification

A verifier MAY perform:

~~~text
1. Load current object.
2. Recompute canonical representation.
3. Recompute/verify CID.
4. Compare with expected CID.
5. Read previous_cid.
6. Verify previous object.
7. Continue backward or forward.
8. Verify sequence continuity.
9. Verify signatures.
10. Verify applicable consensus records.
~~~

A chain failure can indicate:

- changed content;
- missing fragment;
- wrong predecessor;
- sequence discontinuity;
- invalid signature;
- incompatible protocol version;
- incomplete archive.

The exact failure classification belongs to the verification subsystem.

---

# 38. Fragmentation and Recovery

Fragmentation enables partial recovery.

Example:

~~~text
CID-001
CID-002
CID-003
CID-004
CID-005
~~~

If CID-003 is unavailable, the verifier can detect:

~~~text
CID-002 → MISSING → CID-004
~~~

The chain remains evidence of a missing segment rather than silently becoming a continuous history.

Recovery mechanisms may obtain the missing fragment from:

- another node;
- decentralized storage;
- archival storage;
- participant-held evidence;
- replicated logs.

---

# 39. Idempotency

CID generation for the same canonical content MUST be deterministic under the same CID profile.

~~~text
Same Canonical Content
        +
Same CID Profile
        ↓
Same Content Identifier
~~~

Repeated publication of identical content MUST NOT create a logically different content identity merely because it was submitted again.

A new wrapper record, signature set or protocol event may receive a distinct identity if its canonical content differs.

---

# 40. Content Identity vs. Record Identity

CPG MUST distinguish:

~~~text
CONTENT IDENTITY
=
identity of the content

RECORD IDENTITY
=
identity of the protocol record referencing or authorizing that content
~~~

For example:

~~~text
Document
   ↓
Content CID

Signed Submission
   ↓
Record CID
~~~

This distinction prevents signatures, timestamps, or context fields from being confused with the identity of the underlying artifact.

---

# 41. Privacy

The CID Engine SHOULD follow privacy-by-design principles.

A public CID may reveal no plaintext content, but CID publication can still create correlation risks depending on the content and storage model.

Implementations MUST consider:

- sensitive content;
- encrypted objects;
- access authorization;
- metadata leakage;
- linkability;
- identity correlation;
- retention requirements.

The CID Engine MUST NOT require public disclosure of sensitive evidence merely to preserve content integrity.

---

# 42. Security Invariants

### Invariant 1 — Deterministic Identity

Same canonical content and same CID profile produce the same content identifier.

### Invariant 2 — Change Detection

A canonical content change that changes the digest MUST produce a different identifier.

### Invariant 3 — No Truth Claim

A CID MUST NOT be interpreted as an automatic truth certificate.

### Invariant 4 — Signature Separation

A CID MUST NOT be interpreted as proof of authorization unless an applicable signature record exists.

### Invariant 5 — Consensus Separation

A CID MUST NOT be interpreted as a consensus result unless an applicable consensus record exists.

### Invariant 6 — Chain Integrity

A chained fragment MUST reference the expected predecessor according to the applicable chain model.

### Invariant 7 — Historical Preservation

Rejected or disputed content MUST NOT be silently rewritten or deleted from the evidence history merely because another object was accepted.

### Invariant 8 — Replay Integrity

A replay artifact identified by CID MUST remain content-consistent with the referenced object.

### Invariant 9 — Version Binding

Historical records MUST remain interpretable through their applicable protocol and engine version metadata.

### Invariant 10 — No Mandatory External Anchor

Internal CPG integrity MUST NOT depend on Bitcoin or another external blockchain.

---

# 43. Failure Conditions

The CID verification subsystem SHOULD distinguish at least:

~~~text
INVALID_CANONICALIZATION
CID_MISMATCH
MISSING_FRAGMENT
BROKEN_PREVIOUS_REFERENCE
SEQUENCE_GAP
INVALID_SIGNATURE
UNKNOWN_CID_PROFILE
PROTOCOL_VERSION_MISMATCH
ENGINE_VERSION_MISMATCH
INCOMPLETE_EVIDENCE_PACKAGE
UNAUTHORIZED_REFERENCE
STORAGE_UNAVAILABLE
DECRYPTION_UNAVAILABLE
~~~

Storage unavailability MUST NOT automatically be interpreted as content invalidity.

---

# 44. Canonical Processing Flow

~~~text
1. RECEIVE OBJECT
        ↓
2. SELECT CID PROFILE
        ↓
3. CANONICALIZE
        ↓
4. CALCULATE CONTENT IDENTITY
        ↓
5. BUILD CPG CONTENT REFERENCE
        ↓
6. ADD SEQUENCE / CONTEXT
        ↓
7. ADD PREVIOUS CID, WHEN APPLICABLE
        ↓
8. SIGN, WHEN REQUIRED
        ↓
9. SUBMIT TO APPROPRIATE PROTOCOL LAYER
        ↓
10. STORE / REPLICATE, WHEN REQUIRED
        ↓
11. RETURN CID / RECORD REFERENCE
~~~

---

# 45. Relationship With Consensus

The CID Engine does not replace consensus.

Recommended flow:

~~~text
CID ENGINE
     ↓
CONTENT REFERENCE
     ↓
CONSENSUS
     ↓
CONSENSUS RECORD
     ↓
CONSENSUS CID
~~~

Consensus can therefore refer to precise content without copying all content into every consensus message.

---

# 46. Relationship With Conflict Resolution

The Conflict Resolution Engine may use CIDs to construct an evidence graph.

~~~text
CLAIM
 ↓
CID

COUNTERCLAIM
 ↓
CID

EVIDENCE
 ↓
CID

AGREEMENT / RESOLUTION
 ↓
CID
~~~

This creates a traceable relationship between:

- what was claimed;
- what evidence was presented;
- what alternatives existed;
- what agreement was reached;
- what the protocol ultimately recognized.

---

# 47. Relationship With Reputation Engine

The Reputation Engine may reference CID-linked events.

~~~text
CID-LINKED EVENT
       ↓
CONFLICT / PROTOCOL RESULT
       ↓
CONSENSUS RESOLUTION
       ↓
REPUTATION EVENT
       ↓
PLAYER REPUTATION STATE
~~~

The Reputation Engine remains responsible for its own policy and calculations.

The CID Engine only provides the verifiable object references.

---

# 48. Relationship With Dealer Engine

Dealer events may be identified by CIDs.

~~~text
Dealer Operation
       ↓
Dealer Event
       ↓
CID
       ↓
Replay / Consensus / Audit
~~~

This allows the exact Dealer operation object to be referenced without confusing the CID Engine with Dealer semantics.

---

# 49. Relationship With Poker Rules Engine

A rules transition may reference:

- previous state CID;
- action CID;
- resulting state CID;
- ruleset identity;
- Dealer/Card state references.

Example:

~~~text
STATE-CID-A
    +
ACTION-CID
    +
RULESET
    ↓
RULE TRANSITION
    ↓
STATE-CID-B
~~~

This creates a cryptographically traceable state-transition history.

---

# 50. Relationship With Table Wallet and Settlement

Settlement records can reference CIDs.

~~~text
GAME RESULT
    ↓
SETTLEMENT REQUEST
    ↓
SETTLEMENT RECORD
    ↓
CID
    ↓
TABLE WALLET / PAYMENT EVIDENCE
~~~

The CID does not authorize payment.

It identifies the settlement-related record.

---

# 51. Relationship With the Canonical Ledger

The canonical ledger can maintain compact references:

~~~text
LEDGER RECORD
   ├── sequence
   ├── actor
   ├── state reference
   ├── event reference
   └── CID
~~~

Large artifacts remain outside the ledger's core representation.

This supports interoperability with:

- Bitcoin;
- Lightning;
- EVM-compatible networks;
- other distributed ledgers;
- enterprise ledger adapters;
- archival systems.

The Ledger remains the canonical protocol representation.

The CID Engine provides content identity.

---

# 52. Node-Generated, Group and Consensus Objects

The protocol SHOULD support at least these conceptual classes:

~~~text
INDIVIDUAL_OBJECT
GROUP_OBJECT
CONSENSUS_OBJECT
SYSTEM_OBJECT
HISTORICAL_OBJECT
~~~

Examples:

**Individual**

~~~text
PLAYER-001 → personal session report CID
~~~

**Group**

~~~text
Players A+B+C → group agreement CID
~~~

**Consensus**

~~~text
Table participants → consensus CID
~~~

**System**

~~~text
Protocol checkpoint → system CID
~~~

**Historical**

~~~text
Daily / period / historical root CID
~~~

The exact enumeration belongs to the canonical object-type registry.

---

# 53. Evidence Graph

CPG can construct an evidence graph:

~~~text
HAND H042
 ├── Replay CID
 ├── Video CID
 ├── Image CID
 ├── State CID
 ├── Settlement CID
 ├── Dispute CID
 └── Resolution CID
          ↓
       Manifest CID
          ↓
    Historical Root
~~~

This allows auditors to navigate from a high-level historical record toward underlying evidence.

---

# 54. Protocol History Without Mandatory Bitcoin

A complete CPG history can conceptually be represented by:

~~~text
EVENT CIDs
     ↓
CHAINED LOG FRAGMENTS
     ↓
SESSION / TABLE ROOTS
     ↓
CONSENSUS RECORDS
     ↓
HISTORICAL ROOT
~~~

This is a native CPG integrity structure.

Bitcoin can add an independent external checkpoint, but CPG does not cease to be internally verifiable if no Bitcoin anchor exists.

---

# 55. What the CID Engine Does Not Do

The CID Engine does NOT:

- determine poker legality;
- determine winners;
- create poker rules;
- determine truth;
- determine identity authenticity;
- perform KYC adjudication;
- determine reputation;
- resolve conflicts by itself;
- authorize settlements;
- custody player funds;
- create randomness;
- determine card order;
- replace consensus;
- replace the canonical ledger;
- replace IPFS;
- require Bitcoin;
- determine legal status;
- act as a centralized authority.

Its purpose is content identity, reference integrity and evidence linkage.

---

# 56. Architectural Responsibilities

~~~text
CID ENGINE
    =
CONTENT IDENTITY
+
CANONICAL REFERENCES
+
CHAINED OBJECT LINKS
+
EVIDENCE REFERENCES
+
FRAGMENTED LOG SUPPORT
+
HISTORICAL OBJECT STRUCTURES
~~~

Other engines retain their own authority.

---

# 57. Core Data Relationship

The central CPG evidence relationship may be expressed as:

~~~text
OBJECT
+
CANONICALIZATION
+
CID
+
IDENTITY
+
SIGNATURE
+
SEQUENCE
+
PREVIOUS REFERENCE
+
CONSENSUS
=
VERIFIABLE PROTOCOL HISTORY
~~~

Not every object requires every field.

The applicable object profile determines the required fields.

---

# 58. Final Architectural Definition

The **CID Engine** is the Chain Poker Genesis protocol component responsible for generating and validating content identifiers and canonical content references for protocol objects, evidence, events, logs, state records, reports, agreements, consensus records and historical structures.

It enables CPG to:

- identify exact content;
- detect content changes;
- fragment and chain logs;
- preserve independent node observations;
- construct group and consensus records;
- identify session and historical reports;
- reference identity and KYC evidence;
- support P2P conflict resolution;
- provide evidence references for reputation;
- connect protocol states and replay artifacts;
- integrate with decentralized storage;
- construct historical roots;
- optionally provide external anchoring references.

Its central architectural rule is:

~~~text
CID IDENTIFIES.
SIGNATURE AUTHORIZES.
CONSENSUS RECOGNIZES.
CONFLICT RESOLUTION RESOLVES.
REPUTATION INTERPRETS RESOLVED EVENTS.
STORAGE PRESERVES.
LEDGER REPRESENTS.
~~~

And:

~~~text
CID
≠
TRUTH

CID
=
VERIFIABLE CONTENT IDENTITY
~~~

---

# 59. Status and Future Normative Work

**Status: CONSOLIDATED ARCHITECTURAL SPECIFICATION v1.0**

This specification establishes the CID Engine as a first-class CPG protocol component.

The following future specifications may refine the implementation contract without changing the architectural boundary:

- canonicalization profile;
- CID version/profile selection;
- CPG object-type registry;
- signed content reference schema;
- log-fragment format;
- chain verification algorithm;
- Merkle/historical-root specification;
- identity evidence policy;
- KYC evidence policy;
- P2P conflict-resolution integration;
- consensus record format;
- storage adapter interface;
- optional Bitcoin anchoring format.

---

© 2026 Lerry Alexander Elizondo Villalobos (LAEV).  
Chain Poker Genesis by LAEV.
