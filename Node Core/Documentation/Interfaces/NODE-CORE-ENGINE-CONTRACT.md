# Node Core Engine Contract
Status: NORMATIVE DESIGN BASELINE

Every Node Core engine must declare:
- name
- version
- engine type
- dependencies
- required Node Core services
- initialization requirements
- lifecycle hooks
- configuration schema
- integrity information
- compatibility information

Lifecycle:
DISCOVERED → REGISTERED → INITIALIZING → ACTIVE → STOPPING → STOPPED / FAILED

Engines must not directly mutate another engine's private state. Cross-engine access occurs through declared Node Core service interfaces.
