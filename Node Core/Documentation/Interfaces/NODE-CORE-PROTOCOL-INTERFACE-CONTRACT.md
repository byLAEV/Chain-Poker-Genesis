# Node Core Protocol Interface Contract

**Status:** CANONICAL  
**Version:** 1.1.0  
**Scope:** Minimal administrative boundary between protocol-neutral Node Core and independently installed protocols

## 1. Purpose

Protocol Interface is the single Node Core boundary through which an independently versioned protocol may be discovered, verified, compatibility-checked, registered, installed, associated with its required engines and transitioned through its lifecycle.

It also defines the minimal administrative interface used by Node Core to inspect installed protocols and available protocol installers.

It does not implement protocol semantics.

## 2. Canonical lifecycle

`DISCOVERED → COMPATIBLE → REGISTERED → INSTALLED → ACTIVE`

Alternative controlled states:

- SUSPENDED
- REMOVED

An implementation MUST reject invalid forward transitions.

**Important:** `INSTALLED`, `ACTIVE` and protocol execution state are distinct concepts. Installation alone MUST NOT imply activation or execution.

## 3. Required descriptor and protocol identity

Every protocol descriptor MUST identify:

- `protocol_id`;
- `version`;
- `engine_id`;
- `manifest_hash`.

Optional capabilities and metadata may be supplied.

The protocol identity belongs to the protocol descriptor/manifest. Node Core MUST NOT replace it with a CPG-specific identity or infer protocol identity from presentation text.

## 4. Protocol catalog and download boundary

**Install Protocol** is a protocol catalog, not a direct view of the local installer directory.

The catalog may contain protocol packages published through supported remote sources, including:

- CID / content-addressed sources;
- GitHub repositories or release/download sources.

Each catalog entry MUST expose the source type and a usable download/reference link.

The catalog flow is:

`Protocol Catalog → Source Link → Download → Node Core/Protocols/ → Local Protocol Package → Verification → Installation`

The user MUST be able to see where a protocol package will be obtained before downloading it.

A downloaded package is written into the local Node Core protocol directory:

```text
Node Core/
└── Protocols/
    └── <downloaded-protocol-package>/
```

The downloaded package is then the local source used by Protocol Interface for verification and protocol installation.

A remote catalog entry is **not** itself an installed protocol.

An unverified downloaded package MUST NOT be treated as an installed or active protocol.

## 5. Canonical protocol storage boundary

Node Core provides one local protocol area for downloaded protocol packages and installed protocol associations:

```text
Node Core/
└── Protocols/
    ├── <downloaded-protocol-package>/
    └── Installed/
        └── <protocol-id>/
```

The canonical semantic distinction is:

- remote CID/GitHub catalog = available protocol sources;
- `Protocols/<downloaded-protocol-package>/` = locally downloaded package awaiting or undergoing verification/installation;
- `Protocols/Installed/<protocol-id>/` = protocol installed into this Node Core instance.

The interface MUST NOT represent the remote catalog as if it were the local installer directory.

Installing a protocol MUST result in an installed protocol association represented under the Installed protocol boundary.

Node Core hosts and manages the protocol; the protocol remains a separately versioned protocol and is not part of the Node Core implementation itself.

## 6. Required operations

The reference interface provides:

- `discover(descriptor)`;
- `check_compatibility(protocol_id, node_capabilities)`;
- `register(protocol_id)`;
- `install(protocol_id)`;
- `activate(protocol_id)`;
- `suspend(protocol_id)`;
- `remove(protocol_id)`;
- `get(protocol_id)`;
- `all()`.

The administrative presentation boundary additionally requires the ability to represent:

- installed protocol listing;
- protocol detail/status view;
- available installer listing;
- installer verification/install action.

Presentation operations MUST delegate to the Protocol Interface and MUST NOT create a second protocol registry or lifecycle.

## 7. Compatibility gate

A protocol MUST NOT be treated as compatible unless its declared required capabilities are satisfied by the Node Core capability set.

Compatibility is a prerequisite for registration in the canonical lifecycle.

## 8. Engine association

Required protocol engines are associated with the protocol during installation.

The Protocol Interface MAY request engine registration/activation through Engine Runtime, but Engine Runtime remains the authority for engine lifecycle.

