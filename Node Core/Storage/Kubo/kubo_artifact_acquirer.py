#!/usr/bin/env python3
"""Verified Kubo artifact acquisition. Never installs or executes Kubo."""
from __future__ import annotations
import hashlib, os, re, tempfile
from pathlib import Path
from urllib import request
from kubo_release_source import KuboArtifact, KuboSourceError

class KuboDownloadError(RuntimeError):
    pass

class KuboArtifactAcquirer:
    MAX_PACKAGE_BYTES = 512 * 1024 * 1024

    def __init__(self, *, opener=None, timeout: float = 30.0):
        self.opener = opener or request.urlopen
        self.timeout = timeout

    def fetch_expected_sha512(self, artifact: KuboArtifact) -> str:
        response = self.opener(artifact.checksum_url, timeout=self.timeout)
        try:
            raw = response.read(1024 * 1024).decode("utf-8")
        finally:
            response.close()
        match = re.search(r"([0-9a-fA-F]{128})", raw)
        if not match:
            raise KuboDownloadError("official SHA-512 sidecar contains no valid digest")
        return match.group(1).lower()

    def acquire(self, artifact: KuboArtifact, destination: str | Path, expected_sha512: str | None = None) -> Path:

        if expected_sha512 is None:
            expected_sha512 = self.fetch_expected_sha512(artifact)
        if not re.fullmatch(r"[0-9a-fA-F]{128}", expected_sha512):
            raise KuboDownloadError("expected SHA-512 must be 128 hex characters")
        dest = Path(destination).resolve()
        dest.mkdir(parents=True, exist_ok=True)
        final = dest / artifact.filename
        fd, temp_name = tempfile.mkstemp(prefix=".kubo-download-", dir=dest)
        digest = hashlib.sha512()
        total = 0
        try:
            with os.fdopen(fd, "wb") as out:
                response = self.opener(artifact.download_url, timeout=self.timeout)
                try:
                    while True:
                        chunk = response.read(1024 * 1024)
                        if not chunk: break
                        total += len(chunk)
                        if total > self.MAX_PACKAGE_BYTES:
                            raise KuboDownloadError("package exceeds size limit")
                        digest.update(chunk)
                        out.write(chunk)
                finally:
                    response.close()
                out.flush(); os.fsync(out.fileno())
            observed = digest.hexdigest().lower()
            if observed != expected_sha512.lower():
                raise KuboDownloadError("SHA-512 integrity mismatch")
            os.replace(temp_name, final)
            return final
        except Exception:
            if os.path.exists(temp_name): os.unlink(temp_name)
            raise

    def promote_verified(self, package: Path, verified_dir: str | Path) -> Path:
        package = Path(package).resolve()
        target_dir = Path(verified_dir).resolve()
        if not package.is_file(): raise KuboDownloadError("package does not exist")
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / package.name
        os.replace(package, target)
        return target
