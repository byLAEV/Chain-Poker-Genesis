"""Protocol-neutral Node Core Engine Runtime.

Implements only the canonical Engine Runtime Contract. Node Core lifecycle is
owned by Runtime; protocol installation is owned by Protocol Interface.
"""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class EngineRecord:
    name: str
    version: str
    state: str = "REGISTERED"

@dataclass
class EngineRuntime:
    engines: dict[str, EngineRecord] = field(default_factory=dict)

    def register(self, name: str, version: str) -> EngineRecord:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("engine name required")
        if not isinstance(version, str) or not version.strip():
            raise ValueError("engine version required")
        if name in self.engines:
            raise ValueError("engine already registered")
        record = EngineRecord(name=name, version=version)
        self.engines[name] = record
        return record

    def unregister(self, name: str) -> None:
        record = self.engines[name]
        if record.state == "ACTIVE":
            raise RuntimeError("active engine must be stopped before unregister")
        del self.engines[name]

    def start(self, name: str) -> None:
        record = self.engines[name]
        if record.state == "ACTIVE":
            raise RuntimeError("engine already active")
        if record.state == "STOPPED":
            record.state = "ACTIVE"
            return
        if record.state != "REGISTERED":
            raise RuntimeError("invalid engine state")
        record.state = "ACTIVE"

    def stop(self, name: str) -> None:
        record = self.engines[name]
        if record.state != "ACTIVE":
            raise RuntimeError("engine is not active")
        record.state = "STOPPED"

    def snapshot(self) -> dict[str, dict[str, str]]:
        return {
            name: {"name": r.name, "version": r.version, "state": r.state}
            for name, r in self.engines.items()
        }
