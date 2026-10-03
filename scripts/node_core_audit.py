#!/usr/bin/env python3
"""Deterministic structural audit for Chain Poker Genesis Node Core.

This audit intentionally stays within Node Core boundaries. It verifies:
- canonical Node Core files/directories exist;
- no Node Core source remains under Main Temporal;
- required JSON manifests/schemas are valid JSON;
- Node Core Python sources are syntactically compilable;
- the Node Core root contains its canonical manifest and README.

It does not modify repository state.
"""

from __future__ import annotations

import json
import py_compile
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NODE_CORE = ROOT / "Node Core"
MAIN_TEMPORAL = ROOT / "Main Temporal"

REQUIRED = [
    NODE_CORE / "README.md",
    NODE_CORE / "NODE-CORE-MANIFEST.json",
    NODE_CORE / "Bootstrap/Installer/bootstrap_node.py",
    NODE_CORE / "Runtime/node_runtime.py",
    NODE_CORE / "Runtime/State/runtime_state.py",
    NODE_CORE / "Runtime/Readiness/health_readiness.py",
    NODE_CORE / "Recovery/recovery_manager.py",
    NODE_CORE / "Network/Synchronization/synchronization_state.py",
    NODE_CORE / "Protocol Interface/Protocol Installation/protocol_installation_boundary.py",
    NODE_CORE / "Storage/storage_locator.py",
    NODE_CORE / "Storage/Storage Manager/storage_manager.py",
    NODE_CORE / "Storage/Providers/storage_provider.py",
    NODE_CORE / "Storage/Object Registry/object_registry.py",
    NODE_CORE / "Tools/Validation/final_node_core_audit.py",
]

def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)

def main() -> int:
    if not NODE_CORE.is_dir():
        fail("Node Core directory is missing")

    missing = [str(p.relative_to(ROOT)) for p in REQUIRED if not p.is_file()]
    if missing:
        fail("Missing required Node Core artifacts:\n  " + "\n  ".join(missing))

    if MAIN_TEMPORAL.is_dir():
        forbidden_prefixes = (
            "docs/node/",
            "reference-implementation/node-installation/",
            "engines/cryptographic-core-engine/",
            "engines/cryptographic-connection-engine/",
            "deterministic-manifest-based-node-and-protocol-storage-architecture/",
            "docs/developer-specifications/node-infrastructure/",
            "docs/developer-specifications/storage/",
        )
        leftovers = []
        for p in MAIN_TEMPORAL.rglob("*"):
            if p.is_file():
                rel = p.relative_to(MAIN_TEMPORAL).as_posix()
                if rel.startswith(forbidden_prefixes):
                    leftovers.append(rel)
        if leftovers:
            fail("Node Core artifacts remain under Main Temporal:\n  " + "\n  ".join(leftovers))

    json_files = sorted(NODE_CORE.rglob("*.json"))
    for path in json_files:
        try:
            with path.open("r", encoding="utf-8") as fh:
                json.load(fh)
        except Exception as exc:
            fail(f"Invalid JSON: {path.relative_to(ROOT)} ({exc})")

    python_files = sorted(NODE_CORE.rglob("*.py"))
    for path in python_files:
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            fail(f"Python syntax failure: {path.relative_to(ROOT)} ({exc})")

    print(f"[PASS] Node Core structural audit: {len(REQUIRED)} required artifacts verified")
    print(f"[PASS] JSON validation: {len(json_files)} files")
    print(f"[PASS] Python compilation: {len(python_files)} files")
    print("[PASS] Main Temporal contains no audited Node Core source families")
    return 0

if __name__ == "__main__":
    sys.exit(main())
