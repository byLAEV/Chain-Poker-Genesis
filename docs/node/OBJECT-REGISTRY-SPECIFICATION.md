# Node Core Object Registry Specification

Project: Chain Poker Genesis by LAEV
Layer: Node Core
Version: 0.1.0
Status: Implementation baseline
Protocol installation: Explicitly excluded

## Purpose

The Object Registry is the authoritative Node Core index of managed storage objects. It records identity, class, location, version, hash, and storage status without replacing the object payload.

## Required fields

- object_id
- object_class
- relative_path
- content_hash
- storage_version
- provider_type
- location_state
- object_state
- synchronization_state

## Separation

The registry is not the CPG Dedicated Ledger, a blockchain, consensus, backup, or network propagation log.

## Invariants

An object has exactly one canonical logical identity in the Node Core registry. Registry entries are invalid when their paths escape Node Core storage, their class is incompatible with their location, their hash is malformed, provider state is contradictory, or object and synchronization state are conflated.

## Protocol boundary

Node Core 0.1.0 must not create CPG objects.