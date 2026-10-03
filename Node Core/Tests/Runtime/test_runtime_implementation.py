#!/usr/bin/env python3
from pathlib import Path
from tempfile import TemporaryDirectory
import json,sys
BASE=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(BASE))
from Runtime.runtime_manager import RuntimeManager
def main():
    with TemporaryDirectory() as d:
        root=Path(d); s=root/"node-storage"
        for p in ("configuration","state","recovery","identity"): (s/p).mkdir(parents=True)
        (s/"configuration/node-config.json").write_text(json.dumps({"node_core_version":"1.0.0","protocol_associations":[],"cpg_protocol":"NOT_INSTALLED"}))
        (s/"state/node-state.json").write_text("{}")
        (s/"identity/node-identity.json").write_text("{}")
        m=RuntimeManager(root)
        assert m.start()["state"]=="RUNNING"
        assert m.stop()["state"]=="STOPPED"
    with TemporaryDirectory() as d:
        root=Path(d); s=root/"node-storage"; (s/"configuration").mkdir(parents=True); (s/"state").mkdir(); (s/"recovery").mkdir()
        (s/"configuration/node-config.json").write_text(json.dumps({"node_core_version":"1.0.0","protocol_associations":[],"cpg_protocol":"NOT_INSTALLED"}))
        (s/"state/node-state.json").write_text("{}")
        try: RuntimeManager(root).start()
        except RuntimeError: pass
        else: raise AssertionError("runtime started without node identity")
    print("Node Core Runtime implementation tests: PASS")
if __name__=="__main__": main()
