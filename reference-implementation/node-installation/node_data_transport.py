#!/usr/bin/env python3
"""Protocol-neutral FN-024A node data networking / transport substrate."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256


class TransportState(str, Enum):
    UNAVAILABLE = "UNAVAILABLE"
    CONNECTING = "CONNECTING"
    CONNECTED = "CONNECTED"
    DEGRADED = "DEGRADED"
    DISCONNECTED = "DISCONNECTED"


@dataclass(frozen=True)
class NetworkEndpoint:
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("endpoint value is required")


@dataclass(frozen=True)
class TransportMessage:
    source_node_id: str
    destination_node_id: str
    payload_hash: str
    payload: bytes


@dataclass
class TransportSession:
    local_node_id: str
    remote_node_id: str
    endpoint: NetworkEndpoint
    state: TransportState = TransportState.UNAVAILABLE
    latency_ms: float | None = None
    capacity_bps: int | None = None

    def snapshot(self) -> dict[str, object]:
        return {
            "local_node_id": self.local_node_id,
            "remote_node_id": self.remote_node_id,
            "endpoint": self.endpoint.value,
            "state": self.state.value,
            "latency_ms": self.latency_ms,
            "capacity_bps": self.capacity_bps,
        }


class NodeDataTransport:
    """Minimal deterministic transport boundary; concrete sockets are intentionally separate."""

    def __init__(self, local_node_id: str) -> None:
        if not local_node_id:
            raise ValueError("local node identity is required")
        self.local_node_id = local_node_id
        self._sessions: dict[str, TransportSession] = {}
        self._inbox: list[TransportMessage] = []

    def open_session(self, remote_node_id: str, endpoint: str) -> TransportSession:
        if not remote_node_id or not endpoint:
            raise ValueError("remote node identity and endpoint are required")
        if remote_node_id == self.local_node_id:
            raise ValueError("local identity cannot be its own transport peer")
        session = TransportSession(
            local_node_id=self.local_node_id,
            remote_node_id=remote_node_id,
            endpoint=NetworkEndpoint(endpoint),
            state=TransportState.CONNECTING,
        )
        self._sessions[remote_node_id] = session
        return session

    def set_state(self, remote_node_id: str, state: TransportState) -> None:
        self._session(remote_node_id).state = state

    def set_network_conditions(
        self, remote_node_id: str, *, latency_ms: float | None, capacity_bps: int | None
    ) -> None:
        if latency_ms is not None and latency_ms < 0:
            raise ValueError("latency_ms cannot be negative")
        if capacity_bps is not None and capacity_bps < 0:
            raise ValueError("capacity_bps cannot be negative")
        session = self._session(remote_node_id)
        session.latency_ms = latency_ms
        session.capacity_bps = capacity_bps

    def send(self, remote_node_id: str, payload: bytes) -> TransportMessage:
        session = self._session(remote_node_id)
        if session.state not in {TransportState.CONNECTED, TransportState.DEGRADED}:
            raise ConnectionError("transport session is not available for data exchange")
        if not isinstance(payload, bytes):
            raise TypeError("payload must be bytes")
        message = TransportMessage(
            source_node_id=self.local_node_id,
            destination_node_id=remote_node_id,
            payload_hash=sha256(payload).hexdigest(),
            payload=payload,
        )
        self._inbox.append(message)
        return message

    def receive_all(self) -> tuple[TransportMessage, ...]:
        messages = tuple(self._inbox)
        self._inbox.clear()
        return messages

    def snapshot(self) -> dict[str, object]:
        return {
            "local_node_id": self.local_node_id,
            "sessions": [self._sessions[node_id].snapshot() for node_id in sorted(self._sessions)],
            "inbox_size": len(self._inbox),
        }

    def _session(self, remote_node_id: str) -> TransportSession:
        try:
            return self._sessions[remote_node_id]
        except KeyError as exc:
            raise KeyError(remote_node_id) from exc

