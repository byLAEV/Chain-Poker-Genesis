# Node Core — Identity

Status: IMPLEMENTED / PARTIAL
Version: 1.0.0

Identity is a protocol-neutral Node Core service. It establishes the cryptographic identity and lifecycle of a node; it does not define CPG player identity, table membership, settlement, rake, or the CPG ledger.

## Implemented reference boundary

- Ed25519 Node Identity generation.
- Deterministic Node ID derivation from canonical public identity material.
- Node Life creation.
- Append-only lifecycle event chain with integrity hashes.
- Identity validation.
- Offline lifecycle reconstruction.
- Canonical identity schema.
- Identity Manager import boundary.
- Reference tests, including tamper detection.

## Not yet implemented

- External credential adapters.
- Identity binding / United Identity.
- Protocol-controlled identity requests.
- Production ZK proof systems.
- Persistent identity storage and Kubo/IPFS integration.
- Network identity propagation.
- Recovery integration.
- Production security audit.

## Security boundary

Private keys are not part of the canonical Node Identity record and are not serialized by the reference implementation. Key custody remains outside the identity record.

The reference Node ID profile is explicit and deterministic:
sha256-canonical-public-identity-v1

This is a Node Core reference implementation of the defined cryptographic profile. It does not create CPG-specific identity semantics.

## Verification

Run:
python3 "Node Core/Tests/Identity/test_identity_core.py"
