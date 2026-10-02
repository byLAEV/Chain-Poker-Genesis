# SREC — ENCRYPTED EXTERNAL BACKUP SYSTEM

**Backup, Recovery, and Operational Continuity Subsystem**  
**Red de Nodos by LAEV**  
**Technical Specification and Encrypted Backup Strategy**  
**Version:** 1.0

---

## 1. Purpose

The **SREC (Encrypted External Backup System)** is the subsystem responsible for preserving and recovering critical node information when failures exceed the node's local recovery capabilities.

Its primary function is to provide a protection layer against scenarios such as:

- total equipment loss;
- local storage corruption;
- operating system failure;
- physical destruction of the host;
- fire, theft, or device loss;
- database corruption;
- configuration loss;
- human error;
- prolonged local service failures;
- the need to rebuild a node in a new environment.

SREC does not replace local storage, the synchronization system, or IPFS/Kubo. It constitutes an **additional operational continuity and disaster recovery layer**.

---

## 2. Fundamental Principle

The architecture must clearly distinguish between:

```text
STORAGE
IDENTITY
SYNCHRONIZATION
DISTRIBUTION
BACKUP
RECOVERY
```

An object may be stored locally, distributed through IPFS, referenced by a CID, or externally backed up, and each of these conditions represents a different property.

In particular:

> **A CID identifies content, but by itself it is not a backup and does not guarantee that the content will remain available.**

For this reason, SREC must retain sufficient information to reconstruct the node's critical state independently of the immediate availability of the original storage.

---

## 3. Continuity Objective

SREC must support the following conceptual operation:

```text
ORIGINAL NODE
      │
      ▼
CRITICAL STATE
      │
      ▼
SNAPSHOT
      │
      ▼
COMPRESSION
      │
      ▼
ENCRYPTION
      │
      ▼
VERIFICATION / SIGNATURE
      │
      ▼
EXTERNAL BACKUP
      │
      ▼
NODE LOSS
      │
      ▼
NEW NODE
      │
      ▼
RECOVERY
      │
      ▼
AUDIT
      │
      ▼
RECONCILIATION
      │
      ▼
NORMAL OPERATION
```

The objective is not to preserve absolutely every file on the machine, but to preserve in a controlled manner the elements required to reconstruct the node's operational and administrative state.

---

## 4. Scope

SREC primarily manages:

### 4.1 Infrastructure State

- critical configuration;
- node identification;
- operational parameters;
- module configuration;
- policies;
- schema versions;
- references required for reconstruction.

### 4.2 Metadata

- Metadata Store;
- manifests;
- indexes;
- object references;
- versions;
- states;
- relationships between objects.

### 4.3 Journal and Operations

- Operation Journal;
- critical pending operations;
- history required for recovery;
- states required for reconciliation.

### 4.4 Cryptographic Information

When permitted by the security policy:

- material required for identity recovery;
- key references;
- cryptographic configuration information;
- secret recovery mechanisms.

Master keys must not be indiscriminately stored inside the same backup package that they protect.

### 4.5 Distributed References

- critical CIDs;
- content indexes;
- distribution manifests;
- pinning state when relevant;
- references required for reconstruction.

---

## 5. Backup Content Classification

SREC must classify each object according to its recovery requirement.

### 5.1 CRITICAL

Information whose loss prevents correct reconstruction of the node.

Examples:

```text
Metadata Store
Node Identity
Critical Configuration
Backup Metadata
Manifest Index
Operation Journal
Critical CID Index
Security Configuration
```

It must be included in mandatory backups.

---

### 5.2 IMPORTANT

Information required to restore certain functionality but which can be partially reconstructed.

Examples:

```text
Module Metadata
Derived Indexes
Synchronization Metadata
Operational Reports
Non-critical Manifests
```

Its inclusion depends on policy.

---

### 5.3 REBUILDABLE

Information that can be regenerated from other sources.

Examples:

```text
cache
temporary files
derived indexes
processing artifacts
reconstructable queues
```

It may be excluded from backups to reduce size.

