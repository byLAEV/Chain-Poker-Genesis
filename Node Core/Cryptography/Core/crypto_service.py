#!/usr/bin/env python3
"""Unified protocol-neutral Node Core cryptography service."""
from __future__ import annotations
from .crypto_core import canonicalize, sha256, sha256_hex, hash_canonical, hash_canonical_hex, random_bytes, constant_time_equal
from .signatures import generate_keypair, sign, verify, sign_canonical, verify_canonical

class CryptoService:
    version="1.1.0"
    def canonicalize(self,value): return canonicalize(value)
    def sha256(self,data): return sha256(data)
    def sha256_hex(self,data): return sha256_hex(data)
    def hash_canonical(self,value): return hash_canonical(value)
    def hash_canonical_hex(self,value): return hash_canonical_hex(value)
    def random_bytes(self,size=32): return random_bytes(size)
    def constant_time_equal(self,left,right): return constant_time_equal(left,right)
    def generate_ed25519_keypair(self): return generate_keypair()
    def sign_ed25519(self,message,private_key): return sign(message,private_key)
    def verify_ed25519(self,message,signature,public_key): return verify(message,signature,public_key)
    def sign_canonical(self,value,private_key): return sign_canonical(value,private_key)
    def verify_canonical(self,value,signature,public_key): return verify_canonical(value,signature,public_key)
