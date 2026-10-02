#!/usr/bin/env python3
from synchronization_state import validate_transition

def main():
    assert not validate_transition("THRESHOLD_REACHED", "SYNCHRONIZED", False, False)
    assert validate_transition("THRESHOLD_REACHED", "SYNCHRONIZED", True, True)
    assert validate_transition("PROPAGATING", "CONFLICT")
    print("status = VERIFIED")
    print("synchronization_state_machine = READY")

if __name__ == "__main__":
    main()
