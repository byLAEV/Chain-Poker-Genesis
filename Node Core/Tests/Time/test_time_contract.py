#!/usr/bin/env python3
from pathlib import Path
import sys
BASE=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(BASE/"Time"))
from time_service import TimeService

def main():
    t=TimeService()

    assert t.validate_timestamp(0)
    try:
        t.validate_timestamp(-1)
        raise AssertionError("negative timestamp accepted")
    except ValueError:
        pass
    try:
        t.validate_timestamp("1")
        raise AssertionError("non-integer timestamp accepted")
    except ValueError:
        pass

    a=t.record(100)
    b=t.record(101)
    assert a.sequence == 0
    assert a.previous_hash is None
    assert b.sequence == 1
    assert b.previous_hash == a.record_hash
    assert b.record_hash != a.record_hash
    assert t.verify_record(a, None)
    assert t.verify_record(b, a.record_hash)
    assert not t.verify_record(b, "tampered")

    # Same canonical inputs produce the same digest.
    t2=TimeService()
    a2=t2.record(100)
    assert a2.record_hash == a.record_hash

    status=t.reference_status()
    assert status["consensus_authority"] is False
    assert status["trust"] == "LOCAL_OBSERVATION"

    assert t.logical_tick() == 2
    assert t.logical_tick() == 3

    print("Node Core Time contract tests: PASS")

if __name__=="__main__":
    main()
