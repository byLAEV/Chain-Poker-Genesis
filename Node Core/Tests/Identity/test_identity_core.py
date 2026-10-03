#!/usr/bin/env python3
"""Executable reference tests for Node Core Identity."""
import importlib.util
import json
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "Identity" / "identity_core.py"
SPEC = importlib.util.spec_from_file_location("node_core_identity_core_test", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

class IdentityCoreTests(unittest.TestCase):
    def test_identity_creation_and_validation(self):
        manager = MODULE.IdentityManager()
        identity, private_key = manager.create_identity(timestamp=1700000000)
        self.assertTrue(identity.validate())
        self.assertEqual(len(private_key), 32)
        self.assertNotIn("private", json.dumps(identity.canonical_record()).lower())

    def test_lifecycle_creation_initialization_activation(self):
        manager = MODULE.IdentityManager()
        manager.create_identity(timestamp=1700000000)
        manager.initialize(timestamp=1700000001)
        manager.activate(timestamp=1700000002)
        self.assertEqual(manager.node_life.state, "ACTIVE")
        self.assertTrue(manager.node_life.verify_history())

    def test_lifecycle_reconstruction(self):
        manager = MODULE.IdentityManager()
        manager.create_identity(timestamp=1700000000)
        manager.initialize(timestamp=1700000001)
        manager.activate(timestamp=1700000002)
        events = [MODULE.asdict(e) for e in manager.node_life.state_history]
        self.assertEqual(MODULE.reconstruct_lifecycle(events), "ACTIVE")

    def test_tampered_identity_id_is_rejected(self):
        manager = MODULE.IdentityManager()
        identity, _ = manager.create_identity(timestamp=1700000000)
        tampered = MODULE.NodeIdentity(identity.identity_version, "0" * 64, identity.public_key_algorithm, identity.public_key, identity.creation_timestamp)
        self.assertFalse(tampered.validate())

    def test_tampered_lifecycle_event_is_rejected(self):
        manager = MODULE.IdentityManager()
        manager.create_identity(timestamp=1700000000)
        manager.initialize(timestamp=1700000001)
        events = [MODULE.asdict(e) for e in manager.node_life.state_history]
        events[1]["state"] = "ACTIVE"
        with self.assertRaises(ValueError):
            MODULE.reconstruct_lifecycle(events)

if __name__ == "__main__":
    unittest.main()
