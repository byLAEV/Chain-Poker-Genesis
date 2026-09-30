# Implementation Annex

## Operational Requirements for the Storage Infrastructure of the Red de Nodos by LAEV

**Version:** 1.1-A  
**Nature:** Complementary implementation requirements  
**Application:** Development of the Storage Manager, Metadata Store, Synchronization Engine, and Recovery mechanisms

---

## 1. Objective

This annex transforms selected architectural aspects into concrete requirements that must be resolved during implementation.

The following three domains are defined as mandatory engineering requirements:

```text
1. Concurrent consistency of Metadata + Storage
2. Growth control for Recovery + Quarantine
3. Optional deterministic object identity
```

---

# 2. Concurrent Consistency of the Metadata Store

## 2.1 Requirement

The `Metadata Store` must provide an appropriate transactional mechanism to coordinate:

```text
Storage Manager
Synchronization Queue
Recovery Manager
Manifest Manager
```

Operations that simultaneously modify:

```text
manifest
object state
sync state
distributed state
operation record
```

must use a coherent transactional unit whenever those modifications belong to the same metadata store.

---

## 2.2 ACID Property

The implementation must use a system that provides the transactional guarantees required by the design.

An initial implementation based on SQLite is compatible with this model and provides ACID transactions; its WAL mode may improve reader/writer concurrency on the same host.

An implementation based on RocksDB may also use transactional mechanisms for multiple operations.

The final engine selection must be made during implementation and documented.

---

## 2.3 Transaction Boundary

The fact that the Metadata Store is transactional does not mean that an ACID transaction automatically spans:

```text
Metadata Store
+
Filesystem
+
Kubo
+
IPFS
```

Therefore, the architecture must continue to use:

```text
operation journal
state machine
reconciliation
retry
verification
recovery
```

to coordinate partial failures.

---

## 2.4 Concurrency Control

The implementation must select an explicit strategy:

```text
OPTIMISTIC
```

or:

```text
PESSIMISTIC / LOCKING
```

or a combination of both according to the operation.

Manifest and state updates must provide, at minimum, protection against:

```text
lost update
duplicate operation
stale version
race condition
double publish
double delete
```

---

## 2.5 Metadata Versioning

Critical modifications must be able to verify that the state read remains valid.

Conceptual model:

```text
read manifest
      │
      ▼
version = 7
      │
      ▼
modify
      │
      ▼
commit only if version = 7
      │
      ▼
version = 8
```

If another operation has already modified the manifest:

```text
expected version = 7
actual version   = 8
```

the operation must be rejected or reconciled, never silently overwritten.

---

# 3. Recovery and Quarantine: Growth Control

## 3.1 Requirement

The areas:

```text
storage/recovery/
storage/synchronization/quarantine/
```

must not grow indefinitely.

A specific capacity and retention policy must exist.

---

## 3.2 Retention Policy

Each recovery or quarantine object must be able to have:

```text
created_at
expires_at
retention_policy
size
reason
source
severity
status
```

Automatic deletion may only occur when the corresponding policy authorizes it.

---

## 3.3 Quarantine States

Quarantine must distinguish, at minimum:

```text
QUARANTINED
UNDER_REVIEW
VALIDATED
REJECTED
EXPIRED
PURGED
```

Example:

```text
RECEIVED
   │
   ▼
VERIFY
   │
   ├── VALID ─────► ACCEPT
   │
   └── INVALID
          │
          ▼
      QUARANTINE
          │
      ┌───┴────┐
      ▼        ▼
 VALIDATED  REJECTED
              │
              ▼
           RETENTION
              │
              ▼
            PURGE
```

---

## 3.4 Protection Against Saturation

The system must provide configurable limits:

```text
MAX_TOTAL_SIZE
MAX_OBJECT_COUNT
MAX_SINGLE_OBJECT_SIZE
MAX_RETENTION_TIME
MAX_RECOVERY_SIZE
MAX_QUARANTINE_SIZE
```

When a limit is reached, an operational state transition and alert must occur.

Example:

```text
NORMAL
   │
   ▼
WARNING
   │
   ▼
CRITICAL
   │
   ▼
PROTECTION MODE
```

---

## 3.5 Protection of Important Objects

Automatic cleanup must never indiscriminately delete information required for:

- active recovery;
- integrity investigations;
- operations in progress;
- restoration;
- auditing;
- compliance with an explicit retention policy.

There must be a mechanism to mark an object as:

```text
RETENTION_HOLD
```

to prevent automatic deletion.

---

# 4. Local Storage Capacity Control

Space management must separately account for:

```text
LOCAL DATA
CACHE
TEMPORARY
SYNC QUEUES
RECOVERY
QUARANTINE
BACKUP
KUBO REPOSITORY
```

It must not be assumed that freeing space in one of these areas frees space in all of them.

---

## 4.1 Thresholds

The implementation should define:

```text
NORMAL
WARNING
CRITICAL
EMERGENCY
```

according to percentage or absolute capacity.

Example:

```text
NORMAL
      ↓
WARNING
      ↓
CRITICAL
      ↓
EMERGENCY
```

In a critical state, non-essential operations may be suspended, such as:

```text
non-critical synchronization
cache generation
temporary exports
optional replication
```

