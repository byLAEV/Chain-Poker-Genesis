#!/usr/bin/env python3
from pathlib import Path
import sys

BASE=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(BASE/"Protocol Interface"))

from protocol_catalog import ProtocolCatalog, ProtocolCatalogEntry
from protocol_source_resolver import ProtocolSourceResolver
from protocol_download import ProtocolDownloadBoundary


def main():
    entry=ProtocolCatalogEntry(
        "example.protocol",
        "Example Protocol",
        "1.0.0",
        "GitHub",
        "https://github.com/example/example-protocol/releases/tag/v1.0.0",
        "https://github.com/example/example-protocol/releases/download/v1.0.0/example-protocol.zip",
    )
    catalog=ProtocolCatalog([entry])
    assert catalog.get("example.protocol") is entry

    resolved=ProtocolSourceResolver().resolve(entry)
    assert resolved.download_url == entry.download_url

    try:
        ProtocolCatalogEntry(
            "bad.protocol","Bad","1.0.0","GitHub","source",
            "https://example.org/package.zip"
        )
        raise AssertionError("non-GitHub source accepted")
    except ValueError:
        pass

    boundary=ProtocolDownloadBoundary(BASE/"Protocols")
    assert boundary.protocols_root.name == "Protocols"

    print("Node Core Protocol Catalog / Source Resolver / Download Boundary tests: PASS")


if __name__=="__main__":
    main()
