#!/usr/bin/env python3
"""Protocol-neutral Identity Node networking substrate derived from Red de Nodos V1.8."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum


class PeerState(str, Enum):
    DISCOVERED = "DISCOVERED"
    CONNECTING = "CONNECTING"
    CONNECTED = "CONNECTED"
    DEGRADED = "DEGRADED"
    DISCONNECTED = "DISCONNECTED"


@dataclass(frozen=True)
class IdentityNode:
    node_id: str
    public_identity_reference: str
    node_instance_id: str
    protocol_association: str = "NONE"

    def __post_init__(self) -> None:
        if not self.node_id or not self.public_identity_reference:
            raise ValueError("identity node requires node_id and public identity reference")
        if not self.node_instance_id:
            raise ValueError("node instance identifier is required")
        if self.protocol_association != "NONE":
            raise ValueError("base Identity Node must remain protocol-neutral")


@dataclass
class PeerRelationship:
    peer_node_id: str
    endpoint: str
    state: PeerState = PeerState.DISCOVERED

    def snapshot(self) -> dict[str, str]:
        return {
            "peer_node_id": self.peer_node_id,
            "endpoint": self.endpoint,
            "state": self.state.value,
        }


class IdentityNodeNetwork:
    """Minimal peer-network registry; transport execution is intentionally separate."""

    def __init__(self, local_identity: IdentityNode) -> None:
        self.local_identity = local_identity
        self._peers: dict[str, PeerRelationship] = {}

    def register_peer(self, peer_node_id: str, endpoint: str) -> PeerRelationship:
        if not peer_node_id or not endpoint:
            raise ValueError("peer registration requires peer_node_id and endpoint")
        if peer_node_id == self.local_identity.node_id:
            raise ValueError("local identity cannot be registered as its own peer")
        relationship = PeerRelationship(peer_node_id=peer_node_id, endpoint=endpoint)
        self._peers[peer_node_id] = relationship
        return relationship

    def set_peer_state(self, peer_node_id: str, state: PeerState) -> None:
        if peer_node_id not in self._peers:
            raise KeyError(peer_node_id)
        self._peers[peer_node_id].state = state

    def get_peer(self, peer_node_id: str) -> PeerRelationship:
        return self._peers[peer_node_id]

    def snapshot(self) -> dict[str, object]:
        return {
            "local_identity": asdict(self.local_identity),
            "peer_count": len(self._peers),
            "peers": [
                self._peers[node_id].snapshot()
                for node_id in sorted(self._peers)
            ],
        }
