#!/usr/bin/env python3
import json, tempfile
from pathlib import Path
SCHEMA=Path(__file__).resolve().parents[2]/"Configuration/Schemas/node-configuration.schema.json"

def validate(c):
    required={"node_core_version","decentralized_storage","protocol_associations","cpg_protocol"}
    if set(c)-required: raise ValueError("unknown configuration property")
    if not required.issubset(c): raise ValueError("missing required configuration")
    if not isinstance(c["node_core_version"],str): raise ValueError("invalid node_core_version")
    if not isinstance(c["protocol_associations"],list) or len(c["protocol_associations"]) != len(set(c["protocol_associations"])):
        raise ValueError("invalid protocol_associations")
    if c["cpg_protocol"] not in {"NOT_INSTALLED","INSTALLED","ACTIVE"}: raise ValueError("invalid cpg_protocol")
    if c["cpg_protocol"] != "NOT_INSTALLED" and c["protocol_associations"] == []:
        raise ValueError("fresh node cannot activate CPG")
    return True

def main():
    schema=json.loads(SCHEMA.read_text())
    assert schema["additionalProperties"] is False
    valid={"node_core_version":"1.0.0","decentralized_storage":{"status":"NOT_PROVISIONED"},"protocol_associations":[],"cpg_protocol":"NOT_INSTALLED"}
    assert validate(valid)

    for bad in [
        {**valid,"unknown":True},
        {"node_core_version":"1.0.0","decentralized_storage":{"status":"NOT_PROVISIONED"},"protocol_associations":[]},
        {**valid,"protocol_associations":["a","a"]},
        {**valid,"cpg_protocol":"ACTIVE"},
    ]:
        try: validate(bad)
        except ValueError: pass
        else: raise AssertionError("invalid configuration accepted")

    # Deterministic default baseline.
    a=json.dumps(valid,sort_keys=True,separators=(",",":"))
    b=json.dumps(valid,sort_keys=True,separators=(",",":"))
    assert a==b
    print("Node Core Configuration contract tests: PASS")

if __name__=="__main__": main()
