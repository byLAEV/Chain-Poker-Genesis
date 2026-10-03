#!/usr/bin/env python3
"""Node Core Ed25519 signature boundary.

The implementation uses the Python standard library when Ed25519 is exposed
by the runtime's cryptographic backend. No protocol-specific semantics live
here.
"""
from __future__ import annotations

from typing import Any

from crypto_core import canonicalize

try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import (
        Ed25519PrivateKey,
        Ed25519PublicKey,
    )
except ImportError as exc:  # pragma: no cover - environment dependent
    Ed25519PrivateKey = None
    Ed25519PublicKey = None
    _IMPORT_ERROR = exc
else:
    _IMPORT_ERROR = None


def _require_backend() -> None:
    if Ed25519PrivateKey is None or Ed25519PublicKey is None:
        raise RuntimeError(
            "Ed25519 backend unavailable; install the approved cryptography backend"
        ) from _IMPORT_ERROR


def generate_keypair() -> tuple[bytes, bytes]:
    """Return (private_key_raw, public_key_raw)."""
    _require_backend()
    private = Ed25519PrivateKey.generate()
    public = private.public_key()
    return (
        private.private_bytes_raw(),
        public.public_bytes_raw(),
    )


def sign(message: bytes, private_key: bytes) -> bytes:
    """Sign exact bytes with an Ed25519 private key."""
    _require_backend()
    if len(private_key) != 32:
        raise ValueError("Ed25519 private key must be 32 bytes")
    return Ed25519PrivateKey.from_private_bytes(private_key).sign(bytes(message))


def verify(message: bytes, signature: bytes, public_key: bytes) -> bool:
    """Return True only when the exact signature verifies."""
    _require_backend()
    if len(public_key) != 32 or len(signature) != 64:
        return False
    try:
        Ed25519PublicKey.from_public_bytes(public_key).verify(
            bytes(signature), bytes(message)
        )
    except (ValueError, TypeError):
        return False
    return True


def sign_canonical(value: Any, private_key: bytes) -> bytes:
    return sign(canonicalize(value), private_key)


def verify_canonical(value: Any, signature: bytes, public_key: bytes) -> bool:
    return verify(canonicalize(value), signature, public_key)


__all__ = [
    "generate_keypair",
    "sign",
    "verify",
    "sign_canonical",
    "verify_canonical",
]
