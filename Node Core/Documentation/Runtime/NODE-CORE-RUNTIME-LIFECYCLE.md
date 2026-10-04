# Node Core Runtime Lifecycle

## Formal Contract

**Project:** Chain Poker Genesis by LAEV  
**Component:** Node Core  
**Status:** Normative contract baseline  
**Scope:** Protocol-neutral Node Core lifecycle

### 1. Purpose

This contract defines the lifecycle of Node Core from initialization through operational readiness, shutdown and recovery.

The lifecycle does not install, activate, associate or execute the Chain Poker Genesis protocol.

### 2. Canonical lifecycle states

Normal states:

- UNINITIALIZED
- ENVIRONMENT_VALIDATED
- IDENTITY_INITIALIZED
- STORAGE_INITIALIZED
- STORAGE_STRUCTURE_VERIFIED
- INTEGRITY_VERIFIED
- RECOVERY_READY
- NODE_CORE_READY
- RUNNING
- DEGRADED
- RECOVERY
- SHUTTING_DOWN
- STOPPED

Failure states:

- ENVIRONMENT_INVALID
- IDENTITY_FAILED
- STORAGE_FAILED
- STRUCTURE_MISMATCH
- INTEGRITY_FAILED
- RECOVERY_FAILED
- MANIFEST_INVALID
- PROTOCOL_ISOLATION_FAILED

### 3. Canonical transitions

```text
UNINITIALIZED
      ↓
ENVIRONMENT_VALIDATED
      ↓
IDENTITY_INITIALIZED
      ↓
STORAGE_INITIALIZED
      ↓
STORAGE_STRUCTURE_VERIFIED
      ↓
INTEGRITY_VERIFIED
      ↓
RECOVERY_READY
      ↓
NODE_CORE_READY
      ↓
RUNNING
      ├──→ DEGRADED → RECOVERY → NODE_CORE_READY
      ├──→ RECOVERY → NODE_CORE_READY
      └──→ SHUTTING_DOWN → STOPPED → ENVIRONMENT_VALIDATED
```

At each controlled validation boundary, the corresponding failure state may be entered.

Invalid transitions MUST fail explicitly.

### 4. Readiness contract

NODE_CORE_READY requires:

- environment available;
- identity initialized;
- storage available;
- configuration valid;
- storage structure verified;
- integrity verified;
- recovery ready;
- provider ready;
- storage coherence verified;
- protocol associations empty;
- CPG status NOT_INSTALLED.

RUNNING requires the same readiness conditions.

### 5. Protocol boundary

Runtime MUST NOT:

- install CPG;
- activate CPG;
- create a CPG protocol association;
- claim network synchronization from local coherence;
- write protocol-reserved objects.

Baseline:

```text
CPG = NOT_INSTALLED
CPG = NOT_ASSOCIATED
CPG = NOT_ACTIVE
```

### 6. Recovery

DEGRADED may enter RECOVERY.

RECOVERY may return to NODE_CORE_READY only after readiness is revalidated.

RECOVERY_FAILED is a terminal failure for that recovery attempt and MUST NOT silently become healthy.

### 7. Shutdown

SHUTTING_DOWN is a controlled stop. It transitions to STOPPED.

STOPPED may return to ENVIRONMENT_VALIDATED for a subsequent initialization sequence.

### 8. Health and readiness

Health describes condition. Readiness describes whether Node Core satisfies the operational gate.

COHERENT MUST NOT be interpreted as SYNCHRONIZED.

### 9. Implementation authority

The canonical implementation state machine is:

`Node Core/Runtime/State/runtime_state.py`

The lifecycle contract and implementation MUST remain semantically synchronized.

### 10. Verification

The lifecycle verification suite MUST cover:

1. valid normal transitions;
2. invalid transitions;
3. readiness prerequisites;
4. shutdown;
5. recovery;
6. failure states;
7. protocol isolation.
