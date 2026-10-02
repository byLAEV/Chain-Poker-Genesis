#!/usr/bin/env python3
"""Canonical Node Core object synchronization between local storage and Kubo MFS.

This module extends manifest synchronization to registered Node Core objects.
It does not install Kubo, activate CPG, or implement peer-to-peer replication.
"""
from __future__ import annotations

import hashlib
import json
import secrets
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from object_registry import ObjectRegistry, RegistryError

MFS_ROOT = "/node-storage"


class ObjectSynchronizationError(RuntimeError):
    pass


@dataclass(frozen=True)
class ObjectSynchronizationResult:
    object_id: str
    content_hash: str
    version: str
    cid: str
    location_state: str
    synchronization_state: str


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_json(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


class KuboObjectSync:
    """Synchronize one registered local object into Kubo MFS and verify it."""

    def __init__(self, node_root: Path, kubo_api: str, timeout: float = 5.0) -> None:
        self.node_root = Path(node_root).resolve()
        self.api_base = kubo_api.rstrip("/")
        self.timeout = timeout
        self.registry = ObjectRegistry(self.node_root)

    def _request(
        self,
        endpoint: str,
        *,
        params: dict[str, str],
        data: bytes = b"",
        multipart: bool = False,
    ) -> bytes:
        query = urllib.parse.urlencode(params)
        headers = {}
        body = data
        if multipart:
            boundary = "----CPGKubo" + secrets.token_hex(12)
            headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
            body = (
                f"--{boundary}\r\n"
                'Content-Disposition: form-data; name="file"; filename="object"\r\n'
                "Content-Type: application/octet-stream\r\n\r\n"
            ).encode("ascii") + data + f"\r\n--{boundary}--\r\n".encode("ascii")
        request = urllib.request.Request(
            f"{self.api_base}/api/v0/{endpoint}?{query}",
            data=body,
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                if response.status >= 300:
                    raise ObjectSynchronizationError(f"Kubo API returned HTTP {response.status}")
                return response.read()
        except urllib.error.HTTPError as exc:
            response_body = exc.read().decode("utf-8", errors="replace").strip()
            detail = f": {response_body}" if response_body else ""
            raise ObjectSynchronizationError(
                f"Kubo API returned HTTP {exc.code}{detail}"
            ) from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            raise ObjectSynchronizationError(f"Kubo API unavailable: {exc}") from exc

    def _entry(self, object_id: str) -> dict:
        try:
            return self.registry.get(object_id)
        except RegistryError as exc:
            raise ObjectSynchronizationError(str(exc)) from exc

    def _local_bytes(self, entry: dict) -> bytes:
        path = (self.node_root / entry["relative_path"]).resolve()
        if self.node_root not in path.parents or not path.is_file():
            raise ObjectSynchronizationError("registered local object is unavailable")
        data = path.read_bytes()
        if _sha256(data) != entry["content_hash"]:
            raise ObjectSynchronizationError("local object hash does not match registry")
        return data

    @staticmethod
    def _mfs_path(entry: dict) -> str:
        relative = entry["relative_path"].replace("\\", "/").lstrip("/")
        return f"{MFS_ROOT}/{relative.removeprefix('node-storage/')}"

    def _write(self, path: str, data: bytes) -> None:
        self._request(
            "files/write",
            params={"arg": path, "create": "true", "parents": "true", "truncate": "true"},
            data=data,
            multipart=True,
        )

    def _stat(self, path: str) -> dict:
        raw = self._request("files/stat", params={"arg": path, "hash": "true"})
        try:
            return json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ObjectSynchronizationError("Kubo returned an invalid files/stat response") from exc

    def _read(self, path: str) -> bytes:
        return self._request("files/read", params={"arg": path})

    def _stat_optional(self, path: str) -> dict | None:
        try:
            return self._stat(path)
        except ObjectSynchronizationError as exc:
            message = str(exc)
            if "HTTP 404" in message:
                return None
            if "HTTP 500" in message:
                detail = message.lower()
                if "file does not exist" in detail or "path does not exist" in detail:
                    return None
            raise

    def _mark_conflict(self, object_id: str, *, cid: str, version: str) -> None:
        self.registry.record_conflict(object_id, cid=cid)

    def synchronize(self, object_id: str) -> ObjectSynchronizationResult:
        entry = self._entry(object_id)
        data = self._local_bytes(entry)
        local_hash = _sha256(data)
        mfs_path = self._mfs_path(entry)

        existing = self._stat_optional(mfs_path)
        if existing is not None:
            remote = self._read(mfs_path)
            remote_hash = _sha256(remote)
            remote_cid = existing.get("Hash")
            if not isinstance(remote_cid, str) or not remote_cid:
                raise ObjectSynchronizationError("Kubo returned an invalid existing object CID")
            if remote_hash != local_hash:
                self._mark_conflict(
                    object_id,
                    cid=remote_cid,
                    version=entry["storage_version"],
                )
                raise ObjectSynchronizationError(
                    "distributed object diverges from local canonical content; conflict recorded"
                )
            cid = remote_cid
        else:
            self._write(mfs_path, data)
            remote = self._read(mfs_path)
            remote_hash = _sha256(remote)
            if remote_hash != local_hash:
                raise ObjectSynchronizationError("remote object hash mismatch after synchronization")
            stat = self._stat(mfs_path)
            cid = stat.get("Hash")
            if not isinstance(cid, str) or not cid:
                raise ObjectSynchronizationError("Kubo did not return an object CID")

        self.registry.update_distribution_state(
            object_id,
            cid=cid,
            version=entry["storage_version"],
            location_state="LOCAL_AND_DISTRIBUTED",
            synchronization_state="SYNCHRONIZED",
        )

        return ObjectSynchronizationResult(
            object_id=object_id,
            content_hash=local_hash,
            version=entry["storage_version"],
            cid=cid,
            location_state="LOCAL_AND_DISTRIBUTED",
            synchronization_state="SYNCHRONIZED",
        )


    def synchronize_all(self) -> list[ObjectSynchronizationResult]:
        results = []
        for object_id in sorted(self.registry.entries):
            results.append(self.synchronize(object_id))
        return results


def synchronize_object(node_root: Path, kubo_api: str, object_id: str) -> ObjectSynchronizationResult:
    return KuboObjectSync(node_root, kubo_api).synchronize(object_id)
