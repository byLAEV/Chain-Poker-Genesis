#!/usr/bin/env python3
from pathlib import Path
import sys
BASE=Path(__file__).resolve().parents[2]/"Cryptography"
sys.path.insert(0,str(BASE/"Core"))
from crypto_service import CryptoService

def main():
    crypto=CryptoService()
    message=b"node-core-cryptography-test"
    assert crypto.sha256_hex(message)==crypto.sha256_hex(message)
    assert crypto.hash_canonical_hex({"b":2,"a":1})==crypto.hash_canonical_hex({"a":1,"b":2})
    assert len(crypto.random_bytes(32))==32
    private,public=crypto.generate_ed25519_keypair()
    signature=crypto.sign_ed25519(message,private)
    assert crypto.verify_ed25519(message,signature,public)
    assert not crypto.verify_ed25519(message+b"x",signature,public)
    canonical={"component":"Node Core","operation":"verify"}
    sig=crypto.sign_canonical(canonical,private)
    assert crypto.verify_canonical(canonical,sig,public)
    print("Node Core Cryptography implementation tests: PASS")

if __name__=="__main__":
    main()


def test_private_material_is_not_exposed_by_custody_interface():
    from crypto_provider import KeyCustodyProvider

    class TestCustody(KeyCustodyProvider):
        name = "test-custody"
        version = "1.0"

        def capabilities(self):
            return ("sign_ed25519", "public_key")

        def sign_ed25519(self, message, key_ref):
            return b"signature"

        def public_key(self, key_ref):
            return b"public-key"

    provider = TestCustody()
    assert not hasattr(provider, "private_key")
    assert not hasattr(provider, "secret")
    assert "private" not in repr(provider).lower()
    assert "secret" not in repr(provider).lower()


def test_custody_boundary_uses_key_reference_not_private_bytes():
    import inspect
    from crypto_provider import KeyCustodyProvider
    params = inspect.signature(KeyCustodyProvider.sign_ed25519).parameters
    assert "key_ref" in params
    assert "private_key" not in params
