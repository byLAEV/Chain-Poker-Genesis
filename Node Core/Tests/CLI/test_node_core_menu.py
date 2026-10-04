import io
from contextlib import redirect_stdout
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "CLI/node_cli.py"
spec = importlib.util.spec_from_file_location("node_cli", TARGET)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


class Network:
    def __init__(self, status, connected):
        self.status = status
        self.connected_peers = connected


class Node:
    def __init__(self, status, connected):
        self._network = Network(status, connected)

    def menu_state(self):
        ready = self._network.connected_peers >= 5
        return {
            "connection_status": self._network.status,
            "connected_nodes": self._network.connected_peers,
            "protocol_readiness": "READY" if ready else "NOT_READY",
            "minimum_nodes_required": 5,
        }


def render(node):
    out = io.StringIO()
    with redirect_stdout(out):
        code = module.NodeCLI(node).run(["menu"])
    return code, out.getvalue()


def test_menu_not_ready_below_five_nodes():
    code, output = render(Node("ONLINE", 4))
    assert code == 0
    assert "Connection Status: ONLINE" in output
    assert "Connected Nodes: 4" in output
    assert "Protocol Readiness: NOT READY" in output
    assert "Minimum Nodes Required: 5" in output


def test_menu_ready_at_five_nodes():
    code, output = render(Node("ONLINE", 5))
    assert code == 0
    assert "Protocol Readiness: READY" in output


def test_menu_searching_for_connections():
    code, output = render(Node("SEARCHING_FOR_CONNECTIONS", 0))
    assert code == 0
    assert "Connection Status: SEARCHING FOR CONNECTIONS" in output
    assert "Protocol Readiness: NOT READY" in output
