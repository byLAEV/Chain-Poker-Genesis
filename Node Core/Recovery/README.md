# Node Core Recovery

**Status:** IMPLEMENTED_PARTIAL / RECONCILED
**Version:** 1.2.0

Recovery is the protocol-neutral recovery boundary for Node Core installation and runtime prerequisites.

Canonical lifecycle: `NORMAL → FAILURE_DETECTED → RECOVERY_PENDING → RECOVERING → VERIFYING → RECOVERED / FAILED`.

Recovery records preserve a journal of attempts and do not silently overwrite an already verified recovered state.

It:
- inspects the Node Core environment;
- verifies essential storage/configuration/state prerequisites;
- creates the recovery boundary;
- records recovery status;
- reports RECOVERY_READY, RECOVERY_INCOMPLETE, or RECOVERY_FAILED.

Storage-specific object restoration remains the responsibility of Node Core Storage Recovery.

Identity key recovery remains external to Node Core and must not be implemented as private-key generation or extraction by this module.

Recovery does not restore CPG ledger state, CPG consensus state, table state, or protocol-specific data.