---

### 5.4 EPHEMERAL

Temporary information whose recovery provides no permanent value.

Examples:

```text
temporary/
cache/
runtime temporary files
transient processing data
```

It should not be included unless a specific application establishes an exception.

---

## 6. Elements Normally Excluded from Backup

The default strategy should avoid indiscriminately copying:

```text
cache/
temporary/
runtime/
processing/
rejected quarantine/
purged quarantine/
temporary sync queues/
```

However, this exclusion must be **configurable by policy**.

A critical system may require certain normally rebuildable elements to be backed up.

Therefore:

> Exclusion is a policy, not an absolute rule.

---

## 7. Backup Repository

External storage must be separated from the primary operational storage.

Conceptually:

```text
NODE
│
├── LOCAL STORAGE
├── METADATA STORE
├── KUBO
└── SREC
      │
      ├── BACKUP BUILDER
      ├── ENCRYPTION
      ├── MANIFEST
      ├── VERIFICATION
      └── EXTERNAL STORAGE
```

SREC must not depend on a single external location.

The architecture must support different adapters:

```text
S3-compatible
SFTP
WebDAV
Remote IPFS
Object Storage
Other External Repository
```

The destination must remain decoupled from the main backup logic.

---

## 8. Logical Architecture

```text
                 RED DE NODOS BY LAEV
                         │
                         ▼
                STORAGE INFRASTRUCTURE
                         │
                         ▼
                   SREC ENGINE
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
 BACKUP POLICY    SNAPSHOT MANAGER   RECOVERY MANAGER
        │                │                │
        └────────────┬───┴───────┬────────┘
                     ▼
               BACKUP BUILDER
                     │
             ┌───────┴───────┐
             ▼               ▼
        COMPRESSOR       MANIFEST
             │               │
             └───────┬───────┘
                     ▼
                 ENCRYPTION
                     │
                     ▼
                 INTEGRITY
                     │
                     ▼
               DIGITAL SIGNATURE
                     │
                     ▼
              EXTERNAL ADAPTER
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
         S3         SFTP       IPFS
```

---

## 9. Backup Generation Process

The process must be deterministic with respect to the contents of the backup.

### Flow

```text
IDENTIFY STATE
        ↓
APPLY BACKUP POLICY
        ↓
GENERATE CONSISTENT SNAPSHOT
        ↓
COLLECT METADATA
        ↓
GENERATE BACKUP MANIFEST
        ↓
BUILD PACKAGE
        ↓
COMPRESS
        ↓
ENCRYPT
        ↓
HASH / INTEGRITY
        ↓
OPTIONAL / RECOMMENDED SIGNATURE
        ↓
TRANSFER
        ↓
REMOTE VERIFICATION
        ↓
CONFIRM BACKUP
```

---

## 10. Backup Consistency

The backup must represent a coherent node state.

It must not be assumed that indiscriminately copying active files produces a valid recovery.

In particular, databases and stores with concurrent operations must use consistent snapshot or backup mechanisms.

Conceptually:

```text
ACTIVE SYSTEM
     │
     ▼
CONSISTENT SNAPSHOT
     │
     ├── Metadata
     ├── Journal
     ├── Configuration
     └── Manifest Index
```

Temporary files, WAL files, or internal structures must be copied using mechanisms compatible with the storage technology.

---

## 11. Backup Manifest

Each backup must contain its own manifest.

Conceptual example:

```text
backup_id
node_id
backup_type
schema_version
software_version
created_at
source_state
included_objects
excluded_objects
content_hash
compression_algorithm
encryption_algorithm
signature_algorithm
parent_backup_id
previous_backup_hash
retention_policy
```

The manifest must make it possible to determine:

- what was backed up;
- what was excluded;
- when it was created;
- which version produced the backup;
- which algorithms were used;
- which backup preceded it;
- which content is protected;
- how it can be verified.

---

## 12. Backup Identity

Each backup must have its own identity.

The following must remain distinct:

```text
node_id
object_id
operation_id
backup_id
```

