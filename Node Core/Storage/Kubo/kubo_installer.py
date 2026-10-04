#!/usr/bin/env python3
"""Install a previously verified Kubo package without initializing its repository."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import tarfile
import tempfile
from pathlib import Path


class KuboInstallationError(RuntimeError):
    pass


class KuboInstaller:
    def __init__(self, *, path_manager):
        self.path_manager = path_manager

    def install(self, package: str | Path, *, version: str, expected_sha512: str) -> dict:
        package = Path(package).resolve()
        if not package.is_file():
            raise KuboInstallationError("verified package does not exist")
        digest = self._sha512(package)
        if digest.lower() != expected_sha512.lower():
            raise KuboInstallationError("verified package integrity mismatch")

        paths = self.path_manager.paths(version)
        self.path_manager.validate(paths)
        if paths.release_root.exists():
            raise KuboInstallationError("release directory already exists")

        staging = paths.release_root.parent / f".{version}.installing"
        if staging.exists():
            shutil.rmtree(staging)
        staging.mkdir(parents=True)

        try:
            self._extract_safe(package, staging)
            executable = self._find_executable(staging)
            reported_version = self._read_version(executable)
            if reported_version != version:
                raise KuboInstallationError(
                    f"executable version mismatch: expected {version}, got {reported_version}"
                )

            # Kubo archives commonly contain a single top-level kubo/ directory.
            source_root = self._normalize_archive_root(staging)
            source_root.rename(paths.release_root)
            installation = {
                "manifest_type": "KUBO-INSTALLATION-MANIFEST",
                "manifest_version": "1.0.0",
                "provider": "Kubo",
                "version": version,
                "package_sha512": digest,
                "installation_root": str(paths.release_root),
                "executable_path": str(paths.release_root / self._relative_executable(source_root, executable)),
                "repository_path": str(paths.repository),
                "ipfs_path": str(paths.ipfs_path),
                "status": "INSTALLED",
            }
            manifest_path = paths.release_root / "installation-manifest.json"
            manifest_path.write_text(json.dumps(installation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            return installation
        except Exception:
            if staging.exists():
                shutil.rmtree(staging)
            if paths.release_root.exists():
                shutil.rmtree(paths.release_root)
            raise

    @staticmethod
    def _sha512(path: Path) -> str:
        digest = hashlib.sha512()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    @staticmethod
    def _extract_safe(package: Path, destination: Path) -> None:
        if package.suffixes[-2:] != [".tar", ".gz"]:
            raise KuboInstallationError("Linux installer requires a .tar.gz Kubo package")
        root = destination.resolve()
        with tarfile.open(package, "r:gz") as archive:
            for member in archive.getmembers():
                target = (root / member.name).resolve()
                try:
                    target.relative_to(root)
                except ValueError as exc:
                    raise KuboInstallationError("archive path traversal detected") from exc
                if member.issym() or member.islnk():
                    link_target = (target.parent / member.linkname).resolve()
                    try:
                        link_target.relative_to(root)
                    except ValueError as exc:
                        raise KuboInstallationError("unsafe archive link detected") from exc
            archive.extractall(root)

    @staticmethod
    def _normalize_archive_root(staging: Path) -> Path:
        entries = list(staging.iterdir())
        if len(entries) == 1 and entries[0].is_dir():
            return entries[0]
        return staging

    @staticmethod
    def _find_executable(root: Path) -> Path:
        candidates = [p for p in root.rglob("ipfs") if p.is_file()]
        if len(candidates) != 1:
            raise KuboInstallationError("Kubo archive must contain exactly one ipfs executable")
        return candidates[0]

    @staticmethod
    def _read_version(executable: Path) -> str:
        import subprocess
        try:
            result = subprocess.run(
                [str(executable), "version", "--number"],
                check=True, capture_output=True, text=True, timeout=10,
                env={**os.environ, "IPFS_PATH": str(executable.parent / ".installation-check")},
            )
        except (OSError, subprocess.SubprocessError) as exc:
            raise KuboInstallationError("unable to verify Kubo executable version") from exc
        value = result.stdout.strip()
        if not value.startswith("v"):
            value = "v" + value
        return value

    @staticmethod
    def _relative_executable(root: Path, executable: Path) -> Path:
        return executable.relative_to(root)
