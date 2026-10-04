# Node Core Runtime

**Status:** SUPPORTING / RECONCILED  
**Version:** 1.1.0

Runtime is the lifecycle and execution boundary of Node Core.

It coordinates readiness and lifecycle state only. It does not implement protocol execution, CPG consensus, CPG ledger, poker state, or protocol-specific engines.

Lifecycle:

UNINITIALIZED → ENVIRONMENT_VALIDATED → IDENTITY_INITIALIZED → STORAGE_INITIALIZED → STORAGE_STRUCTURE_VERIFIED → INTEGRITY_VERIFIED → RECOVERY_READY → NODE_CORE_READY → RUNNING

Runtime refuses to enter RUNNING unless a node identity has already been provisioned and the Node Core bootstrap/storage prerequisites are present.

Shutdown:

RUNNING → SHUTTING_DOWN → STOPPED

Failure/recovery states remain explicit in the runtime state machine.


**Authority:** `Documentation/Runtime/NODE-CORE-RUNTIME-LIFECYCLE.md`.

RuntimeManager and node_runtime.py implement the same canonical state machine; they do not define an alternate lifecycle. Configuration readiness is evaluated through the canonical Configuration Manager. Engine Runtime is subordinate to this Node Core lifecycle.
