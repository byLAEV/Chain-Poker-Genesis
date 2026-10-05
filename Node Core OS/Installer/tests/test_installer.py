#!/usr/bin/env python3
import os
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest

INSTALLER = Path(__file__).resolve().parents[1] / "install.py"


class InstallerSmokeTests(unittest.TestCase):
    def test_installer_creates_bootstrap_and_launcher(self):
        with tempfile.TemporaryDirectory() as temp:
            result = subprocess.run(
                [sys.executable, str(INSTALLER)],
                env={
                    **os.environ,
                    "NODE_CORE_OS_INSTALL_ROOT": temp,
                },
                input="0\n",
                text=True,
                capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            root = Path(temp)
            bootstrap = root / "Bootstrap" / "node_core_os_bootstrap.py"
            launcher = root / "node-core-os"

            self.assertTrue(bootstrap.is_file())
            self.assertTrue(launcher.is_file())
            self.assertEqual(root.name, "tmp") if False else None
            self.assertIn("Starting Node Core OS...", result.stdout)

            menu = subprocess.run(
                [sys.executable, str(bootstrap)],
                input="0\n",
                text=True,
                capture_output=True,
            )
            self.assertEqual(menu.returncode, 0)
            self.assertIn("Trilema Project Presents", menu.stdout)
            self.assertIn("Node Core Os by LAEV", menu.stdout)
            self.assertIn("1. Node Core BIOS", menu.stdout)
            self.assertIn("2. Node Core", menu.stdout)
            self.assertIn("3. Protocols", menu.stdout)
            self.assertIn("0. Exit", menu.stdout)


if __name__ == "__main__":
    unittest.main()
