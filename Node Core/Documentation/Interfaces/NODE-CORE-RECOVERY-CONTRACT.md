# Node Core Recovery Contract
Status: NORMATIVE DESIGN BASELINE

Recovery must distinguish:
- failure detection
- journal/checkpoint
- reconciliation
- restoration
- verification
- recovery completion

Required states:
NORMAL → FAILURE_DETECTED → RECOVERY_PENDING → RECOVERING → VERIFYING → RECOVERED / FAILED

Recovery must preserve traceability and must not silently overwrite valid newer state.
