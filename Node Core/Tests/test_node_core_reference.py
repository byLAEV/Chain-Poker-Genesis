import importlib.util
import sys
import tempfile
import unittest
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for path in (
    ROOT / "Cryptography" / "Core",
    ROOT / "Cryptography" / "Providers",
    ROOT / "Protocol Interface",
):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

spec = importlib.util.spec_from_file_location("node_core", ROOT / "node_core.py")
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)

class NodeCoreReferenceTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        root = Path(self.temp_dir.name) / "node-storage" / "configuration"
        root.mkdir(parents=True)
        (root / "node-config.json").write_text(json.dumps({
            "node_core_version": "1.0.0",
            "decentralized_storage": {"status": "NOT_PROVISIONED", "mode": "LOCAL"},
            "protocol_associations": [],
            "cpg_protocol": "NOT_INSTALLED",
        }), encoding="utf-8")

    def tearDown(self):
        self.temp_dir.cleanup()

    def node(self):
        return mod.NodeCore(self.temp_dir.name)

    def test_boot_initialize_activate(self):
        n = self.node()
        self.assertEqual(n.initialize()["state"], "INITIALIZED")
        self.assertEqual(n.activate(), "ACTIVE")

    def test_crypto(self):
        n = self.node()
        self.assertEqual(len(n.crypto.sha256_hex(b"test")), 64)
        self.assertEqual(len(n.crypto.hash_canonical_hex({"test": "value"})), 64)

    def test_time_chain(self):
        n = self.node()
        a = n.time.record(1)
        b = n.time.record(2)
        self.assertEqual(b.sequence, a.sequence + 1)
        self.assertNotEqual(a.previous_hash, b.previous_hash)

    def test_security(self):
        n = self.node()
        self.assertFalse(n.security.validate_path("../escape").allowed)
        self.assertFalse(n.security.validate_path("CPG/x").allowed)

if __name__ == "__main__":
    unittest.main()