These identifiers must not be reused for different functions.

Example:

```text
NODE-001
OBJECT-8472
OP-99201
BACKUP-2026-09-29-00017
```

The `backup_id` identifies the backup as a recovery unit.

---

## 13. Backup Chain

Backups may form a verifiable chain.

Example:

```text
BACKUP A
   │
   ▼
BACKUP B
   │
   ▼
BACKUP C
   │
   ▼
BACKUP D
```

Each backup may retain:

```text
parent_backup_id
previous_backup_hash
```

This allows the system to detect unauthorized alteration, deletion, or replacement within the backup sequence.

---

## 14. Backup Types

SREC must support at least:

### FULL

Complete copy of the selected state.

```text
FULL
```

### INCREMENTAL

Only changes made after the reference backup.

```text
FULL
  ↓
INC 1
  ↓
INC 2
  ↓
INC 3
```

### SNAPSHOT

A coherent representation of a specific state.

### RECOVERY CHECKPOINT

A backup specially validated and marked as suitable for recovery.

---

## 15. Compression

The backup may be compressed before encryption.

Example:

```text
DATA
 ↓
TAR
 ↓
ZSTD
 ↓
ENCRYPTION
```

An implementation may use an equivalent versioned container.

Compression must produce a reproducible and verifiable stream.

---

## 16. Encryption

Every backup containing sensitive information must be encrypted **before leaving the node's cryptographic control**.

Suitable AEAD algorithms may include:

```text
AES-256-GCM
ChaCha20-Poly1305
```

Encryption must provide:

- confidentiality;
- authentication;
- tamper detection.

The system must not implement custom cryptography.

It must use mature and maintained cryptographic libraries.

---

## 17. Key Separation

SREC must distinguish at least:

```text
NODE IDENTITY KEY
BACKUP ENCRYPTION KEY
BACKUP RECOVERY KEY
APPLICATION SECRET
MASTER KEY
```

They must not be treated as one universal credential.

In particular:

> The key used to decrypt a backup must not be stored inside the same package protected by that key.

Key recovery must follow an independent policy.

---

## 18. Integrity and Authenticity

SREC must distinguish three concepts:

### Cryptographic Integrity

Detects modifications.

```text
HASH
```

### Authentication of Encrypted Content

May be provided by:

```text
AEAD authentication tag
```

### Authenticity of Origin

May be provided by:

```text
DIGITAL SIGNATURE
```

A hash must not be treated as a substitute for a signature.

HMAC must not be treated as conceptually equivalent to a digital signature.

The implementation may use:

```text
AEAD
+
HASH
+
DIGITAL SIGNATURE
```

according to the defined security model.

---

## 19. Backup Package

Conceptually:

```text
SREC BACKUP
│
├── manifest
├── metadata
├── journal
├── configuration
├── indexes
├── critical_references
└── payload
```

Then:

```text
PACKAGE
   ↓
COMPRESS
   ↓
ENCRYPT
   ↓
SIGN
```

The result is the artifact transferred to external storage.

---

## 20. External Storage Policy

The architecture must remain provider-independent.

Example:

```text
SREC
 ├── S3 Adapter
 ├── SFTP Adapter
 ├── WebDAV Adapter
 ├── IPFS Adapter
 └── Custom Adapter
```

Each adapter must implement a common interface:

```text
connect()
put()
get()
list()
verify()
delete()
restore()
```

The policy must determine which destinations are authorized.

---

## 21. Redundancy

SREC may use multiple destinations:

```text
LOCAL
   +
OFFSITE A
   +
OFFSITE B
```

The strategy may apply policies such as:

```text
7 daily
4 weekly
12 monthly
```

or any other combination defined by node administration.

A universal retention policy must not be imposed when different installations may require different protection levels.

---

## 22. Retention

Each backup must have a retention policy.

Example:

```text
RETENTION_POLICY
├── daily
├── weekly
├── monthly
├── archival
└── legal/security hold
```

Automatic deletion must respect:

```text
RETENTION_HOLD
```

