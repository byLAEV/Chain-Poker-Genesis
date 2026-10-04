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
        storage = sub.add_parser("storage")
        storage_sub = storage.add_subparsers(dest="command", required=True)
        storage_sub.add_parser("status")
        mode = storage_sub.add_parser("mode")
        mode_sub = mode.add_subparsers(dest="mode_command", required=True)
        mode_sub.add_parser("get")
        set_mode = mode_sub.add_parser("set")
        set_mode.add_argument("value", choices=("LOCAL","DUAL_STORAGE"))
        args = parser.parse_args(argv)
        try:
            if args.group == "storage":
                config = self.node.configuration
                if args.command == "status":
                    result = config.get()["decentralized_storage"]
                elif args.mode_command == "get":
                    result = {"mode": config.get()["decentralized_storage"].get("mode","LOCAL"), "status": config.get()["decentralized_storage"]["status"]}
                elif args.mode_command == "set":
                    readiness = self.node.storage_coherence.verify_all() if args.value == "DUAL_STORAGE" else {"dual_storage_ready": False}
                    result = {"decentralized_storage": config.set_storage_mode(args.value, readiness=readiness)}["decentralized_storage"]
                else:
                    raise RuntimeError("unsupported storage command")
            elif args.group == "node":
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
            print(json.dumps(result, sort_keys=True, separators=(",", ":"), ensure_ascii=False))
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
