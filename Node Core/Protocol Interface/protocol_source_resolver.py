"""Resolve supported protocol catalog sources without installing them."""
from __future__ import annotations
from dataclasses import dataclass
from urllib.parse import urlparse

@dataclass(frozen=True)
class ResolvedProtocolSource:
    protocol_id: str
    source_type: str
    source: str
    download_url: str

class ProtocolSourceResolver:
    def resolve(self, entry):
        parsed = urlparse(entry.download_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("protocol download URL is invalid")
        if entry.source_type == "GitHub" and "github.com" not in parsed.netloc.lower():
            raise ValueError("GitHub source must resolve to github.com")
        return ResolvedProtocolSource(
            entry.protocol_id,
            entry.source_type,
            entry.source,
            entry.download_url,
        )
