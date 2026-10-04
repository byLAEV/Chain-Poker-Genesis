"""Local protocol package verification and persistent installation boundary."""
from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
import zipfile
from pathlib import Path

from protocol_manifest_validator import validate_manifest


class ProtocolPackageVerifier:
    MANIFEST_NAME = "PROTOCOL-MANIFEST.json"

    def __init__(self, protocols_root):
        self.protocols_root = Path(protocols_root)
        self.protocols_root.mkdir(parents=True, exist_ok=True)
        self.installed_root = self.protocols_root / "Installed"
        self.installed_root.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def canonical_manifest_bytes(manifest):
        return json.dumps(
            manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")

    @classmethod
    def manifest_hash(cls, manifest):
        return hashlib.sha256(cls.canonical_manifest_bytes(manifest)).hexdigest()

    def _read_manifest(self, package_path):
        path = Path(package_path)
        if path.is_dir():
            manifest_path = path / self.MANIFEST_NAME
            if not manifest_path.is_file():
                raise ValueError("protocol manifest not found")
            with manifest_path.open("r", encoding="utf-8") as handle:
                return json.load(handle)

        if not zipfile.is_zipfile(path):
            raise ValueError("protocol package must be a directory or ZIP archive")

        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            if self.MANIFEST_NAME not in names:
                raise ValueError("protocol manifest not found")
            with archive.open(self.MANIFEST_NAME) as handle:
                return json.loads(handle.read().decode("utf-8"))

    def verify(self, package_path):
        manifest = self._read_manifest(package_path)
        validate_manifest(manifest)
        actual_hash = self.manifest_hash(manifest)
        declared_hash = manifest["manifest_hash"].lower()
        if declared_hash != actual_hash:
            raise ValueError("protocol manifest hash mismatch")
        return manifest

    def install(self, package_path, protocol_id):
        manifest = self.verify(package_path)
        if manifest["protocol_id"] != protocol_id:
            raise ValueError("protocol identity does not match installation target")

        destination = self.installed_root / protocol_id
        if destination.exists():
            raise FileExistsError("protocol is already installed")

        source = Path(package_path)
        staging = Path(tempfile.mkdtemp(prefix=".protocol-", dir=self.installed_root))
        try:
            if source.is_dir():
                shutil.copytree(source, staging / source.name)
                payload = staging / source.name
            else:
                payload = staging / "package.zip"
                shutil.copy2(source, payload)
            (staging / "INSTALLATION-MANIFEST.json").write_text(
                json.dumps(
                    {
                        "protocol_id": manifest["protocol_id"],
                        "version": manifest["version"],
                        "manifest_hash": manifest["manifest_hash"],
                    },
                    sort_keys=True,
                    indent=2,
                ) + "\n",
                encoding="utf-8",
            )
            staging.replace(destination)
        except Exception:
            shutil.rmtree(staging, ignore_errors=True)
            raise
        return destination
