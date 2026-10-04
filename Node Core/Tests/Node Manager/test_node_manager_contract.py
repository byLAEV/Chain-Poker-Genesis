#!/usr/bin/env python3
from pathlib import Path
import sys
import tempfile

BASE=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(BASE/"Bootstrap/Installer"))
sys.path.insert(0,str(BASE/"Node Manager"))
sys.path.insert(0,str(BASE/"Protocol Interface"))

from bootstrap_node import bootstrap_node
from node_manager import NodeManager
from protocol_interface import ProtocolDescriptor, ProtocolInterface

def main():
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)/"node"
        bootstrap_node(root)
        config=root/"node-storage/configuration/node-config.json"

        pi=ProtocolInterface()
        d=ProtocolDescriptor("example.protocol","1.0.0","engine.main","abc123")
        pi.discover(d)
        pi.register(d.protocol_id)

        m=NodeManager(protocol_interface=pi, configuration_path=config)
        assert m.snapshot()["state"]=="UNINITIALIZED"

        m.initialize()
        assert m.readiness() is True
        assert m.snapshot()["state"]=="READY"

        m.register_engine("engine.main","1.0.0")
        assert "engine.main" in m.snapshot()["engines"]

        m.start()
        assert m.snapshot()["state"]=="RUNNING"

        m.request_protocol_installation(d.protocol_id)
        assert m.snapshot()["protocols"]==[d.protocol_id]
        assert pi.get(d.protocol_id).state=="INSTALLED"

        m.stop()
        assert m.snapshot()["state"]=="STOPPED"
        assert [e["event"] for e in m.snapshot()["events"]] == [
            "NODE_READY","ENGINE_REGISTERED","NODE_STARTED",
            "PROTOCOL_INSTALL_REQUESTED","NODE_STOPPED"
        ]

        try:
            m.start()
            raise AssertionError("STOPPED node started without reinitialization")
        except RuntimeError:
            pass

        try:
            NodeManager(protocol_interface=pi).initialize()
            raise AssertionError("Node Manager initialized without configuration")
        except RuntimeError:
            pass

    print("Node Core Node Manager contract tests: PASS")

if __name__=="__main__":
    main()
