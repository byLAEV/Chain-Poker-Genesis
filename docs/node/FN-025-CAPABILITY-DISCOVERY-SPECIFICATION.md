# FN-025 Capability Discovery — Minimum Node Core Specification

**Project:** Chain Poker Genesis by LAEV  
**Layer:** Full Node Core  
**Source:** Red de Nodos by LAEV V1.8  
**Status:** Architectural Definition

## Purpose
FN-025 provides protocol-neutral capability description for an Identity Node. It answers what the node can support without installing, inferring, or activating Chain Poker Genesis.

## Canonical model
Identity Node → Capability Set → Capability Evidence

## Rules
1. A capability belongs to an existing Identity Node.
2. Capability discovery must be deterministic for the same node state.
3. Capability identifiers are explicit strings; no implicit capability is inferred from a protocol name.
4. A base Identity Node may advertise infrastructure capabilities without CPG association.
5. Capability discovery must not install or activate a protocol.
6. Player Identity Node semantics are outside FN-025.
7. Channel Node, poker-table, consensus, wallet, Lightning and settlement semantics are outside FN-025.
8. FN-025 describes capability; it does not prove that the capability was successfully executed. Proof of Functions remains FN-027.

## Minimum capability classes
The initial vocabulary is intentionally small:
- identity.node
- network.peer
- network.transport
- network.endpoint
- storage.local
- storage.distributed

## Evidence
Capability evidence is a deterministic representation of node identity, node instance, capability identifiers, and capability schema version. The evidence is descriptive, not a PoF result and not a consensus artifact.

## Boundary
FN-024 → Identity / Peer substrate → FN-025 → Capability description → FN-026 → Propagation / peer evidence → FN-027 → Proof of Functions → CPG protocol

FN-025 does not create Player Identity Nodes. A Player Identity Node may later be represented as an Identity Node with an explicitly installed/associated CPG capability and player role.