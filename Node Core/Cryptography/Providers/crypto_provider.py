"""Provider contracts for external cryptographic implementations."""
from __future__ import annotations
from abc import ABC, abstractmethod

class CryptoProvider(ABC):
    name="UNDEFINED"
    version="UNDEFINED"
    @abstractmethod
    def capabilities(self): ...
