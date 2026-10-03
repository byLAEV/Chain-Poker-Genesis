# Node Core — Canonical State Model
Status: DESIGN BASELINE

## Node lifecycle
UNINITIALIZED
→ BOOTSTRAPPING
→ INITIALIZING
→ IDENTITY_REQUIRED
→ CONFIGURING
→ VERIFYING
→ READY
→ RUNNING
→ DEGRADED
→ RECOVERY
→ SHUTTING_DOWN
→ STOPPED

Failure at a controlled phase enters the appropriate recovery/error state rather than silently advancing.

## Protocol state
NOT_INSTALLED
→ INSTALL_REQUESTED
→ VALIDATING
→ INSTALLED
→ ACTIVATED
→ DEACTIVATED

Protocol state is independent from Node Core lifecycle. Node Core bootstrap MUST remain valid with protocol state NOT_INSTALLED.

## Engine state
DISCOVERED
→ REGISTERED
→ INITIALIZING
→ ACTIVE
→ STOPPING
→ STOPPED
→ FAILED

## Storage object state
CREATED
→ VERIFIED
→ STORED
→ SYNC_PENDING
→ SYNCING
→ DISTRIBUTED
→ QUARANTINED
→ RECOVERY_PENDING
→ RECOVERED
→ DELETED

Exact transitions require the Storage state contract and policy engine.

## Network peer state
DISCOVERED
→ CONNECTING
→ CONNECTED
→ DISCONNECTED
→ FAILED

The state model is normative until superseded by a more detailed component contract.
