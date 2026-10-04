#!/usr/bin/env python3
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE / "Engine Runtime"))

from engine_runtime import EngineRuntime

def main():
    runtime = EngineRuntime()

    try:
        runtime.register("", "1.0.0")
        raise AssertionError("empty engine name accepted")
    except ValueError:
        pass

    try:
        runtime.register("engine.main", "")
        raise AssertionError("empty engine version accepted")
    except ValueError:
        pass

    record = runtime.register("engine.main", "1.0.0")
    assert record.state == "REGISTERED"

    runtime.start("engine.main")
    assert runtime.snapshot()["engine.main"]["state"] == "ACTIVE"

    runtime.stop("engine.main")
    assert runtime.snapshot()["engine.main"]["state"] == "STOPPED"

    try:
        runtime.start("missing.engine")
        raise AssertionError("unknown engine accepted")
    except KeyError:
        pass

    print("Node Core Engine Runtime contract tests: PASS")

if __name__ == "__main__":
    main()
