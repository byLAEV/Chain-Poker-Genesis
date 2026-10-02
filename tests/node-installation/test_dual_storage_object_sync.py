from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from dual_storage_object_sync import KuboObjectSync
from object_registry import ObjectRegistry
from storage_manager import StorageManager


class FakeKubo(BaseHTTPRequestHandler):
    files: dict[str, bytes] = {}
    cids: dict[str, str] = {}

    def do_POST(self):  # noqa: N802
        from urllib.parse import parse_qs, urlparse
        query = parse_qs(urlparse(self.path).query)
        arg = query.get("arg", [""])[0]

        if self.path.startswith("/api/v0/files/write"):
            length = int(self.headers.get("Content-Length", "0"))
            self.__class__.files[arg] = self.rfile.read(length)
            self.__class__.cids[arg] = "bafy-test-" + __import__("hashlib").sha256(self.__class__.files[arg]).hexdigest()[:16]
            self.send_response(200)
            self.end_headers()
            return

        if self.path.startswith("/api/v0/files/read"):
            if arg not in self.__class__.files:
                self.send_response(404)
                self.end_headers()
                return
            payload = self.__class__.files[arg]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(payload)
            return

        if self.path.startswith("/api/v0/files/stat"):
            if arg not in self.__class__.files:
                self.send_response(404)
                self.end_headers()
                return
            payload = json.dumps({"Hash": self.__class__.cids[arg]}).encode()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(payload)
            return

        self.send_response(404)
        self.end_headers()

    def log_message(self, *_args):
        return


def run_server():
    FakeKubo.files = {}
    FakeKubo.cids = {}
    server = HTTPServer(("127.0.0.1", 0), FakeKubo)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def test_registered_object_is_synchronized_with_cid(tmp_path: Path):
    StorageManager(tmp_path).put_json("state", "state-001", {"value": "canonical"})
    data = (tmp_path / "node-storage/state/state-001.json").read_bytes()
    import hashlib
    registry = ObjectRegistry(tmp_path)
    registry.register({
        "object_id": "state-001",
        "object_class": "state",
        "relative_path": "node-storage/state/state-001.json",
        "content_hash": hashlib.sha256(data).hexdigest(),
        "storage_version": "0.1.0",
        "provider_type": "LOCAL",
        "location_state": "SYNC_PENDING",
        "object_state": "PRESENT",
        "synchronization_state": "NOT_SYNCHRONIZED",
    })

    server = run_server()
    try:
        result = KuboObjectSync(tmp_path, f"http://127.0.0.1:{server.server_port}").synchronize("state-001")
        assert result.content_hash == hashlib.sha256(data).hexdigest()
        assert result.version == "0.1.0"
        assert result.cid.startswith("bafy-test-")
        assert result.location_state == "LOCAL_AND_DISTRIBUTED"
        assert result.synchronization_state == "SYNCHRONIZED"
    finally:
        server.shutdown()
