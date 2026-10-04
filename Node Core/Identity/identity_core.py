#!/usr/bin/env python3
"""Protocol-neutral Node Core Identity reference implementation."""
from __future__ import annotations
import hashlib
import json
import secrets
import time
from dataclasses import asdict, dataclass, field, replace
from typing import Any, Iterable

try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
except ImportError as exc:  # pragma: no cover
    Ed25519PrivateKey = None
    Ed25519PublicKey = None
    _CRYPTO_ERROR = exc
else:
    _CRYPTO_ERROR = None

IDENTITY_VERSION = "1.0"
NODE_ID_PROFILE = "sha256-canonical-public-identity-v1"
IDENTITY_STATES = ("UNINITIALIZED", "GENERATED_OR_IMPORTED", "VALIDATED", "REGISTERED", "ACTIVE")
LIFECYCLE_STATES = ("UNINITIALIZED", "CREATED", "INITIALIZED", "ACTIVE", "SUSPENDED", "TERMINATED", "RECOVERED")


def canonicalize(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def _require_crypto() -> None:
    if Ed25519PrivateKey is None or Ed25519PublicKey is None:
        raise RuntimeError("approved Ed25519 cryptographic backend unavailable") from _CRYPTO_ERROR


def _timestamp() -> int:
    return int(time.time())


def _node_id(identity_version: str, algorithm: str, public_key_hex: str) -> str:
    payload = {
        "identity_version": identity_version,
        "public_key_algorithm": algorithm,
        "public_key": public_key_hex,
    }
    return hashlib.sha256(canonicalize(payload)).hexdigest()


@dataclass(frozen=True)
class NodeIdentity:
    identity_version: str
    node_id: str
    public_key_algorithm: str
    public_key: str
    creation_timestamp: int
    status: str = "GENERATED_OR_IMPORTED"
    registration_reference: str | None = None
    verification_reference: str | None = None

    def canonical_record(self) -> dict[str, Any]:
        return asdict(self)

    def validate(self) -> bool:
        if self.identity_version != IDENTITY_VERSION or self.public_key_algorithm != "Ed25519":
            return False
        if self.status not in IDENTITY_STATES:
            return False
        try:
            public_key = bytes.fromhex(self.public_key)
        except ValueError:
            return False
        if len(public_key) != 32:
            return False
        return self.node_id == _node_id(self.identity_version, self.public_key_algorithm, self.public_key)


@dataclass(frozen=True)
class LifecycleEvent:
    sequence: int
    node_life_id: str
    node_id: str
    event: str
    state: str
    timestamp: int
    previous_event_hash: str | None
    event_hash: str

    @staticmethod
    def create(
        sequence: int,
        node_life_id: str,
        node_id: str,
        event: str,
        state: str,
        previous_event_hash: str | None,
        timestamp: int | None = None,
    ) -> "LifecycleEvent":
        ts = _timestamp() if timestamp is None else timestamp
        body = {
            "sequence": sequence,
            "node_life_id": node_life_id,
            "node_id": node_id,
            "event": event,
            "state": state,
            "timestamp": ts,
            "previous_event_hash": previous_event_hash,
        }
        return LifecycleEvent(**body, event_hash=hashlib.sha256(canonicalize(body)).hexdigest())

    def verify_integrity(self, expected_previous: str | None = None) -> bool:
        if self.previous_event_hash != expected_previous:
            return False
        body = {
            "sequence": self.sequence,
            "node_life_id": self.node_life_id,
            "node_id": self.node_id,
            "event": self.event,
            "state": self.state,
            "timestamp": self.timestamp,
            "previous_event_hash": self.previous_event_hash,
        }
        return self.event_hash == hashlib.sha256(canonicalize(body)).hexdigest()


@dataclass
class NodeLife:
    node_life_id: str
    node_id: str
    creation_event: LifecycleEvent
    state: str = "CREATED"
    state_history: list[LifecycleEvent] = field(default_factory=list)

    @staticmethod
    def create(node_id: str, timestamp: int | None = None) -> "NodeLife":
        life_id = secrets.token_hex(16)
        event = LifecycleEvent.create(0, life_id, node_id, "NODE_LIFE_CREATED", "CREATED", None, timestamp)
        return NodeLife(life_id, node_id, event, "CREATED", [event])

    def transition(self, event: str, state: str, timestamp: int | None = None) -> LifecycleEvent:
        if state not in LIFECYCLE_STATES or not _valid_transition(self.state, state):
            raise ValueError(f"invalid lifecycle transition: {self.state} -> {state}")
        previous = self.state_history[-1]
        next_event = LifecycleEvent.create(
            previous.sequence + 1,
            self.node_life_id,
            self.node_id,
            event,
            state,
            previous.event_hash,
            timestamp,
        )
        self.state = state
        self.state_history.append(next_event)
        return next_event

    def verify_history(self) -> bool:
        previous = None
        for event in self.state_history:
            if (
                event.node_life_id != self.node_life_id
                or event.node_id != self.node_id
                or not event.verify_integrity(previous)
            ):
                return False
            previous = event.event_hash
        return bool(self.state_history) and self.state_history[-1].state == self.state


def _valid_transition(current: str, target: str) -> bool:
    return target in {
        "UNINITIALIZED": {"CREATED"},
        "CREATED": {"INITIALIZED"},
        "INITIALIZED": {"ACTIVE"},
        "ACTIVE": {"SUSPENDED", "TERMINATED"},
        "SUSPENDED": {"ACTIVE", "TERMINATED"},
        "TERMINATED": {"RECOVERED"},
        "RECOVERED": {"ACTIVE", "TERMINATED"},
    }.get(current, set())


class IdentityManager:
    """Offline reference manager for the Node Core Identity boundary."""

    def __init__(self) -> None:
        self.identity: NodeIdentity | None = None
        self.node_life: NodeLife | None = None

    def create_identity(self, timestamp: int | None = None) -> tuple[NodeIdentity, bytes]:
        _require_crypto()
        private = Ed25519PrivateKey.generate()
        public = private.public_key()
        private_raw = private.private_bytes_raw()
        public_raw = public.public_bytes_raw()
        identity = NodeIdentity(
            IDENTITY_VERSION,
            _node_id(IDENTITY_VERSION, "Ed25519", public_raw.hex()),
            "Ed25519",
            public_raw.hex(),
            _timestamp() if timestamp is None else timestamp,
            "GENERATED_OR_IMPORTED",
        )
        if not identity.validate():
            raise RuntimeError("generated Node Identity failed validation")
        self.identity = identity
        self.node_life = NodeLife.create(identity.node_id, identity.creation_timestamp)
        return identity, private_raw

    def validate_identity(self, verification_reference: str | None = None) -> NodeIdentity:
        self._require_ready()
        if not self.identity.validate():
            raise ValueError("identity validation failed")
        if self.identity.status != "GENERATED_OR_IMPORTED":
            if self.identity.status in {"VALIDATED", "REGISTERED", "ACTIVE"}:
                return self.identity
            raise ValueError(f"identity cannot be validated from state {self.identity.status}")
        self.identity = replace(
            self.identity,
            status="VALIDATED",
            verification_reference=verification_reference,
        )
        return self.identity

    def register(self, registration_reference: str) -> NodeIdentity:
        self._require_ready()
        if not registration_reference:
            raise ValueError("registration reference is required")
        if self.identity.status == "GENERATED_OR_IMPORTED":
            self.validate_identity()
        if self.identity.status != "VALIDATED":
            raise ValueError(f"identity cannot be registered from state {self.identity.status}")
        self.identity = replace(
            self.identity,
            status="REGISTERED",
            registration_reference=registration_reference,
        )
        return self.identity

    def initialize(
        self,
        timestamp: int | None = None,
        registration_reference: str = "LOCAL_NODE_REGISTRATION",
    ) -> LifecycleEvent:
        """Compatibility boundary: validate/register the identity and initialize Node Life."""
        self._require_ready()
        self.validate_identity()
        self.register(registration_reference)
        return self.node_life.transition("NODE_INITIALIZED", "INITIALIZED", timestamp)

    def activate(self, timestamp: int | None = None, node_core_ready: bool = False) -> LifecycleEvent:
        self._require_ready()
        if not node_core_ready:
            raise RuntimeError("Node Core readiness is required before identity activation")
        if not self.identity.validate():
            raise ValueError("identity validation failed")
        if self.identity.status != "REGISTERED":
            raise ValueError(f"identity cannot be activated from state {self.identity.status}")
        self.identity = replace(self.identity, status="ACTIVE")
        return self.node_life.transition("NODE_ACTIVATED", "ACTIVE", timestamp)

    def snapshot(self) -> dict[str, Any]:
        self._require_ready()
        return {
            "identity": self.identity.canonical_record(),
            "node_life": {
                "node_life_id": self.node_life.node_life_id,
                "node_id": self.node_life.node_id,
                "state": self.node_life.state,
                "state_history": [asdict(e) for e in self.node_life.state_history],
            },
            "profile": NODE_ID_PROFILE,
        }

    def _require_ready(self) -> None:
        if self.identity is None or self.node_life is None:
            raise RuntimeError("Node Identity has not been created")


def reconstruct_lifecycle(events: Iterable[dict[str, Any]]) -> str:
    normalized = list(events)
    if not normalized:
        raise ValueError("lifecycle event sequence is empty")
    previous = None
    state = "UNINITIALIZED"
    for raw in normalized:
        event = LifecycleEvent(**raw)
        if not event.verify_integrity(previous):
            raise ValueError("lifecycle integrity verification failed")
        if not _valid_transition(state, event.state):
            raise ValueError(f"invalid lifecycle sequence: {state} -> {event.state}")
        state = event.state
        previous = event.event_hash
    return state


__all__ = [
    "IDENTITY_VERSION",
    "NODE_ID_PROFILE",
    "IDENTITY_STATES",
    "NodeIdentity",
    "NodeLife",
    "LifecycleEvent",
    "IdentityManager",
    "reconstruct_lifecycle",
]