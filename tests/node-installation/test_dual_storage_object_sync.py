from __future__ import annotations

import hashlib
import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from dual_storage_object_sync import KuboObjectSync
from synchronization_queue import DurableSynchronizationQueue
from synchronization_reliability import RetryBackoffCircuitBreaker, SynchronizationCircuitOpenError
from object_registry import ObjectRegistry
from storage_manager import StorageManager
from dual_storage_bootstrap import initialize_local




class TestSynchronizationReliability(unittest.TestCase):
    def test_retry_backoff_and_success_reset(self):
        delays = []
        attempts = []
        failures = [RuntimeError("transient"), RuntimeError("transient")]
        policy = RetryBackoffCircuitBreaker(max_retries=2, base_delay=0.25, backoff_multiplier=2.0, failure_threshold=5, sleep=delays.append)
        def operation():
            attempts.append(1)
            if failures:
                raise failures.pop(0)
            return "ok"
        self.assertEqual(policy.execute(operation), "ok")
        self.assertEqual(len(attempts), 3)
        self.assertEqual(delays, [0.25, 0.5])
        self.assertEqual(policy.state, "CLOSED")

    def test_circuit_opens_after_failure_threshold(self):
        now = [0.0]
        policy = RetryBackoffCircuitBreaker(max_retries=0, failure_threshold=2, recovery_timeout=10.0, sleep=lambda _: None, clock=lambda: now[0])
        operation = lambda: (_ for _ in ()).throw(RuntimeError("failure"))
        with self.assertRaises(RuntimeError):
            policy.execute(operation)
        with self.assertRaises(RuntimeError):
            policy.execute(operation)
        self.assertEqual(policy.state, "OPEN")
        with self.assertRaises(SynchronizationCircuitOpenError):
            policy.execute(lambda: "blocked")

    def test_circuit_enters_half_open_after_recovery_timeout(self):
        now = [0.0]
        policy = RetryBackoffCircuitBreaker(max_retries=0, failure_threshold=1, recovery_timeout=5.0, sleep=lambda _: None, clock=lambda: now[0])
        with self.assertRaises(RuntimeError):
            policy.execute(lambda: (_ for _ in ()).throw(RuntimeError("failure")))
        self.assertEqual(policy.state, "OPEN")
        now[0] = 5.0
        self.assertEqual(policy.state, "HALF_OPEN")
        self.assertEqual(policy.execute(lambda: "recovered"), "recovered")
        self.assertEqual(policy.state, "CLOSED")
\n\nclass FakeKubo(BaseHTTPRequestHandler):
    files: dict[str, bytes] = {}
    cids: dict[str, str] = {}
    stat_missing_status: int = 500

    def _multipart_file(self, body: bytes, content_type: str) -> bytes:
        boundary = content_type.split("boundary=", 1)[1].encode("ascii")
        marker = b"--" + boundary
        for part in body.split(marker):
            if b"filename=" in part and b"\r\n\r\n" in part:
                payload = part.split(b"\r\n\r\n", 1)[1]
                if payload.endswith(b"\r\n"):
                    payload = payload[:-2]
                return payload
        raise ValueError("multipart file part not found")

    def do_POST(self):  # noqa: N802
        from urllib.parse import parse_qs, urlparse
        query = parse_qs(urlparse(self.path).query)
        arg = query.get("arg", [""])[0]
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)

        if self.path.startswith("/api/v0/files/write"):
            if self.headers.get("Content-Type", "").startswith("multipart/form-data;"):
                body = self._multipart_file(body, self.headers["Content-Type"])
            self.__class__.files[arg] = body
            self.__class__.cids[arg] = "bafy-test-" + hashlib.sha256(body).hexdigest()[:16]
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
                if self.__class__.stat_missing_status == 500:
                    self.send_response(500)
                    self.end_headers()
                    self.wfile.write(b'{"Message":"file does not exist","Code":0}')
                else:
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
    FakeKubo.stat_missing_status = 500
    server = HTTPServer(("127.0.0.1", 0), FakeKubo)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


