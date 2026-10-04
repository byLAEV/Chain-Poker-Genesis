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
