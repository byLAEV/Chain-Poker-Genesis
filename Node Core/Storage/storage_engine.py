#!/usr/bin/env python3
"""Protocol-neutral storage execution engine.

The engine owns physical storage/provider operations. Storage Manager owns policy,
registry lifecycle, synchronization orchestration, and recovery decisions.
"""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib import request, parse

STORAGE_VERSION = "1.2.0"
STORAGE_CLASSES = {
    "temporary": "temporary",
    "public": "public",
    "private": "private",
    "restricted": "restricted",
    "personal": "personal",
    "protocol-reserved": "protocol",
}

class StorageError(Exception):
    pass

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def canonical_json(value) -> bytes:
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")

class LocalStore:
    def __init__(self, node_root):
        self.node_root = Path(node_root).resolve()
        self.root = self.node_root / "node-storage"
        self.registry_path = self.root / "state" / "object-registry.json"
        self.ensure_layout()

    def ensure_layout(self):
        for name in STORAGE_CLASSES.values():
            (self.root / name).mkdir(parents=True, exist_ok=True)
        for name in ("state", "recovery", "quarantine"):
            (self.root / name).mkdir(parents=True, exist_ok=True)
        if not self.registry_path.exists():
            self.registry_path.write_text("{}\n", encoding="utf-8")

    def _path(self, object_class, object_id):
        if object_class not in STORAGE_CLASSES or object_class == "protocol-reserved":
            raise StorageError("unsupported or protocol-reserved storage class")
        if not object_id or "/" in object_id or chr(92) in object_id or ".." in object_id:
            raise StorageError("invalid object id")
        path = (self.root / STORAGE_CLASSES[object_class] / (object_id + ".bin")).resolve()
        if self.root not in path.parents:
            raise StorageError("object path escapes storage root")
        return path

    def put(self, object_class, object_id, data):
        if not isinstance(data, (bytes, bytearray)):
            raise StorageError("storage data must be bytes")
        data = bytes(data)
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
        return self.metadata(object_class, object_id, data=data)

    def get(self, object_class, object_id):
        path = self._path(object_class, object_id)
        if not path.is_file():
            raise StorageError("object not found locally")
        data = path.read_bytes()
        return data, self.metadata(object_class, object_id, data=data)

    def delete(self, object_class, object_id):
        path = self._path(object_class, object_id)
        if not path.exists():
            return False
        path.unlink()
        return True

    def exists(self, object_class, object_id):
        return self._path(object_class, object_id).is_file()

    def metadata(self, object_class, object_id, data=None, *, created_at=None, updated_at=None):
        if data is None:
            data = self._path(object_class, object_id).read_bytes()
        path = self._path(object_class, object_id)
        now = datetime.now(timezone.utc).isoformat()
        created = created_at or now
        updated = updated_at or now
        return {
            "object_id": object_id,
            "object_class": object_class,
            "storage_class": object_class,
            "relative_path": path.relative_to(self.node_root).as_posix(),
            "location": path.relative_to(self.node_root).as_posix(),
            "content_hash": sha256(data),
            "size": len(data),
            "storage_version": STORAGE_VERSION,
            "version": STORAGE_VERSION,
            "provider_type": "LOCAL",
            "location_state": "LOCAL_ONLY",
            "object_state": "PRESENT",
            "state": "PRESENT",
            "created_at": created,
            "updated_at": updated,
            "synchronization_state": "NOT_SYNCHRONIZED",
            "encryption_state": "PLAINTEXT",
        }

    def verify(self, object_class, object_id, expected_hash):
        data, _ = self.get(object_class, object_id)
        return sha256(data) == expected_hash

