# Node Core Manifest Authority Contract

**Status:** CANONICAL
**Version:** 1.0.0
**Scope:** Authority, hierarchy and conflict rules for Node Core manifests

## 1. Authority hierarchy

There are two distinct canonical manifest classes:

1. **Node Core Component Manifest** — `Node Core/NODE-CORE-MANIFEST.json`
   - identifies the Node Core component, version, scope, component implementation status and protocol-isolation boundary.
2. **Node Core Installation Manifest** — generated `node-installation-manifest.json`
   - records the state of a specific installed Node Core instance.

They MUST NOT be treated as competing manifests.

## 2. Normative authority

The canonical contracts indexed by `NODE-CORE-CANONICAL-CONTRACT-INDEX.md` define normative behavior.

`NODE-CORE-MANIFEST.json` declares repository/component identity and implementation-status metadata.

The installation manifest declares instance state and MUST conform to its canonical installation schema.

README files are descriptive/supporting unless explicitly classified otherwise.

Executable code is authoritative only as implementation evidence and MUST conform to canonical contracts.

## 3. Schema authority

The canonical Node Core installation manifest schema is:

`Node Core/Configuration/Schemas/node-core-installation-manifest.schema.json`

The similarly named `node-installation-manifest.schema.json` is a legacy/supporting schema and MUST NOT define a second conflicting installation-manifest authority.

## 4. Conflict detection

A validation pass MUST detect:

- duplicate canonical manifest schemas;
- conflicting required fields;
- conflicting lifecycle constants;
- conflicting protocol-isolation claims;
- version/status contradictions;
- README claims unsupported by canonical manifests;
- implementation output that violates the canonical schema.

A conflict is a validation failure, not an invitation for the implementation to choose arbitrarily.

## 5. Version authority

Node Core component version is declared by `NODE-CORE-MANIFEST.json`.

Installation manifest version identifies the installation-manifest format and MUST be validated against its schema.

Protocol engine versions remain independently governed by Protocol Interface.

A protocol engine update MUST NOT silently modify the Node Core component version.

## 6. Canonicalization

Canonical manifest serialization MUST be deterministic:

- UTF-8;
- JSON object keys sorted for hashing/canonical comparison;
- stable separators;
- no implementation-specific transient fields in canonical declarations.

## 7. Instance state boundary

The installation manifest is generated from the actual installed state. It MUST NOT be used to redefine the Node Core architecture or contract.

A component manifest status MUST reflect the reconciled implementation status recorded by the canonical contract index. A component MUST NOT be declared fully IMPLEMENTED when its canonical implementation mapping remains partial.

In particular:

`cpg_protocol.status = NOT_INSTALLED`

and:

`protocol_associations = []`

for a fresh protocol-neutral Node Core installation.

## 8. Phase gate

Manifest authority is closed only when:

- one component manifest authority is identified;
- one installation manifest schema is authoritative;
- legacy duplicate schema is classified;
- validation detects conflicts;
- implementation and tests map to the authority;
- version rules are explicit;
- component implementation-status declarations match the canonical reconciliation state.

## 9. Phase 2 relationship

This contract establishes authority for the subsequent:

`MANIFEST ↔ README ↔ CODE`

reconciliation.

It does not perform that reconciliation itself.