class ObjectSynchronizationTests(unittest.TestCase):
    def test_registered_object_is_synchronized_with_cid(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            initialize_local(root)
            StorageManager(root).put_json("state", "state-001", {"value": "canonical"})
            data = (root / "node-storage/state/state-001.json").read_bytes()
            registry = ObjectRegistry(root)
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
                result = KuboObjectSync(root, f"http://127.0.0.1:{server.server_port}").synchronize("state-001")
                self.assertEqual(result.content_hash, hashlib.sha256(data).hexdigest())
                self.assertEqual(result.version, "0.1.0")
                self.assertTrue(result.cid.startswith("bafy-test-"))
                self.assertEqual(result.location_state, "LOCAL_AND_DISTRIBUTED")
                self.assertEqual(result.synchronization_state, "SYNCHRONIZED")
                persisted = ObjectRegistry(root).get("state-001")
                self.assertEqual(persisted["distributed_cid"], result.cid)
                self.assertEqual(persisted["distributed_version"], "0.1.0")
                self.assertEqual(persisted["location_state"], "LOCAL_AND_DISTRIBUTED")
                self.assertEqual(persisted["synchronization_state"], "SYNCHRONIZED")
            finally:
                server.shutdown()

    def test_pending_synchronization_survives_restart_and_resumes(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            initialize_local(root)
            StorageManager(root).put_json("state", "state-restart", {"value": "canonical"})
            data = (root / "node-storage/state/state-restart.json").read_bytes()
            registry = ObjectRegistry(root)
            registry.register({
                "object_id": "state-restart",
                "object_class": "state",
                "relative_path": "node-storage/state/state-restart.json",
                "content_hash": hashlib.sha256(data).hexdigest(),
                "storage_version": "0.1.0",
                "provider_type": "LOCAL",
                "location_state": "SYNC_PENDING",
                "object_state": "PRESENT",
                "synchronization_state": "NOT_SYNCHRONIZED",
            })

            first_queue = DurableSynchronizationQueue(root)
            first_queue.enqueue(
                "state-restart",
                content_hash=hashlib.sha256(data).hexdigest(),
                storage_version="0.1.0",
            )
            first_queue.mark_processing("state-restart")

            restarted_queue = DurableSynchronizationQueue(root)
            self.assertEqual(restarted_queue.pending()[0]["object_id"], "state-restart")
            self.assertEqual(restarted_queue.pending()[0]["status"], "PENDING")

            server = run_server()
            try:
                sync = KuboObjectSync(root, f"http://127.0.0.1:{server.server_port}")
                results = sync.synchronize_pending()
                self.assertEqual([item.object_id for item in results], ["state-restart"])
                self.assertEqual(DurableSynchronizationQueue(root).entries["state-restart"]["status"], "COMPLETED")
                persisted = ObjectRegistry(root).get("state-restart")
                self.assertEqual(persisted["synchronization_state"], "SYNCHRONIZED")
                self.assertEqual(persisted["location_state"], "LOCAL_AND_DISTRIBUTED")
                self.assertIn("/node-storage/state/state-restart.json", FakeKubo.files)
            finally:
                server.shutdown()

    def test_divergent_distributed_object_is_recorded_as_conflict(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            initialize_local(root)
            StorageManager(root).put_json("state", "state-conflict", {"value": "local"})
            data = (root / "node-storage/state/state-conflict.json").read_bytes()
            registry = ObjectRegistry(root)
            registry.register({
                "object_id": "state-conflict",
                "object_class": "state",
                "relative_path": "node-storage/state/state-conflict.json",
                "content_hash": hashlib.sha256(data).hexdigest(),
                "storage_version": "0.1.0",
                "provider_type": "LOCAL",
                "location_state": "SYNC_PENDING",
                "object_state": "PRESENT",
                "synchronization_state": "NOT_SYNCHRONIZED",
            })
            server = run_server()
            try:
                path = "/node-storage/state/state-conflict.json"
                remote_payload = b'{"value":"remote"}\n'
                FakeKubo.files[path] = remote_payload
                FakeKubo.cids[path] = "bafy-test-conflict"
                with self.assertRaisesRegex(Exception, "conflict recorded"):
                    KuboObjectSync(root, f"http://127.0.0.1:{server.server_port}").synchronize("state-conflict")
                persisted = ObjectRegistry(root).get("state-conflict")
                self.assertEqual(persisted["location_state"], "CONFLICT")
                self.assertEqual(persisted["synchronization_state"], "CONFLICT")
                self.assertEqual(persisted["distributed_cid"], "bafy-test-conflict")
                self.assertEqual(FakeKubo.files[path], remote_payload)
            finally:
                server.shutdown()


if __name__ == "__main__":
    unittest.main()
