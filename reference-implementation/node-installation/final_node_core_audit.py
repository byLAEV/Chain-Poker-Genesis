#!/usr/bin/env python3
"""Final Node Core audit and completion gate."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

BASE = Path(__file__).resolve().parent

def run(script: str, root: Path) -> None:
    subprocess.run([sys.executable, str(BASE / script), str(root)], check=True)

def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "node"

        run("bootstrap_node.py", root)
        run("verify_node_installation.py", root)
        run("verify_storage_coherence.py", root)
        run("test_installation_manifest.py", root)
        subprocess.run([sys.executable, str(BASE / "test_node_installation_e2e.py")], check=True)

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
        print("completion_gate = NODE_CORE_COMPLETE")
        print("protocol_associations = []")
        print("cpg_protocol = NOT_INSTALLED")
        print("synchronization = NOT_EVALUATED")
        return 0

if __name__ == "__main__":
    raise SystemExit(main())
