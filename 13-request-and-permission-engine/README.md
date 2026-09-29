# CHAIN POKER GENESIS BY LAEV

# 13 — Request & Permission Engine

## Official Technical Specification v1.2.1

**Document Class:** CORE ENGINE  
**Document Status:** AUDIT-PENDING  
**Architecture Role:** Inter-Engine Request Validation, Permission and Multi-Stage Authorization Coordination  
**Previous Specification:** v1.1  
**Revision:** v1.2  
**Protocol:** Chain Poker Genesis by LAEV

---

## 0. Document Control

~~~text
[LCCP]
SEQ: 13
PREV: 12
SELF: 13
NEXT: 14
CLASS: CORE ENGINE
STATUS: AUDIT-PENDING
[/LCCP]
~~~

This specification extends the historical v1.0, v1.1 and v1.2 definitions of the Request & Permission Engine.

Engine 13 is the protocol boundary for validating, authorizing and coordinating controlled requests between engines. It may coordinate a request through multiple stages when the destination engine must first declare the conditions required for execution and the requesting engine must subsequently provide the required authorization evidence.

Engine 13 does not acquire the business authority of the engine that owns the requested operation.

---

# 1. Purpose

The Request & Permission Engine validates, authorizes and coordinates protocol requests exchanged between engines when an inter-engine authorization boundary is required.

Its responsibilities include:

- validating the requesting engine;
- validating the destination engine;
- validating the request type against the requesting engine's request catalog;
- validating that the destination is authorized to receive the request;
- obtaining execution requirements from the destination engine when the operation requires them;
- returning those requirements to the requesting engine;
- receiving and correlating authorization evidence required by the request contract;
- forwarding the request and its evidence to the destination engine;
- validating destination responses against the request context;
- maintaining request/response correlation across all stages;
- preserving an auditable lifecycle for the complete request workflow;
- preventing unauthorized, malformed, stale or incorrectly correlated operations from crossing the protocol boundary.

Engine 13 is therefore a request-control and authorization-coordination layer. It is not the owner of the business state or rule operated on by the destination engine.

---

# 2. Architectural Principle

For a simple operation, the canonical path is:

~~~text
ENGINE A
   ↓
REQUEST
   ↓
ENGINE 13
   ↓
AUTHORIZED / REJECTED
   ↓
ENGINE B
   ↓
RESPONSE
   ↓
ENGINE 13
   ↓
ENGINE A
~~~

For an operation that requires destination-defined conditions or additional authorization evidence, the workflow may contain multiple correlated stages:

~~~text
ENGINE A
   ↓
ENGINE 13
   ↓
ENGINE B — requirements inquiry
   ↓
ENGINE 13
   ↓
ENGINE A — requirements received
   ↓
ENGINE A — authorization evidence produced
   ↓
ENGINE 13
   ↓
ENGINE B — final request + evidence
   ↓
ENGINE B — independent validation
   ↓
ENGINE B — execution / rejection
   ↓
ENGINE 13
   ↓
ENGINE A
~~~

All stages belong to the same controlled operation context and must remain logically and, where applicable, cryptographically bound to the original request identity and applicable protocol state.

Engine 13 controls the communication and authorization workflow. It does not become the owner of Engine B's business operation.

---

# 3. Authority Boundary

Authority is separated into three distinct concepts:

~~~text
BUSINESS AUTHORITY
        ≠
REQUEST-WORKFLOW AUTHORIZATION
        ≠
AUTHORIZATION EVIDENCE
~~~

The engine that owns the business object or operation remains authoritative for that operation.

The engine producing a consensus or governance decision remains authoritative for producing that decision and its associated evidence.

Engine 13 controls the request path, validates applicable request permissions, coordinates required conditions, correlates evidence and transports the controlled request between the participating engines.

Examples:

~~~text
ENGINE 05
= authority over canonical RakeObligation

ENGINE 09
= authority over TABLE_WALLET_INSTANCE lifecycle

ENGINE 10
= authority over disconnection / removal / seat-release lifecycle

ENGINE 12
= authority over settlement execution

CONSENSUS / GOVERNANCE ENGINE
= authority over the consensus or governance decision it produces

TARGET BUSINESS ENGINE
= authority over the final business-state validation and execution

ENGINE 13
= authority over the inter-engine request-control workflow
~~~

Engine 13 must not invent, weaken or replace conditions established by the engine that owns the requested operation.

---

# 4. Request Catalog

