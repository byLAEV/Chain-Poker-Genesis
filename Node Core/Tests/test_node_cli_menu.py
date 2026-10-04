import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI_PATH = ROOT / "CLI" / "node_cli.py"

spec = importlib.util.spec_from_file_location("node_cli_menu_test", CLI_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class FakeNode:
    def menu_state(self):
        return {
            "connection_status": "ONLINE",
            "connected_nodes": 5,
            "protocol_readiness": "READY",
            "minimum_nodes_required": 5,
        }


class NodeCLIMenuTests(unittest.TestCase):
    def test_render_menu_uses_node_state(self):
        output = module.NodeCLI(FakeNode()).render_menu()
        self.assertIn("NODE CORE MENU", output)
        self.assertIn("Connection Status: ONLINE", output)
        self.assertIn("Connected Nodes: 5", output)
        self.assertIn("Protocol Readiness: READY", output)
        self.assertIn("1. Node Core", output)
        self.assertIn("2. Protocols", output)
        self.assertIn("3. Admin", output)
        self.assertIn("0. Exit", output)


if __name__ == "__main__":
    unittest.main()
