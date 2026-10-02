#!/usr/bin/env python3
"""Tests for minimum FN-025 capability discovery."""

from capability_discovery import BASE_CAPABILITIES, CapabilityDiscovery

def test_base_capability_discovery_is_deterministic() -> None:
    discovery = CapabilityDiscovery("NODE-001", "INSTANCE-001")
    a = discovery.discover_base().snapshot()
    b = discovery.describe(reversed(sorted(BASE_CAPABILITIES))).snapshot()
    assert a == b
    assert a["capabilities"] == sorted(BASE_CAPABILITIES)

def test_capability_evidence_is_node_bound() -> None:
    evidence = CapabilityDiscovery("NODE-001", "INSTANCE-001").discover_base()
    assert evidence.node_id == "NODE-001"
    assert evidence.node_instance_id == "INSTANCE-001"
    assert evidence.schema_version == "1"

def test_invalid_capability_is_rejected() -> None:
    discovery = CapabilityDiscovery("NODE-001", "INSTANCE-001")
    try:
        discovery.describe(["CPG_PLAYER"])
    except ValueError:
        return
    raise AssertionError("non-canonical capability identifier was accepted")

def test_capability_does_not_create_protocol_association() -> None:
    evidence = CapabilityDiscovery("NODE-001", "INSTANCE-001").discover_base()
    assert "chain-poker-genesis" not in evidence.capabilities
    assert "cpg.player" not in evidence.capabilities

if __name__ == '__main__':
    test_base_capability_discovery_is_deterministic()
    test_capability_evidence_is_node_bound()
    test_invalid_capability_is_rejected()
    test_capability_does_not_create_protocol_association()
    print("FN-025 capability discovery: PASS")