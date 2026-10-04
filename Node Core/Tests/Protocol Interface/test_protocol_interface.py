#!/usr/bin/env python3
from pathlib import Path
import sys
BASE=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(BASE/"Protocol Interface"))
from protocol_interface import ProtocolDescriptor,ProtocolInterface
from protocol_manifest_validator import validate_manifest

def main():
    d=ProtocolDescriptor("example.protocol","1.0.0","engine.main","abc123",("storage","cryptography"))
    validate_manifest({"protocol_id":d.protocol_id,"version":d.version,"engine_id":d.engine_id,"manifest_hash":d.manifest_hash,"capabilities":list(d.capabilities)})
    i=ProtocolInterface(); i.discover(d)
    assert i.check_compatibility(d.protocol_id,("storage","cryptography"))
    i.register(d.protocol_id); i.install(d.protocol_id); assert i.activate(d.protocol_id).state=="ACTIVE"
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
    print("Node Core Protocol Interface implementation tests: PASS")
if __name__=="__main__": main()
