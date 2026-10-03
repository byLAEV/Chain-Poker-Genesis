#!/usr/bin/env python3
"""Ed25519 tests for the Node Core cryptographic boundary."""
from __future__ import annotations

import sys
from pathlib import Path

CORE = Path(__file__).resolve().parents[2] / "Cryptography" / "Core"
sys.path.insert(0, str(CORE))

from signatures import generate_keypair, sign, sign_canonical, verify, verify_canonical  # noqa: E402


def test_sign_and_verify_roundtrip() -> None:
    private, public = generate_keypair()
    message = b"node-core-ed25519"
    signature = sign(message, private)
    assert len(signature) == 64
    assert verify(message, signature, public)


def test_modified_payload_fails() -> None:
    private, public = generate_keypair()
    signature = sign(b"original", private)
    assert not verify(b"modified", signature, public)


def test_modified_signature_fails() -> None:
    private, public = generate_keypair()
    signature = bytearray(sign(b"payload", private))
    signature[0] ^= 1
    assert not verify(b"payload", bytes(signature), public)


def test_invalid_key_lengths_fail_closed() -> None:
    private, public = generate_keypair()
    assert not verify(b"payload", b"short", public)
    assert not verify(b"payload", sign(b"payload", private), b"short")


def test_canonical_signing_roundtrip() -> None:
    private, public = generate_keypair()
    payload = {"b": 2, "a": 1}
    signature = sign_canonical(payload, private)
    assert verify_canonical(payload, signature, public)
    assert not verify_canonical({"a": 1, "b": 3}, signature, public)


if __name__ == "__main__":
    test_sign_and_verify_roundtrip()
    test_modified_payload_fails()
    test_modified_signature_fails()
    test_invalid_key_lengths_fail_closed()
    test_canonical_signing_roundtrip()
    print("ed25519_tests = PASS")
