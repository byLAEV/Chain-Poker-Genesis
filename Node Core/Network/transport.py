#!/usr/bin/env python3
"""Reference TCP transport for the Node Core Network boundary."""

from __future__ import annotations

import json
import socket
import struct
from typing import Any

MAX_FRAME_SIZE = 1_048_576

def encode_frame(message: dict[str, Any]) -> bytes:
    payload = json.dumps(message, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    if len(payload) > MAX_FRAME_SIZE:
        raise ValueError("message exceeds MAX_FRAME_SIZE")
    return struct.pack("!I", len(payload)) + payload

def _read_exact(sock: socket.socket, size: int) -> bytes:
    chunks: list[bytes] = []
    remaining = size
    while remaining:
        chunk = sock.recv(remaining)
        if not chunk:
            raise ConnectionError("peer closed connection")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)

def decode_frame(sock: socket.socket) -> dict[str, Any]:
    header = _read_exact(sock, 4)
    size = struct.unpack("!I", header)[0]
    if size > MAX_FRAME_SIZE:
        raise ValueError("frame exceeds MAX_FRAME_SIZE")
    message = json.loads(_read_exact(sock, size).decode("utf-8"))
    if not isinstance(message, dict):
        raise ValueError("network message must be an object")
    return message

class TCPReferenceTransport:
    def __init__(self, host: str = "127.0.0.1", port: int = 0) -> None:
        self.host = host
        self.port = port
        self._server: socket.socket | None = None

    def listen(self) -> tuple[str, int]:
        if self._server is not None:
            return self.host, self.port
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(8)
        self._server = server
        self.host, self.port = server.getsockname()
        return self.host, self.port

    def accept_once(self) -> dict[str, Any]:
        if self._server is None:
            raise RuntimeError("transport is not listening")
        conn, _ = self._server.accept()
        with conn:
            return decode_frame(conn)

    def send(self, host: str, port: int, message: dict[str, Any], timeout: float = 2.0) -> dict[str, Any]:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            sock.sendall(encode_frame(message))
            return decode_frame(sock)

    def close(self) -> None:
        if self._server is not None:
            self._server.close()
            self._server = None
