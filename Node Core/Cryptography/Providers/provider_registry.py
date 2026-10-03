"""Registry for Node Core cryptography providers."""
from __future__ import annotations
class ProviderRegistry:
    def __init__(self): self._providers={}
    def register(self,provider): self._providers[provider.name]=provider
    def get(self,name): return self._providers[name]
    def names(self): return tuple(sorted(self._providers))
