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
- remote protocol catalog listing;
- CID/GitHub source and download link;
- protocol package download into `Node Core/Protocols/`;
- local package verification;
- protocol installation.

These are presentation/control requests. They do not create a second protocol registry.

The download and installation stages are distinct:

`Remote Catalog → Download → Local Package → Verify → Install`

## Isolation

A protocol may consume Node Core services but cannot redefine Node Core semantics through this API.

CPG consensus, ledger, poker/NLHE rules, table state, Table Wallet, settlement and rake remain outside the Node Core API.
