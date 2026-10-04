# Node Core Protocol Interface

**Status:** SUPPORTING / RECONCILED  
**Version:** 1.1.0  
**Canonical authority:** `Documentation/Interfaces/NODE-CORE-PROTOCOL-INTERFACE-CONTRACT.md`

Protocol Interface is the minimal administrative and lifecycle boundary between protocol-neutral Node Core and independently installed protocols.

## Responsibilities

- discover protocol descriptors;
- validate protocol manifests;
- verify capability compatibility;
- register protocols;
- verify and install recognized protocol installers;
- associate required protocol engines through Engine Runtime;
- expose installed protocol state;
- expose recognized installers;
- activate, suspend and remove protocols according to the canonical lifecycle.

## Administrative interface

The Node Core Protocols interface is intentionally sober:

- white background;
- black primary text;
- dark gray secondary text;
- light gray supporting text;
- clear text hierarchy;
- no decorative background graphics.

The Protocols layer contains:

```text
PROTOCOLS

Installed Protocols
- <installed protocol>

Install Protocol
- <recognized installer>
```

The installer view represents `Node Core/Protocols/Installers/`. Installed protocols are represented under `Node Core/Protocols/Installed/`.

The presentation layer is not a second registry. It delegates protocol state and installation decisions to Protocol Interface.

## State distinction

`AVAILABLE INSTALLER ≠ INSTALLED ≠ ACTIVE ≠ RUNNING`

The interface must never imply that installation automatically means activation or execution.

## Isolation

Node Core hosts and manages protocols but does not become the protocol.

CPG-specific consensus, ledger, poker rules, table state, Table Wallet, settlement and rake remain outside Node Core.

Protocol engines remain independently versioned and are not global Node Core versions.
