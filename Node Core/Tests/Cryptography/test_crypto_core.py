#!/usr/bin/env python3
"""Deterministic tests for the Node Core cryptographic primitive boundary."""

from __future__ import annotations

import sys
from pathlib import Path

CORE = Path(__file__).resolve().parents[2] / "Cryptography" / "Core"
sys.path.insert(0, str(CORE))

from crypto_core import (  # noqa: E402
    canonicalize,
    constant_time_equal,
    generate_nonce,
    hash_canonical_hex,
    sha256_hex,
)


def test_canonical_serialization_is_deterministic() -> None:
    left = canonicalize({"b": 2, "a": 1})
    right = canonicalize({"a": 1, "b": 2})
    assert left == right == b'{"a":1,"b":2}'


def test_canonical_serialization_is_utf8() -> None:
    assert canonicalize({"message": "á"}) == '{"message":"á"}'.encode("utf-8")


def test_canonicalization_rejects_nan() -> None:
    try:
        canonicalize({"value": float("nan")})
    except ValueError:
        return
    raise AssertionError("NaN must be rejected")


def test_sha256_known_vector() -> None:
    assert (
        sha256_hex(b"abc")
        == "ba7816bf8f01cfea414140de5dae2223"
           "b00361a396177a9cb410ff61f20015ad"
    )


def test_canonical_hash_known_vector() -> None:
    assert hash_canonical_hex({"a": 1}) == (
        "015abd7f5cc57a2dd94b7590f04ad808"
        "4273905ee33ec5cebeae62276a97f862"
    )

def test_nonce_length_and_uniqueness() -> None:
    first = generate_nonce(32)
    second = generate_nonce(32)
    assert len(first) == 32
    assert len(second) == 32
    assert first != second


def test_invalid_nonce_size() -> None:
    for size in (0, -1, True):
        try:
            generate_nonce(size)
        except ValueError:
            continue
        raise AssertionError("invalid nonce size must fail closed")


def test_constant_time_equal() -> None:
    assert constant_time_equal(b"abc", b"abc")
    assert not constant_time_equal(b"abc", b"abd")


if __name__ == "__main__":
    for name, value in sorted(globals().items()):
        if name.startswith("test_") and callable(value):
            value()
    print("cryptography_core_tests = PASS")


def test_canonical_serialization_rejects_finite_float() -> None:
    try:
        canonicalize({"value": 1.5})
    except TypeError:
        return
    raise AssertionError("finite floating-point values must be rejected")


def test_canonical_serialization_rejects_unsupported_type() -> None:
    class Unsupported:
        pass

    try:
        canonicalize({"value": Unsupported()})
    except TypeError:
        return
    raise AssertionError("unsupported protocol values must be rejected")


def test_canonical_serialization_preserves_large_integer() -> None:
    assert canonicalize({"n": 9007199254740993}) == b'{"n":9007199254740993}'
