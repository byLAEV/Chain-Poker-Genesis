#!/usr/bin/env python3
import tempfile
from pathlib import Path
from bootstrap_node import main as bootstrap_main
from storage_manager import StorageError, StorageManager

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
        metadata = manager.put_json("record", "reference-record-0001",
                                    {"type":"NODE_CORE_REFERENCE","status":"VALID"})
        assert len(metadata["content_hash"]) == 64
        value, read_metadata = manager.get_json("record", "reference-record-0001")
        assert value["status"] == "VALID"
        assert manager.verify("record", "reference-record-0001", read_metadata["content_hash"])
        try:
            manager.put_json("protocol-reserved", "cpg-test-object", {"x":1})
        except StorageError as exc:
            assert str(exc) == "protocol-reserved storage is not writable by Node Core"
        else:
            raise AssertionError("protocol-reserved write unexpectedly succeeded")

        for bad_id in ("../escape", "a/b", "a\\\\b", "..", ""):
            try:
                manager.put_json("record", bad_id, {"x": 1})
            except StorageError:
                pass
            else:
                raise AssertionError("invalid object id accepted")
        try:
            manager.get_json("record", "missing-record")
        except StorageError as exc:
            assert str(exc) == "object not found"
        else:
            raise AssertionError("missing object unexpectedly returned")

        print("status = VERIFIED")
        print("storage_manager = READY")
        print("protocol_reserved = ISOLATED")

if __name__ == "__main__":
    main()
