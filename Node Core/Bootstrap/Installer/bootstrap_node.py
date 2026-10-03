#!/usr/bin/env python3
"""Fixed Node Core Bootstrap installer."""
from __future__ import annotations
import sys
from pathlib import Path

BASE=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(BASE/"Initialization"))
sys.path.insert(0,str(BASE/"Verification"))
from node_initializer import initialize
from bootstrap_verifier import verify

def install(target):
    target=Path(target).resolve()
    result=initialize(target)
    verification=verify(target)
    return {"installation":result,"verification":verification}

if __name__=="__main__":
    if len(sys.argv)!=2:
        raise SystemExit("usage: bootstrap_node.py <target-directory>")
    result=install(sys.argv[1])
    print("status = BOOTSTRAPPED")
    print("node_status = "+result["verification"]["state"])
