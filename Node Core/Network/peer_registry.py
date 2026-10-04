#!/usr/bin/env python3
"""Protocol-neutral peer registry for Node Core."""

from __future__ import annotations

from dataclasses import dataclass

PEER_STATES = {"DISCOVERED", "CONNECTING", "CONNECTED", "DISCONNECTED", "FAILED"}

@dataclass(frozen=True)
class Peer:
    peer_id: str
    host: str
    port: int
    state: str = "DISCOVERED"

class PeerRegistry:
    def __init__(self) -> None:
        self._peers: dict[str, Peer] = {}

    def register(self, peer: Peer) -> None:
        if not peer.peer_id:
            raise ValueError("peer_id is required")
        if peer.state not in PEER_STATES:
            raise ValueError("invalid peer state")
        if not 1 <= peer.port <= 65535:
            raise ValueError("invalid peer port")
        if peer.peer_id in self._peers:
            raise ValueError("peer already registered")
        self._peers[peer.peer_id] = peer

    def update_state(self, peer_id: str, state: str) -> Peer:
        if peer_id not in self._peers:
            raise KeyError(peer_id)
        if state not in PEER_STATES:
            raise ValueError("invalid peer state")
        old = self._peers[peer_id]
        new = Peer(old.peer_id, old.host, old.port, state)
        self._peers[peer_id] = new
        return new

    def get(self, peer_id: str) -> Peer | None:
        return self._peers.get(peer_id)

    def all(self) -> tuple[Peer, ...]:
        return tuple(sorted(self._peers.values(), key=lambda p: p.peer_id))

    def connected(self) -> tuple[Peer, ...]:
        return tuple(p for p in self.all() if p.state == "CONNECTED")
