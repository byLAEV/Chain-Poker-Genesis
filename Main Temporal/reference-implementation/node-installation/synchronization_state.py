#!/usr/bin/env python3
"""Protocol-neutral synchronization state helpers."""

SYNC_STATES = {
    "NOT_SYNCHRONIZED", "PROPAGATION_PENDING", "PROPAGATING",
    "THRESHOLD_NOT_REACHED", "THRESHOLD_REACHED", "SYNCHRONIZED",
    "SYNC_FAILED", "RETRY_WAIT", "CONFLICT", "QUARANTINED",
}

def validate_transition(current, proposed, provider_ready=False, threshold_reached=False):
    if current == proposed:
        return True
    if proposed not in SYNC_STATES:
        return False
    if proposed == "SYNCHRONIZED" and not (provider_ready and threshold_reached):
        return False
    if proposed in {"CONFLICT", "QUARANTINED"}:
        return True
    allowed = {
        "NOT_SYNCHRONIZED": {"PROPAGATION_PENDING", "SYNC_FAILED", "CONFLICT"},
        "PROPAGATION_PENDING": {"PROPAGATING", "SYNC_FAILED", "CONFLICT"},
        "PROPAGATING": {"THRESHOLD_NOT_REACHED", "THRESHOLD_REACHED", "SYNC_FAILED", "CONFLICT"},
        "THRESHOLD_NOT_REACHED": {"PROPAGATING", "RETRY_WAIT", "SYNC_FAILED", "CONFLICT"},
        "THRESHOLD_REACHED": {"SYNCHRONIZED", "CONFLICT"},
        "SYNCHRONIZED": {"CONFLICT"},
        "SYNC_FAILED": {"RETRY_WAIT", "PROPAGATION_PENDING", "CONFLICT"},
        "RETRY_WAIT": {"PROPAGATION_PENDING", "SYNC_FAILED", "CONFLICT"},
    }
    return proposed in allowed.get(current, set())
