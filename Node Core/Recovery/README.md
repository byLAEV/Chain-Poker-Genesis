# Node Core Recovery

**Status:** IMPLEMENTED
**Version:** 1.1.0

Recovery is the protocol-neutral recovery boundary for Node Core installation and runtime prerequisites.

It:
- inspects the Node Core environment;
- verifies essential storage/configuration/state prerequisites;
- creates the recovery boundary;
- records recovery status;
- reports RECOVERY_READY, RECOVERY_INCOMPLETE, or RECOVERY_FAILED.

Storage-specific object restoration remains the responsibility of Node Core Storage Recovery.

Identity key recovery remains external to Node Core and must not be implemented as private-key generation or extraction by this module.

Recovery does not restore CPG ledger state, CPG consensus state, table state, or protocol-specific data.
