#!/usr/bin/env python3
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
BASE=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(BASE))
from Bootstrap.bootstrap import Bootstrap
from Runtime.runtime_manager import RuntimeManager

def main():
    with TemporaryDirectory() as d:
        root=Path(d)
        Bootstrap().bootstrap(root)
        identity=root/"node-storage/identity"
        identity.mkdir(parents=True)
        (identity/"node-identity.json").write_text("provisioned",encoding="utf-8")
        m=RuntimeManager(root)
        assert m.readiness().integrity_ready is True
        assert m.start()["state"]=="RUNNING"
        assert m.stop()["state"]=="STOPPED"

    with TemporaryDirectory() as d:
        root=Path(d)
        Bootstrap().bootstrap(root)
        identity=root/"node-storage/identity"
        identity.mkdir(parents=True)
        (identity/"node-identity.json").write_text("provisioned",encoding="utf-8")
        config=root/"node-storage/configuration/node-config.json"
        config.write_text(config.read_text(encoding="utf-8")+"corruption",encoding="utf-8")
        try:
            RuntimeManager(root).start()
        except ValueError:
            raise AssertionError("runtime advanced after failed bootstrap integrity")
        except RuntimeError:
            raise AssertionError("runtime identity check masked bootstrap integrity failure")
        else:
            raise AssertionError("runtime started with corrupted bootstrap artifacts")

    with TemporaryDirectory() as d:
        root=Path(d)
        Bootstrap().bootstrap(root)
        try:
            RuntimeManager(root).start()
        except RuntimeError:
            pass
        else:
            raise AssertionError("runtime started without node identity")

    print("Node Core Runtime implementation tests: PASS")

if __name__=="__main__":
    main()
