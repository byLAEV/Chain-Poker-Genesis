#!/usr/bin/env python3
"""Complete protocol-neutral Node Core storage orchestration boundary.

Local storage is authoritative for writes. Kubo/IPFS is an optional mirror and
preferred read source when available. Any Kubo failure falls back to local.
Private/restricted distributed objects must be supplied as encrypted bytes;
this layer never owns encryption keys.
"""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any

from urllib import request, error

STORAGE_VERSION = "1.0.0"
STORAGE_CLASSES = {
    "temporary": "temporary",
    "public": "public",
    "private": "private",
    "restricted": "restricted",
    "personal": "personal",
    "protocol-reserved": "protocol",
}
LOCAL_STATES = {"LOCAL_ONLY", "LOCAL_AND_DISTRIBUTED", "MISSING_LOCAL", "CONFLICT", "QUARANTINED"}

class StorageError(Exception):
    pass


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n").encode()


class LocalStore:
    """Atomic local storage with canonical class directories."""
    def __init__(self, node_root: str | os.PathLike[str]):
        self.node_root = Path(node_root).resolve()
        self.root = self.node_root / "node-storage"
        self.registry_path = self.root / "state" / "object-registry.json"
        self.ensure_layout()

    def ensure_layout(self) -> None:
        for directory in STORAGE_CLASSES.values():
            (self.root / directory).mkdir(parents=True, exist_ok=True)
        (self.root / "state").mkdir(parents=True, exist_ok=True)
        (self.root / "recovery").mkdir(parents=True, exist_ok=True)
        if not self.registry_path.exists():
            self.registry_path.write_text("{}\n", encoding="utf-8")

    def _path(self, object_class: str, object_id: str) -> Path:
        if object_class not in STORAGE_CLASSES or object_class == "protocol-reserved":
            raise StorageError("unsupported or protocol-reserved storage class")
        if not object_id or "/" in object_id or "\\" in object_id or ".." in object_id:
            raise StorageError("invalid object id")
        path = (self.root / STORAGE_CLASSES[object_class] / f"{object_id}.bin").resolve()
        if self.root not in path.parents:
            raise StorageError("object path escapes storage root")
        return path

    def put(self, object_class: str, object_id: str, data: bytes) -> dict[str, Any]:
        path = self._path(object_class, object_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(prefix=f".{object_id}.", dir=path.parent)
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp, path)
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)
        digest = sha256(data)
        return {"object_id": object_id, "object_class": object_class, "relative_path": path.relative_to(self.node_root).as_posix(), "content_hash": digest, "storage_version": STORAGE_VERSION, "provider_type": "LOCAL", "location_state": "LOCAL_ONLY", "object_state": "PRESENT", "synchronization_state": "NOT_SYNCHRONIZED"}

    def get(self, object_class: str, object_id: str) -> tuple[bytes, dict[str, Any]]:
        path = self._path(object_class, object_id)
        if not path.is_file():
            raise StorageError("object not found locally")
        data = path.read_bytes()
        metadata = {"object_id": object_id, "object_class": object_class, "relative_path": path.relative_to(self.node_root).as_posix(), "content_hash": sha256(data), "storage_version": STORAGE_VERSION, "provider_type": "LOCAL"}
        return data, metadata

    def delete(self, object_class: str, object_id: str) -> bool:
        path = self._path(object_class, object_id)
        if not path.exists():
            return False
        path.unlink()
        return True

    def verify(self, object_class: str, object_id: str, expected_hash: str) -> bool:
        data, _ = self.get(object_class, object_id)
        return sha256(data) == expected_hash

    def load_registry(self) -> dict[str, Any]:
        return json.loads(self.registry_path.read_text(encoding="utf-8"))

    def register(self, metadata: dict[str, Any]) -> None:
        registry = self.load_registry()
        registry[metadata["object_id"]] = metadata
        tmp = self.registry_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(registry, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        os.replace(tmp, self.registry_path)


class KuboIPFSProvider:
    """Reference HTTP adapter for a local Kubo API endpoint."""
    provider_type = "DECENTRALIZED"

    def __init__(self, api_url: str = "http://127.0.0.1:5001/api/v0", timeout: float = 5.0):
        self.api_url = api_url.rstrip("/")
        self.timeout = timeout

    def status(self) -> dict[str, Any]:
        try:
            with request.urlopen(self.api_url + "/id", timeout=self.timeout) as response:
                return {"provider_type": self.provider_type, "status": "READY", "http_status": response.status}
        except Exception as exc:
            return {"provider_type": self.provider_type, "status": "OFFLINE", "error": type(exc).__name__}

    def add(self, data: bytes) -> str:
        boundary = "----NodeCoreStorageBoundary"
        body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"object\"\r\nContent-Type: application/octet-stream\r\n\r\n").encode() + data + f"\r\n--{boundary}--\r\n".encode()
        req = request.Request(self.api_url + "/add?pin=true", data=body, method="POST", headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
        with request.urlopen(req, timeout=self.timeout) as response:
            result = json.loads(response.read().decode())
        return result["Hash"]

    def get(self, cid: str) -> bytes:
        with request.urlopen(self.api_url + "/cat?arg=" + cid, timeout=self.timeout) as response:
            return response.read()


class StorageEngine:
    """Node Core storage service implementing local + optional Kubo mirror."""
    def __init__(self, node_root: str | os.PathLike[str], kubo: KuboIPFSProvider | None = None):
        self.local = LocalStore(node_root)
        self.kubo = kubo

    def put(self, object_class: str, object_id: str, data: bytes, *, mirror: bool = True, encrypted: bool = False) -> dict[str, Any]:
        if object_class in {"private", "restricted"} and mirror and not encrypted:
            raise StorageError("private/restricted distributed objects must be encrypted before mirroring")
        metadata = self.local.put(object_class, object_id, data)
        if mirror and self.kubo is not None:
            try:
                cid = self.kubo.add(data)
                metadata.update({"provider_type": "DECENTRALIZED", "location_state": "LOCAL_AND_DISTRIBUTED", "synchronization_state": "SYNCHRONIZED", "cid": cid})
            except Exception:
                metadata.update({"provider_type": "LOCAL", "location_state": "SYNC_PENDING", "synchronization_state": "SYNC_FAILED"})
        self.local.register(metadata)
        return metadata

    def get(self, object_class: str, object_id: str) -> tuple[bytes, dict[str, Any]]:
        entry = self.local.load_registry().get(object_id)
        if entry and entry.get("cid") and self.kubo is not None:
            try:
                data = self.kubo.get(entry["cid"])
                if sha256(data) == entry["content_hash"]:
                    return data, {**entry, "read_source": "KUBO_IPFS"}
            except Exception:
                pass
        data, metadata = self.local.get(object_class, object_id)
        if entry and entry.get("content_hash") and entry["content_hash"] != sha256(data):
            raise StorageError("local content integrity mismatch")
        return data, {**(entry or metadata), "read_source": "LOCAL_FALLBACK"}

    def verify(self, object_class: str, object_id: str, expected_hash: str) -> bool:
        data, _ = self.get(object_class, object_id)
        return sha256(data) == expected_hash

    def status(self) -> dict[str, Any]:
        result = {"storage_version": STORAGE_VERSION, "local": "READY"}
        result["kubo"] = self.kubo.status() if self.kubo else {"status": "NOT_CONFIGURED"}
        return result
