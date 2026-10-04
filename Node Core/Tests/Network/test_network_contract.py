#!/usr/bin/env python3
from pathlib import Path
import sys

BASE=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(BASE/"Network"))

from network_manager import NetworkManager
from peer_registry import PeerRegistry, Peer
from transport import encode_frame
from synchronization_state import validate_transition

class FakeTransport:
    def __init__(self):
        self.sent=[]
    def send(self, host, port, message, timeout=2.0):
        self.sent.append((host,port,message))
        if message["type"] == "NODE_CORE_HELLO":
            return {"type":"NODE_CORE_HELLO_ACK"}
        return {"type":"NODE_CORE_MESSAGE_ACK"}

def main():
    registry=PeerRegistry()
    registry.register(Peer("peer-b","127.0.0.1",9002))
    registry.register(Peer("peer-a","127.0.0.1",9001))
    try:
        registry.register(Peer("peer-a","127.0.0.1",9001))
        raise AssertionError("duplicate peer accepted")
    except ValueError:
        pass
    assert [p.peer_id for p in registry.all()] == ["peer-a","peer-b"]

    transport=FakeTransport()
    network=NetworkManager("node-a",transport=transport)
    network.register_peer("peer-b","127.0.0.1",9002)
    network.connect_peer("peer-b")
    assert network.get_network_state().connected_peers == 1
    assert network.get_network_state().status == "CONNECTED"

    response=network.send_message("peer-b",{"kind":"NODE_CORE_TEST"})
    assert response["type"]=="NODE_CORE_MESSAGE_ACK"
    assert transport.sent[-1][2]["type"]=="NODE_CORE_MESSAGE"

    results=network.propagate({"kind":"PROPAGATION_TEST"})
    assert results=={"peer-b":"SENT"}

    # Network synchronization must not claim SYNCHRONIZED without
    # both provider readiness and threshold evidence.
    assert not validate_transition("THRESHOLD_REACHED","SYNCHRONIZED",False,True)
    assert validate_transition("THRESHOLD_REACHED","SYNCHRONIZED",True,True)

    # Frame encoding is deterministic and bounded by the transport contract.
    frame=encode_frame({"b":2,"a":1})
    assert frame[:4] == len(frame[4:]).to_bytes(4,"big")

    assert network.get_network_state().status != "READY"

    # Protocol isolation: transport envelope is Node Core, not CPG state.
    envelope=transport.sent[-1][2]
    assert envelope["type"]=="NODE_CORE_MESSAGE"
    assert "cpg_consensus" not in envelope
    assert "table_state" not in envelope
    assert "ledger" not in envelope

    print("Node Core Network contract tests: PASS")

if __name__=="__main__":
    main()
