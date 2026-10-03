#!/usr/bin/env python3
"""Node Core CLI reference entry point."""
import argparse, json
from pathlib import Path
def build_parser():
    p=argparse.ArgumentParser(prog="node-core")
    sub=p.add_subparsers(dest="command",required=True)
    sub.add_parser("status")
    sub.add_parser("version")
    return p
def main(argv=None):
    args=build_parser().parse_args(argv)
    if args.command=="version": print("Node Core reference 1.0.0")
    elif args.command=="status": print(json.dumps({"service":"Node Core","status":"READY"}))
if __name__=="__main__": main()
