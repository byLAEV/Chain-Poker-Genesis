# Node Core Runtime Lifecycle

## Formal Specification

**Project:** Chain Poker Genesis by LAEV  
**Component:** Node Core  
**Status:** Architectural Definition  
**Scope:** Node Core lifecycle only

### 1. Purpose

This specification defines the lifecycle of a protocol-neutral Node Core from initialization through shutdown and recovery.

The lifecycle does not install, activate, associate, or execute the Chain Poker Genesis protocol.

### 2. Lifecycle States

- UNINITIALIZED
- INITIALIZING
- VERIFYING
- READY
- RUNNING
- DEGRADED
- RECOVERY
- SHUTTING_DOWN
- STOPPED
- INITIALIZATION_FAILED
- VERIFICATION_FAILED
- RECOVERY_FAILED

### 3. Valid Transitions

~~~text
UNINITIALIZED
      |
      v
INITIALIZING -----> INITIALIZATION_FAILED
      |
      v
VERIFYING --------> VERIFICATION_FAILED
      |
      v
READY
      |
      +-----------> RUNNING
      |               |
      |               +--> DEGRADED
      |               |       |
      |               |       v
      |               |    RECOVERY --> READY
      |               |       |
      |               |       +------> RECOVERY_FAILED
      |               |
      |               +--> SHUTTING_DOWN
      |
      v
SHUTTING_DOWN
      |
      v
STOPPED
      |
      v
INITIALIZING
~~~

### 4. Runtime Readiness Preconditions

READY requires all of the following:

- identity is initialized;
- configuration is valid;
- storage is available;
- storage provider is ready;
- local storage coherence is verified;
- recovery is ready;
- protocol associations are empty;
- CPG protocol status is NOT_INSTALLED.

RUNNING may only be entered from READY and only after the same readiness conditions remain true.

### 5. Protocol Boundary

The runtime lifecycle is intentionally protocol-neutral.

The runtime implementation MUST NOT:

- install Chain Poker Genesis;
- activate Chain Poker Genesis;
- create a protocol association;
- claim network synchronization merely from local coherence;
- write protocol-reserved storage objects.

The expected baseline remains:

~~~text
CPG = NOT_INSTALLED
CPG = NOT_ASSOCIATED
CPG = NOT_ACTIVE
~~~

### 6. Recovery

Recovery is an explicit lifecycle state. A degraded runtime may enter RECOVERY.

Recovery may return to READY only after readiness conditions are revalidated. Failed recovery enters RECOVERY_FAILED and does not silently restore the runtime to a healthy state.

### 7. Shutdown

SHUTTING_DOWN represents an intentional controlled stop. The final state is STOPPED.

A stopped Node Core may be initialized again; this does not install or activate any protocol.

### 8. Health and Readiness

Health is an observation of runtime conditions. Readiness is a gate for entering operational states.

A healthy Node Core reports:

~~~text
Identity         = READY
Configuration    = READY
Storage          = READY
Provider         = READY
Coherence        = COHERENT
Recovery         = READY
Synchronization  = NOT_EVALUATED
CPG              = NOT_INSTALLED

NODE CORE        = READY
~~~

COHERENT MUST NOT be interpreted as SYNCHRONIZED.

### 9. Determinism

The reference implementation uses explicit state-transition validation so invalid lifecycle transitions fail rather than being silently accepted.
