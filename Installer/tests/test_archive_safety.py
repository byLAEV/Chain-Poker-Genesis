import tarfile
import unittest
from pathlib import Path

from Installer.install import InstallationError, _safe_archive_member


class ArchiveSafetyTests(unittest.TestCase):
    def setUp(self):
        self.prefix = Path("package") / "Node Core"

    def member(self, name, kind="file"):
        info = tarfile.TarInfo(name)
        if kind == "symlink":
            info.type = tarfile.SYMTYPE
            info.linkname = "/tmp/outside"
        return info

    def test_normal_member_is_accepted(self):
        member = self.member("package/Node Core/Bootstrap/Installer/bootstrap_node.py")
        self.assertEqual(
            _safe_archive_member(member, self.prefix),
            Path("Bootstrap/Installer/bootstrap_node.py"),
        )

    def test_path_traversal_is_rejected(self):
        member = self.member("package/Node Core/../../outside.txt")
        with self.assertRaises(InstallationError):
            _safe_archive_member(member, self.prefix)

    def test_absolute_path_is_rejected(self):
        member = self.member("package/Node Core//etc/passwd")
        with self.assertRaises(InstallationError):
            _safe_archive_member(member, self.prefix)

    def test_symlink_is_rejected(self):
        member = self.member("package/Node Core/unsafe-link", "symlink")
        with self.assertRaises(InstallationError):
            _safe_archive_member(member, self.prefix)


if __name__ == "__main__":
    unittest.main()
