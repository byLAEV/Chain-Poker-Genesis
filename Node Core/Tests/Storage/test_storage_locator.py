#!/usr/bin/env python3
"""Reference tests for the canonical Node Core Storage Locator."""

import tempfile
from pathlib import Path
from bootstrap_node import main as bootstrap_main
from object_registry import ObjectRegistry
from storage_manager import StorageManager
from storage_locator import StorageLocator

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
        metadata = manager.put_json("record", "locator-record-0001", {"status": "VALID"})
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
        ObjectRegistry(target).register(registry_entry)
        location = StorageLocator(target).locate("locator-record-0001")
        assert location["logical_path"] == metadata["relative_path"]
        assert location["provider_type"] == "LOCAL"
        assert location["location_state"] == "LOCAL_ONLY"

        registry = ObjectRegistry(target)
        bad = dict(registry_entry)
        bad["provider_type"] = "UNSUPPORTED"
        bad["object_id"] = "locator-record-unsupported"
        registry.register(bad)
        try:
            StorageLocator(target).locate("locator-record-unsupported")
        except Exception:
            pass
        else:
            raise AssertionError("unsupported provider unexpectedly accepted")

        print("status = VERIFIED")
        print("locator = READY")

if __name__ == "__main__":
    main()
