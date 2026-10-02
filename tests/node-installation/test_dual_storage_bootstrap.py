#!/usr/bin/env python3
"""Tests for the protocol-neutral dual-storage bootstrap contract."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "reference-implementation" / "node-installation"))

from dual_storage_bootstrap import REQUIRED_PATHS, STORAGE_STRUCTURE_VERSION, BootstrapError, bootstrap, initialize_local


class DualStorageBootstrapTests(unittest.TestCase):
    def test_local_bootstrap_is_complete_without_installing_kubo(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = bootstrap(Path(directory))
            self.assertTrue(result.local_ready)
            self.assertFalse(result.ipfs_ready)
            self.assertEqual(result.synchronization_state, "NOT_EVALUATED")
            for relative in REQUIRED_PATHS:
                self.assertTrue((Path(directory) / relative).is_dir())
            manifest = Path(directory) / "node-storage/state/storage-manifest.json"
            self.assertTrue(manifest.is_file())
            self.assertIn(STORAGE_STRUCTURE_VERSION, manifest.read_text(encoding="utf-8"))

    def test_local_manifest_rejects_missing_canonical_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            initialize_local(root)
            (root / "node-storage/protocol").rmdir()
            with self.assertRaises(BootstrapError):
                from dual_storage_bootstrap import verify_local
                verify_local(root)

    def test_kubo_is_not_assumed_when_endpoint_is_absent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = bootstrap(Path(directory), kubo_api=None)
            self.assertFalse(result.ipfs_ready)
            self.assertEqual(result.synchronization_state, "NOT_EVALUATED")


if __name__ == "__main__":
    unittest.main()