Each participating engine maintains an authoritative request catalog as part of its protocol specification.

The catalog defines:

- requests the engine may initiate;
- requests the engine may receive;
- required permissions;
- valid request states;
- valid response types;
- protocol versions accepted;
- applicable authorization conditions.

A request catalog is part of the engine's protocol configuration and must not be modified during an active table lifecycle unless the protocol explicitly defines a governance-controlled configuration transition.

For multi-stage operations, the catalog must identify the permitted request stages or request types and the valid transitions between them.

---

# 5. Request Context

Every controlled operation must have a persistent request context capable of correlating all stages of the workflow.

At minimum, the context identifies:

~~~text
request_id
source_engine
destination_engine
operation_type
request_version
protocol_version
table_id — when applicable
request_state
authorization_context
target_requirements — when applicable
authorization_evidence — when applicable
expected_response
received_response
final_result
~~~

Additional identifiers may be referenced when applicable:

~~~text
operation_id
parent_request_id
hand_id
obligation_id
settlement_id
wallet_context
configuration_version
~~~

The exact use of additional identifiers is determined by the applicable engine contract.

The request context does not transfer ownership of any referenced business object to Engine 13.

---

# 6. Initial Request Validation

Before forwarding or coordinating a request, Engine 13 validates at minimum:

1. source engine identity;
2. destination engine identity;
3. request type;
4. source request catalog authorization;
5. destination receive authorization;
6. protocol version compatibility;
7. request schema;
8. required authorization context;
9. current protocol state;
10. replay / duplicate conditions;
11. correlation identity;
12. applicable permission rules.

A request that fails validation is not forwarded.

The validation result must be deterministic for the same protocol state and request context.

---

# 7. Destination-Defined Execution Requirements

Where the applicable request contract defines a destination-requirements stage, Engine 13 may initiate that stage before final forwarding. The stage is conditional; it must not be assumed for every request.

The destination engine is responsible for declaring the conditions required for its operation when its specification exposes such a requirements contract. If no such contract exists, Engine 13 must not invent one; the request follows the destination's already-defined request/response contract or is rejected as unsupported.

Conceptually:

~~~text
ENGINE A
   ↓
ENGINE 13
   ↓
ENGINE B
   ↓
REQUIRED EXECUTION CONDITIONS
   ↓
ENGINE 13
   ↓
ENGINE A
~~~

Engine 13 transports and correlates these requirements.

It must not independently invent or reduce the destination's business conditions.

Examples of possible requirements include, where defined by the applicable protocol contract:

- required authorization evidence;
- required consensus evidence;
- required cryptographic signatures;
- required table state;
- required configuration version;
- required protocol version;
- required identifiers or references.

The exact threshold, membership rule, signature scheme or business condition belongs to the authoritative engine or governance contract that defines it.

---

# 8. Authorization Evidence

When a controlled operation requires authorization evidence, Engine 13 coordinates the collection and transport of that evidence.

Examples may include:

~~~text
consensus evidence
signature set
authorization record
governance proof
cryptographic commitment
~~~

Engine 13 must preserve the binding between the evidence and the request context for which it was produced.

At minimum, evidence must not be silently reusable for:

- another request;
- another table;
- another operation;
- another configuration version;
- another protocol context.

Engine 13 may validate structural and contextual properties required by the request contract, but the authority to determine whether the evidence constitutes a valid business authorization remains with the engine or governance component that owns that rule.

---

# 9. Multi-Stage Request Lifecycle

A multi-stage request is one controlled operation composed of more than one request/response exchange.

A canonical lifecycle may be:

~~~text
REQUEST_CREATED
      ↓
REQUEST_VALIDATED
      ↓
TARGET_REQUIREMENTS_REQUESTED
      ↓
TARGET_REQUIREMENTS_RECEIVED
      ↓
AUTHORIZATION_EVIDENCE_REQUESTED
      ↓
AUTHORIZATION_EVIDENCE_RECEIVED
      ↓
REQUEST_AUTHORIZED
      ↓
REQUEST_FORWARDED
      ↓
TARGET_RESPONSE_RECEIVED
      ↓
RESPONSE_VALIDATED
      ↓
REQUEST_COMPLETED
~~~

Not every request requires every stage.

A simple request may use:

~~~text
REQUEST_CREATED
      ↓
REQUEST_VALIDATED
      ↓
REQUEST_AUTHORIZED
      ↓
REQUEST_FORWARDED
      ↓
