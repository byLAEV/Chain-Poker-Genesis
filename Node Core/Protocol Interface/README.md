# Node Core Protocol Interface

**Status:** SUPPORTING / RECONCILED  
**Version:** 1.2.0  
**Canonical authority:** `Documentation/Interfaces/NODE-CORE-PROTOCOL-INTERFACE-CONTRACT.md`

Protocol Interface is the minimal administrative and lifecycle boundary between protocol-neutral Node Core and independently installed protocols.

## Responsibilities

- expose the remote protocol catalog;
- represent CID and GitHub protocol sources;
- expose a visible download/reference link;
- resolve a supported source into a downloadable package;
- download the package into `Node Core/Protocols/`;
- validate the local package before installation;
- register and install the protocol;
- associate required protocol engines through Engine Runtime;
- expose installed protocol state;
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

Install Protocols
- <remote protocol catalog entry>
```

Selecting **Install Protocols** opens the remote protocol catalog.

Catalog entries may originate from:

- CID / content-addressed publication;
- GitHub publication.

Each entry exposes its source/reference and download link.

The download action writes the package into:

`Node Core/Protocols/`

The local package then becomes the source for verification and installation.

Installed protocols are represented under:

`Node Core/Protocols/Installed/`

## Installation boundary

`Remote Catalog → Source Resolver → Download → Local Protocol Package → Verification → Protocol Interface Installation`

The catalog does not install a protocol. The downloader does not activate a protocol. Protocol Interface remains the authority for installation and lifecycle.

## State distinction

`REMOTE CATALOG ENTRY ≠ DOWNLOADED PACKAGE ≠ INSTALLED ≠ ACTIVE ≠ RUNNING`

## Isolation

Node Core hosts and manages protocols but does not become the protocol.

CPG-specific consensus, ledger, poker rules, table state, Table Wallet, settlement and rake remain outside Node Core.

Protocol engines remain independently versioned and are not global Node Core versions.
