"""Remote protocol catalog model for the Node Core Protocol Interface."""
from __future__ import annotations
from dataclasses import dataclass
from urllib.parse import urlparse

SUPPORTED_SOURCES = {"CID", "GitHub"}


@dataclass(frozen=True)
class ProtocolCatalogEntry:
    protocol_id: str
    name: str
    version: str
    source_type: str
    source: str
    download_url: str
    manifest_hash: str = ""

    def __post_init__(self):
        if not self.protocol_id or not self.name or not self.version:
            raise ValueError("protocol identity fields are required")
        if self.source_type not in SUPPORTED_SOURCES:
            raise ValueError("unsupported protocol source")
        if not self.source:
            raise ValueError("source is required")
        parsed = urlparse(self.download_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("download_url must be an absolute HTTP(S) URL")


class ProtocolCatalog:
    """Validated remote catalog; it does not install protocols."""

    def __init__(self, entries=()):
        self._entries = {}
        for entry in entries:
            self.add(entry)

    def add(self, entry: ProtocolCatalogEntry):
        if entry.protocol_id in self._entries:
            raise ValueError("duplicate protocol catalog entry")
        self._entries[entry.protocol_id] = entry
        return entry

    def get(self, protocol_id):
        return self._entries[protocol_id]

    def all(self):
        return tuple(self._entries.values())
