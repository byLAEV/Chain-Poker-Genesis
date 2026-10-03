# Node Manager API

Controls and observes the lifecycle of Node Core services and registered engines.

## Contract

Conceptual operations:

- getNodeState
- getNodeHealth
- startService
- stopService
- restartService
- registerEngine
- unregisterEngine
- listEngines
- getCapabilities
- enterRecovery
- exitRecovery

The Node Manager API does not manage CPG application state.
