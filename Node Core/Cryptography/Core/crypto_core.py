#!/usr/bin/env python3
"""Executable Node Core cryptographic primitives.

This module implements only primitives already fixed by the Node Core
cryptographic profile. Protocol-specific cryptography remains outside this
module.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import secrets
from typing import Any


def canonicalize(value: Any) -> bytes:
    """Return deterministic UTF-8 JSON bytes for hash/signature inputs."""
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def sha256(data: bytes | bytearray | memoryview) -> bytes:
    """Return the canonical SHA-256 digest."""
    return hashlib.sha256(bytes(data)).digest()


def sha256_hex(data: bytes | bytearray | memoryview) -> str:
    """Return the canonical lowercase hexadecimal SHA-256 digest."""
    return sha256(data).hex()


def hash_canonical(value: Any) -> bytes:
    """Canonicalize a value and hash the resulting bytes with SHA-256."""
    return sha256(canonicalize(value))


def hash_canonical_hex(value: Any) -> str:
    """Canonicalize a value and return its SHA-256 digest as lowercase hex."""
    return hash_canonical(value).hex()


def generate_nonce(size: int = 32) -> bytes:
    """Generate cryptographically secure random bytes."""
    if not isinstance(size, int) or isinstance(size, bool) or size <= 0:
        raise ValueError("nonce size must be a positive integer")
    return secrets.token_bytes(size)


def random_bytes(size: int) -> bytes:
    """Provider-neutral CSPRNG boundary."""
    return generate_nonce(size)


def constant_time_equal(left: bytes, right: bytes) -> bool:
    """Compare cryptographic byte values without early-exit timing."""
    return hmac.compare_digest(bytes(left), bytes(right))


__all__ = [
    "canonicalize",
    "sha256",
    "sha256_hex",
    "hash_canonical",
    "hash_canonical_hex",
    "generate_nonce",
    "random_bytes",
    "constant_time_equal",
]