RESPONSE_RECEIVED
      ↓
RESPONSE_VALIDATED
      ↓
REQUEST_COMPLETED
~~~

Terminal paths may include:

~~~text
REQUEST_REJECTED
AUTHORIZATION_REJECTED
FORWARDING_FAILED
RESPONSE_INVALID
RESPONSE_TIMEOUT
REQUEST_FAILED
~~~

Engine 13's request lifecycle is distinct from the business lifecycle executed by the destination engine.

---

# 10. Destination Verification

Engine 13 performs the request-boundary verification required by its protocol contract.

The destination engine independently verifies the final request using its own authoritative specification and state.

Canonical flow:

~~~text
ENGINE A
   ↓
ENGINE 13
   ↓
ENGINE B
   ↓
ENGINE B — INDEPENDENT VALIDATION
   ↓
EXECUTION / REJECTION
~~~

For a multi-stage operation:

~~~text
ENGINE A
   ↓
ENGINE 13
   ↓
ENGINE B — REQUIREMENTS
   ↓
ENGINE A — EVIDENCE
   ↓
ENGINE 13
   ↓
ENGINE B — FINAL VALIDATION
   ↓
EXECUTION / REJECTION
~~~

Engine 13 must not override a destination rejection.

This is the second verification boundary for the business operation; it is not a transfer of destination authority to Engine 13.

---

# 11. Authorization Semantics

REQUEST_AUTHORIZED means that the request-control workflow has satisfied the authorization conditions required by the applicable request contract for forwarding the controlled request to its destination.

It does not mean that the destination business operation has succeeded.

Therefore:

~~~text
REQUEST_AUTHORIZED
        ≠
BUSINESS_OPERATION_SUCCEEDED
~~~

The destination engine retains the authority to accept or reject execution after independently validating its authoritative state and required conditions.

---

# 12. Response Validation

Responses return through the same request-control boundary.

Engine 13 validates:

- correlation with the correct request context;
- response type;
- response schema;
- response version;
- source identity;
- destination identity;
- applicable authorization context;
- request lifecycle consistency;
- duplicate/replay conditions;
- expected stage or transition.

Engine 13 does not independently declare that a destination business operation succeeded merely because a response is syntactically valid.

For example:

~~~text
ENGINE 12
   ↓
SETTLEMENT_FAILED
   ↓
ENGINE 13
   ↓
RESPONSE_VALIDATED
   ↓
REQUEST_COMPLETED_WITH_FAILURE
~~~

A valid failure response is still a valid protocol response.

---

# 13. Shared Request State

Engine 13 maintains the state required to correlate and audit each controlled request.

At minimum:

~~~text
request_id
source_engine
destination_engine
operation_type
request_version
protocol_version
request_state
authorization_context
target_requirements
authorization_evidence
expected_response
received_response
created_at
validated_at
requirements_requested_at — when applicable
requirements_received_at — when applicable
evidence_received_at — when applicable
authorized_at
forwarded_at
response_at
completed_at
result
~~~

The state is request-control state.

It must not be used as a replacement for the authoritative state maintained by another engine.

---

# 14. Relationship to Engine 05

Engine 05 owns the canonical rake and monetary obligation.

The request path may therefore be:

~~~text
RakeObligation
      ↓
SettlementRequest
      ↓
ENGINE 13
      ↓
authorization workflow
      ↓
ENGINE 12
~~~

Engine 13 does not modify the canonical obligation_id or reconstruct the monetary obligation.

---

# 15. Relationship to Engine 09

Engine 09 owns TABLE_WALLET_INSTANCE and its lifecycle.

Engine 13 may coordinate a request involving Engine 09 when the request satisfies the applicable permission and request-contract conditions.

It does not:

- create the wallet instance;
- change wallet lifecycle;
- replace wallet authority;
- determine custody;
- decide settlement authorization merely from wallet state.

Engine 13 does not control the lifecycle of TABLE_WALLET_INSTANCE.

---

# 16. Relationship to Engine 10

Engine 10 owns connection, absence, removal and seat-release lifecycle.

A request authorized by Engine 13 does not by itself create:

~~~text
DISCONNECTED
REMOVED
SEAT_RELEASED
~~~

Nor does an Engine 10 lifecycle event automatically authorize a financial operation.

---

# 17. Relationship to Engine 11

Engine 11 documents, versions, publishes and preserves protocol specifications.

Engine 13 uses the authoritative protocol/request contracts defined by the protocol documentation.

