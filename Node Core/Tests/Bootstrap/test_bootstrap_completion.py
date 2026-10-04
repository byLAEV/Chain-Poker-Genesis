#!/usr/bin/env python3
"""Bootstrap P0 acceptance matrix.

This test suite treats Bootstrap as complete only when the canonical execution
path, schema, cross-manifest consistency, recovery, isolation and integration
boundaries are executable and reject representative invalid states.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
INSTALLER = BASE / "Bootstrap/Installer/bootstrap_node.py"
COORDINATOR = BASE / "Bootstrap/bootstrap.py"
VERIFIER = BASE / "Bootstrap/Verification/bootstrap_verifier.py"
RECOVERY = BASE / "Bootstrap/Recovery/bootstrap_recovery.py"
VALIDATOR = BASE / "Tools/Validation/validate_installation_manifest_schema.py"
SCHEMA = BASE / "Configuration/Schemas/node-core-installation-manifest.schema.json"


def run(script: Path, root: Path, expect=0):
    p = subprocess.run([sys.executable, str(script), str(root)], cwd=BASE, text=True,
                       capture_output=True)
    if p.returncode != expect:
        raise AssertionError(f"{script.name}: expected {expect}, got {p.returncode}\n{p.stdout}\n{p.stderr}")
    return p


def load(root, relative):
    return json.loads((root / relative).read_text(encoding="utf-8"))


def dump(root, relative, value):
    path = root / relative
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main():
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp) / "node"

        # 1. Canonical public execution path.
        probe = subprocess.run(
            [sys.executable, "-c",
             "import sys; sys.path.insert(0, sys.argv[1]); "
             "from Bootstrap.bootstrap import Bootstrap; "
             "print(Bootstrap().bootstrap(sys.argv[2])['status'])",
             str(BASE), str(base)],
            cwd=BASE, text=True, capture_output=True,
        )
        assert probe.returncode == 0, probe.stderr
        assert "VERIFIED" in probe.stdout

        # 2. Canonical schema validation.
        run(VALIDATOR, base)

        # 3. Cross-manifest consistency must be enforced.
        manifest = load(base, "node-installation-manifest.json")
        manifest["storage"]["storage_structure_version"] = "9.9.9"
        dump(base, "node-installation-manifest.json", manifest)
        run(VERIFIER, base, expect=1)
        shutil.rmtree(base)
        run(INSTALLER, base)

        # 4. Identity boundary: Bootstrap initializes metadata but never private keys.
        identity = load(base, "node-storage/identity/node-identity.json")
        assert identity["identity_status"] == "INITIALIZED"
        assert "private_key" not in identity and "private_key_hex" not in identity

        # 5. Protocol isolation is fail-closed.
        config = load(base, "node-storage/configuration/node-config.json")
        config["cpg_protocol"] = "INSTALLED"
        dump(base, "node-storage/configuration/node-config.json", config)
        run(VERIFIER, base, expect=1)
        shutil.rmtree(base)
        run(INSTALLER, base)

        # 6. Recovery from incomplete installation.
        (base / "node-installation-manifest.json").unlink()
        run(RECOVERY, base)
        run(VERIFIER, base)

        # 7. Recovery from malformed installation is not silently accepted.
        manifest = base / "node-installation-manifest.json"
        manifest.write_text("{not-json", encoding="utf-8")
        run(RECOVERY, base, expect=1)
        shutil.rmtree(base)
        run(INSTALLER, base)

        # 8. Idempotent existing installation.
        first = run(INSTALLER, base)
        assert "VALID_EXISTING_INSTALLATION" in first.stdout

        # 9. Missing required path is detected.
        shutil.rmtree(base / "node-storage/protocol")
        run(VERIFIER, base, expect=1)
        shutil.rmtree(base)
        run(INSTALLER, base)

        # 10. Integrity mutation is detected.
        state = base / "node-storage/state/node-state.json"
        state.write_text(json.dumps({"state": "CORRUPTED"}) + "\n", encoding="utf-8")
        run(VERIFIER, base, expect=1)

    print("bootstrap_p0_matrix = PASS")
    print("bootstrap_completion = 100%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
