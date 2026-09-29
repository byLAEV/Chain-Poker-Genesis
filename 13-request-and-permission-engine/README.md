# CHAIN POKER GENESIS BY LAEV

# 13 — Request & Permission Engine

## Official Technical Specification v1.1

**Document Class:** CORE ENGINE  
**Document Status:** AUDIT-PENDING  
**Architecture Role:** Inter-Engine Request Validation, Permission and Authorization  
**Previous Specification:** v1.0  
**Revision:** v1.1  
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

This specification is the corrected integration version of the historical v1.0 Request & Permission Engine specification.

The engine provides the protocol boundary for validating and authorizing inter-engine requests. It does not acquire the business authority of the engine that owns the underlying rule, state, wallet, membership, settlement obligation or other protocol object.

---

# 1. Purpose

The Request & Permission Engine validates, authorizes and coordinates protocol requests exchanged between engines when the operation requires an inter-engine permission boundary.

Its responsibilities include:

- validating the requesting engine;
- validating the destination engine;
- validating the request type against the requesting engine's request catalog;
- validating that the destination is authorized to receive the request;
- validating required permissions and authorization context;
- maintaining the request/response correlation;
- forwarding authorized requests to their destination;
- validating responses against the originating request and permitted response catalog;
- preserving an auditable request lifecycle;
- preventing unauthorized or malformed inter-engine operations from crossing the protocol boundary.

The engine is an authorization and communication-control layer. It does not replace the operational authority of the destination or source engine.

---

# 2. Architectural Principle

For an operation that requires inter-engine authorization, the canonical path is:

~~~text
ENGINE A
   ↓
REQUEST
   ↓
REQUEST & PERMISSION ENGINE
   ↓
AUTHORIZED / REJECTED
   ↓
ENGINE B
   ↓
RESPONSE
   ↓
REQUEST & PERMISSION ENGINE
   ↓
ENGINE A
~~~

The Request & Permission Engine therefore controls the communication boundary without becoming the owner of the business state operated on by Engine B.

A permission to send or execute a request is not itself ownership of the underlying resource.

---

# 3. Authority Boundary

The Request & Permission Engine authorizes the request path and required permission conditions.

It does not independently create or replace the authoritative business decision that caused the request.

Examples:

~~~text
ENGINE 05
= authority over canonical RakeObligation

ENGINE 09
= authority over TABLE_WALLET_INSTANCE lifecycle

ENGINE 10
= authority over disconnection / removal lifecycle

ENGINE 12
= authority over settlement execution

ENGINE 13
= authority over inter-engine request permission
~~~

Therefore:

~~~text
REQUEST AUTHORIZATION
        ≠
BUSINESS OBJECT AUTHORITY
~~~

A valid permission cannot transform an invalid business instruction into a valid one.

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

---

# 5. Request Validation

Before forwarding a request, Engine 13 validates at minimum:

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

# 6. Destination Verification

Engine 13 performs the first protocol-boundary verification.

The destination engine performs the second, independent verification using its own specification and local authority.

Canonical flow:

~~~text
ENGINE A
   ↓
13 — REQUEST VALIDATION
   ↓
ENGINE B
   ↓
ENGINE B — DESTINATION VALIDATION
   ↓
EXECUTION / PROCESSING
~~~

The destination engine remains responsible for rejecting an instruction that is inconsistent with its own authoritative state or rules.

Engine 13 must not override a destination rejection.

---

# 7. Authorization Does Not Transfer Business Authority

This distinction is mandatory.

For example:

~~~text
ENGINE 05
creates canonical RakeObligation
        ↓
ENGINE 05 creates SettlementRequest
        ↓
ENGINE 13 authorizes inter-engine request
        ↓
ENGINE 12 executes authorized settlement
~~~

Engine 13 does not calculate the rake.

Engine 13 does not create the RakeObligation.

Engine 13 does not control the Table Wallet.

Engine 13 does not execute monetary settlement.

Engine 13 does not determine the poker result.

