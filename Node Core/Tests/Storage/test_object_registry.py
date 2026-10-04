#!/usr/bin/env python3
import tempfile, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"Storage"/"Storage Manager"))
sys.path.insert(0,str(ROOT/"Storage"/"Object Registry"))
from storage_manager import StorageManager
from object_registry import ObjectRegistry, RegistryError

def main():
    with tempfile.TemporaryDirectory() as temp:
        metadata=StorageManager(temp).put_json("public","registry-record-0001",{"status":"VALID"},mirror=False)
        registry=ObjectRegistry(temp)
        entry=registry.get("registry-record-0001")
        assert entry["storage_class"]=="public"
        assert entry["state"]=="PRESENT"
        assert entry["version"]==1
        assert entry["created_at"] and entry["updated_at"]
        invalid=dict(entry); invalid["content_hash"]="invalid"
        try: registry.register(invalid)
        except RegistryError: pass
        else: raise AssertionError("invalid registry hash was accepted")
        reserved=dict(entry); reserved["object_id"]="cpg-test"; reserved["object_class"]="protocol-reserved"; reserved["storage_class"]="protocol-reserved"
        try: registry.register(reserved)
        except RegistryError: pass
        else: raise AssertionError("protocol-reserved object was registered")
    print("Node Core Storage registry tests: PASS")

if __name__=="__main__": main()
