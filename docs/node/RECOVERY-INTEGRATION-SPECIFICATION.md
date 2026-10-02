# Node Core Recovery Integration Specification

**Project:** Chain Poker Genesis by LAEV
**Component:** Node Core Recovery
**Status:** Formal Specification

Recovery is an explicit lifecycle operation, not an implicit reset.

Recovery may begin only from RUNNING or DEGRADED.

Recovery succeeds only when identity, configuration, storage, local provider, coherence, and recovery metadata remain valid, protocol associations remain empty, and CPG remains NOT_INSTALLED.

If validation fails, the runtime enters RECOVERY_FAILED.

A failed recovery MUST NOT silently return to READY.

Recovery never installs or activates Chain Poker Genesis.
