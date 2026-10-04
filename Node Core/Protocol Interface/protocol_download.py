"""Download boundary for protocol packages.

This module performs transport only. Verification and installation remain
owned by Protocol Interface after the package reaches the local protocol area.
"""
from __future__ import annotations
from pathlib import Path
from urllib.request import Request, urlopen
import hashlib
import shutil

MAX_DOWNLOAD_BYTES = 256 * 1024 * 1024


class ProtocolDownloadBoundary:
    def __init__(self, protocols_root):
        self.protocols_root = Path(protocols_root)
        self.protocols_root.mkdir(parents=True, exist_ok=True)

    def download(self, source, filename=None):
        if not source.download_url.startswith(("https://", "http://")):
            raise ValueError("unsupported download scheme")
        name = filename or Path(source.download_url.split("?", 1)[0]).name
        if not name or name in {".", ".."}:
            raise ValueError("download filename is invalid")
        destination = self.protocols_root / name
        request = Request(
            source.download_url,
            headers={"User-Agent": "Chain-Poker-Genesis-Node-Core-Protocol-Downloader/1.0"},
        )
        total = 0
        with urlopen(request, timeout=30) as response, destination.open("wb") as output:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_DOWNLOAD_BYTES:
                    output.close()
                    destination.unlink(missing_ok=True)
                    raise ValueError("protocol package exceeds download limit")
                output.write(chunk)
        return destination

    @staticmethod
    def sha256(path):
        digest = hashlib.sha256()
        with Path(path).open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def verify_hash(self, path, expected_hash):
        if not expected_hash:
            raise ValueError("expected manifest/package hash is required")
        return self.sha256(path).lower() == expected_hash.lower()
