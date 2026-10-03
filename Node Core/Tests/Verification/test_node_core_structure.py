import subprocess
import sys
import unittest
from pathlib import Path


NODE_CORE = Path(__file__).resolve().parents[2]
REPO_ROOT = NODE_CORE.parent


class TestNodeCoreStructure(unittest.TestCase):
    def test_structural_audit_passes(self):
        script = REPO_ROOT / "scripts" / "node_core_audit.py"
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
