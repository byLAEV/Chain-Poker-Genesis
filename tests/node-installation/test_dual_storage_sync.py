from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from reference_implementation.node_installation.dual_storage_bootstrap import initialize_local
from reference_implementation.node_installation.dual_storage_sync import (
    KuboManifestSync,
    load_local_manifest,
    manifest_hash,
)


class FakeKubo(BaseHTTPRequestHandler):
    manifest: bytes | None = None

    def do_POST(self):  # noqa: N802
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)
        if self.path.startswith("/api/v0/files/read"):
            if self.__class__.manifest is None:
                self.send_response(404)
                self.end_headers()
                return
            payload = self.__class__.manifest
        elif self.path.startswith("/api/v0/files/write"):
            self.__class__.manifest = body
            payload = b""
        else:
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *_args):
        return


def run_server():
    server = HTTPServer(("127.0.0.1", 0), FakeKubo)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def test_manifest_is_reconciled_into_kubo(tmp_path: Path):
    initialize_local(tmp_path)
    server = run_server()
    try:
        api = f"http://127.0.0.1:{server.server_port}"
        manifest = load_local_manifest(tmp_path)
        result = KuboManifestSync(api).synchronize_manifest(manifest)
        assert result.state == "SYNCED"
        assert result.remote_hash == manifest_hash(manifest)
    finally:
        server.shutdown()


def test_manifest_hash_is_deterministic(tmp_path: Path):
    initialize_local(tmp_path)
    manifest = load_local_manifest(tmp_path)
    reordered = json.loads(json.dumps(manifest))
    assert manifest_hash(manifest) == manifest_hash(reordered)
