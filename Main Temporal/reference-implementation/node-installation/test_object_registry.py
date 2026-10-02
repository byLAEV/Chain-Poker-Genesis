#!/usr/bin/env python3
import tempfile
from pathlib import Path
from bootstrap_node import main as bootstrap_main
from object_registry import ObjectRegistry, RegistryError
from storage_manager import StorageManager

def bootstrap(target):
    import sys
    old = sys.argv
    try:
        sys.argv = ["bootstrap_node.py", str(target)]
        assert bootstrap_main() == 0
    finally:
        sys.argv = old

def main():
    with tempfile.TemporaryDirectory() as temp:
        target = Path(temp) / "node"
        bootstrap(target)
        manager = StorageManager(target)
        metadata = manager.put_json("record", "registry-record-0001", {"status": "VALID"})
        registry = ObjectRegistry(target)
        registry_entry = {
            "object_id": metadata["object_id"],
            "object_class": metadata["object_class"],
            "relative_path": metadata["relative_path"],
            "content_hash": metadata["content_hash"],
            "storage_version": metadata["storage_version"],
            "provider_type": "LOCAL",
            "location_state": "LOCAL_ONLY",
            "object_state": "PRESENT",
            "synchronization_state": "NOT_SYNCHRONIZED",
        }
        registry.register(registry_entry)
        assert registry.get("registry-record-0001")["location_state"] == "LOCAL_ONLY"
        try:
            registry.register({"object_id": "cpg-test", "object_class": "protocol-reserved"})
        except RegistryError:
            pass
        else:
            raise AssertionError("protocol-reserved object was registered")

        invalid = {
            **registry_entry,
            "content_hash": "invalid",
        }
        try:
            registry.register(invalid)
        except RegistryError:
            pass
        else:
            raise AssertionError("invalid registry hash was accepted")
        print("status = VERIFIED")
        print("registry = READY")

if __name__ == "__main__":
    main()
