#!/usr/bin/env python3
"""Protocol-neutral local persistence and optional Kubo/IPFS mirroring."""

from __future__ import annotations
import hashlib
import json
import os
import tempfile
from pathlib import Path
from urllib import request

STORAGE_VERSION = "1.1.0"
STORAGE_CLASSES = {
    "temporary": "temporary", "public": "public", "private": "private",
    "restricted": "restricted", "personal": "personal", "protocol-reserved": "protocol",
}

class StorageError(Exception): pass

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def canonical_json(value) -> bytes:
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n").encode()

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
        path = (self.root / STORAGE_CLASSES[object_class] / f"{object_id}.bin").resolve()
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
                handle.write(data); handle.flush(); os.fsync(handle.fileno())
            os.replace(tmp, path)
        finally:
            if os.path.exists(tmp): os.unlink(tmp)
        return self.metadata(object_class, object_id)

    def get(self, object_class, object_id):
        path = self._path(object_class, object_id)
        if not path.is_file(): raise StorageError("object not found locally")
        data = path.read_bytes()
        return data, self.metadata(object_class, object_id, data=data)

    def delete(self, object_class, object_id):
        path = self._path(object_class, object_id)
        if not path.exists(): return False
        path.unlink(); return True

    def exists(self, object_class, object_id):
        return self._path(object_class, object_id).is_file()

    def metadata(self, object_class, object_id, data=None):
        if data is None:
            data = self._path(object_class, object_id).read_bytes()
        path = self._path(object_class, object_id)
        return {
            "object_id": object_id, "object_class": object_class,
            "relative_path": path.relative_to(self.node_root).as_posix(),
            "content_hash": sha256(data), "size": len(data),
            "storage_version": STORAGE_VERSION, "provider_type": "LOCAL",
            "location_state": "LOCAL_ONLY", "object_state": "PRESENT",
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

    def _request(self, endpoint, data=None, headers=None):
        req = request.Request(self.api_url + endpoint, data=data, method="POST" if data is not None else "POST", headers=headers or {})
        with request.urlopen(req, timeout=self.timeout) as response:
            return response.read()

    def status(self):
        try:
            with request.urlopen(self.api_url + "/id", timeout=self.timeout) as response:
                return {"provider_type": self.provider_type, "status": "READY", "http_status": response.status}
        except Exception as exc:
            return {"provider_type": self.provider_type, "status": "OFFLINE", "error": type(exc).__name__}

    def add(self, data, *, pin=True):
        boundary = "----NodeCoreStorageBoundary"
        body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"object\"\r\nContent-Type: application/octet-stream\r\n\r\n").encode() + bytes(data) + f"\r\n--{boundary}--\r\n".encode()
        query = "?pin=true" if pin else ""
        raw = self._request("/add" + query, body, {"Content-Type": f"multipart/form-data; boundary={boundary}"})
        return json.loads(raw.decode())["Hash"]

    def get(self, cid):
        with request.urlopen(self.api_url + "/cat?arg=" + cid, timeout=self.timeout) as response:
            return response.read()

    def exists(self, cid):
        try:
            self.get(cid); return True
        except Exception:
            return False

    def pin(self, cid):
        self._request("/pin/add?arg=" + cid); return True

    def unpin(self, cid):
        self._request("/pin/rm?arg=" + cid); return True

    def verify(self, cid, expected_hash):
        return sha256(self.get(cid)) == expected_hash

class StorageEngine:
    def __init__(self, node_root, kubo=None):
        self.local = LocalStore(node_root)
        self.kubo = kubo
        self.version = STORAGE_VERSION

    def put(self, object_class, object_id, data, *, mirror=True, encrypted=False):
        if object_class in {"private", "restricted"} and mirror and not encrypted:
            raise StorageError("private/restricted distributed objects must be encrypted before mirroring")
        metadata = self.local.put(object_class, object_id, data)
        if encrypted:
            metadata["encryption_state"] = "ENCRYPTED"
        if mirror and self.kubo:
            try:
                cid = self.kubo.add(data, pin=True)
                metadata.update({"provider_type":"DECENTRALIZED","location_state":"LOCAL_AND_DISTRIBUTED","synchronization_state":"SYNCHRONIZED","cid":cid})
            except Exception as exc:
                metadata.update({"location_state":"SYNC_PENDING","synchronization_state":"SYNC_FAILED","sync_error":type(exc).__name__})
        self._write_registry(metadata)
        return metadata

    def _write_registry(self, metadata):
        path = self.local.registry_path
        current = json.loads(path.read_text(encoding="utf-8"))
        current[metadata["object_id"]] = metadata
        fd, tmp = tempfile.mkstemp(prefix=".registry.", dir=path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(current, handle, indent=2, sort_keys=True); handle.write("\n"); handle.flush(); os.fsync(handle.fileno())
            os.replace(tmp, path)
        finally:
            if os.path.exists(tmp): os.unlink(tmp)

    def registry(self):
        return json.loads(self.local.registry_path.read_text(encoding="utf-8"))

    def get(self, object_class, object_id):
        entry = self.registry().get(object_id)
        if entry and entry.get("cid") and self.kubo:
            try:
                data = self.kubo.get(entry["cid"])
                if sha256(data) == entry["content_hash"]:
                    return data, {**entry, "read_source":"KUBO_IPFS"}
            except Exception:
                pass
        data, local_meta = self.local.get(object_class, object_id)
        if entry and sha256(data) != entry["content_hash"]:
            raise StorageError("local content integrity mismatch")
        return data, {**(entry or local_meta), "read_source":"LOCAL_FALLBACK" if entry and entry.get("cid") else "LOCAL"}

    def exists(self, object_class, object_id):
        return self.local.exists(object_class, object_id)

    def delete(self, object_class, object_id):
        entry = self.registry().get(object_id)
        if entry and entry.get("cid") and self.kubo:
            try: self.kubo.unpin(entry["cid"])
            except Exception: pass
        deleted = self.local.delete(object_class, object_id)
        current = self.registry(); current.pop(object_id, None)
        self.local.registry_path.write_text(json.dumps(current, indent=2, sort_keys=True)+"\n", encoding="utf-8")
        return deleted

    def synchronize(self, object_class, object_id, *, encrypted=False):
        if not self.kubo: raise StorageError("Kubo provider is not configured")
        data, metadata = self.local.get(object_class, object_id)
        if object_class in {"private","restricted"} and not encrypted:
            raise StorageError("private/restricted distribution requires encrypted bytes")
        cid = self.kubo.add(data, pin=True)
        metadata.update({"provider_type":"DECENTRALIZED","location_state":"LOCAL_AND_DISTRIBUTED","synchronization_state":"SYNCHRONIZED","cid":cid})
        self._write_registry(metadata)
        return metadata

    def status(self):
        return {"storage_version": self.version, "local":"READY", "kubo": self.kubo.status() if self.kubo else {"status":"NOT_CONFIGURED"}}
