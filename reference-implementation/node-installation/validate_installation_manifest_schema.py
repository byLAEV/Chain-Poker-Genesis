#!/usr/bin/env python3
"""Validate Node Core Installation Manifest against its JSON Schema."""

from __future__ import annotations

import json
import sys
from pathlib import Path

def validate(manifest, schema):
    required = schema["required"]
    for key in required:
        if key not in manifest:
            raise AssertionError(f"missing required manifest field: {key}")
    if schema.get("additionalProperties") is False:
        extra = set(manifest) - set(schema["properties"])
        if extra:
            raise AssertionError(f"unexpected manifest fields: {sorted(extra)}")
    for key, spec in schema["properties"].items():
        if "const" in spec and manifest.get(key) != spec["const"]:
            raise AssertionError(f"{key}: expected {spec['const']!r}")
    return True

def main():
    root = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else Path("/tmp/cpg-node-manifest-schema-test")
    manifest_path = root / "node-installation-manifest.json"
    schema_path = Path(__file__).resolve().parents[2] / "docs/node/node-core-installation-manifest.schema.json"
    if not manifest_path.is_file():
        raise AssertionError("installation manifest missing")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validate(manifest, schema)
    print("schema_validation = PASS")

if __name__ == "__main__":
    main()
