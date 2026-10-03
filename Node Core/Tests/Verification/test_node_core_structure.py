import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class TestNodeCoreStructure(unittest.TestCase):
    def test_structural_audit_passes(self):
        script = ROOT.parent.parent / "scripts" / "node_core_audit.py"
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd=ROOT.parent.parent,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
