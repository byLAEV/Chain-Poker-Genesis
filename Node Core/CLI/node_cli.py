"""Protocol-neutral Node Core CLI reference implementation."""
from __future__ import annotations
import argparse
import json
import sys

class NodeCLI:
    def __init__(self, node):
        self.node = node

    def run(self, argv: list[str]) -> int:
        parser = argparse.ArgumentParser(prog="node-core")
        sub = parser.add_subparsers(dest="group", required=True)
        node = sub.add_parser("node")
        node_sub = node.add_subparsers(dest="command", required=True)
        for name in ("status","readiness","start","stop","recover"):
            node_sub.add_parser(name)
        args = parser.parse_args(argv)
        try:
            if args.group == "node":
                if args.command == "status":
                    result = self.node.snapshot()
                elif args.command == "readiness":
                    result = {"ready": self.node.manager.readiness()}
                elif args.command == "start":
                    result = {"state": self.node.manager.start().state}
                elif args.command == "stop":
                    result = {"state": self.node.manager.stop().state}
                elif args.command == "recover":
                    result = {"state": self.node.manager.recover().state}
                else:
                    raise RuntimeError("unsupported command")
            print(json.dumps(result, sort_keys=True, separators=(",", ":")))
            return 0
        except (RuntimeError, ValueError, KeyError) as exc:
            print(json.dumps({"error": str(exc)}, sort_keys=True, separators=(",", ":")), file=sys.stderr)
            return 1

def main(argv=None, node=None) -> int:
    if node is None:
        raise RuntimeError("Node Core instance is required")
    return NodeCLI(node).run(list(argv or []))

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