Its authorization means that the request is permitted to cross the inter-engine protocol boundary under the applicable rules.

---

# 8. Request Lifecycle

The request lifecycle is distinct from the lifecycle of the business operation performed by the destination engine.

Canonical request lifecycle:

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

Terminal rejection/failure paths may include:

~~~text
REQUEST_CREATED
      ↓
REQUEST_REJECTED
~~~

or:

~~~text
REQUEST_FORWARDED
      ↓
RESPONSE_RECEIVED
      ↓
RESPONSE_VALIDATED
      ↓
REQUEST_FAILED
~~~

Engine 13 must not reinterpret a destination engine's internal lifecycle as its own.

---

# 9. Response Validation

Responses return through the same request-control boundary.

Engine 13 verifies:

- correlation with the original request;
- response type;
- response schema;
- response version;
- source identity;
- destination identity;
- authorization context;
- request lifecycle consistency;
- duplicate/replay conditions.

Engine 13 may classify a response as valid, invalid, failed or unexpected according to the request contract.

It does not independently decide that the destination's business operation succeeded.

For example:

~~~text
REQUEST
   ↓
13 AUTHORIZES
   ↓
12 EXECUTES
   ↓
12 = SETTLEMENT_FAILED
   ↓
13 VALIDATES RESPONSE
   ↓
REQUEST_COMPLETED_WITH_FAILURE
~~~

A valid failure response is still a valid protocol response.

---

# 10. Shared Request State

Engine 13 maintains the state required to correlate and audit each controlled request.

At minimum:

~~~text
request_id
source_engine
destination_engine
request_type
request_version
permission_context
authorization_reference
request_state
expected_response
received_response
created_at
validated_at
forwarded_at
response_at
completed_at
result
~~~

Where applicable, the request may also reference:

~~~text
obligation_id
settlement_id
table_id
hand_id
wallet_context
~~~

These references do not transfer authority to Engine 13.

---

# 11. Identity and Replay Protection

Every controlled request must have a unique request identity.

~~~text
request_id
~~~

The request identity is distinct from business identities such as:

~~~text
obligation_id
settlement_id
hand_id
table_id
~~~

Engine 13 must prevent unauthorized replay of a previously accepted request.

A replayed request must not create a second business operation merely because the request-control layer receives it again.

---

# 12. Relationship to Engine 05

Engine 05 owns the canonical rake and monetary obligation.

The request path may therefore be:

~~~text
RakeObligation
      ↓
SettlementRequest
      ↓
ENGINE 13
      ↓
authorized request
      ↓
ENGINE 12
~~~

Engine 13 does not modify the canonical obligation_id or reconstruct the monetary obligation.

---

# 13. Relationship to Engine 09

Engine 09 owns the TABLE_WALLET_INSTANCE and its lifecycle.

Engine 13 may authorize a request involving Engine 09 when the request satisfies the applicable permission rules.

It does not:

- create the wallet instance;
- change wallet lifecycle;
- replace wallet authority;
- determine custody;
- change wallet configuration without an explicitly authorized protocol operation.

---

# 14. Relationship to Engine 10

Engine 10 owns connection, absence, removal and seat-release lifecycle.

A request authorized by Engine 13 does not by itself create:

~~~text
DISCONNECTED
REMOVED
SEAT_RELEASED
~~~

Nor does an Engine 10 lifecycle event automatically authorize a financial operation.

---

# 15. Relationship to Engine 11

Engine 11 documents, versions, publishes and preserves protocol specifications.

Engine 13 consumes the authoritative protocol/request catalogs defined by the protocol documentation.

Engine 11 does not acquire operational request authority merely by documenting Engine 13.

Engine 13 does not modify authoritative documentation through normal request processing.

---

# 16. Relationship to Engine 12

Engine 12 executes monetary settlement.

The canonical settlement request path is:

~~~text
ENGINE 05
RakeObligation
      ↓
SettlementRequest
      ↓
ENGINE 13
Request / Permission Validation
      ↓
