#!/usr/bin/env python3
"""Build and verify deterministic Node Core release integrity metadata."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ARTIFACTS = [
    "reference-implementation/node-installation/bootstrap_node.py",
    "reference-implementation/node-installation/verify_node_installation.py",
    "reference-implementation/node-installation/storage_manager.py",
    "reference-implementation/node-installation/storage_provider.py",
    "reference-implementation/node-installation/verify_storage_coherence.py",
    "reference-implementation/node-installation/object_registry.py",
    "reference-implementation/node-installation/storage_locator.py",
    "reference-implementation/node-installation/synchronization_state.py",
    "reference-implementation/node-installation/runtime_state.py",
    "reference-implementation/node-installation/node_runtime.py",
    "reference-implementation/node-installation/health_readiness.py",
    "reference-implementation/node-installation/recovery_manager.py",
    "reference-implementation/node-installation/final_node_core_audit.py",
    "reference-implementation/node-installation/protocol_installation_boundary.py",
    "reference-implementation/node-installation/release_integrity.py",
    "reference-implementation/node-installation/test_installation_manifest.py",
    "reference-implementation/node-installation/validate_installation_manifest_schema.py",
    "reference-implementation/node-installation/test_node_installation_e2e.py",
    "reference-implementation/node-installation/test_storage_manager.py",
    "reference-implementation/node-installation/test_storage_provider.py",
    "reference-implementation/node-installation/test_object_registry.py",
    "reference-implementation/node-installation/test_storage_locator.py",
    "reference-implementation/node-installation/test_synchronization_state.py",
    "reference-implementation/node-installation/test_specification_coverage.py",
    "docs/node/NODE-CORE-INSTALLATION-MANIFEST.md",
    "docs/node/node-core-installation-manifest.schema.json",
    "docs/node/NODE-CORE-RUNTIME-LIFECYCLE.md",
    "docs/node/HEALTH-AND-READINESS-SPECIFICATION.md",
    "docs/node/RECOVERY-INTEGRATION-SPECIFICATION.md",
    "docs/node/STORAGE-MANAGER-SPECIFICATION.md",
    "docs/node/STORAGE-PROVIDER-INTERFACE.md",
    "docs/node/STORAGE-COHERENCE-SPECIFICATION.md",
    "docs/node/OBJECT-REGISTRY-SPECIFICATION.md",
    "docs/node/STORAGE-LOCATOR-SPECIFICATION.md",
    "docs/node/SYNCHRONIZATION-STATE-MACHINE.md",
    "docs/node/FINAL-NODE-CORE-AUDIT.md",
    "docs/node/NODE-CORE-COMPLETION-GATE.md",
    "docs/node/NODE-CORE-RELEASE-ARTIFACT-SPECIFICATION.md",
    "docs/node/NODE-CORE-RELEASE-INTEGRITY.md",
    "docs/node/PROTOCOL-INSTALLATION-BOUNDARY.md",
    "docs/node/NODE-CORE-SPECIFICATION-COVERAGE-AUDIT.md",
    ".github/workflows/node-installation-validation.yml",
]
def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> int:
    if len(sys.argv) != 2:
        print("usage: release_integrity.py <repository-root>")
        return 2

    root = Path(sys.argv[1]).resolve()
    entries = []
    for relative in ARTIFACTS:
        path = root / relative
        if not path.is_file():
            print("status = FAILED")
            print(f"reason = missing artifact: {relative}")
            return 1
        entries.append({"path": relative, "sha256": digest(path)})

    manifest = {
        "release_manifest_version": "0.1.0",
        "node_core_version": "0.1.0",
        "artifacts": entries,
        "protocol_boundary": {
            "protocol_associations": [],
            "cpg_protocol": "NOT_INSTALLED",
            "synchronization": "NOT_EVALUATED",
        },
    }

    output = root / "node-core-release-integrity.json"
    output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("status = VERIFIED")
    print("release_integrity = VERIFIED")
    print(f"artifact_count = {len(entries)}")
    print("cpg_protocol = NOT_INSTALLED")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
