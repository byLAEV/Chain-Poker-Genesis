"""Node Core control-plane manager.

Node Manager coordinates canonical subsystems; it does not reimplement their
state machines. Runtime owns Node Core runtime lifecycle, Configuration owns
configuration validation, Engine Runtime owns engine lifecycle, and Protocol
Interface owns protocol installation.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "Configuration"))
sys.path.insert(0, str(ROOT / "Runtime"))
sys.path.insert(0, str(ROOT / "Engine Runtime"))
from configuration_manager import ConfigurationManager
from runtime_manager import RuntimeManager
from engine_runtime import EngineRuntime

@dataclass
class NodeStatus:
    state: str = "UNINITIALIZED"
    protocols: list[str] = field(default_factory=list)
    engines: list[str] = field(default_factory=list)
    events: list[dict] = field(default_factory=list)

class NodeManager:
    STATES = {"UNINITIALIZED","READY","RUNNING","DEGRADED","RECOVERY","SHUTTING_DOWN","STOPPED"}

    def __init__(self, protocol_interface=None, configuration_path=None,
                 runtime_manager=None, engine_runtime=None, recovery=None):
        self.status = NodeStatus()
        self.protocol_interface = protocol_interface
        self.configuration_manager = ConfigurationManager(Path(configuration_path)) if configuration_path else None
        self.runtime_manager = runtime_manager
        self.engine_runtime = engine_runtime or EngineRuntime()
        self.recovery = recovery
        self.configuration = None

    def _event(self, event: str, **data):
        self.status.events.append({"event": event, **data})

    def initialize(self) -> NodeStatus:
        if self.status.state != "UNINITIALIZED":
            raise RuntimeError("node must be uninitialized")
        if self.configuration_manager is None:
            raise RuntimeError("Node Core configuration is required")
        self.configuration = self.configuration_manager.load()
        if self.runtime_manager is None:
            self.runtime_manager = RuntimeManager(self.configuration_manager.path.parents[2])
        readiness = self.runtime_manager.readiness()
        if not readiness.is_ready():
            raise RuntimeError("Node Core readiness requirements are not satisfied")
        self.status.state = "READY"
        self._event("NODE_READY")
        return self.status

    def start(self) -> NodeStatus:
        if self.status.state != "READY":
            raise RuntimeError("node must be ready")
        if self.runtime_manager is None:
            raise RuntimeError("Runtime Manager is required")
        self.runtime_manager.start()
        self.status.state = "RUNNING"
        self._event("NODE_STARTED")
        return self.status

    def stop(self) -> NodeStatus:
        if self.status.state not in {"RUNNING","DEGRADED","RECOVERY"}:
            raise RuntimeError("node is not running")
        if self.runtime_manager is not None:
            self.status.state = "SHUTTING_DOWN"
            self.runtime_manager.stop()
        else:
            self.status.state = "SHUTTING_DOWN"
        self.status.state = "STOPPED"
        self._event("NODE_STOPPED")
        return self.status

    def degrade(self) -> NodeStatus:
        """Enter the canonical degraded state after an external subsystem fault."""
        if self.status.state != "RUNNING": raise RuntimeError("node must be running")
        if self.runtime_manager is None: raise RuntimeError("Runtime Manager is required")
        from runtime_state import RuntimeState
        self.runtime_manager.runtime.transition(RuntimeState.DEGRADED)
        self.status.state = "DEGRADED"
        self._event("NODE_DEGRADED")
        return self.status

    def recover(self) -> NodeStatus:
        if self.status.state not in {"DEGRADED","RECOVERY"}:
            raise RuntimeError("node is not in recovery condition")
        if self.recovery is None:
            raise RuntimeError("Recovery service is required")
        result = self.recovery.recover()
        if result.get("status") not in {"RECOVERY_READY","RECOVERED","READY"}:
            raise RuntimeError("recovery did not reach a ready state")
        if self.runtime_manager is not None:
            readiness = self.runtime_manager.readiness()
            self.runtime_manager.complete_recovery_to_ready(readiness)
        self.status.state = "READY"
        self._event("NODE_RECOVERED")
        return self.status

    def register_engine(self, name: str, version: str = "UNSPECIFIED") -> None:
        if self.status.state not in {"READY","RUNNING"}:
            raise RuntimeError("node must be ready or running")
        record = self.engine_runtime.register(name, version)
        self.status.engines.append(record.name)
        self._event("ENGINE_REGISTERED", name=record.name, version=record.version)

    def unregister_engine(self, name: str) -> None:
        self.engine_runtime.unregister(name)
        if name in self.status.engines:
            self.status.engines.remove(name)
        self._event("ENGINE_UNREGISTERED", name=name)

    def request_protocol_installation(self, name: str) -> None:
        if not name or name == "Node Core":
            raise ValueError("invalid protocol")
        if self.protocol_interface is None:
            raise RuntimeError("Protocol Interface is required")
        if self.status.state not in {"READY","RUNNING"}:
            raise RuntimeError("node must be ready or running")
        record = self.protocol_interface.get(name)
        self.protocol_interface.install(name)
        if record.descriptor.protocol_id not in self.status.protocols:
            self.status.protocols.append(record.descriptor.protocol_id)
        self._event("PROTOCOL_INSTALL_REQUESTED", protocol_id=record.descriptor.protocol_id)

    def install_protocol(self, name: str) -> None:
        self.request_protocol_installation(name)

    def status_view(self) -> dict:
        return self.snapshot()

    def readiness(self) -> bool:
        if self.status.state not in {"READY","RUNNING"}:
            return False
        return self.runtime_manager is not None and self.runtime_manager.readiness().is_ready()

    def snapshot(self) -> dict:
        return {
            "state": self.status.state,
            "protocols": list(self.status.protocols),
            "engines": list(self.status.engines),
            "events": list(self.status.events),
        }
