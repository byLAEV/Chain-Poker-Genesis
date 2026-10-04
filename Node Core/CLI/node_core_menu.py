#!/usr/bin/env python3
"""Node Core operator entry point.

Creates the protocol-neutral NodeCore composition and exposes the canonical
operator menu through the existing NodeCLI implementation.
"""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import sys


CLI_ROOT = Path(__file__).resolve().parent
NODE_CORE_ROOT = CLI_ROOT.parent
DEFAULT_INSTALL_ROOT = Path.home() / ".chain-poker-genesis" / "node-core"


def _load_node_core():
    path = NODE_CORE_ROOT / "node_core.py"
    spec = importlib.util.spec_from_file_location("node_core_entrypoint", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load Node Core composition.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.NodeCore


def resolve_node_root() -> Path:
    configured = os.environ.get("NODE_CORE_ROOT")
    return Path(configured).expanduser().resolve() if configured else DEFAULT_INSTALL_ROOT


def main(argv: list[str] | None = None) -> int:
    from node_cli import main as cli_main

    node_root = resolve_node_root()
    if not node_root.is_dir():
        print(f"Node Core installation not found: {node_root}", file=sys.stderr)
        print(
            "Set NODE_CORE_ROOT to the installed Node Core directory or install Node Core first.",
            file=sys.stderr,
        )
        return 1

    NodeCore = _load_node_core()
    node = NodeCore(node_root)
    return cli_main(argv or ["menu"], node=node)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
