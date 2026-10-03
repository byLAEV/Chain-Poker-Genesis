#!/usr/bin/env python3
"""Deterministic tests for the Node Core Network reference boundary."""

from __future__ import annotations

import socket
import threading

from Node_Core.Network.peer_registry import Peer, PeerRegistry
from Node_Core.Network.transport import TCPReferenceTransport, decode_frame, encode_frame

def test_peer_registry() -> None:
    registry = PeerRegistry()
    registry.register(Peer("peer-b", "127.0.0.1", 10002))
    registry.register(Peer("peer-a", "127.0.0.1", 10001))
    assert [p.peer_id for p in registry.all()] == ["peer-a", "peer-b"]
    assert registry.update_state("peer-a", "CONNECTED").state == "CONNECTED"

def test_frame_roundtrip() -> None:
    left, right = socket.socketpair()
    try:
        message = {"payload": {"state": "READY"}, "sender": "node-a"}
        left.sendall(encode_frame(message))
        assert decode_frame(right) == message
    finally:
        left.close()
        right.close()

def test_tcp_reference_transport() -> None:
    receiver = TCPReferenceTransport()
    host, port = receiver.listen()
    received: list[dict] = []

    def accept() -> None:
        received.append(receiver.accept_once())

    thread = threading.Thread(target=accept)
    thread.start()
    sender = TCPReferenceTransport()
    response = sender.send(host, port, {"type": "ACK", "ok": True})
    thread.join(timeout=2)

    assert response == {"type": "ACK", "ok": True}
    assert received == [{"type": "ACK", "ok": True}]
    receiver.close()