Protocol Interface MUST NOT create a second engine lifecycle or engine registry.

## 9. Installation and activation gates

Installation MUST require REGISTERED state and successful installer verification.

Activation MUST require INSTALLED state.

Node Core MUST NOT silently activate an uninstalled protocol.

Activation does not mean that protocol-specific work is being executed by Node Core itself.

## 10. Minimal administrative interface

The Protocol Interface presentation is intentionally minimal and functional.

### 10.1 Visual baseline

- background: white;
- primary text: black;
- secondary text: dark gray;
- tertiary/supporting text: light gray;
- no decorative background graphics;
- no visual treatment that implies protocol semantics;
- sober spacing and clear hierarchy.

Text size MUST follow information importance:

1. **Highest:** interface title and primary protocol identity;
2. **High:** protocol name, primary state and principal action;
3. **Medium:** version, identifier, engine association and verification information;
4. **Low:** paths, timestamps, secondary technical information and instructions.

The visual baseline is subordinate to accessibility and platform conventions; exact pixel sizes are implementation details, not protocol semantics.

### 10.2 Protocols layer

Selecting the Node Core **Protocols** menu MUST open a protocol layer/window containing:

1. **Installed Protocols**
2. **Install Protocol**

The Installed Protocols section MUST list the protocols currently associated with the Node Core instance.

A protocol entry SHOULD expose at minimum:

- protocol name/identifier;
- version;
- lifecycle state;
- protocol identity/manifest reference.

### 10.3 Install Protocol view

Selecting **Install Protocol** MUST open the protocol catalog.

The catalog MUST support remote protocol sources and MUST present, at minimum:

- protocol name/identifier;
- version when available;
- source type (CID or GitHub);
- source/download link;
- enough metadata to identify the package before download.

Selecting **Download** MUST write the selected protocol package into:

`Node Core/Protocols/`

The downloaded package then enters the local installation pipeline:

`Catalog → Download → Local Protocol Package → Verification → Protocol Identity → Required Engines → Compatibility → Installation → Installed Protocol Association`

The interface MUST distinguish:

- remote catalog entry;
- downloaded local package;
- installed protocol;
- active protocol.

The interface MUST NOT treat a remote link or a downloaded-but-unverified package as an installed protocol.

### 10.4 State presentation

The interface MUST preserve the distinction:

`AVAILABLE INSTALLER ≠ INSTALLED ≠ ACTIVE ≠ RUNNING`

If a state is not implemented by the current runtime, the interface MUST NOT fabricate it.

## 11. Protocol isolation

Protocol Interface MUST NOT define or implement:

- CPG consensus;
- CPG ledger;
- poker/NLHE rules;
- table state;
- Table Wallet;
- settlement;
- rake;
- protocol-specific cryptographic semantics.

For CPG specifically, these remain inside the separately installed Chain Poker Genesis protocol.

The interface may display protocol metadata supplied by CPG, but display MUST NOT make CPG logic part of Node Core authority.

## 12. Node Core completion boundary

Before any protocol is installed:

```text
protocol_associations = []
cpg_protocol = NOT_INSTALLED
synchronization = NOT_EVALUATED
```

The installation boundary may report `ARMED`; this means a verified separation point exists, not that CPG is installed.

## 13. Independent versioning

Protocol engine versions are independent of Node Core versions.

Updating Node Core MUST NOT imply an automatic update of installed protocol engines.

## 14. Verification

The canonical verification suite MUST verify:

1. descriptor validation;
2. discovery;
3. capability compatibility;
4. registration;
5. remote catalog source representation;
6. visible CID/GitHub download reference;
7. local download destination under `Node Core/Protocols/`;
8. installer/package recognition and validation;
9. installation;
7. installed-protocol association;
8. activation;
9. suspension;
10. removal;
11. invalid lifecycle transitions;
12. engine association boundary;
13. administrative listing semantics;
14. installer listing semantics;
15. protocol isolation;
16. distinction between installed and active states.

Reference implementation:

`Node Core/Protocol Interface/protocol_interface.py`

Reference manifest:

`Node Core/Protocol Interface/PROTOCOL-INTERFACE-MANIFEST.json`
