#!/usr/bin/env python3
"""Reference tests for the canonical Node Core Storage engine."""
from __future__ import annotations
import importlib.util
import tempfile
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "Storage" / "storage_engine.py"
SPEC = importlib.util.spec_from_file_location("node_core_storage_engine", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)

class StorageEngineTests(unittest.TestCase):
    def test_layout_and_local_write_read_verify(self):
        with tempfile.TemporaryDirectory() as tmp:
            engine = MODULE.StorageEngine(tmp)
            metadata = engine.put("public", "object-a", b"hello", mirror=False)
            self.assertEqual(metadata["provider_type"], "LOCAL")
            self.assertEqual(metadata["storage_class"], "public")
            self.assertEqual(metadata["state"], "PRESENT")
            self.assertEqual(metadata["version"], MODULE.STORAGE_VERSION)
            self.assertIn("created_at", metadata)
            self.assertIn("updated_at", metadata)
            data, read_meta = engine.get("public", "object-a")
            self.assertEqual(data, b"hello")
            self.assertEqual(read_meta["content_hash"], metadata["content_hash"])
            self.assertTrue(engine.verify("public", "object-a", metadata["content_hash"]))

    def test_path_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            engine = MODULE.StorageEngine(tmp)
            with self.assertRaises(MODULE.StorageError):
                engine.put("public", "../escape", b"x", mirror=False)

if __name__ == "__main__":
    unittest.main()
