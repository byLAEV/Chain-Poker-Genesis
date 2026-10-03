"""Protocol-neutral zero-knowledge provider contract."""
from __future__ import annotations
from abc import ABC, abstractmethod

class ZeroKnowledgeProvider(ABC):
    name="zero-knowledge"
    version="1.0.0"
    @abstractmethod
    def capabilities(self): ...
    @abstractmethod
    def verify(self, proof, public_inputs): ...
