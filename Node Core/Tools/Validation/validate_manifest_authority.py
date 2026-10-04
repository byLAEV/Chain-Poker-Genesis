#!/usr/bin/env python3
"""Validate Node Core manifest authority and detect conflicting schemas."""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
CANONICAL=ROOT/"Configuration/Schemas/node-core-installation-manifest.schema.json"
LEGACY=ROOT/"Configuration/Schemas/node-installation-manifest.schema.json"
COMPONENT=ROOT/"NODE-CORE-MANIFEST.json"

def load(p): return json.loads(p.read_text(encoding="utf-8"))

def main():
    component=load(COMPONENT)
    canonical=load(CANONICAL)
    legacy=load(LEGACY)

    assert component["component"]=="Node Core"
    assert component["scope"]=="Protocol-neutral base node infrastructure"
    assert component["components"]["protocol_interface"]=="IMPLEMENTED_PARTIAL"
    assert canonical["title"]=="Node Core Installation Manifest"

    # Legacy schema is detected as non-authoritative when it diverges.
    if legacy != canonical:
        legacy_status="LEGACY_CONFLICT_DETECTED"
    else:
        legacy_status="DUPLICATE_SCHEMA"

    assert "cpg_protocol" in canonical["required"]
    assert "protocol_associations" in canonical["required"]
    assert canonical["properties"]["protocol_associations"]["maxItems"] == 0
    assert canonical["properties"]["cpg_protocol"]["properties"]["status"]["const"] == "NOT_INSTALLED"
    assert canonical["properties"]["protocol_associations"]["maxItems"] == 0

    print("component_manifest = CANONICAL")
    print("installation_schema = CANONICAL")
    print(f"legacy_installation_schema = {legacy_status}")
    print("manifest_authority = PASS")

if __name__=="__main__":
    main()
