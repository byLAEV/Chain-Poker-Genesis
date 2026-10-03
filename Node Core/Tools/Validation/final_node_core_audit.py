#!/usr/bin/env python3
"""Final Node Core audit and completion gate."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

VALIDATION_DIR = Path(__file__).resolve().parent
NODE_CORE = VALIDATION_DIR.parents[1]
TESTS = NODE_CORE / "Tests"
REPO_ROOT = NODE_CORE.parent

def run(script: Path, root: Path) -> None:
    subprocess.run([sys.executable, str(script), str(root)], check=True, cwd=REPO_ROOT)

def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "node"

        run(NODE_CORE / "Bootstrap/Installer/bootstrap_node.py", root)
        run(VALIDATION_DIR / "verify_node_installation.py", root)
        run(VALIDATION_DIR / "verify_storage_coherence.py", root)
        run(NODE_CORE / "Protocol Interface/Protocol Installation/protocol_installation_boundary.py", root)

        subprocess.run(
            [sys.executable, str(TESTS / "Integration/test_installation_manifest.py"), str(root)],
            check=True, cwd=REPO_ROOT
        )
        subprocess.run(
            [sys.executable, str(TESTS / "Integration/test_node_installation_e2e.py")],
            check=True, cwd=REPO_ROOT
        )

        manifest = json.loads((root / "node-installation-manifest.json").read_text(encoding="utf-8"))
        assert manifest["node"]["status"] == "READY"
        assert manifest["readiness"]["state"] == "NODE_CORE_READY"
        assert manifest["provider"] == {"type": "LOCAL", "status": "READY"}
        assert manifest["coherence"] == {"status": "COHERENT"}
        assert manifest["synchronization"] == {"state": "NOT_EVALUATED"}
        assert manifest["recovery"]["status"] == "READY"
        assert manifest["integrity"]["status"] == "VERIFIED"
        assert manifest["protocol_associations"] == []
        assert manifest["cpg_protocol"]["status"] == "NOT_INSTALLED"

        print("audit_status = PASS")
        print("completion_gate = NODE_CORE_IMPLEMENTATION_BASELINE")
        print("protocol_associations = []")
        print("cpg_protocol = NOT_INSTALLED")
        print("synchronization = NOT_EVALUATED")
        return 0

if __name__ == "__main__":
    raise SystemExit(main())
