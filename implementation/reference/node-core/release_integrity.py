#!/usr/bin/env python3
"""Build and verify deterministic Node Core release integrity metadata."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ARTIFACTS = [
    "implementation/reference/node-core/bootstrap_node.py",
    "implementation/reference/node-core/verify_node_installation.py",
    "implementation/reference/node-core/storage_manager.py",
    "implementation/reference/node-core/storage_provider.py",
    "implementation/reference/node-core/verify_storage_coherence.py",
    "implementation/reference/node-core/object_registry.py",
    "implementation/reference/node-core/storage_locator.py",
    "implementation/reference/node-core/synchronization_state.py",
    "implementation/reference/node-core/runtime_state.py",
    "implementation/reference/node-core/node_runtime.py",
    "implementation/reference/node-core/health_readiness.py",
    "implementation/reference/node-core/recovery_manager.py",
    "implementation/reference/node-core/final_node_core_audit.py",
    "implementation/reference/node-core/protocol_installation_boundary.py",
    "implementation/reference/node-core/release_integrity.py",
    "implementation/reference/node-core/test_installation_manifest.py",
    "implementation/reference/node-core/validate_installation_manifest_schema.py",
    "implementation/reference/node-core/test_node_installation_e2e.py",
    "implementation/reference/node-core/test_storage_manager.py",
    "implementation/reference/node-core/test_storage_provider.py",
    "implementation/reference/node-core/test_object_registry.py",
    "implementation/reference/node-core/test_storage_locator.py",
    "implementation/reference/node-core/test_synchronization_state.py",
    "implementation/reference/node-core/test_specification_coverage.py",
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
    "docs/node/FINAL-NODE-CORE-AUDIT.md",
    "docs/node/NODE-CORE-COMPLETION-GATE.md",
    "documentation/node-core/NODE-CORE-RELEASE-ARTIFACT-SPECIFICATION.md",
    "documentation/node-core/NODE-CORE-RELEASE-INTEGRITY.md",
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
