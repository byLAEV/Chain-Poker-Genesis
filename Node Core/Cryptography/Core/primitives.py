"""Compatibility exports for the canonical Node Core cryptographic primitives.

Merkle construction is intentionally not implemented here. It requires a
separate deterministic Merkle specification before becoming normative.
"""
from __future__ import annotations

from crypto_core import (
    canonicalize,
    sha256,
    sha256_hex,
    hash_canonical,
    hash_canonical_hex,
    random_bytes,
    constant_time_equal,
)

__all__ = [
    "canonicalize",
    "sha256",
    "sha256_hex",
    "hash_canonical",
    "hash_canonical_hex",
    "random_bytes",
    "constant_time_equal",
]
