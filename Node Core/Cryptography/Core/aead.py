#!/usr/bin/env python3
"""Normative AES-256-GCM implementation for Node Core Cryptography."""

from __future__ import annotations

import hashlib
from typing import Optional

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class AEADFailure(RuntimeError):
    """Generic fail-closed AEAD error without unauthenticated plaintext."""


class NonceReuseError(AEADFailure):
    """Raised when the same nonce is reused with the same key at the caller boundary."""


class NonceReuseGuard:
    """Minimal in-process boundary guard for per-key nonce uniqueness."""

    def __init__(self) -> None:
        self._seen: dict[bytes, set[bytes]] = {}

    def reserve(self, key: bytes, nonce: bytes) -> None:
        key_id = hashlib.sha256(key).digest()
        nonces = self._seen.setdefault(key_id, set())
        if nonce in nonces:
            raise NonceReuseError("nonce reuse")
        nonces.add(nonce)


def _validate_key(key: bytes) -> bytes:
    key = bytes(key)
    if len(key) != 32:
        raise ValueError("AES-256-GCM key must be 32 bytes")
    return key


def _validate_nonce(nonce: bytes) -> bytes:
    nonce = bytes(nonce)
    if len(nonce) != 12:
        raise ValueError("AES-256-GCM nonce must be 12 bytes")
    return nonce


def _validate_aad(aad: bytes) -> bytes:
    return bytes(aad)


def encrypt_aead(
    key: bytes,
    nonce: bytes,
    plaintext: bytes,
    associated_data: bytes = b"",
    guard: Optional[NonceReuseGuard] = None,
) -> dict[str, object]:
    """Encrypt using AES-256-GCM and return the canonical logical container."""
    key = _validate_key(key)
    nonce = _validate_nonce(nonce)
    plaintext = bytes(plaintext)
    associated_data = _validate_aad(associated_data)

    if guard is not None:
        guard.reserve(key, nonce)

    encrypted = AESGCM(key).encrypt(nonce, plaintext, associated_data)
    return {
        "version": 1,
        "algorithm": "AES-256-GCM",
        "nonce": nonce.hex(),
        "ciphertext": encrypted[:-16].hex(),
        "tag": encrypted[-16:].hex(),
    }


def decrypt_aead(
    key: bytes,
    container: dict[str, object],
    associated_data: bytes = b"",
) -> bytes:
    """Decrypt only after successful authentication; never return unauthenticated plaintext."""
    key = _validate_key(key)
    associated_data = _validate_aad(associated_data)

    try:
        if container.get("version") != 1 or container.get("algorithm") != "AES-256-GCM":
            raise AEADFailure("malformed container")
        nonce = bytes.fromhex(str(container["nonce"]))
        ciphertext = bytes.fromhex(str(container["ciphertext"]))
        tag = bytes.fromhex(str(container["tag"]))
        nonce = _validate_nonce(nonce)
        if len(tag) != 16:
            raise AEADFailure("malformed container")
    except (KeyError, TypeError, ValueError) as exc:
        raise AEADFailure("malformed container") from exc

    try:
        return AESGCM(key).decrypt(nonce, ciphertext + tag, associated_data)
    except InvalidTag as exc:
        raise AEADFailure("authentication failed") from exc


__all__ = [
    "AEADFailure",
    "NonceReuseError",
    "NonceReuseGuard",
    "encrypt_aead",
    "decrypt_aead",
]
