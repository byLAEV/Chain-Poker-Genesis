# Node Core Storage

**Status:** IMPLEMENTED
**Version:** 1.1.0
**Scope:** Protocol-neutral persistence substrate for Node Core.

Node Core Storage provides local persistence, optional decentralized mirroring through Kubo/IPFS, integrity verification, synchronization state management, fallback reads, and recovery from a verified distributed copy.

## Architecture

- Storage Manager — single orchestration boundary.
- Storage Policy — class and distribution rules.
- Object Registry — canonical object metadata and location state.
- Providers — provider contract and provider registry.
- Local — authoritative local persistence.
- Kubo-IPFS — optional decentralized mirror.
- Synchronization — explicit synchronization state machine.
- Integrity — content hash verification.
- Disaster Recovery — verified distributed-to-local restoration.
- API — programmatic boundary delegating to Storage Manager.

## Storage classes

temporary, public, private, restricted, personal.

protocol-reserved is explicitly outside the Node Core write boundary.

Private and restricted objects may be mirrored only when the caller supplies encrypted bytes. Node Core Storage does not own encryption keys.

## Read and recovery model

1. Local persistence is the authoritative write boundary.
2. When a valid CID exists, Kubo/IPFS is the preferred read source.
3. Distributed content is hash-verified against the registry.
4. Kubo failure or invalid distributed content falls back to local storage.
5. If the local copy is missing, Disaster Recovery restores it from Kubo only after hash verification.
6. The recovery result is written back to the canonical registry.

## Verification

Run:
python3 "Node Core/Tests/Storage/test_storage_complete.py"

The live Kubo path remains environment-dependent.

## Protocol isolation

This subsystem does not implement or store CPG ledger, CPG consensus, poker table state, settlement, rake, or poker rules. Those belong to protocol layers above Node Core Storage.
