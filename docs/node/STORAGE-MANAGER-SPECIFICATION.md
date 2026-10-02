# Node Core Storage Manager Specification

**Project:** Chain Poker Genesis by LAEV
**Layer:** Node Core
**Version:** 0.1.0
**Protocol installation:** Explicitly excluded

## Purpose

The Storage Manager is the protocol-neutral storage abstraction of Node Core.

It provides object classification, canonical location, local persistence, deterministic hashing, integrity verification, and a provider boundary.

It does not implement CPG ledger semantics, poker state, settlement, consensus, or protocol networking.

## Object classes

- identity
- cryptography
- configuration
- state
- record
- recovery
- protocol-reserved

The protocol-reserved class is intentionally non-writable during Node Core installation.

## Object contract

Each managed object has:

- object_id
- object_class
- relative_path
- content_hash
- content_encoding
- storage_version

The baseline uses SHA-256 for byte-level integrity metadata.

## Safety

The Storage Manager rejects absolute paths, path traversal, invalid object identifiers, and writes to the protocol-reserved namespace.

## Provider boundary

Local storage is the baseline provider. External providers such as IPFS/Kubo are adapters and are not silently installed.

## Acceptance

The implementation must create, retrieve, hash, verify, and safely locate Node Core objects while leaving protocol-reserved storage untouched.
