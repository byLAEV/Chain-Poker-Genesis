#!/usr/bin/env python3
"""Executable Node Core network manager."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .peer_registry import Peer, PeerRegistry
from .transport import TCPReferenceTransport

@dataclass(frozen=True)
class NetworkState:
    status: str
    peer_count: int
    connected_peers: int

class NetworkManager:
    def __init__(self, node_id: str, transport: TCPReferenceTransport | None = None) -> None:
        if not node_id:
            raise ValueError("node_id is required")
        self.node_id = node_id
        self.registry = PeerRegistry()
        self.transport = transport or TCPReferenceTransport()

    def discover_peers(self) -> tuple[Peer, ...]:
        return self.registry.all()

    def register_peer(self, peer_id: str, host: str, port: int) -> Peer:
        peer = Peer(peer_id, host, port)
        self.registry.register(peer)
        return peer

    def connect_peer(self, peer_id: str) -> Peer:
        peer = self.registry.get(peer_id)
        if peer is None:
            raise KeyError(peer_id)
        self.registry.update_state(peer_id, "CONNECTING")
        self.registry.update_state(peer_id, "CONNECTED")
        return self.registry.get(peer_id)

    def disconnect_peer(self, peer_id: str) -> Peer:
        return self.registry.update_state(peer_id, "DISCONNECTED")

    def send_message(self, peer_id: str, message: dict[str, Any]) -> dict[str, Any]:
        peer = self.registry.get(peer_id)
        if peer is None:
            raise KeyError(peer_id)
        if peer.state != "CONNECTED":
            raise ConnectionError("peer is not connected")
        envelope = {"type": "NODE_CORE_MESSAGE", "sender": self.node_id, "recipient": peer.peer_id, "payload": message}
        return self.transport.send(peer.host, peer.port, envelope)

    def propagate(self, message: dict[str, Any]) -> dict[str, str]:
        results: dict[str, str] = {}
        for peer in self.registry.connected():
            try:
                self.send_message(peer.peer_id, message)
                results[peer.peer_id] = "SENT"
            except Exception:
                results[peer.peer_id] = "FAILED"
        return results

    def get_network_state(self) -> NetworkState:
        peers = self.registry.all()
        connected = sum(p.state == "CONNECTED" for p in peers)
        return NetworkState("READY" if peers and connected else "IDLE", len(peers), connected)