Engine 11 does not acquire operational request authority merely by documenting Engine 13.

Engine 13 does not modify authoritative documentation through normal request processing.

---

# 18. Relationship to Engine 12

Engine 12 executes monetary settlement.

The canonical settlement request path is:

~~~text
ENGINE 05
RakeObligation
      ↓
SettlementRequest
      ↓
ENGINE 13
Request / Permission Workflow
      ↓
SETTLEMENT_AUTHORIZED
      ↓
ENGINE 12
Settlement Execution
      ↓
Settlement Result
~~~

Engine 13 coordinates and authorizes the inter-engine request path.

Engine 12 remains responsible for settlement execution and settlement-result reporting.

Engine 13 does not execute funds.

---

# 19. Consensus / Configuration Change Example

A representative multi-stage workflow is a governance-controlled configuration transition in which a consensus engine requests that the engine owning table configuration apply a permitted change affecting the table's Card Engine selection or configuration. Such a transition must respect the Table Creation Engine's canonical configuration, lifecycle and version-transition rules; Engine 13 must not be interpreted as permitting an arbitrary mutation of an active table or active hand.

The following is a representative conceptual flow; the exact request types, requirement contract, consensus evidence format and configuration-transition rules must be defined by the authoritative Consensus and Table Creation specifications:

~~~text
TABLE CONSENSUS ENGINE
        ↓
Request configuration change
        ↓
ENGINE 13
        ↓
validate source, destination, request and table context
        ↓
TABLE CREATION ENGINE
        ↓
declare required execution conditions
        ↓
ENGINE 13
        ↓
return conditions to TABLE CONSENSUS ENGINE
        ↓
TABLE CONSENSUS ENGINE
        ↓
produce required consensus authorization evidence
        ↓
ENGINE 13
        ↓
correlate and transport evidence
        ↓
TABLE CREATION ENGINE
        ↓
independent validation of:
- request
- table state
- configuration state
- required authorization evidence
        ↓
EXPLICIT CONFIGURATION / VERSION TRANSITION
        ↓
RESULT
        ↓
ENGINE 13
        ↓
TABLE CONSENSUS ENGINE
~~~

This example establishes the authority separation:

~~~text
CONSENSUS ENGINE
= produces the consensus decision/evidence

ENGINE 13
= coordinates and controls the request workflow

TABLE CREATION ENGINE
= owns final table-configuration validation and execution

The current Table Creation specification identifies Engine 13 as the authorization boundary for creation/lifecycle requests and requires explicit versioned configuration transitions. It does not yet define the full destination-requirements exchange shown above; that interface remains an integration item rather than an assumed existing contract.
~~~

Engine 13 must not decide the required consensus threshold, membership set, signature algorithm or final table-configuration rule unless another authoritative specification explicitly assigns that responsibility to Engine 13.

---

# 20. Event Model

Engine 13 may produce request-control events such as:

~~~text
REQUEST_CREATED
REQUEST_VALIDATED
TARGET_REQUIREMENTS_REQUESTED
TARGET_REQUIREMENTS_RECEIVED
AUTHORIZATION_EVIDENCE_REQUESTED
AUTHORIZATION_EVIDENCE_RECEIVED
REQUEST_AUTHORIZED
REQUEST_REJECTED
AUTHORIZATION_REJECTED
REQUEST_FORWARDED
RESPONSE_RECEIVED
RESPONSE_VALIDATED
REQUEST_COMPLETED
REQUEST_FAILED
~~~

These events describe the request-control lifecycle.

They do not replace domain events owned by other engines.

For example, a table-configuration change remains a configuration-domain event owned by the authoritative table-configuration engine, even if Engine 13 transported and validated the request that caused it.

---

# 21. Security Requirements

Engine 13 must protect against:

- unauthorized source engines;
- unauthorized destinations;
- malformed requests;
- unauthorized request types;
- invalid protocol versions;
- replay;
- duplicate processing;
- forged responses;
- request/response mismatch;
- unauthorized permission escalation;
- stale authorization context;
- cross-table request confusion;
- cross-operation request confusion;
- cross-configuration-version evidence reuse;
- evidence substitution;
- partial multi-stage workflow reuse.

Authorization and authorization evidence must remain bound to the request context for which they were issued.

A permission or evidence package for one operation must not silently authorize another operation.

---

# 22. Failure Handling

Engine 13 distinguishes at least:

