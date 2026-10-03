#!/usr/bin/env python3
"""Registry of storage provider instances."""

class ProviderRegistry:
    def __init__(self):
        self._providers = {}

    def register(self, provider):
        if not getattr(provider, "provider_type", None):
            raise ValueError("provider must expose provider_type")
        self._providers[provider.provider_type] = provider
        return provider

    def get(self, provider_type):
        return self._providers.get(provider_type)

    def list(self):
        return dict(self._providers)

    def capabilities(self, provider_type):
        provider = self.get(provider_type)
        return provider.capabilities() if provider else set()
