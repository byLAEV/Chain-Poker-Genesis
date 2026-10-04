#!/usr/bin/env python3
"""Canonical verification gate for Node Core Bootstrap."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

class BootstrapVerificationError(Exception):
    pass

REQUIRED = (
    "node-storage","node-storage/identity","node-storage/cryptography",
    "node-storage/configuration","node-storage/state","node-storage/records",
    "node-storage/recovery","node-storage/protocol",
)
ARTIFACTS = (
    "node-storage/identity/node-identity.json",
    "node-storage/configuration/node-config.json",
    "node-storage/state/node-state.json",
    "node-storage/recovery/recovery.json",
    "node-storage/state/storage-manifest.json",
    "node-installation-manifest.json",
)
SCHEMA_PATH = Path(__file__).resolve().parents[2] / "Configuration/Schemas/node-core-installation-manifest.schema.json"

def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def _validate_schema(value, schema, path="manifest"):
    if schema.get("type") == "object":
        if not isinstance(value, dict):
            raise BootstrapVerificationError(f"{path}: expected object")
        properties = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                raise BootstrapVerificationError(f"{path}: missing required field {key}")
        if schema.get("additionalProperties") is False:
            extra = set(value) - set(properties)
            if extra:
                raise BootstrapVerificationError(f"{path}: unexpected fields {sorted(extra)}")
        for key, spec in properties.items():
            if key in value:
                _validate_schema(value[key], spec, f"{path}.{key}")
    elif schema.get("type") == "array":
        if not isinstance(value, list):
            raise BootstrapVerificationError(f"{path}: expected array")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            raise BootstrapVerificationError(f"{path}: too many items")
        for i, item in enumerate(value):
            _validate_schema(item, schema.get("items", {}), f"{path}[{i}]")
    elif schema.get("type") == "string" and not isinstance(value, str):
        raise BootstrapVerificationError(f"{path}: expected string")
    elif schema.get("type") == "boolean" and not isinstance(value, bool):
        raise BootstrapVerificationError(f"{path}: expected boolean")
    elif schema.get("type") == "integer" and (not isinstance(value, int) or isinstance(value, bool)):
        raise BootstrapVerificationError(f"{path}: expected integer")
    if "const" in schema and value != schema["const"]:
        raise BootstrapVerificationError(f"{path}: expected {schema['const']!r}")

def _load_json(path: Path, label: str):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BootstrapVerificationError(f"{label} is invalid") from exc

def verify(target: Path):
    target = Path(target).resolve()
    missing = [p for p in REQUIRED if not (target / p).is_dir()]
    if missing:
        raise BootstrapVerificationError("missing bootstrap paths: " + ", ".join(missing))

    identity = _load_json(target / ARTIFACTS[0], "identity metadata")
    config = _load_json(target / ARTIFACTS[1], "configuration metadata")
    state = _load_json(target / ARTIFACTS[2], "node state")
    recovery = _load_json(target / ARTIFACTS[3], "recovery metadata")
    storage = _load_json(target / ARTIFACTS[4], "storage manifest")
    installation = _load_json(target / ARTIFACTS[5], "installation manifest")
    integrity = _load_json(target / "node-storage/state/bootstrap-integrity.json", "integrity manifest")
    schema = _load_json(SCHEMA_PATH, "canonical installation schema")

    _validate_schema(installation, schema)

    if identity.get("identity_status") != "INITIALIZED":
        raise BootstrapVerificationError("identity is not initialized")
    if config.get("protocol_associations") != [] or config.get("cpg_protocol") != "NOT_INSTALLED":
        raise BootstrapVerificationError("protocol isolation invariant failed")
    if state.get("state") != "NODE_CORE_READY":
        raise BootstrapVerificationError("invalid bootstrap state")
    if recovery.get("status") != "READY":
        raise BootstrapVerificationError("recovery is not ready")
    if storage.get("root") != "node-storage" or storage.get("required_paths") != list(REQUIRED):
        raise BootstrapVerificationError("storage structure mismatch")

    if installation["storage"]["required_paths"] != storage["required_paths"]:
        raise BootstrapVerificationError("installation/storage manifest mismatch")
    if installation["storage"]["storage_structure_version"] != storage["storage_structure_version"]:
        raise BootstrapVerificationError("storage structure version mismatch")
    if installation["node"]["node_core_version"] != config.get("node_core_version"):
        raise BootstrapVerificationError("Node Core version mismatch")
    if installation["provider"] != {"type": "LOCAL", "status": "READY"}:
        raise BootstrapVerificationError("provider baseline mismatch")
    if installation["coherence"] != {"status": "COHERENT"}:
        raise BootstrapVerificationError("coherence baseline mismatch")
    if installation["synchronization"] != {"state": "NOT_EVALUATED"}:
        raise BootstrapVerificationError("synchronization baseline mismatch")
    if installation["recovery"] != {"status": recovery.get("status")}:
        raise BootstrapVerificationError("recovery manifest mismatch")
    if installation["protocol_associations"] != [] or installation["cpg_protocol"]["status"] != "NOT_INSTALLED":
        raise BootstrapVerificationError("installation protocol isolation failed")

    if integrity.get("algorithm") != "SHA-256":
        raise BootstrapVerificationError("unsupported integrity algorithm")
    expected = integrity.get("artifacts", {})
    if set(expected) != set(ARTIFACTS):
        raise BootstrapVerificationError("integrity artifact set mismatch")
    for relative in ARTIFACTS:
        if expected.get(relative) != sha256_file(target / relative):
            raise BootstrapVerificationError(f"bootstrap artifact integrity failure: {relative}")

    return {"status": "VERIFIED", "state": state["state"], "integrity": "VERIFIED"}


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        raise SystemExit("usage: bootstrap_verifier.py <target-directory>")
    try:
        result = verify(Path(sys.argv[1]))
    except BootstrapVerificationError as exc:
        print(f"BOOTSTRAP VERIFICATION FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print(json.dumps(result, sort_keys=True))
