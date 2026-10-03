#!/usr/bin/env python3
"""Deterministic tests for the Node Core Network reference boundary."""

from __future__ import annotations

import importlib.util
import pathlib
import socket
import threading

ROOT = pathlib.Path(__file__).resolve().parents[1]
NETWORK = ROOT / "Network"

def load(name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module

peer_registry = load("node_core_peer_registry", NETWORK / "peer_registry.py")
transport = load("node_core_transport", NETWORK / "transport.py")

def test_peer_registry() -> None:
    registry = peer_registry.PeerRegistry()
    registry.register(peer_registry.Peer("peer-b", "127.0.0.1", 10002))
    registry.register(peer_registry.Peer("peer-a", "127.0.0.1", 10001))
    assert [p.peer_id for p in registry.all()] == ["peer-a", "peer-b"]
    assert registry.update_state("peer-a", "CONNECTED").state == "CONNECTED"

def test_frame_roundtrip() -> None:
    left, right = socket.socketpair()
    try:
        message = {"payload": {"state": "READY"}, "sender": "node-a"}
        left.sendall(transport.encode_frame(message))
        assert transport.decode_frame(right) == message
    finally:
        left.close()
        right.close()

def test_tcp_reference_transport() -> None:
    receiver = transport.TCPReferenceTransport()
    host, port = receiver.listen()
    received: list[dict] = []

    def accept() -> None:
        message = receiver.accept_once(lambda m: {"type": "NODE_CORE_HELLO_ACK"} if m["type"] == "NODE_CORE_HELLO" else None)
        received.append(message)

    thread = threading.Thread(target=accept)
    thread.start()

    with socket.create_connection((host, port), timeout=2) as sock:
        sock.sendall(transport.encode_frame({"type": "NODE_CORE_HELLO", "sender": "node-a"}))
        assert transport.decode_frame(sock) == {"type": "NODE_CORE_HELLO_ACK"}

    thread.join(timeout=2)
    assert received == [{"type": "NODE_CORE_HELLO", "sender": "node-a"}]
    receiver.close()
