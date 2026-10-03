# Node Core Storage Provider Interface

Project: Chain Poker Genesis by LAEV
Layer: Node Core
Version: 0.1.0
Status: Implementation baseline
Protocol installation: Explicitly excluded

## Purpose

The Storage Provider Interface separates the Node Core Storage Manager from any specific storage backend.

The Storage Manager defines the logical object contract. A provider implements that contract for a particular storage domain.

## Provider roles

- LOCAL — directly controlled Node Core storage.
- DECENTRALIZED — reserved interface for a future decentralized provider.
- EXTERNAL — reserved interface for future external storage providers.

Only LOCAL is implemented by the current reference baseline.

## Required provider operations

- put
- get
- exists
- delete
- verify
- describe
- status

Implementations must return deterministic metadata for the same stored object.

## Provider independence

The Node Core must not assume that a provider is a protocol.

A provider does not define poker state, protocol consensus, CPG ledger semantics, CPG participation, or CPG installation.

## External provider boundary

An external or decentralized provider remains NOT_PROVISIONED until a dedicated provider implementation is explicitly installed and verified.

The Node Core reference implementation therefore operates correctly with only the local provider.

## Acceptance

A compliant provider implementation must:

1. satisfy the logical storage object contract;
2. preserve object identifiers;
3. return verifiable content hashes;
4. expose explicit availability state;
5. fail closed when the provider cannot verify an object.