import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from Installer import install


class TermuxCryptographyDependencyTests(unittest.TestCase):
    def test_termux_uses_native_cryptography_and_system_site_packages(self):
        calls = []

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            staging = root / "staging"
            cryptography_dir = staging / "Cryptography"
            cryptography_dir.mkdir(parents=True)
            (cryptography_dir / "requirements.txt").write_text(
                "cryptography==46.0.4\n",
                encoding="utf-8",
            )

            environment = root / ".node-core-python"

            def fake_run(command, **kwargs):
                calls.append(command)
                if command[:3] == [install.sys.executable, "-m", "venv"]:
                    (environment / "bin").mkdir(parents=True)
                    (environment / "bin" / "python").write_text(
                        "#!/bin/sh\n",
                        encoding="utf-8",
                    )
                return type(
                    "Completed",
                    (),
                    {"returncode": 0, "stdout": "46.0.4\n", "stderr": ""},
                )()

            with patch.object(install, "detect_platform", return_value="TERMUX"), \
                 patch.object(
                     install.shutil,
                     "which",
                     return_value="/data/data/com.termux/files/usr/bin/pkg",
                 ), \
                 patch.object(install.subprocess, "run", side_effect=fake_run):
                result = install.prepare_python_environment(staging, root)

        self.assertEqual(result, environment / "bin/python")
        self.assertEqual(
            calls[0],
            [
                "/data/data/com.termux/files/usr/bin/pkg",
                "install",
                "-y",
                "python-cryptography",
            ],
        )
        self.assertEqual(
            calls[1],
            [
                install.sys.executable,
                "-m",
                "venv",
                "--system-site-packages",
                str(environment),
            ],
        )
        self.assertEqual(
            calls[2][0],
            str(environment / "bin/python"),
        )
        self.assertEqual(calls[2][1], "-c")
        self.assertIn("AESGCM.generate_key", calls[2][2])
        self.assertIn("Ed25519PrivateKey.generate", calls[2][2])
        self.assertIn("ssl.OPENSSL_VERSION", calls[2][2])
        self.assertEqual(len(calls[2]), 3)

        pip_commands = [
            command
            for command in calls
            if "pip" in command
        ]
        self.assertEqual(
            pip_commands,
            [],
            "Termux must not attempt a pip cryptography source build",
        )

    def test_termux_requires_native_package_manager(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            cryptography_dir = root / "staging" / "Cryptography"
            cryptography_dir.mkdir(parents=True)
            (cryptography_dir / "requirements.txt").write_text(
                "cryptography==46.0.4\n",
                encoding="utf-8",
            )

            with patch.object(install, "detect_platform", return_value="TERMUX"), \
                 patch.object(install.shutil, "which", return_value=None):
                with self.assertRaises(install.InstallationError):
                    install.prepare_python_environment(root / "staging", root)


if __name__ == "__main__":
    unittest.main()
