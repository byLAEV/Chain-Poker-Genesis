#!/usr/bin/env python3
from pathlib import Path
import json
import hashlib
import sys
import tempfile
import zipfile

BASE=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(BASE/"Protocol Interface"))
sys.path.insert(0,str(BASE/"Engine Runtime"))

from protocol_interface import ProtocolInterface
from protocol_package import ProtocolPackageVerifier
from engine_runtime import EngineRuntime


def make_manifest():
    manifest={
        "protocol_id":"example.protocol",
        "version":"1.0.0",
        "engine_id":"engine.main",
        "capabilities":["storage"],
    }
    raw=json.dumps(manifest,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
    manifest["manifest_hash"]=hashlib.sha256(raw).hexdigest()
    return manifest


def make_package(root, manifest):
    package=root/"example-protocol.zip"
    with zipfile.ZipFile(package,"w") as archive:
        archive.writestr("PROTOCOL-MANIFEST.json",json.dumps(manifest))
        archive.writestr("protocol.txt","protocol-neutral package payload")
    return package


def main():
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)
        manifest=make_manifest()
        package=make_package(root,manifest)

        engines=EngineRuntime()
        interface=ProtocolInterface(root/"Protocols",engines)
        interface.discover_manifest(manifest)
        assert interface.check_compatibility("example.protocol",("storage",))
        interface.register("example.protocol")
        record=interface.install("example.protocol",package)

        installed=root/"Protocols"/"Installed"/"example.protocol"
        assert installed.is_dir()
        assert (installed/"package.zip").is_file()
        assert record.descriptor.metadata["installed_path"] == str(installed)
        assert "engine.main" in engines.engines

        interface.activate("example.protocol")
        assert engines.engines["engine.main"].state=="ACTIVE"

        bad=dict(manifest)
        bad["manifest_hash"]="0"*64
        bad_package=make_package(root,bad)
        interface2=ProtocolInterface(root/"OtherProtocols",EngineRuntime())
        interface2.discover_manifest(bad)
        assert interface2.check_compatibility("example.protocol",("storage",))
        interface2.register("example.protocol")
        try:
            interface2.install("example.protocol",bad_package)
            raise AssertionError("tampered manifest accepted")
        except ValueError:
            pass

    print("Node Core Protocol persistent installation / manifest / identity / engine tests: PASS")


if __name__=="__main__":
    main()
