"""Unified protocol-neutral Node Core reference composition."""
from __future__ import annotations
from pathlib import Path
import importlib.util, sys
ROOT=Path(__file__).resolve().parent
def _load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path); mod=importlib.util.module_from_spec(spec); assert spec and spec.loader; sys.modules[name]=mod; spec.loader.exec_module(mod); return mod
crypto=_load("node_core_crypto","Cryptography/Core/crypto_service.py")
identity=_load("node_core_identity","Identity/identity_core.py")
manager=_load("node_core_manager","Node Manager/node_manager.py")
runtime=_load("node_core_engine_runtime","Engine Runtime/engine_runtime.py")
time_service=_load("node_core_time","Time/time_service.py")
security=_load("node_core_security","Security/security_service.py")
class NodeCore:
    VERSION="1.0.0"
    def __init__(self):
        self.crypto=crypto.CryptoService()
        self.identity=identity.IdentityManager()
        self.manager=manager.NodeManager()
        self.engines=runtime.EngineRuntime()
        self.time=time_service.TimeService()
        self.security=security.SecurityService()
    def initialize(self):
        self.manager.initialize(); return self.manager.snapshot()
    def activate(self):
        return self.manager.start().state
    def snapshot(self):
        return {"node_core_version":self.VERSION,"node":self.manager.snapshot(),"engines":self.engines.snapshot(),"time_sequence":self.time.sequence}