without automatically destroying persistent data.

---

# 5. Deterministic Object Identity

## 5.1 General Model

The architecture maintains two possibilities:

```text
NON-DETERMINISTIC OBJECT ID
```

and:

```text
DETERMINISTIC OBJECT ID
```

The type used must be a decision of the corresponding module or policy.

---

## 5.2 UUIDv4

`UUIDv4` may be used when the system requires an identifier generated independently of prior registry queries.

Primary advantage:

```text
generated locally
no central registry required
```

It must be treated as an identifier of the logical entity, not as a content hash.

---

## 5.3 UUIDv5

`UUIDv5` may be used when a logical identity is derivable from:

```text
namespace
+
canonical name
```

The same namespace and canonical name produce the same UUID. RFC 9562 defines UUIDv5 as a name-based UUID using SHA-1.

Conceptual example:

```text
namespace = MODULE-X
name      = user:12345:document:7

        ↓

object_id = deterministic UUID
```

---

## 5.4 UUIDv5 Must Not Be Used as a Universal Hash

UUIDv5 must not be used to replace:

```text
content_hash
```

The system must preserve both concepts:

```text
object_id
content_hash
```

For example:

```text
object_id    = logical identity
content_hash = cryptographic identity of the content
```

---

## 5.5 Content-Based Identity

When the requirement is that an identifier be derived directly from content, an explicitly content-based scheme must be used.

The following must not be confused:

```text
name-based identity
```

with:

```text
content-addressed identity
```

The latter is especially relevant to CIDs and content integrity.

---

## 5.6 UUIDv8 for Modern Deterministic Schemes

When a module requires a 128-bit identifier based on a canonical name but needs SHA-256 or another modern algorithm, a UUIDv8 scheme compatible with RFC 9562 should be evaluated rather than assuming UUIDv5.

RFC 9562 expressly provides for this use of UUIDv8 for UUIDs based on SHA-256 or other modern algorithms.

---

# 6. Idempotency Rules

Idempotency must not depend exclusively on `object_id`.

An operation must be identifiable through:

```text
operation_id
object_id
version
content_hash
operation_type
```

Example:

```text
CREATE OBJECT
object_id = X
version   = 1
```

If the same request arrives again, the `Storage Manager` must be able to determine whether it is:

```text
a new operation
```

or:

```text
a repetition of the previous operation
```

---

# 7. Separation Between Identity and Idempotency

The following distinction must be maintained:

```text
OBJECT IDENTITY
        ≠
OPERATION IDENTITY
```

For example:

```text
object_id = A
```

may have:

```text
operation_id = 001
operation_id = 002
operation_id = 003
```

corresponding to different operations on the same object.

---

# 8. Versioning Rule

If the content of a logical object changes:

```text
object_id = A
```

the object may maintain:

```text
version 1
version 2
version 3
```

Each version must maintain its own integrity.

Therefore:

```text
Object A
 ├── v1 → hash H1 → CID C1
 ├── v2 → hash H2 → CID C2
 └── v3 → hash H3 → CID C3
```

This prevents silent overwrites and preserves history.

---

# 9. Testing Requirements

Before the implementation is considered complete, tests must exist for:

```text
concurrent read/write
concurrent manifest update
duplicate create
duplicate publish
interrupted transaction
process crash
power-loss recovery
Kubo unavailable
Kubo timeout
network interruption
queue saturation
quarantine saturation
recovery expiration
object version conflict
deterministic ID collision handling
```

---

# 10. Specific Recovery Tests

At minimum, the following must be simulated:

```text
FAIL BEFORE METADATA COMMIT
FAIL AFTER METADATA COMMIT
FAIL BEFORE LOCAL WRITE
FAIL AFTER LOCAL WRITE
FAIL BEFORE KUBO REQUEST
FAIL AFTER KUBO ACCEPTS
FAIL AFTER KUBO SUCCESS BUT BEFORE LOCAL CONFIRMATION
PROCESS CRASH DURING RETRY
```

The expected result must be:

```text
RECONCILIABLE
```

and not:

```text
UNKNOWN PERMANENT STATE
```

---

# 11. Expected Result

With these additional requirements, the storage infrastructure is prepared not only to store data, but to operate correctly under:

```text
concurrency
partial failures
interruptions
saturation
retries
recovery
versioning
duplication
deterministic identity
distribution
```

The architecture is therefore structured as:

```text
OBJECT
   ↓
IDENTITY
   ↓
POLICY
   ↓
LOCAL STORAGE
   ↓
METADATA
   ↓
STATE MACHINE
   ↓
SYNCHRONIZATION
   ↓
KUBO/IPFS
   ↓
RECOVERY
```

while always maintaining the separation between:

```text
object_id
operation_id
version
content_hash
CID
```

and between:

```text
stored
pinned
provided
replicated
backed-up
```

---

# 12. Final Implementation Requirement

Implementation must not seek merely to make operations work under normal conditions.

It must demonstrate that the system can:

> **fail, stop, restart, lose connectivity, receive duplicate operations, and recover its state without losing traceability or turning a temporary inconsistency into permanent corruption.**

This requirement constitutes a quality condition for the Storage Infrastructure of the Red de Nodos by LAEV.

---

**End of document.**
