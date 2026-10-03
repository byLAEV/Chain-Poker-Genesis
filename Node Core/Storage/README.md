# Node Core — Storage

**Status:** IMPLEMENTED  
**Version:** 1.0.0

Storage is the protocol-neutral persistence substrate of Node Core. It is independent from the CPG ledger and must not write protocol-reserved storage.

## Architecture

```text
Node Core Storage
│
├── Local Node Storage
│   ├── temporary
│   ├── public
│   ├── private
│   ├── restricted
│   ├── personal
│   └── state / recovery
│
├── Object Registry
│
└── Kubo / IPFS mirror
    ├── Public
    ├── Private
    ├── Restricted
    └── Encrypted
```

The local store is the authoritative write boundary. When Kubo is configured and an object has a valid CID, Kubo is the preferred read source. Any Kubo read failure or integrity mismatch falls back to the local copy.

## Implemented

- Canonical storage layout.
- Atomic local writes.
- Object registry metadata.
- SHA-256 content integrity.
- Local storage classes.
- Kubo/IPFS HTTP reference adapter.
- Local → Kubo mirror.
- Kubo-preferred reads.
- Local fallback on Kubo failure.
- Synchronization-state metadata.
- Path traversal protection.
- Protocol-reserved write protection.
- Private/restricted distribution encryption boundary.
- Storage status reporting.
- Executable reference tests.

## Security boundary

Node Core Storage never owns private encryption keys. For private or restricted objects, plaintext may remain local when distribution is disabled. If distribution is requested, the caller must provide encrypted bytes and explicitly mark the operation as encrypted.

## Verification

Run:

`python3 "Node Core/Tests/Storage/test_storage_engine.py"`

A live Kubo node is environment-dependent; absence of Kubo does not invalidate the local storage implementation because the defined local fallback remains operational.
