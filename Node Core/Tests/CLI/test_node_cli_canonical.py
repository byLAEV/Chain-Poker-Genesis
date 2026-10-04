#!/usr/bin/env python3
import io
import json
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"CLI"))
from node_cli import NodeCLI

class Manager:
    def __init__(self):
        self.calls=[]
    def snapshot(self):
        self.calls.append("status"); return {"state":"READY"}
    def readiness(self):
        self.calls.append("readiness"); return True
    def start(self):
        self.calls.append("start"); return type("S",(),{"state":"RUNNING"})()
    def stop(self):
        self.calls.append("stop"); return type("S",(),{"state":"STOPPED"})()
    def recover(self):
        self.calls.append("recover"); return type("S",(),{"state":"READY"})()

class Node:
    def __init__(self):
        self.manager=Manager()
    def snapshot(self):
        return self.manager.snapshot()

def run(node,args):
    out=io.StringIO()
    with redirect_stdout(out):
        code=NodeCLI(node).run(args)
    return code,out.getvalue()

def main():
    node=Node()
    code,out=run(node,["node","status"])
    assert code==0 and json.loads(out)=={"state":"READY"}
    assert node.manager.calls==["status"]
    code,out=run(node,["node","readiness"])
    assert code==0 and json.loads(out)=={"ready":True}
    assert node.manager.calls[-1]=="readiness"
    print("Node Core CLI tests: PASS")

if __name__=="__main__": main()
