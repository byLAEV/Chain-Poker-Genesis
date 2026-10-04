#!/usr/bin/env python3
"""Cross-component Node Core lifecycle validation.

Validates hand-off boundaries among Runtime, Identity, Storage, Recovery,
Network and Protocol Interface. This test does not install CPG and does not
exercise or modify Merkle.
"""
from __future__ import annotations
import sys
import tempfile
from pathlib import Path

BASE=Path(__file__).resolve().parents[2]
CRYPTO=BASE/"Cryptography"/"Core"
CRYPTO_PROVIDERS=BASE/"Cryptography"/"Providers"
# Explicit import boundary required by the existing crypto service module layout.
for p in (
    BASE, BASE/"Bootstrap/Installer", BASE/"Runtime", BASE/"Identity",
    BASE/"Recovery", BASE/"Network", BASE/"Protocol Interface", CRYPTO, CRYPTO_PROVIDERS,
):
    sys.path.insert(0,str(p))

from bootstrap_node import install
from identity_core import IdentityManager
from network_manager import NetworkManager
from node_core import NodeCore
from node_runtime import evaluate_readiness
from protocol_interface import ProtocolDescriptor, ProtocolInterface
from protocol_manifest_validator import validate_manifest
from recovery_manager import RecoveryManager
from runtime_state import Runtime, RuntimeState

class FakeTransport:
    def __init__(self): self.sent=[]
    def send(self,host,port,message,timeout=2.0):
        self.sent.append((host,port,message))
        return {"type":"NODE_CORE_HELLO_ACK"} if message["type"]=="NODE_CORE_HELLO" else {"type":"NODE_CORE_MESSAGE_ACK"}

def main():
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)/"node"
        install(root)

        readiness=evaluate_readiness(root)
        assert readiness.is_ready()
        runtime=Runtime()
        for target in (
            RuntimeState.ENVIRONMENT_VALIDATED,
            RuntimeState.IDENTITY_INITIALIZED,
            RuntimeState.STORAGE_INITIALIZED,
            RuntimeState.STORAGE_STRUCTURE_VERIFIED,
            RuntimeState.INTEGRITY_VERIFIED,
            RuntimeState.RECOVERY_READY,
            RuntimeState.NODE_CORE_READY,
        ):
            runtime.transition(target,readiness)

        identity=IdentityManager()
        node_identity,_=identity.create_identity(1)
        identity.validate_identity()
        identity.register("CROSS_COMPONENT_TEST")
        identity.initialize(2,"CROSS_COMPONENT_TEST")
        identity.activate(3,node_core_ready=True)
        assert identity.node_life.state=="ACTIVE"

        node=NodeCore(root)
        record=node.storage.create("public","cross-component-test",b"lifecycle",mirror=False)
        assert record["object_id"]=="cross-component-test"
        data,metadata=node.storage.read("public","cross-component-test")
        assert data==b"lifecycle" and metadata["read_source"]=="LOCAL"

        recovery=RecoveryManager(root).recover()
        assert recovery["status"]=="RECOVERY_READY"

        transport=FakeTransport()
        network=NetworkManager(node_identity.node_id,transport=transport)
        network.register_peer("peer-b","127.0.0.1",9002)
        network.connect_peer("peer-b")
        assert network.get_network_state().connected_peers==1
        assert network.send_message("peer-b",{"kind":"CROSS_COMPONENT_TEST"})["type"]=="NODE_CORE_MESSAGE_ACK"
        envelope=transport.sent[-1][2]
        assert envelope["sender"]==node_identity.node_id
        assert envelope["type"]=="NODE_CORE_MESSAGE"
        assert "cpg_consensus" not in envelope and "table_state" not in envelope and "ledger" not in envelope

        descriptor=ProtocolDescriptor("cross.component.protocol","1.0.0","engine.cross","abc123",("storage","cryptography"))
        validate_manifest({"protocol_id":descriptor.protocol_id,"version":descriptor.version,"engine_id":descriptor.engine_id,"manifest_hash":descriptor.manifest_hash,"capabilities":list(descriptor.capabilities)})
        protocols=ProtocolInterface(engine_runtime=node.engines)
        protocols.discover(descriptor)
        assert protocols.check_compatibility(descriptor.protocol_id, descriptor.capabilities)
        protocols.register(descriptor.protocol_id)
        protocols.install(descriptor.protocol_id)
        assert protocols.get(descriptor.protocol_id).state=="INSTALLED"

        assert node.storage is not None
        assert node.recovery is not None
        assert node.manager.recovery is node.recovery
        assert node.protocol_interface.engine_runtime is node.engines
        assert node.engines.snapshot()==[]

        print("Node Core cross-component lifecycle validation: PASS")
        print("runtime_identity_storage_recovery = PASS")
        print("identity_network = PASS")
        print("protocol_interface_isolation = PASS")
        print("cpg_protocol = NOT_INSTALLED")
        print("merkle = UNTOUCHED")
        return 0

if __name__=="__main__":
    raise SystemExit(main())
