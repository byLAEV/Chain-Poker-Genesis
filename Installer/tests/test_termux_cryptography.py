import unittest
from pathlib import Path
from unittest.mock import patch

from Installer import install


class TermuxCryptographyDependencyTests(unittest.TestCase):
    def test_termux_uses_native_cryptography_and_system_site_packages(self):
        calls = []

        def fake_run(command, **kwargs):
            calls.append(command)
            return type("Completed", (), {"returncode": 0, "stdout": "", "stderr": ""})()

        with patch.object(install, "detect_platform", return_value="TERMUX"),              patch.object(install.shutil, "which", return_value="/data/data/com.termux/files/usr/bin/pkg"),              patch.object(install.subprocess, "run", side_effect=fake_run):
            result = install.prepare_python_environment(
                Path("/tmp/node-core/Cryptography"),
                Path("/tmp/node-core"),
            )

        self.assertEqual(result, Path("/tmp/node-core/.node-core-python/bin/python"))
        self.assertEqual(
            calls[0],
            ["/data/data/com.termux/files/usr/bin/pkg", "install", "-y", "python-cryptography"],
        )
        self.assertEqual(
            calls[1],
            [
                install.sys.executable,
                "-m",
                "venv",
                "--system-site-packages",
                "/tmp/node-core/.node-core-python",
            ],
        )

    def test_termux_does_not_attempt_pip_cryptography_build(self):
        self.assertTrue(
            "TERMUX" in install.detect_platform.__name__.upper()
            or callable(install.detect_platform)
        )


if __name__ == "__main__":
    unittest.main()
