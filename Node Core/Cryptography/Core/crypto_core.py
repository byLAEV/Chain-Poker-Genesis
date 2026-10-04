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
from typing import Any, Callable


_ALLOWED_SCALAR_TYPES = (str, int, bool, type(None))


def _validate_canonical_value(value: Any) -> None:
    if isinstance(value, float):
        raise TypeError("floating-point values are prohibited")
    if isinstance(value, _ALLOWED_SCALAR_TYPES):
        return
    if isinstance(value, list):
        for item in value:
            _validate_canonical_value(item)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise TypeError("canonical object keys must be strings")
            _validate_canonical_value(item)
        return
    raise TypeError("unsupported protocol value")


def canonicalize(value: Any) -> bytes:
    """Return deterministic UTF-8 JSON bytes for hash/signature inputs."""
    _validate_canonical_value(value)
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


class CSPRNGFailure(RuntimeError):
    """Typed failure at the approved cryptographic randomness boundary."""


def _os_csprng(size: int) -> bytes:
    return secrets.token_bytes(size)


def random_bytes(size: int = 32, provider: Callable[[int], bytes] = _os_csprng) -> bytes:
    """Return exactly size bytes from the approved CSPRNG or fail closed."""
    if not isinstance(size, int) or isinstance(size, bool) or size <= 0:
        raise ValueError("random byte size must be a positive integer")
    try:
        result = provider(size)
    except Exception as exc:
        raise CSPRNGFailure("cryptographic randomness provider failed") from exc
    if not isinstance(result, bytes) or len(result) != size:
        raise CSPRNGFailure("cryptographic randomness provider returned invalid output")
    return result


def generate_nonce(size: int = 32) -> bytes:
    """Generate cryptographically secure random bytes."""
    return random_bytes(size)


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
    "CSPRNGFailure",
    "constant_time_equal",
]
