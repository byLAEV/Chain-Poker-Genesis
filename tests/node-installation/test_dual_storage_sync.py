from __future__ import annotations

import json
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "reference-implementation" / "node-installation"))

from dual_storage_bootstrap import initialize_local
from dual_storage_sync import KuboManifestSync, load_local_manifest, manifest_hash


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
    FakeKubo.manifest = None
    server = HTTPServer(("127.0.0.1", 0), FakeKubo)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


class ManifestSynchronizationTests(unittest.TestCase):
    def test_manifest_is_reconciled_into_kubo(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            initialize_local(root)
            server = run_server()
            try:
                api = f"http://127.0.0.1:{server.server_port}"
                manifest = load_local_manifest(root)
                result = KuboManifestSync(api).synchronize_manifest(manifest)
                self.assertEqual(result.state, "SYNCED")
                self.assertEqual(result.remote_hash, manifest_hash(manifest))
            finally:
                server.shutdown()

    def test_manifest_hash_is_deterministic(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            initialize_local(root)
            manifest = load_local_manifest(root)
            reordered = json.loads(json.dumps(manifest))
            self.assertEqual(manifest_hash(manifest), manifest_hash(reordered))


if __name__ == "__main__":
    unittest.main()
