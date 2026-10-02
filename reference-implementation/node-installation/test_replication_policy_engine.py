from __future__ import annotations

import unittest

from replication_policy_engine import ReplicationPolicyEngine, ReplicationPolicyError


class ReplicationPolicyEngineTests(unittest.TestCase):
    def setUp(self):
        self.engine = ReplicationPolicyEngine()

    def test_local_only(self):
        policy = self.engine.evaluate("LOCAL_ONLY")
        self.assertEqual(policy.minimum_copies, 1)
        self.assertFalse(policy.external_service)
        self.assertTrue(policy.local_required)

    def test_multi_node_requires_multiple_copies(self):
        policy = self.engine.evaluate("MULTI_NODE")
        self.assertEqual(policy.minimum_copies, 2)
        self.assertFalse(policy.external_service)
        self.assertTrue(policy.local_required)

    def test_external_pinning_is_distinct_from_multi_node(self):
        policy = self.engine.evaluate("EXTERNAL_PINNING")
        self.assertEqual(policy.minimum_copies, 2)
        self.assertTrue(policy.external_service)
        self.assertTrue(policy.local_required)

    def test_unknown_policy_is_rejected(self):
        with self.assertRaises(ReplicationPolicyError):
            self.engine.evaluate("BACKUP")

    def test_engine_does_not_execute_replication(self):
        policy = self.engine.evaluate("MULTI_NODE")
        self.assertFalse(hasattr(policy, "replicate"))
        self.assertFalse(hasattr(self.engine, "replicate"))
