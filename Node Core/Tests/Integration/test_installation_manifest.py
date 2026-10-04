#!/usr/bin/env python3
"""Validate the canonical Node Core installation manifest baseline."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE / "Tools/Validation"))
from validate_installation_manifest_schema import validate

EXPECTED = {
    ("node", "status"): "READY",
    ("readiness", "state"): "NODE_CORE_READY",
    ("provider", "type"): "LOCAL",
    ("provider", "status"): "READY",
    ("coherence", "status"): "COHERENT",
    ("synchronization", "state"): "NOT_EVALUATED",
    ("recovery", "status"): "READY",
    ("integrity", "status"): "VERIFIED",
    ("cpg_protocol", "status"): "NOT_INSTALLED",
}

def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else Path("/tmp/cpg-node-manifest-test")
    if root.exists():
        import shutil
        shutil.rmtree(root)

    subprocess.run(
        [sys.executable, str(Path(__file__).resolve().parents[2] / "Bootstrap/Installer/bootstrap_node.py"), str(root)],
        check=True,
        cwd=Path(__file__).resolve().parents[2],
    )

    manifest_path = root / "node-installation-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    for path, expected in EXPECTED.items():
        value = manifest
        for key in path:
            value = value[key]
        if value != expected:
            raise AssertionError(f"{'.'.join(path)}: expected {expected}, got {value!r}")

    if manifest["protocol_associations"] != []:
        raise AssertionError("protocol_associations must be empty")

    schema_path = BASE / "Configuration/Schemas/node-core-installation-manifest.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validate(manifest, schema)

    print("manifest_status = VALID")
    print("node_core = READY")
    print("cpg_protocol = NOT_INSTALLED")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
