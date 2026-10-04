from pathlib import Path
import sys
BASE=Path(__file__).resolve().parents[1]/"Configuration";sys.path.insert(0,str(BASE))
from configuration_manager import validate_configuration,ConfigurationError

def base():
    return {"node_core_version":"1.0.0","decentralized_storage":{"status":"NOT_PROVISIONED"},"protocol_associations":[],"cpg_protocol":"NOT_INSTALLED"}

def test_dual_storage_ready_is_valid():
    c=base(); c["decentralized_storage"]["status"]="DUAL_STORAGE_READY"
    assert validate_configuration(c)["decentralized_storage"]["status"]=="DUAL_STORAGE_READY"

def test_unknown_storage_state_rejected():
    c=base(); c["decentralized_storage"]["status"]="DUAL_STORAGE"
    try: validate_configuration(c)
    except ConfigurationError: pass
    else: raise AssertionError("unknown storage state accepted")


def test_dual_storage_mode_requires_readiness(tmp_path):
    from configuration_manager import ConfigurationManager
    import json
    p=tmp_path/"node.json"; p.write_text(json.dumps(base()))
    manager=ConfigurationManager(p); manager.load()
    try:
        manager.set_storage_mode("DUAL_STORAGE", readiness={"dual_storage_ready":False})
    except ConfigurationError:
        pass
    else:
        raise AssertionError("Dual Storage enabled without readiness")
    result=manager.set_storage_mode("DUAL_STORAGE", readiness={"dual_storage_ready":True})
    assert result["decentralized_storage"]["mode"]=="DUAL_STORAGE"