SETTLEMENT_AUTHORIZED
      ↓
ENGINE 12
Settlement Execution
      ↓
Settlement Result
~~~

Engine 13 authorizes the inter-engine request.

Engine 12 remains responsible for settlement execution and settlement-result reporting.

Engine 13 does not execute funds.

---

# 17. Event Model

Engine 13 may produce request-control events such as:

~~~text
REQUEST_CREATED
REQUEST_VALIDATED
REQUEST_AUTHORIZED
REQUEST_REJECTED
REQUEST_FORWARDED
RESPONSE_RECEIVED
RESPONSE_VALIDATED
REQUEST_COMPLETED
REQUEST_FAILED
~~~

These events describe the request-control lifecycle.

They do not replace domain events owned by other engines.

For example:

~~~text
TABLE_WALLET_SETTLEMENT_EXECUTION_CONFIRMED
~~~

remains a settlement/wallet-domain event and must not be renamed into a generic Engine 13 event merely because Engine 13 transported or validated the response.

---

# 18. Security Requirements

Engine 13 must protect against:

- unauthorized source engines;
- unauthorized destinations;
- malformed requests;
- unauthorized request types;
- invalid protocol versions;
- replay;
- duplicate processing;
- forged responses;
- response/request mismatch;
- unauthorized permission escalation;
- stale authorization context;
- cross-table request confusion;
- cross-operation request confusion.

Authorization must be bound to the request context for which it was issued.

A permission for one operation must not silently authorize another operation.

---

# 19. Failure Handling

Engine 13 distinguishes at least:

~~~text
VALIDATION_REJECTED
AUTHORIZATION_REJECTED
FORWARDING_FAILED
RESPONSE_INVALID
RESPONSE_TIMEOUT
REQUEST_FAILED
REQUEST_COMPLETED
~~~

An uncertain communication result must not be interpreted as successful business execution.

The destination engine or its reconciliation mechanism remains responsible for resolving an uncertain business operation.

---

# 20. Auditability

Every controlled request must be correlatable through:

~~~text
request_id
        ↓
authorization context
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
~~~

The Request & Permission Engine therefore provides the communication-level audit trail while domain engines retain domain-level authority and evidence.

---

# 21. Design Principle

The engine implements:

~~~text
REQUEST CONTROL
        +
PERMISSION VALIDATION
        +
AUTHORIZATION
        +
CORRELATION
        +
RESPONSE VALIDATION
        +
AUDITABILITY
~~~

It does not implement:

~~~text
POKER RULES
TABLE CREATION
PLAYER MEMBERSHIP
WALLET CUSTODY
DISCONNECTION LIFECYCLE
RAKE CALCULATION
MONETARY SETTLEMENT EXECUTION
DOCUMENTATION AUTHORITY
~~~

---

# 22. Integration Principle

The Request & Permission Engine is a cross-functional protocol component.

Its purpose is not to become a universal owner of every decision. Its purpose is to ensure that requests crossing an authorization boundary are:

~~~text
KNOWN
  ↓
VALIDATED
  ↓
AUTHORIZED
  ↓
FORWARDED
  ↓
INDEPENDENTLY VERIFIED
  ↓
RESPONDED
  ↓
CORRELATED
  ↓
AUDITABLE
~~~

This preserves isolation between engines while maintaining deterministic communication and explicit authority boundaries.

---

# 23. Final Authority Rule

The following rule is normative:

~~~text
ENGINE 13 MAY AUTHORIZE THE REQUEST PATH.

ENGINE 13 MUST NOT ACQUIRE THE BUSINESS AUTHORITY
OF THE ENGINE THAT OWNS THE REQUESTED OPERATION.
~~~

Therefore:

~~~text
PERMISSION
    ≠
OWNERSHIP

REQUEST AUTHORIZATION
    ≠
BUSINESS DECISION

REQUEST VALIDATION
    ≠
BUSINESS EXECUTION
~~~

This separation is required for integration with the existing Chain Poker Genesis engine architecture.