A backup protected by `RETENTION_HOLD` must not be removed by automatic rotation.

---

## 23. Verification

Backup creation does not imply that the backup is valid.

SREC must distinguish:

```text
CREATED
UPLOADED
VERIFIED
RECOVERY_VALIDATED
EXPIRED
CORRUPTED
```

A copy should only be considered **Recovery Validated** after passing the checks defined by the system.

---

## 24. Post-Transfer Verification

After uploading a backup:

```text
LOCAL PACKAGE
      │
      ▼
UPLOAD
      │
      ▼
REMOTE OBJECT
      │
      ▼
RECALCULATE HASH
      │
      ▼
COMPARE
      │
      ▼
VERIFY MANIFEST
      │
      ▼
MARK VERIFIED
```

A transfer that completes successfully but fails cryptographic verification must be marked invalid.

---

## 25. Disaster Recovery

The recovery process must begin in a clean environment.

```text
NEW MACHINE
      │
      ▼
INSTALL BASE SYSTEM
      │
      ▼
INSTALL NODE INFRASTRUCTURE
      │
      ▼
INSTALL / CONFIGURE KUBO
      │
      ▼
RECOVERY MODE
      │
      ▼
LOAD BACKUP
```

Then:

```text
VERIFY BACKUP
      ↓
VERIFY SIGNATURE
      ↓
VERIFY MANIFEST
      ↓
VERIFY COMPATIBILITY
      ↓
DECRYPT
      ↓
RESTORE METADATA
      ↓
RESTORE JOURNAL
      ↓
RESTORE CONFIGURATION
      ↓
RESTORE CRITICAL REFERENCES
```

---

## 26. Recovery / Audit Mode

A recovered node must not immediately enter normal operation.

It must begin in:

```text
RECOVERY MODE
```

Its flow is:

```text
NEW NODE
   ↓
RECOVERY
   ↓
AUDIT
   ↓
IDENTITY VERIFICATION
   ↓
METADATA VERIFICATION
   ↓
JOURNAL VERIFICATION
   ↓
CID / CONTENT REFERENCE VERIFICATION
   ↓
KUBO VERIFICATION
   ↓
POLICY VERIFICATION
   ↓
RECONCILIATION
   ↓
NORMAL OPERATION
```

This prevents a partially valid restoration from immediately producing new operations.

---

## 27. Post-Recovery Reconciliation

After restoring state, SREC must activate reconciliation.

It must compare:

```text
RESTORED STATE
      VS
CURRENT LOCAL STATE
      VS
DISTRIBUTED REFERENCES
      VS
KUBO/IPFS STATE
```

The objective is to determine:

- which objects exist;
- which are missing;
- which must be recovered;
- which must be synchronized again;
- which require validation;
- which require administrative intervention.

---

## 28. CID and IPFS in Recovery

CIDs must be used as verifiable references to distributed content.

However:

```text
CID ≠ BACKUP
CID ≠ AVAILABILITY GUARANTEE
CID ≠ ENCRYPTION KEY
CID ≠ ACCESS PERMISSION
CID ≠ NODE IDENTITY
```

When content exists at other IPFS sources, the node may attempt to retrieve it using its CID.

When no provider has the content, the system must rely on:

```text
external backup
replica
pin
archival copy
```

according to the defined policy.

---

## 29. Policy for Kubo-Stored Data

Kubo's internal repository must be treated as independent from the application's storage structure.

SREC must not automatically assume that the entire Kubo internal repository must be backed up.

The policy must determine, case by case:

```text
REBUILD KUBO
+
RESTORE CRITICAL APPLICATION STATE
+
REPIN REQUIRED CONTENT
```

or:

```text
RESTORE SELECTED KUBO STATE
```

When data has no other recovery source and its loss is unacceptable, specific backups of the corresponding state may be included.

---

## 30. Pin Recovery

When the backup retains the required content index, recovery may reconstruct persistence policies.

Conceptually:

