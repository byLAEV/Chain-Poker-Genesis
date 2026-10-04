#!/usr/bin/env python3
"""Official Kubo release metadata and artifact source boundary."""
from __future__ import annotations
import json
import re
from dataclasses import dataclass
from urllib import request, parse

class KuboSourceError(RuntimeError):
    pass

@dataclass(frozen=True)
class KuboArtifact:
    version: str
    os: str
    architecture: str
    filename: str
    download_url: str
    checksum_url: str
    checksum_algorithm: str = "sha512"

class OfficialKuboReleaseSource:
    BASE_URL = "https://dist.ipfs.tech/kubo"
    MAX_METADATA_BYTES = 4 * 1024 * 1024

    def __init__(self, *, opener=None, timeout: float = 15.0):
        self.opener = opener or request.urlopen
        self.timeout = timeout

    def _get_bytes(self, url: str) -> bytes:
        if not url.startswith(self.BASE_URL + "/"):
            raise KuboSourceError("URL outside official Kubo distribution root")
        response = self.opener(url, timeout=self.timeout)
        try:
            chunks, total = [], 0
            while True:
                chunk = response.read(64 * 1024)
                if not chunk: break
                total += len(chunk)
                if total > self.MAX_METADATA_BYTES:
                    raise KuboSourceError("metadata exceeds size limit")
                chunks.append(chunk)
            return b"".join(chunks)
        finally:
            response.close()

    def list_stable_versions(self) -> list[str]:
        raw = self._get_bytes(self.BASE_URL + "/versions").decode("utf-8")
        versions = [v for v in (x.strip() for x in raw.splitlines())
                    if re.fullmatch(r"v\d+\.\d+\.\d+", v)]
        if not versions:
            raise KuboSourceError("no stable versions in official response")
        return versions

    def latest_stable_version(self) -> str:
        return max(self.list_stable_versions(), key=self._version_key)

    def release_metadata(self, version: str) -> dict:
        self._validate_version(version)
        url = f"{self.BASE_URL}/{parse.quote(version, safe='')}/dist.json"
        try:
            return json.loads(self._get_bytes(url).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise KuboSourceError("invalid official dist.json") from exc

    def artifact(self, version: str, *, os_name: str, architecture: str) -> KuboArtifact:
        self.release_metadata(version)
        ext = "tar.gz" if os_name == "linux" else "zip"
        filename = f"kubo_{version}_{os_name}-{architecture}.{ext}"
        base = f"{self.BASE_URL}/{parse.quote(version, safe='')}"
        return KuboArtifact(version, os_name, architecture, filename,
                            f"{base}/{parse.quote(filename, safe='')}",
                            f"{base}/{parse.quote(filename, safe='')}.sha512")

    @staticmethod
    def _validate_version(version: str) -> None:
        if not re.fullmatch(r"v\d+\.\d+\.\d+", version or ""):
            raise KuboSourceError("stable version must match vMAJOR.MINOR.PATCH")

    @staticmethod
    def _version_key(version: str) -> tuple[int, int, int]:
        return tuple(int(x) for x in version.lstrip("v").split("."))
