"""Provider contracts for external cryptographic implementations."""
from __future__ import annotations
from abc import ABC, abstractmethod

class CryptoProvider(ABC):
    name="UNDEFINED"
    version="UNDEFINED"
    @abstractmethod
    def capabilities(self): ...


class KeyCustodyProvider(CryptoProvider):
    """Minimal external custody boundary for private-key operations."""

    @abstractmethod
    def sign_ed25519(self, message: bytes, key_ref: str) -> bytes:
        """Sign without returning private key material to Node Core."""

    @abstractmethod
    def public_key(self, key_ref: str) -> bytes:
        """Return the public key associated with an external key reference."""
