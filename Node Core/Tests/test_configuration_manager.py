import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "Configuration" / "configuration_manager.py"
spec = importlib.util.spec_from_file_location("configuration_manager_test_target", PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = module
spec.loader.exec_module(module)


BASE = {
    "node_core_version": "1.0.0",
    "decentralized_storage": {"status": "NOT_PROVISIONED"},
    "protocol_associations": [],
    "cpg_protocol": "NOT_INSTALLED",
}


class ConfigurationManagerTests(unittest.TestCase):
    def test_network_configuration_is_valid(self):
        config = dict(BASE)
        config["network"] = {"minimum_protocol_nodes": 5}
        self.assertEqual(module.validate_configuration(config)["network"]["minimum_protocol_nodes"], 5)

    def test_network_configuration_requires_five_nodes(self):
        config = dict(BASE)
        config["network"] = {"minimum_protocol_nodes": 4}
        with self.assertRaises(module.ConfigurationError):
            module.validate_configuration(config)

    def test_unknown_configuration_property_still_fails(self):
        config = dict(BASE)
        config["unsupported"] = True
        with self.assertRaises(module.ConfigurationError):
            module.validate_configuration(config)


if __name__ == "__main__":
    unittest.main()
