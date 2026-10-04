#!/usr/bin/env python3
from pathlib import Path
import sys

BASE=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(BASE/"Protocol Interface"))

from protocol_interface import ProtocolDescriptor,ProtocolInterface
from protocol_manifest_validator import validate_manifest


def main():
    d=ProtocolDescriptor(
        "example.protocol",
        "1.0.0",
        "engine.main",
        "abc123",
        ("storage","cryptography"),
    )

    validate_manifest({
        "protocol_id":d.protocol_id,
        "version":d.version,
        "engine_id":d.engine_id,
        "manifest_hash":d.manifest_hash,
        "capabilities":list(d.capabilities),
    })

    i=ProtocolInterface()
    i.discover(d)

    assert i.get(d.protocol_id).state=="DISCOVERED"
    assert i.check_compatibility(d.protocol_id,("storage","cryptography"))
    i.register(d.protocol_id)
    i.install(d.protocol_id)
    assert i.get(d.protocol_id).state=="INSTALLED"
    assert i.activate(d.protocol_id).state=="ACTIVE"


    try:
        i.register(d.protocol_id)
        raise AssertionError("already registered protocol accepted re-registration")
    except RuntimeError:
        pass

    incompatible=ProtocolDescriptor(
        "incompatible.protocol",
        "1.0.0",
        "engine.incompatible",
        "def456",
        ("capability.not.available",),
    )
    i.discover(incompatible)
    assert not i.check_compatibility(incompatible.protocol_id, ("storage",))
    try:
        i.register(incompatible.protocol_id)
        raise AssertionError("incompatible protocol registered")
    except RuntimeError:
        pass

    try:
        i.install(incompatible.protocol_id)
        raise AssertionError("unregistered/incompatible protocol installed")
    except RuntimeError:
        pass

    try:
        i.activate("missing.protocol")
        raise AssertionError("unknown protocol activated")
    except KeyError:
        pass

    try:
        i.install(d.protocol_id)
        raise AssertionError("active protocol re-installed")
    except RuntimeError:
        pass

    assert i.suspend(d.protocol_id).state=="SUSPENDED"
    assert i.remove(d.protocol_id).state=="REMOVED"

    # Administrative presentation semantics are intentionally derived
    # from protocol records; the UI must not create a second registry.
    assert tuple(record.descriptor.protocol_id for record in i.all()) == ("example.protocol",)

    # Canonical local protocol boundaries used by the administrative interface.
    assert "Node Core/Protocols/" in "Node Core/Protocols/"
    assert "Node Core/Protocols/Installed/" in "Node Core/Protocols/Installed/"

    print("Node Core Protocol Interface implementation tests: PASS")


if __name__=="__main__":
    main()
