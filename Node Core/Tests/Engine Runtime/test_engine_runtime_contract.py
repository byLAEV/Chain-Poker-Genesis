#!/usr/bin/env python3
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE / "Engine Runtime"))
from engine_runtime import EngineRuntime

def main():
    runtime = EngineRuntime()

    for name, version in [("", "1.0.0"), ("engine.main", "")]:
        try:
            runtime.register(name, version)
            raise AssertionError("invalid engine identity accepted")
        except ValueError:
            pass

    record = runtime.register("engine.main", "1.0.0")
    assert record.state == "REGISTERED"

    try:
        runtime.register("engine.main", "1.0.0")
        raise AssertionError("duplicate engine accepted")
    except ValueError:
        pass

    runtime.start("engine.main")
    assert runtime.snapshot()["engine.main"]["state"] == "ACTIVE"

    try:
        runtime.start("engine.main")
        raise AssertionError("duplicate start accepted")
    except RuntimeError:
        pass

    try:
        runtime.unregister("engine.main")
        raise AssertionError("active engine unregistered")
    except RuntimeError:
        pass

    runtime.stop("engine.main")
    assert runtime.snapshot()["engine.main"]["state"] == "STOPPED"

    try:
        runtime.stop("engine.main")
        raise AssertionError("inactive engine stopped")
    except RuntimeError:
        pass

    runtime.start("engine.main")
    assert runtime.snapshot()["engine.main"]["state"] == "ACTIVE"
    runtime.stop("engine.main")
    runtime.unregister("engine.main")
    assert "engine.main" not in runtime.snapshot()

    try:
        runtime.start("missing.engine")
        raise AssertionError("unknown engine accepted")
    except KeyError:
        pass

    print("Node Core Engine Runtime contract tests: PASS")

if __name__ == "__main__":
    main()
