#!/usr/bin/env python3
"""Deterministic Local <-> Kubo synchronization primitives for Full Node Core.

This module synchronizes the canonical storage manifest only. It does not install
Kubo, activate CPG, or claim application-object replication is complete.
"""
from __future__ import annotations

import hashlib
import json
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

MANIFEST_MFS_PATH = "/node-storage/state/storage-manifest.json"


class SynchronizationError(RuntimeError):
    pass


@dataclass(frozen=True)
class SynchronizationResult:
    state: str
    local_hash: str
    remote_hash: str | None


def canonical_json(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def manifest_hash(manifest: object) -> str:
    return hashlib.sha256(canonical_json(manifest)).hexdigest()


def load_local_manifest(root: Path) -> dict:
    path = root / "node-storage/state/storage-manifest.json"
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SynchronizationError(f"local manifest unavailable: {exc}") from exc


class KuboManifestSync:
    """Minimal Kubo MFS client used only for canonical manifest synchronization."""

    def __init__(self, api_base: str, timeout: float = 5.0) -> None:
        self.api_base = api_base.rstrip("/")
        self.timeout = timeout

    def _request(self, endpoint: str, *, params: dict[str, str], data: bytes = b"") -> bytes:
        query = urllib.parse.urlencode(params)
        request = urllib.request.Request(
            f"{self.api_base}/api/v0/{endpoint}?{query}",
            data=data,
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                if response.status >= 300:
                    raise SynchronizationError(f"Kubo API returned HTTP {response.status}")
                return response.read()
        except (urllib.error.URLError, TimeoutError) as exc:
            raise SynchronizationError(f"Kubo synchronization API unavailable: {exc}") from exc

    def read_manifest(self) -> dict:
        raw = self._request("files/read", params={"arg": MANIFEST_MFS_PATH})
        try:
            return json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise SynchronizationError(f"remote manifest is invalid: {exc}") from exc

    def write_manifest(self, manifest: dict) -> None:
        self._request(
            "files/write",
            params={"arg": MANIFEST_MFS_PATH, "create": "true", "parents": "true", "truncate": "true"},
            data=canonical_json(manifest),
        )

    def synchronize_manifest(self, local_manifest: dict) -> SynchronizationResult:
        local_hash = manifest_hash(local_manifest)
        try:
            remote = self.read_manifest()
            remote_hash = manifest_hash(remote)
        except SynchronizationError:
            self.write_manifest(local_manifest)
            remote = self.read_manifest()
            remote_hash = manifest_hash(remote)
            if remote_hash != local_hash:
                raise SynchronizationError("remote manifest hash mismatch after write")
            return SynchronizationResult("SYNCED", local_hash, remote_hash)

        if remote_hash == local_hash:
            return SynchronizationResult("SYNCED", local_hash, remote_hash)

        self.write_manifest(local_manifest)
        remote = self.read_manifest()
        remote_hash = manifest_hash(remote)
        if remote_hash != local_hash:
            raise SynchronizationError("remote manifest hash mismatch after reconciliation")
        return SynchronizationResult("RECONCILED", local_hash, remote_hash)


def synchronize(root: Path, kubo_api: str) -> SynchronizationResult:
    return KuboManifestSync(kubo_api).synchronize_manifest(load_local_manifest(root))
