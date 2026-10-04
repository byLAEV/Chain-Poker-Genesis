# Node Core Identity

**Status:** IMPLEMENTED_PARTIAL / RECONCILED
**Version:** 1.2.0

Node Core Identity provides the protocol-neutral cryptographic identity boundary for a node.

## Canonical identity lifecycle

`UNINITIALIZED → GENERATED_OR_IMPORTED → VALIDATED → REGISTERED → ACTIVE`

Identity activation requires Node Core readiness. Failure or revocation must prevent activation.

Node Identity lifecycle is distinct from the **Node Life** lifecycle. Node Life records the operational life of a node and its hash-linked lifecycle events; it does not replace the canonical Identity lifecycle.

## Implemented boundary

- Ed25519 Node Identity generation;
- deterministic Node ID derivation from canonical public identity material;
- identity validation and canonical record validation;
- explicit registration state;
- explicit activation gate requiring Node Core readiness;
- external credential verification;
- hash-linked Node Life events and reconstruction;
- identity binding and verification-result models;
- recovery continuity decision boundary.

Private keys are returned to the caller/provider and are not persisted in the Node Identity record or snapshot. Production signing should use an external secure key provider.

This module does not define CPG player identity, table membership, CPG ledger, CPG consensus, poker state, Table Wallet, settlement or rake.

The implementation remains **PARTIAL** because full registration/trust authority, revocation authority, durable secure identity storage and complete Node Core lifecycle integration are not yet closed.
