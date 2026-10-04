"""Unified protocol-neutral Node Core reference composition."""
from __future__ import annotations
from pathlib import Path
import importlib.util, sys

ROOT=Path(__file__).resolve().parent
CRYPTO_CORE_ROOT=ROOT/"Cryptography"/"Core"
PROTOCOL_INTERFACE_ROOT=ROOT/"Protocol Interface"

for path in (CRYPTO_CORE_ROOT, PROTOCOL_INTERFACE_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0,str(path))

def _load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    mod=importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[name]=mod
    spec.loader.exec_module(mod)
    return mod

crypto=_load("node_core_crypto","Cryptography/Core/crypto_service.py")
identity=_load("node_core_identity","Identity/identity_core.py")
manager=_load("node_core_manager","Node Manager/node_manager.py")
protocol=_load("node_core_protocol_interface","Protocol Interface/protocol_interface.py")
storage=_load("node_core_storage_api","Storage/API/storage_api.py")
recovery=_load("node_core_recovery","Recovery/recovery_manager.py")
runtime=_load("node_core_engine_runtime","Engine Runtime/engine_runtime.py")
time_service=_load("node_core_time","Time/time_service.py")
security=_load("node_core_security","Security/security_service.py")


class NodeCore:
    VERSION="1.0.0"

    def __init__(self, node_root):
        self.root=Path(node_root).resolve()
        self.crypto=crypto.CryptoService()
        self.identity=identity.IdentityManager()
        self.engines=runtime.EngineRuntime()
        self.storage=storage.StorageAPI(self.root)
        self.recovery=recovery.RecoveryManager(self.root)
        self.protocol_interface=protocol.ProtocolInterface(
            protocols_root=self.root/"protocols",
            engine_runtime=self.engines,
        )
        self.manager=manager.NodeManager(
            protocol_interface=self.protocol_interface,
            configuration_path=self.root/"node-storage/configuration/node-config.json",
            engine_runtime=self.engines,
            recovery=self.recovery,
        )
        self.time=time_service.TimeService()
        self.security=security.SecurityService()

    def initialize(self):
        self.manager.initialize()
        return self.manager.snapshot()

    def activate(self):
        return self.manager.start().state

    def snapshot(self):
        return {
            "node_core_version":self.VERSION,
            "node":self.manager.snapshot(),
            "engines":self.engines.snapshot(),
            "storage":self.storage.status(),
            "time_sequence":self.time.sequence,
        }
