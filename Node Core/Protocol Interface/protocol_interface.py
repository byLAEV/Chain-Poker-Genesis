"""Protocol-neutral Node Core protocol interface."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from protocol_manifest_validator import validate_manifest
from protocol_package import ProtocolPackageVerifier

@dataclass(frozen=True)
class ProtocolDescriptor:
    protocol_id:str
    version:str
    engine_id:str
    manifest_hash:str
    capabilities:tuple[str,...]=()
    metadata:dict=field(default_factory=dict)

@dataclass
class ProtocolRecord:
    descriptor:ProtocolDescriptor
    state:str="DISCOVERED"
    registered_at:str=field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class ProtocolInterface:
    STATES={"DISCOVERED","COMPATIBLE","REGISTERED","INSTALLED","ACTIVE","SUSPENDED","REMOVED"}

    def __init__(self, protocols_root=None, engine_runtime=None):
        self._records={}
        self.protocols_root = Path(protocols_root) if protocols_root else None
        self.engine_runtime = engine_runtime
        self.package_verifier = (
            ProtocolPackageVerifier(self.protocols_root) if self.protocols_root else None
        )

    def discover(self,descriptor):
        if descriptor.protocol_id in self._records:
            raise ValueError("protocol already discovered")
        self._records[descriptor.protocol_id]=ProtocolRecord(descriptor)
        return self._records[descriptor.protocol_id]

    def discover_manifest(self, manifest):
        validate_manifest(manifest)
        descriptor=ProtocolDescriptor(
            manifest["protocol_id"],
            manifest["version"],
            manifest["engine_id"],
            manifest["manifest_hash"],
            tuple(manifest.get("capabilities", [])),
            {k:v for k,v in manifest.items() if k not in {
                "protocol_id","version","engine_id","manifest_hash","capabilities"
            }},
        )
        return self.discover(descriptor)

    def check_compatibility(self,protocol_id, node_capabilities=()):
        r=self._records[protocol_id]
        ok=set(r.descriptor.capabilities).issubset(set(node_capabilities))
        r.state="COMPATIBLE" if ok else "DISCOVERED"
        return ok

    def register(self,protocol_id):
        r=self._records[protocol_id]
        if r.state!="COMPATIBLE":
            raise RuntimeError("protocol must be compatible before registration")
        r.state="REGISTERED"
        return r

    def install(self,protocol_id, package_path=None):
        r=self._records[protocol_id]
        if r.state!="REGISTERED":
            raise RuntimeError("protocol must be registered before installation")
        if self.package_verifier is not None:
            if package_path is None:
                raise ValueError("package path required for persistent installation")
            installed_path=self.package_verifier.install(package_path, protocol_id)
            if self.engine_runtime is not None:
                if r.descriptor.engine_id not in self.engine_runtime.engines:
                    self.engine_runtime.register(r.descriptor.engine_id, r.descriptor.version)
            r.descriptor.metadata["installed_path"]=str(installed_path)
        r.state="INSTALLED"
        return r

    def activate(self,protocol_id):
        r=self._records[protocol_id]
        if r.state!="INSTALLED": raise RuntimeError("protocol must be installed before activation")
        if self.engine_runtime is not None:
            engine=self.engine_runtime.engines.get(r.descriptor.engine_id)
            if engine is None:
                raise RuntimeError("required protocol engine is not registered")
            if engine.state!="ACTIVE":
                self.engine_runtime.start(r.descriptor.engine_id)
        r.state="ACTIVE"
        return r

    def suspend(self,protocol_id):
        self._records[protocol_id].state="SUSPENDED"
        return self._records[protocol_id]

    def remove(self,protocol_id):
        self._records[protocol_id].state="REMOVED"
        return self._records[protocol_id]

    def get(self,protocol_id):
        return self._records[protocol_id]

    def all(self):
        return tuple(self._records.values())