~~~text
VALIDATION_REJECTED
AUTHORIZATION_REJECTED
TARGET_REQUIREMENTS_REJECTED
REQUIREMENTS_UNAVAILABLE
FORWARDING_FAILED
EVIDENCE_INVALID
RESPONSE_INVALID
RESPONSE_TIMEOUT
REQUEST_FAILED
REQUEST_COMPLETED
~~~

An uncertain communication result must not be interpreted as successful business execution.

The destination engine or its reconciliation mechanism remains responsible for resolving an uncertain business operation.

For a multi-stage workflow, an incomplete intermediate stage must not be interpreted as final authorization or successful execution.

---

# 23. Auditability

Every controlled request must be correlatable through:

~~~text
request_id
        ↓
request context
        ↓
authorization context
        ↓
target requirements — when applicable
        ↓
authorization evidence — when applicable
        ↓
destination response
        ↓
final request-control result
~~~

Where domain-specific identifiers exist, the request record may additionally reference:

~~~text
table_id
hand_id
obligation_id
settlement_id
configuration_version
~~~

The Request & Permission Engine therefore provides the communication-level and workflow-level audit trail while domain engines retain domain-level authority and evidence.

---

# 24. Protocol Determinism

For the same:

~~~text
protocol version
+
request context
+
authorization context
+
applicable protocol state
~~~

the request-control decision must be deterministic.

Engine 13 must not make an authorization decision based on arbitrary local conditions unrelated to the protocol contract.

Resource availability, implementation details or computational load must not silently alter the business authorization result.

---

# 25. Design Principle

The engine implements:

~~~text
REQUEST CONTROL
        +
PERMISSION VALIDATION
        +
AUTHORIZATION COORDINATION
        +
MULTI-STAGE CORRELATION
        +
EVIDENCE TRANSPORT
        +
RESPONSE VALIDATION
        +
AUDITABILITY
~~~

It does not implement:

~~~text
POKER RULES
TABLE CREATION AUTHORITY
PLAYER MEMBERSHIP
WALLET CUSTODY
DISCONNECTION LIFECYCLE
RAKE CALCULATION
MONETARY SETTLEMENT EXECUTION
CONSENSUS DECISION AUTHORITY
DOCUMENTATION AUTHORITY
~~~

---

# 26. Integration Principle

The Request & Permission Engine is a cross-functional protocol component.

Its purpose is not to become a universal owner of every decision.

Its purpose is to ensure that requests crossing an authorization boundary are:

~~~text
KNOWN
  ↓
VALIDATED
  ↓
REQUIREMENTS DETERMINED — WHEN REQUIRED
  ↓
AUTHORIZATION EVIDENCE COLLECTED — WHEN REQUIRED
  ↓
AUTHORIZED
  ↓
FORWARDED
  ↓
INDEPENDENTLY VERIFIED
  ↓
EXECUTED OR REJECTED BY THE AUTHORITY OWNER
  ↓
RESPONDED
  ↓
CORRELATED
  ↓
AUDITABLE
~~~

This preserves isolation between engines while supporting simple and multi-stage deterministic communication.

---

# 27. Final Authority Rules

The following rules are normative:

~~~text
ENGINE 13 MAY CONTROL AND AUTHORIZE THE REQUEST WORKFLOW.

ENGINE 13 MUST NOT ACQUIRE THE BUSINESS AUTHORITY
OF THE ENGINE THAT OWNS THE REQUESTED OPERATION.

THE DESTINATION ENGINE DEFINES ITS OWN BUSINESS
EXECUTION CONDITIONS.

THE CONSENSUS / GOVERNANCE ENGINE DEFINES
THE AUTHORIZATION EVIDENCE IT IS RESPONSIBLE FOR PRODUCING.

ENGINE 13 MUST NOT INVENT, WEAKEN OR REPLACE
THOSE AUTHORITATIVE CONDITIONS.

DESTINATION VALIDATION REMAINS INDEPENDENT.

REQUEST AUTHORIZATION DOES NOT GUARANTEE
BUSINESS OPERATION SUCCESS.
~~~

Therefore:

~~~text
PERMISSION
    ≠
OWNERSHIP

REQUEST AUTHORIZATION
    ≠
BUSINESS DECISION

AUTHORIZATION EVIDENCE
    ≠
ENGINE 13 BUSINESS AUTHORITY

REQUEST VALIDATION
    ≠
BUSINESS EXECUTION
~~~

This separation is required for correct integration with the Chain Poker Genesis by LAEV engine architecture.