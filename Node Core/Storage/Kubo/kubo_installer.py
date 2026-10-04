#!/usr/bin/env python3
"""Install a previously verified Kubo distribution without starting it."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import tarfile
import tempfile
import zipfile
from pathlib import Path


class KuboInstallationError(RuntimeError):
    pass


class KuboPackageInstaller:
    """Safe extractor/installer for verified Kubo packages."""

    def install(
        self,
        package: str | Path,
        *,
        paths,
        version: str,
        expected_sha512: str,
        platform: str = "linux",
        architecture: str = "amd64",
    ) -> Path:
        package = Path(package).resolve()
        if not package.is_file():
            raise KuboInstallationError("verified package does not exist")
        observed = self._sha512(package)
        if observed != expected_sha512.lower():
            raise KuboInstallationError("package integrity changed after verification")

        if platform != "linux":
            raise KuboInstallationError("Linux installer is the current implementation target")
        if architecture not in {"amd64", "arm64"}:
            raise KuboInstallationError("unsupported Linux architecture")

        destination = paths.release_root
        paths.release_root.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            raise KuboInstallationError("versioned installation directory already exists")

        staging = Path(tempfile.mkdtemp(prefix=".kubo-install-", dir=destination.parent))
        try:
            extracted = staging / "payload"
            extracted.mkdir()
            self._extract_safe(package, extracted)

            root = self._locate_distribution_root(extracted, version)
            self._validate_executable(root)
            shutil.move(str(root), str(destination))

            executable = destination / "kubo" / "ipfs"
            if not executable.is_file():
                executable = destination / "ipfs"
            if not executable.is_file():
                raise KuboInstallationError("installed Kubo executable not found")

            manifest = {
                "manifest_type": "KUBO-ACTIVE-INSTALLATION-MANIFEST",
                "manifest_version": "1.0.0",
                "installation_id": hashlib.sha256(
                    f"{version}:{expected_sha512}".encode()
                ).hexdigest()[:32],
                "provider": "Kubo",
                "version": version,
                "platform": platform,
                "architecture": architecture,
                "package_sha512": expected_sha512.lower(),
                "installation_root": str(destination),
                "executable_path": str(executable),
                "repository_path": str(paths.repository),
                "ipfs_path": str(paths.ipfs_path),
                "repository_initialized": False,
                "process_started": False,
            }
            manifest_path = destination / "INSTALLATION-MANIFEST.json"
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
            return destination
        except Exception:
            if destination.exists():
                shutil.rmtree(destination, ignore_errors=True)
            raise
        finally:
            shutil.rmtree(staging, ignore_errors=True)

    @staticmethod
    def _sha512(path: Path) -> str:
        digest = hashlib.sha512()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    @staticmethod
    def _extract_safe(package: Path, destination: Path) -> None:
        name = package.name.lower()
        if name.endswith((".tar.gz", ".tgz", ".tar")):
            with tarfile.open(package, "r:*") as archive:
                base = destination.resolve()
                for member in archive.getmembers():
                    target = (destination / member.name).resolve()
                    try:
                        target.relative_to(base)
                    except ValueError as exc:
                        raise KuboInstallationError("archive path traversal detected") from exc
                    if member.issym() or member.islnk():
                        raise KuboInstallationError("archive links are not permitted")
                archive.extractall(destination)
        elif name.endswith(".zip"):
            with zipfile.ZipFile(package) as archive:
                base = destination.resolve()
                for member in archive.infolist():
                    target = (destination / member.filename).resolve()
                    try:
                        target.relative_to(base)
                    except ValueError as exc:
                        raise KuboInstallationError("archive path traversal detected") from exc
                archive.extractall(destination)
        else:
            raise KuboInstallationError("unsupported Kubo package format")

    @staticmethod
    def _locate_distribution_root(extracted: Path, version: str) -> Path:
        expected = extracted / f"kubo"
        if expected.is_dir():
            return expected
        candidates = [p for p in extracted.iterdir() if p.is_dir()]
        for candidate in candidates:
            if (candidate / "ipfs").is_file() or (candidate / "bin" / "ipfs").is_file():
                return candidate
        raise KuboInstallationError(f"no Kubo distribution root found for {version}")

    @staticmethod
    def _validate_executable(root: Path) -> None:
        executable = root / "ipfs"
        if not executable.is_file():
            executable = root / "bin" / "ipfs"
        if not executable.is_file():
            raise KuboInstallationError("Kubo executable missing")
        mode = executable.stat().st_mode
        if not mode & stat.S_IXUSR:
            raise KuboInstallationError("Kubo executable is not executable")
