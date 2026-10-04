# Protocol API

**Status:** SUPPORTING / RECONCILED  
**Canonical authority:** `Documentation/Interfaces/NODE-CORE-PROTOCOL-INTERFACE-CONTRACT.md`

Defines the controlled API boundary between Node Core and higher-level protocols.

## Reference operations

- discoverCapabilities
- requestCapabilities
- installProtocol
- validateProtocol
- activateProtocol
- suspendProtocol
- uninstallProtocol
- getProtocolState

The API must preserve the Protocol Interface lifecycle and isolation rules.

## Administrative presentation boundary

The Protocols interface may request:

- installed protocol listing;
- protocol status/details;
- recognized installer listing;
- installer verification/install.

These are presentation/control requests. They do not create a second protocol registry.

## Isolation

A protocol may consume Node Core services but cannot redefine Node Core semantics through this API.

CPG consensus, ledger, poker/NLHE rules, table state, Table Wallet, settlement and rake remain outside the Node Core API.
