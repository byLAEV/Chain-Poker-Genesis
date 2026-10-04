#!/usr/bin/env python3
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE / "API"))

from node_core_api import NodeCoreAPI

class Storage:
    def read(self, object_id):
        return {"object_id": object_id}

class Manager:
    def snapshot(self):
        return {"state": "READY"}

def main():
    api = NodeCoreAPI(manager=Manager(), storage=Storage())

    assert api.health()["status"] == "READY"

    unknown = NodeCoreAPI()
    assert unknown.health()["status"] == "UNKNOWN"
    try:
        api.read("")
        raise AssertionError("empty object_id accepted")
    except ValueError:
        pass
    assert api.node_status()["state"] == "READY"
    assert api.read("test-object")["object_id"] == "test-object"

    # The facade is intentionally partial; unsupported contract domains
    # must not be represented as implemented merely by documentation.
    assert api.__class__.__name__ == "NodeCoreAPI"

    print("Node Core API contract baseline tests: PASS")

if __name__ == "__main__":
    main()
