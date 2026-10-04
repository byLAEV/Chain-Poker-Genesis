import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from Installer.install import InstallationError, install


class RollbackTests(unittest.TestCase):
    def test_failure_after_target_creation_removes_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "node-core"

            with patch("Installer.install.download_archive", side_effect=InstallationError("download failed")):
                with self.assertRaises(InstallationError):
                    install(target, "main")

            self.assertFalse(target.exists())

    def test_nonempty_target_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "node-core"
            target.mkdir()
            marker = target / "partial-file"
            marker.write_text("incomplete")

            with self.assertRaises(InstallationError):
                install(target, "main")

            self.assertTrue(marker.exists())
            self.assertEqual(marker.read_text(), "incomplete")

    def test_target_is_not_created_when_source_download_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "node-core"

            with patch("Installer.install.download_archive", side_effect=KeyboardInterrupt()):
                with self.assertRaises(KeyboardInterrupt):
                    install(target, "main")

            self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
