#!/usr/bin/env python3
"""Regression test for Node Core network composition loading."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_node_core_loads_network_manager():
    spec = importlib.util.spec_from_file_location("node_core_network_import_test", ROOT / "node_core.py")
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    assert module.network.NetworkManager is not None
    assert module.network.PeerRegistry is not None
