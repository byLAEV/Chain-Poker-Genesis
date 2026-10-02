#!/usr/bin/env python3
"""Guard the boundary between Node Core and future CPG installation."""

from __future__ import annotations

import json
import sys
from pathlib import Path

def main() -> int:
    if len(sys.argv) != 2:
        print("status = FAILED")
        print("reason = usage: protocol_installation_boundary.py <node-directory>")
        return 2

    root = Path(sys.argv[1]).resolve()
    manifest_path = root / "node-installation-manifest.json"
    if not manifest_path.is_file():
        print("status = FAILED")
        print("reason = installation manifest missing")
        return 1

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print("status = FAILED")
        print(f"reason = invalid installation manifest: {exc}")
        return 1

    if manifest.get("node", {}).get("status") != "READY":
        return fail("node core is not READY")
    if manifest.get("readiness", {}).get("state") != "NODE_CORE_READY":
        return fail("node core readiness gate failed")
    if manifest.get("protocol_associations") != []:
        return fail("protocol associations are not empty")
    if manifest.get("cpg_protocol", {}).get("status") != "NOT_INSTALLED":
        return fail("CPG is not isolated")
    if manifest.get("synchronization", {}).get("state") != "NOT_EVALUATED":
        return fail("synchronization state crossed the Node Core boundary")

    print("status = VERIFIED")
    print("boundary_state = ARMED")
    print("protocol_associations = []")
    print("cpg_protocol = NOT_INSTALLED")
    print("synchronization = NOT_EVALUATED")
    return 0

def fail(reason: str) -> int:
    print("status = FAILED")
    print(f"reason = {reason}")
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
