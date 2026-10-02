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
        ObjectRegistry(target).register({
            **metadata,
            "provider_type": "LOCAL",
            "location_state": "LOCAL_ONLY",
            "object_state": "PRESENT",
            "synchronization_state": "NOT_SYNCHRONIZED",
        })
        location = StorageLocator(target).locate("locator-record-0001")
        assert location["logical_path"] == metadata["relative_path"]
        assert location["provider_type"] == "LOCAL"
        assert location["location_state"] == "LOCAL_ONLY"
        print("status = VERIFIED")
        print("locator = READY")

if __name__ == "__main__":
    main()
