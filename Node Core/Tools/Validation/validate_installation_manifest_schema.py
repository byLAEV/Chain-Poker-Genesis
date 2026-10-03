#!/usr/bin/env python3
"""Validate Node Core Installation Manifest against the canonical internal schema."""

from __future__ import annotations
import json
import sys
from pathlib import Path

def validate(value, schema, path="manifest"):
    if schema.get("type") == "object":
        if not isinstance(value, dict):
            raise AssertionError(f"{path}: expected object")
        properties = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                raise AssertionError(f"{path}: missing required field {key}")
        if schema.get("additionalProperties") is False:
            extra = set(value) - set(properties)
            if extra:
                raise AssertionError(f"{path}: unexpected fields {sorted(extra)}")
        for key, spec in properties.items():
            if key in value:
                validate(value[key], spec, f"{path}.{key}")
    elif schema.get("type") == "array":
        if not isinstance(value, list):
            raise AssertionError(f"{path}: expected array")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            raise AssertionError(f"{path}: too many items")
        if "items" in schema:
            for i, item in enumerate(value):
                validate(item, schema["items"], f"{path}[{i}]")
    elif schema.get("type") == "string":
        if not isinstance(value, str):
            raise AssertionError(f"{path}: expected string")
    elif schema.get("type") == "boolean":
        if not isinstance(value, bool):
            raise AssertionError(f"{path}: expected boolean")
    elif schema.get("type") == "integer":
        if not isinstance(value, int) or isinstance(value, bool):
            raise AssertionError(f"{path}: expected integer")
    if "const" in schema and value != schema["const"]:
        raise AssertionError(f"{path}: expected {schema['const']!r}")
    return True

def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_installation_manifest_schema.py <node-directory>")
    root = Path(sys.argv[1]).resolve()
    manifest_path = root / "node-installation-manifest.json"
    schema_path = Path(__file__).resolve().parents[2] / "Configuration/Schemas/node-core-installation-manifest.schema.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validate(manifest, schema)
    print("schema_validation = PASS")

if __name__ == "__main__":
    main()
