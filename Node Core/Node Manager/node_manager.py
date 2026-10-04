"""Node Core Manager reference implementation."""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "Configuration"))
from configuration_manager import ConfigurationManager, ConfigurationError

@dataclass
class NodeStatus:
    state: str = "UNINITIALIZED"
    protocols: list[str] = field(default_factory=list)
    engines: list[str] = field(default_factory=list)

class NodeManager:
    STATES = {
        "UNINITIALIZED", "READY", "RUNNING", "DEGRADED",
        "RECOVERY", "SHUTTING_DOWN", "STOPPED",
    }

    def __init__(self, protocol_interface=None, configuration_path=None):
        self.status = NodeStatus()
        self.protocol_interface = protocol_interface
        self.configuration_manager = ConfigurationManager(Path(configuration_path)) if configuration_path else None
        self.configuration = None

    def initialize(self) -> NodeStatus:
        if self.status.state != "UNINITIALIZED":
            raise RuntimeError("node must be uninitialized")
        if self.configuration_manager is not None:
            self.configuration = self.configuration_manager.load()
        self.status.state = "READY"
        return self.status

    def start(self) -> NodeStatus:
        if self.status.state != "READY":
            raise RuntimeError("node must be ready")
        self.status.state = "RUNNING"
        return self.status

    def stop(self) -> NodeStatus:
        if self.status.state not in {"RUNNING", "DEGRADED", "RECOVERY"}:
            raise RuntimeError("node is not running")
        self.status.state = "SHUTTING_DOWN"
        self.status.state = "STOPPED"
        return self.status

    def recover(self) -> NodeStatus:
        if self.status.state not in {"DEGRADED", "RECOVERY"}:
            raise RuntimeError("node is not in recovery condition")
        self.status.state = "RECOVERY"
        self.status.state = "READY"
        return self.status

    def register_engine(self, name: str) -> None:
        if self.status.state not in {"READY", "RUNNING"}:
            raise RuntimeError("node must be ready or running")
        if not name:
            raise ValueError("engine name is required")
        if name not in self.status.engines:
            self.status.engines.append(name)

    def unregister_engine(self, name: str) -> None:
        if name not in self.status.engines:
            raise KeyError(name)
        self.status.engines.remove(name)

    def request_protocol_installation(self, name: str) -> None:
        if not name or name == "Node Core":
            raise ValueError("invalid protocol")
        if self.protocol_interface is None:
            raise RuntimeError("Protocol Interface is required")
        record = self.protocol_interface.get(name)
        self.protocol_interface.install(name)
        self.status.protocols.append(record.descriptor.protocol_id)

    def install_protocol(self, name: str) -> None:
        """Backward-compatible alias; installation still goes through Protocol Interface."""
        self.request_protocol_installation(name)

    def status_view(self) -> dict:
        return self.snapshot()

    def readiness(self) -> bool:
        return self.status.state in {"READY", "RUNNING"} and (self.configuration_manager is None or self.configuration is not None)

    def snapshot(self) -> dict:
        return {
            "state": self.status.state,
            "protocols": list(self.status.protocols),
            "engines": list(self.status.engines),
        }