```text
RESTORED CID INDEX
        ↓
VERIFY CONTENT
        ↓
IDENTIFY REQUIRED OBJECTS
        ↓
REBUILD PIN STATE
        ↓
VERIFY
```

This avoids relying exclusively on the historical configuration of the original node.

---

## 31. RPO — Recovery Point Objective

SREC must define an **RPO**.

RPO represents how much work may be temporarily lost as a consequence of a disaster.

Example:

```text
RPO = 24h
```

means that the design potentially accepts losing up to approximately one day of changes not included in a valid backup.

The policy may establish:

```text
daily RPO
6-hour RPO
hourly RPO
continuous RPO
```

according to criticality.

---

## 32. RTO — Recovery Time Objective

SREC must also define an **RTO**.

RTO represents the target time for recovering the node to the established operational level.

Example:

```text
RTO = 4h
```

This does not mean the system can guarantee exactly that time in every scenario; it is the operational target used to design and measure the infrastructure.

---

## 33. Backup States

A state machine is recommended:

```text
CREATED
   ↓
SNAPSHOT_READY
   ↓
PACKAGED
   ↓
ENCRYPTED
   ↓
SIGNED
   ↓
UPLOADING
   ↓
UPLOADED
   ↓
VERIFIED
   ↓
RECOVERY_VALIDATED
```

Failure states:

```text
FAILED
CORRUPTED
RETRY_WAIT
REJECTED
EXPIRED
PURGED
```

---

## 34. Failure Handling

SREC must treat separately:

```text
NETWORK FAILURE
DESTINATION FAILURE
AUTHENTICATION FAILURE
ENCRYPTION FAILURE
CORRUPTION
INVALID MANIFEST
VERSION INCOMPATIBILITY
INSUFFICIENT STORAGE
KEY UNAVAILABLE
```

Recoverable errors must transition to:

```text
RETRY_WAIT
```

Permanent errors must produce:

```text
FAILED
```

or:

```text
REJECTED
```

according to their nature.

---

## 35. Backoff and Retry Control

Failed transfers must use controlled retry mechanisms.

Conceptually:

```text
ATTEMPT 1
   ↓
WAIT
   ↓
ATTEMPT 2
   ↓
WAIT LONGER
   ↓
ATTEMPT 3
   ↓
...
```

The implementation should use:

```text
exponential backoff
+
jitter
+
maximum retry count
```

to prevent saturation of an external destination.

---

## 36. Operation Records

Each backup operation must contain enough information for auditing:

```text
operation_id
backup_id
attempt
destination
started_at
completed_at
status
error_code
last_error
retry_count
```

The system must not rely exclusively on log files to determine the actual backup state.

Critical information must persist in the Metadata Store or equivalent mechanism.

---

## 37. Operational Security

SREC must apply privilege separation.

Conceptual example:

```text
APPLICATION
     │
     └── NO DIRECT ACCESS TO BACKUP KEYS

SREC ENGINE
     │
     ├── BACKUP DATA ACCESS
     └── CONTROLLED ENCRYPTION OPERATIONS

KEY MANAGEMENT
     │
     └── INDEPENDENT SECRET CONTROL
```

A normal application must not be able to directly extract backup master keys.

---

## 38. Protection Against Corruption and Manipulation

A backup must be considered untrusted until it passes:

```text
HASH VERIFICATION
SIGNATURE VERIFICATION
MANIFEST VALIDATION
SCHEMA VALIDATION
VERSION COMPATIBILITY
```

An invalid package must be placed in:

```text
REJECTED
```

and must not be restored automatically.

---

## 39. Mandatory Tests

SREC implementation must include tests for:

```text
BACKUP CREATION
BACKUP RESTORATION
CORRUPTED BACKUP
INVALID SIGNATURE
WRONG KEY
MISSING DESTINATION
NETWORK INTERRUPTION
PARTIAL UPLOAD
DATABASE FAILURE
NODE LOSS
HARDWARE LOSS
KUBO LOSS
VERSION MIGRATION
KEY RECOVERY
CID RECONCILIATION
```

