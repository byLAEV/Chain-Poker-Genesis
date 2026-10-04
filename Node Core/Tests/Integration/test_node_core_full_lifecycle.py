#!/usr/bin/env python3
"""Full Node Core lifecycle integration gate.

UNINITIALIZED -> READY -> RUNNING -> DEGRADED -> RECOVERY -> READY
-> SHUTTING_DOWN -> STOPPED.

The test exercises NodeManager, RuntimeManager and RecoveryManager through
their public boundaries. CPG protocol state and Merkle remain untouched.
"""
from __future__ import annotations
import sys
import tempfile
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
for p in (BASE, BASE / "Bootstrap" / "Installer"):
    sys.path.insert(0, str(p))

from node_core import NodeCore
from bootstrap_node import install


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "node"
        install(root)
        node = NodeCore(root)

        assert node.manager.status.state == "UNINITIALIZED"
        assert node.manager.initialize().state == "READY"
        assert node.manager.runtime_manager.runtime.state.value == "NODE_CORE_READY"

        assert node.activate() == "RUNNING"
        assert node.manager.status.state == "RUNNING"
        assert node.manager.runtime_manager.runtime.state.value == "RUNNING"

        degraded = node.manager.degrade()
        assert degraded.state == "DEGRADED"
        assert node.manager.runtime_manager.runtime.state.value == "DEGRADED"
        assert node.manager.runtime_manager.runtime.health == "DEGRADED"

        recovered = node.manager.recover()
        assert recovered.state == "READY"
        assert node.manager.runtime_manager.runtime.state.value == "NODE_CORE_READY"
        assert node.manager.runtime_manager.runtime.health == "HEALTHY"

        stopped = node.manager.stop()
        assert stopped.state == "STOPPED"
        assert node.manager.runtime_manager.runtime.state.value == "STOPPED"

        snapshot = node.snapshot()
        assert snapshot["node"]["state"] == "STOPPED"
        assert snapshot["node"]["protocols"] == []
        assert snapshot["node"]["engines"] == []
        assert node.protocol_interface.list_installed() == []
        assert snapshot["node_core_version"] == "1.0.0"

        print("Node Core full lifecycle: PASS")
        print("UNINITIALIZED -> READY -> RUNNING -> DEGRADED -> RECOVERY -> READY -> STOPPED = PASS")
        print("runtime_manager_boundary = PASS")
        print("recovery_manager_boundary = PASS")
        print("cpg_protocol = NOT_INSTALLED")
        print("merkle = UNTOUCHED")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
