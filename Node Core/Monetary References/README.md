# Node Core — Monetary References

This directory defines the Node Core reference layer for external monetary and financial systems that may be used by installed protocols.

## Architectural role

Node Core does **not** perform monetary settlement.

Node Core maintains a protocol-neutral reference layer so installed engines and protocols can discover compatible external monetary systems without embedding a separate copy of each external system inside every settlement engine.

The intended relationship is:

```text
NODE CORE
  │
  └── Monetary References
       ├── Bitcoin
       ├── Ethereum
       ├── Traditional Banking
       └── Other supported systems
              │
              ↓
       Monetary Settlement Engine
              │
              ↓
          Protocol
```

## Responsibilities

The Monetary References layer may provide:

- canonical external-system identifiers;
- upstream repository/provider references;
- resolved versions or commits;
- capability metadata;
- compatibility metadata;
- update provenance;
- references that settlement engines can consume.

It does **not**:

- execute monetary settlement;
- authorize protocol payments;
- custody protocol funds;
- replace the Monetary Settlement Engine;
- create protocol-specific monetary rules;
- make an external system a Node Core implementation.

## Versioning principle

External monetary systems evolve independently from settlement-engine versions.

A change to Bitcoin, Ethereum, or a banking provider MUST NOT by itself require a new Monetary Settlement Engine version.

The settlement engine is versioned when its own execution contract, adapter contract, or settlement semantics change.

External reference updates remain separately identifiable and auditable.

## Update boundary

References are updateable independently from settlement engines, but an update MUST preserve provenance and compatibility information.

The Node Core reference layer MUST NOT silently replace a resolved external dependency during a protocol execution.

An update becomes available to protocols only through the applicable reference/compatibility boundary.

## Current baseline

The initial registry establishes:

- Bitcoin as a blockchain monetary reference;
- Ethereum as a blockchain monetary reference;
- Traditional Banking as a provider/interface reference category.

The registry is protocol-neutral. A protocol may select only a reference for which its settlement implementation declares compatibility.
