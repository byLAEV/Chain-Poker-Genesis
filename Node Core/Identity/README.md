# Node Core Identity

**Status:** IMPLEMENTED
**Version:** 1.1.0

Node Core Identity provides the protocol-neutral cryptographic identity boundary for a node.

Implemented: Ed25519 node identity generation; deterministic Node ID derivation; Node Life lifecycle and hash-linked events; identity validation and reconstruction; external credential verification; Ed25519 signature verification; offline snapshot; Identity API.

Private keys are not persisted by the identity registry or snapshot. Production signing should use an external secure key provider.

Lifecycle:
UNINITIALIZED → CREATED → INITIALIZED → ACTIVE
ACTIVE → SUSPENDED / TERMINATED
SUSPENDED → ACTIVE / TERMINATED
TERMINATED → RECOVERED → ACTIVE / TERMINATED

This module does not define CPG player identity, table membership, CPG ledger, CPG consensus, or poker state.
