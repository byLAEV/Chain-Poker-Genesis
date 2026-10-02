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
    "documentation/node-core/NODE-CORE-INSTALLATION-MANIFEST.md",
    "documentation/node-core/node-core-installation-manifest.schema.json",
    "documentation/node-core/NODE-CORE-RUNTIME-LIFECYCLE.md",
    "documentation/node-core/HEALTH-AND-READINESS-SPECIFICATION.md",
    "documentation/node-core/RECOVERY-INTEGRATION-SPECIFICATION.md",
    "documentation/node-core/STORAGE-MANAGER-SPECIFICATION.md",
    "documentation/node-core/STORAGE-PROVIDER-INTERFACE.md",
    "documentation/node-core/STORAGE-COHERENCE-SPECIFICATION.md",
    "documentation/node-core/OBJECT-REGISTRY-SPECIFICATION.md",
    "documentation/node-core/STORAGE-LOCATOR-SPECIFICATION.md",
    "documentation/node-core/SYNCHRONIZATION-STATE-MACHINE.md",
    "documentation/node-core/FINAL-NODE-CORE-AUDIT.md",
    "documentation/node-core/NODE-CORE-COMPLETION-GATE.md",
    "documentation/node-core/NODE-CORE-RELEASE-ARTIFACT-SPECIFICATION.md",
    "documentation/node-core/NODE-CORE-RELEASE-INTEGRITY.md",
    "documentation/node-core/PROTOCOL-INSTALLATION-BOUNDARY.md",
    "documentation/node-core/NODE-CORE-SPECIFICATION-COVERAGE-AUDIT.md",
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
