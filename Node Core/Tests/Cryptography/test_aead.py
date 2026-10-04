#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

CORE = Path(__file__).resolve().parents[2] / "Cryptography" / "Core"
sys.path.insert(0, str(CORE))

from aead import AEADFailure, NonceReuseError, NonceReuseGuard, decrypt_aead, encrypt_aead


VECTORS = CORE / "Test Vectors" / "aead-aes-256-gcm-v1.0.json"


def _hex(value: str) -> bytes:
    return bytes.fromhex(value)


def test_independent_aes256gcm_vectors() -> None:
    data = json.loads(VECTORS.read_text(encoding="utf-8"))
    for vector in data["vectors"]:
        if vector["result"] != "PASS":
            continue
        inputs = vector["inputs"]
        expected = vector["expected"]
        container = encrypt_aead(
            _hex(inputs["key"]),
            _hex(inputs["nonce"]),
            _hex(inputs["plaintext"]),
            _hex(inputs["aad"]),
        )
        assert container["ciphertext"] == expected["ciphertext"]
        assert container["tag"] == expected["tag"]


def test_modified_ciphertext_tag_aad_and_wrong_key_fail_closed() -> None:
    key = bytes(32)
    nonce = bytes(12)
    plaintext = bytes(16)
    aad = bytes(16)
    container = encrypt_aead(key, nonce, plaintext, aad)

    cases = [
        (bytes.fromhex("01" + container["ciphertext"][2:]), container["tag"], aad),
        (_hex(container["ciphertext"]), "00" * 16, aad),
        (_hex(container["ciphertext"]), container["tag"], b"\x01" + aad[1:]),
        (_hex(container["ciphertext"]), container["tag"], aad),
    ]

    for ciphertext, tag, case_aad in cases[:3]:
        bad = dict(container, ciphertext=ciphertext.hex(), tag=tag)
        try:
            decrypt_aead(key, bad, case_aad)
        except AEADFailure:
            continue
        raise AssertionError("authentication failure must be fail-closed")

    wrong_key = bytes.fromhex("01" + "00" * 31)
    try:
        decrypt_aead(wrong_key, container, aad)
    except AEADFailure:
        return
    raise AssertionError("wrong key must fail authentication")


def test_malformed_container_fails_closed() -> None:
    try:
        decrypt_aead(
            bytes(32),
            {
                "version": 1,
                "algorithm": "AES-256-GCM",
                "nonce": "00" * 10,
                "ciphertext": "",
                "tag": "58e2fccefa7e3061367f1d57a4e7455a",
            },
        )
    except AEADFailure:
        return
    raise AssertionError("malformed container must fail closed")


def test_nonce_reuse_is_rejected_at_calling_boundary() -> None:
    guard = NonceReuseGuard()
    key = bytes(32)
    nonce = bytes(12)
    encrypt_aead(key, nonce, b"first", guard=guard)
    try:
        encrypt_aead(key, nonce, b"second", guard=guard)
    except NonceReuseError:
        return
    raise AssertionError("same-key nonce reuse must be rejected")


if __name__ == "__main__":
    for name, value in sorted(globals().items()):
        if name.startswith("test_") and callable(value):
            value()
    print("aead_tests = PASS")
