#!/usr/bin/env python3
from pathlib import Path
import sys
BASE=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(BASE/"Security"))
from security_service import SecurityService

def main():
    s=SecurityService()
    assert not s.validate_path("../escape").allowed
    assert not s.validate_path("").allowed
    assert not s.validate_path(None).allowed
    assert not s.validate_path("/absolute").allowed
    assert not s.validate_path("\\\\absolute").allowed
    assert not s.validate_path("a/../../escape").allowed
    assert not s.validate_path("CPG/ledger").allowed
    assert not s.validate_path("Protocol/private").allowed
    assert s.validate_path("local/public/object").allowed

    try:
        s.require(False,"unauthorized")
        raise AssertionError("failed authorization accepted")
    except PermissionError:
        pass

    s.require(True,"authorized")

    # Protocol boundary cannot be bypassed by path normalization.
    assert not s.validate_path("foo/../Protocol/private").allowed
    print("Node Core Security contract tests: PASS")

if __name__=="__main__":
    main()
