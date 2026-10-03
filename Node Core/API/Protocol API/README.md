# Protocol API

Defines the controlled interface between Node Core and higher-level protocols.

## Contract

- discoverCapabilities
- requestCapabilities
- installProtocol
- validateProtocol
- activateProtocol
- suspendProtocol
- uninstallProtocol
- getProtocolState

The API must preserve protocol isolation.

A protocol may consume Node Core services but cannot redefine Node Core semantics through this API.