Real restoration tests must also be performed periodically.

A backup that has never been restored in a test must not be considered fully validated.

---

## 40. Full Recovery Test

The highest-level test is:

```text
DESTROYED / SIMULATED NODE
        ↓
NEW MACHINE
        ↓
INSTALL BASE
        ↓
RESTORE KEYS / RECOVERY MATERIAL
        ↓
RESTORE BACKUP
        ↓
RESTORE METADATA
        ↓
RESTORE JOURNAL
        ↓
RESTORE CONFIGURATION
        ↓
RESTORE REFERENCES
        ↓
REINSTALL / CONFIGURE KUBO
        ↓
RECONCILIATION
        ↓
AUDIT
        ↓
NORMAL OPERATION
```

The duration and result must be recorded to measure actual RTO.

---

## 41. Security Model

SREC architecture must pursue five properties:

```text
CONFIDENTIALITY
INTEGRITY
AUTHENTICITY
AVAILABILITY
RECOVERABILITY
```

These properties must be treated separately.

Encryption does not guarantee availability.

A CID does not guarantee availability.

A signature does not guarantee recovery.

Storage redundancy does not guarantee confidentiality.

The architecture must combine these properties through independent layers.

---

## 42. Complete Conceptual Model

```text
                  RED DE NODOS BY LAEV
                           │
                           ▼
                 STORAGE INFRASTRUCTURE
                           │
                           ▼
                      SREC ENGINE
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
 BACKUP POLICY       SNAPSHOT MANAGER    RECOVERY ENGINE
        │                  │                  │
        └──────────────┬───┴───────┬──────────┘
                       ▼
                 BACKUP BUILDER
                       │
              ┌────────┴────────┐
              ▼                 ▼
         MANIFEST          PAYLOAD
              │                 │
              └────────┬────────┘
                       ▼
                  COMPRESSION
                       ▼
                    ENCRYPTION
                       ▼
                  INTEGRITY
                       ▼
                    SIGNING
                       ▼
                EXTERNAL STORAGE
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
         S3           SFTP         IPFS
                       │
                       ▼
                 VERIFICATION
                       │
                       ▼
             RECOVERY VALIDATED
```

---

## 43. Independence Principle

SREC must remain decoupled from higher-level applications.

The correct architecture is:

```text
Red de Nodos by LAEV
        │
        ├── Storage Infrastructure
        │
        ├── Identity Infrastructure
        │
        ├── SREC
        │
        └── Other Engines
```

SREC must not be designed specifically as an internal function of Chain Poker Genesis.

**Chain Poker Genesis by LAEV may use SREC, as may other systems installed on the Red de Nodos by LAEV.**

---

## 44. Final Principle

The purpose of SREC is not simply to preserve a copy of files.

Its purpose is to preserve the **capacity to reconstruct a trustworthy node state**.

Therefore, the backup must consider together:

```text
DATA
+
METADATA
+
IDENTITY
+
CONFIGURATION
+
JOURNAL
+
REFERENCES
+
CRYPTOGRAPHIC PROTECTION
+
RECOVERY INFORMATION
```

The resulting strategy can be summarized as:

```text
PRESERVE
      ↓
PROTECT
      ↓
VERIFY
      ↓
REPLICATE
      ↓
VALIDATE
      ↓
RECOVER
      ↓
RECONCILE
      ↓
CONTINUE
```

SREC must therefore be understood as **operational continuity and disaster recovery infrastructure**, not simply as a backup mechanism.

Its design must allow the complete loss of a physical node without automatically implying irreversible loss of the critical state it managed, provided that recovery keys, valid backups, retention policies, and required content sources remain available.

---

## 45. Official Designation

**Name:** SREC  
**Extended Name:** Encrypted External Backup System  
**Function:** Backup, Disaster Recovery & Continuity  
**Layer:** Red de Nodos by LAEV Infrastructure  
**Conceptual Dependency:** Storage Infrastructure  
**Consumers:** Engines and applications installed on the Red de Nodos by LAEV

**End of document.**
