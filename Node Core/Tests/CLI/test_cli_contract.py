#!/usr/bin/env python3
from pathlib import Path
import sys
BASE=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(BASE/"CLI"))
from node_cli import NodeCLI

class Manager:
    def __init__(self): self.state="READY"
    def readiness(self): return self.state in {"READY","RUNNING"}
    def start(self):
        if self.state!="READY": raise RuntimeError("node must be ready")
        self.state="RUNNING"; return type("S",(),{"state":self.state})()
    def stop(self):
        if self.state!="RUNNING": raise RuntimeError("node is not running")
        self.state="STOPPED"; return type("S",(),{"state":self.state})()
    def recover(self):
        if self.state not in {"DEGRADED","RECOVERY"}: raise RuntimeError("node is not in recovery condition")
        self.state="READY"; return type("S",(),{"state":self.state})()

class Node:
    def __init__(self): self.manager=Manager()
    def snapshot(self): return {"node":{"state":self.manager.state}}

def main():
    cli=NodeCLI(Node())
    assert cli.run(["node","status"]) == 0
    assert cli.run(["node","readiness"]) == 0
    assert cli.run(["node","start"]) == 0
    assert cli.run(["node","stop"]) == 0
    assert cli.run(["node","recover"]) != 0

    # Invalid state/command failures use a deterministic non-zero exit.
    assert cli.run(["node","start"]) != 0
    print("Node Core CLI contract tests: PASS")

if __name__=="__main__":
    main()
