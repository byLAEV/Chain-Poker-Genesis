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

        negatives = [
            {"node_core_version":"1.0.0","decentralized_storage":{"status":"READY"},"protocol_associations":[]},
            {"node_core_version":"1.0.0","decentralized_storage":{"status":"INVALID"},"protocol_associations":[],"cpg_protocol":"NOT_INSTALLED"},
            {"node_core_version":"1.0.0","decentralized_storage":{"status":"READY"},"protocol_associations":["p","p"],"cpg_protocol":"NOT_INSTALLED"},
            {"node_core_version":"1.0.0","decentralized_storage":{"status":"READY"},"protocol_associations":[],"cpg_protocol":"ACTIVE"},
            {"node_core_version":"1.0.0","decentralized_storage":{"status":"READY","mode":"INVALID"},"protocol_associations":[],"cpg_protocol":"NOT_INSTALLED"},
        ]
        for invalid in negatives:
            try: manager.validate(invalid)
            except ConfigurationError: pass
            else: raise AssertionError("invalid configuration accepted")

        try: manager.set_storage_mode("INVALID")
        except ConfigurationError: pass
        else: raise AssertionError("invalid storage mode accepted")

        try: manager.set_storage_mode("DUAL_STORAGE", readiness={"dual_storage_ready": False})
        except ConfigurationError: pass
        else: raise AssertionError("Dual Storage enabled without coherence evidence")
    print("Node Core Configuration tests: PASS")

if __name__=="__main__": main()
