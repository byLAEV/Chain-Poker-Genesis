import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "Runtime/Readiness/protocol_readiness.py"
spec = importlib.util.spec_from_file_location("protocol_readiness", TARGET)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


def test_protocol_readiness_below_minimum():
    result = module.evaluate_protocol_readiness(4)
    assert result["status"] == "NOT_READY"
    assert result["ready"] is False
    assert result["minimum_nodes_required"] == 5


def test_protocol_readiness_at_minimum():
    result = module.evaluate_protocol_readiness(5)
    assert result["status"] == "READY"
    assert result["ready"] is True


def test_protocol_readiness_above_minimum():
    result = module.evaluate_protocol_readiness(7)
    assert result["status"] == "READY"
