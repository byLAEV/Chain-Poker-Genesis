#!/usr/bin/env python3
import tempfile
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from node_core import NodeCore

def main():
    with tempfile.TemporaryDirectory() as d:
        node=NodeCore(d)
        assert node.storage is not None
        assert node.recovery is not None
        assert node.manager.recovery is node.recovery
        assert node.protocol_interface.engine_runtime is node.engines
        snapshot=node.snapshot()
        assert "storage" in snapshot
        assert snapshot["storage"]["local"]=="READY"
        assert snapshot["engines"]==[]
    print("Node Core composition integration: PASS")

if __name__=="__main__": main()
