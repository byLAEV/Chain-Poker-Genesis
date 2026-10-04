#!/usr/bin/env python3
import tempfile, json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"Configuration"))
from configuration_manager import ConfigurationManager, ConfigurationError

VALID={
"node_core_version":"1.0.0",
"decentralized_storage":{"status":"READY"},
"protocol_associations":[],
"cpg_protocol":"NOT_INSTALLED"
}

def main():
    with tempfile.TemporaryDirectory() as d:
        path=Path(d)/"node-config.json"
        path.write_text(json.dumps(VALID))
        manager=ConfigurationManager(path)
        assert manager.load()["cpg_protocol"]=="NOT_INSTALLED"
        updated=manager.update({"decentralized_storage":{"status":"NOT_PROVISIONED"}})
        assert updated["decentralized_storage"]["status"]=="NOT_PROVISIONED"
        try: manager.update({"cpg_protocol":"ACTIVE"})
        except ConfigurationError: pass
        else: raise AssertionError("configuration manager activated CPG")
        try: manager.update({"unknown":"value"})
        except ConfigurationError: pass
        else: raise AssertionError("unknown configuration property accepted")
    print("Node Core Configuration tests: PASS")

if __name__=="__main__": main()
