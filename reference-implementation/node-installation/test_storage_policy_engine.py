from __future__ import annotations

import unittest

from storage_policy_engine import StoragePolicyEngine, StoragePolicyError


class StoragePolicyEngineTests(unittest.TestCase):
    def setUp(self):
        self.engine = StoragePolicyEngine()

    def test_private_is_local_and_sync_disabled_by_default(self):
        policy = self.engine.evaluate("LOCAL_PRIVATE")
        self.assertEqual(policy.storage_class, "LOCAL_PRIVATE")
        self.assertEqual(policy.where, "NODE_LOCAL")
        self.assertEqual(policy.who, "NODE_LOCAL")
        self.assertEqual(policy.when, "IMMEDIATE")
        self.assertEqual(policy.how_long, "PERSISTENT")
        self.assertEqual(policy.placement, "LOCAL_ONLY")
        self.assertEqual(policy.sync, "DISABLED")
        self.assertEqual(policy.encryption, "REQUIRED")
        self.assertEqual(policy.replicate, "LOCAL_ONLY")

    def test_restricted_and_personal_are_not_implicitly_published(self):
        for storage_class in ("LOCAL_RESTRICTED", "LOCAL_PERSONAL"):
            policy = self.engine.evaluate(storage_class)
            self.assertEqual(policy.sync, "DISABLED")
            self.assertEqual(policy.placement, "LOCAL_ONLY")
            self.assertEqual(policy.pin, "DISABLED")

    def test_temporary_does_not_assume_persistence_or_distribution(self):
        policy = self.engine.evaluate("TEMPORARY")
        self.assertEqual(policy.persistence, "TEMPORARY")
        self.assertEqual(policy.retention, "TEMPORARY")
        self.assertEqual(policy.sync, "DISABLED")
        self.assertEqual(policy.replicate, "DISABLED")

    def test_overrides_are_explicit_and_constrained(self):
        policy = self.engine.evaluate(
            "LOCAL_PUBLIC",
            {"sync": "ENABLED", "placement": "DUAL_STORAGE"},
        )
        self.assertEqual(policy.sync, "ENABLED")
        self.assertEqual(policy.placement, "DUAL_STORAGE")

    def test_unknown_class_is_rejected(self):
        with self.assertRaises(StoragePolicyError):
            self.engine.evaluate("UNKNOWN")

    def test_unknown_field_is_rejected(self):
        with self.assertRaises(StoragePolicyError):
            self.engine.evaluate("LOCAL_PUBLIC", {"replicas": 3})

    def test_sync_disabled_cannot_claim_nonlocal_placement(self):
        with self.assertRaises(StoragePolicyError):
            self.engine.evaluate(
                "LOCAL_PRIVATE",
                {"placement": "DUAL_STORAGE"},
            )


if __name__ == "__main__":
    unittest.main()
