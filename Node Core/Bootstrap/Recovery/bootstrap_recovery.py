#!/usr/bin/env python3
"""Public bootstrap recovery entry point."""
from __future__ import annotations
from pathlib import Path
import json
import sys

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))
from bootstrap_recovery_impl import recover

__all__ = ["recover"]

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: bootstrap_recovery.py <target-directory>")
    try:
        result = recover(Path(sys.argv[1]))
    except Exception as exc:
        print(json.dumps({
            "status": "FAILED",
            "error": {
                "type": "BOOTSTRAP_RECOVERY_ERROR",
                "message": str(exc),
            },
        }, sort_keys=True))
        raise SystemExit(1)
    print(json.dumps(result, sort_keys=True))