class KuboIPFSProvider:
    provider_type = "DECENTRALIZED"

    def __init__(self, api_url="http://127.0.0.1:5001/api/v0", timeout=5.0):
        self.api_url = api_url.rstrip("/")
        self.timeout = timeout

    def status(self):
        try:
            with request.urlopen(self.api_url + "/id", timeout=self.timeout) as response:
                return {"provider_type": self.provider_type, "status": "READY", "http_status": response.status}
        except Exception as exc:
            return {"provider_type": self.provider_type, "status": "OFFLINE", "error": type(exc).__name__}

    def _post(self, endpoint, data=None, headers=None):
        req = request.Request(
            self.api_url + endpoint,
            data=data,
            method="POST",
            headers=headers or {},
        )
        with request.urlopen(req, timeout=self.timeout) as response:
            return response.read()

    def add(self, data, *, pin=True):
        boundary = "----NodeCoreStorageBoundary"
        body = (
            f"--{boundary}\r\n"
            'Content-Disposition: form-data; name="file"; filename="object"\r\n'
            "Content-Type: application/octet-stream\r\n\r\n"
        ).encode() + bytes(data) + f"\r\n--{boundary}--\r\n".encode()
        query = "?pin=true" if pin else ""
        raw = self._post(
            "/add" + query,
            body,
            {"Content-Type": f"multipart/form-data; boundary={boundary}"},
        )
        result = json.loads(raw.decode("utf-8"))
        if "Hash" not in result:
            raise StorageError("Kubo add response did not contain CID")
        return result["Hash"]

    def get(self, cid):
        encoded = parse.quote(str(cid), safe="")
        with request.urlopen(self.api_url + "/cat?arg=" + encoded, timeout=self.timeout) as response:
            return response.read()

    def exists(self, cid):
        try:
            self.get(cid)
            return True
        except Exception:
            return False

    def pin(self, cid):
        self._post("/pin/add?arg=" + parse.quote(str(cid), safe=""))
        return True

    def unpin(self, cid):
        self._post("/pin/rm?arg=" + parse.quote(str(cid), safe=""))
        return True

    def verify(self, cid, expected_hash):
        return sha256(self.get(cid)) == expected_hash

class StorageEngine:
    def __init__(self, node_root, kubo=None):
        self.local = LocalStore(node_root)
        self.kubo = kubo
        self.version = STORAGE_VERSION

    def put(self, object_class, object_id, data, *, mirror=False, encrypted=False):
        metadata = self.put_local(object_class, object_id, data)
        if mirror:
            if self.kubo is None:
                raise StorageError("Kubo provider is not configured")
            metadata.update({"cid": self.mirror(data), "provider_type": "DECENTRALIZED", "location_state": "LOCAL_AND_DISTRIBUTED", "synchronization_state": "SYNCHRONIZED"})
        if encrypted:
            metadata["encryption_state"] = "ENCRYPTED"
        return metadata

    def get(self, object_class, object_id):
        return self.get_local(object_class, object_id)

    def verify(self, object_class, object_id, expected_hash):
        return self.local.verify(object_class, object_id, expected_hash)

    def put_local(self, object_class, object_id, data):
        return self.local.put(object_class, object_id, data)

    def get_local(self, object_class, object_id):
        return self.local.get(object_class, object_id)

    def delete_local(self, object_class, object_id):
        return self.local.delete(object_class, object_id)

    def exists_local(self, object_class, object_id):
        return self.local.exists(object_class, object_id)

    def mirror(self, data):
        if self.kubo is None:
            raise StorageError("Kubo provider is not configured")
        return self.kubo.add(data, pin=True)

    def read_distributed(self, cid):
        if self.kubo is None:
            raise StorageError("Kubo provider is not configured")
        return self.kubo.get(cid)

    def verify_distributed(self, cid, expected_hash):
        if self.kubo is None:
            raise StorageError("Kubo provider is not configured")
        return self.kubo.verify(cid, expected_hash)

    def status(self):
        return {
            "storage_version": self.version,
            "local": "READY",
            "kubo": self.kubo.status() if self.kubo else {"status": "NOT_CONFIGURED"},
        }
