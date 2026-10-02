#!/usr/bin/env python3
"""Validate Node Core Installation Manifest against its JSON Schema."""

from __future__ import annotations

import json
import sys
from pathlib import Path

def validate(manifest, schema, path="manifest"):
    if schema.get("type") == "object":
        if not isinstance(manifest, dict):
            raise AssertionError(f"{path}: expected object")
        required = schema.get("required", [])
        for key in required:
            if key not in manifest:
                raise AssertionError(f"{path}: missing required field {key}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extra = set(manifest) - set(properties)
            if extra:
                raise AssertionError(f"{path}: unexpected fields {sorted(extra)}")
        for key, spec in properties.items():
            if key in manifest:
                validate(manifest[key], spec, f"{path}.{key}")
    elif schema.get("type") == "array":
        if not isinstance(manifest, list):
            raise AssertionError(f"{path}: expected array")
        if "maxItems" in schema and len(manifest) > schema["maxItems"]:
            raise AssertionError(f"{path}: too many items")
    elif schema.get("type") == "string":
        if not isinstance(manifest, str):
            raise AssertionError(f"{path}: expected string")
    if "const" in schema and manifest != schema["const"]:
        raise AssertionError(f"{path}: expected {schema['const']!r}")
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
