#!/usr/bin/env python3
"""Tests for the minimum FN-024 Identity Node networking substrate."""

from identity_node_network import IdentityNode, IdentityNodeNetwork, PeerState


def test_identity_node_is_protocol_neutral() -> None:
    node = IdentityNode(
        node_id="NODE-001",
        public_identity_reference="PUB-001",
        node_instance_id="INSTANCE-001",
    )
    assert node.protocol_association == "NONE"


def test_identity_node_rejects_cpg_association() -> None:
    try:
        IdentityNode(
            node_id="NODE-001",
            public_identity_reference="PUB-001",
            node_instance_id="INSTANCE-001",
            protocol_association="chain-poker-genesis",
        )
    except ValueError:
        return
    raise AssertionError("base Identity Node accepted a protocol association")


def test_peer_lifecycle_and_deterministic_snapshot() -> None:
    local = IdentityNode(
        node_id="NODE-001",
        public_identity_reference="PUB-001",
        node_instance_id="INSTANCE-001",
    )
    network = IdentityNodeNetwork(local)
    network.register_peer("NODE-003", "/ip4/127.0.0.1/tcp/4003")
    network.register_peer("NODE-002", "/ip4/127.0.0.1/tcp/4002")
    network.set_peer_state("NODE-002", PeerState.CONNECTED)
    network.set_peer_state("NODE-003", PeerState.DEGRADED)

    snapshot = network.snapshot()
    assert snapshot["local_identity"]["node_id"] == "NODE-001"
    assert snapshot["peer_count"] == 2
    assert [peer["peer_node_id"] for peer in snapshot["peers"]] == ["NODE-002", "NODE-003"]
    assert snapshot["peers"][0]["state"] == "CONNECTED"
    assert snapshot["peers"][1]["state"] == "DEGRADED"


def test_local_identity_cannot_be_its_own_peer() -> None:
    local = IdentityNode(
        node_id="NODE-001",
        public_identity_reference="PUB-001",
        node_instance_id="INSTANCE-001",
    )
    network = IdentityNodeNetwork(local)
    try:
        network.register_peer("NODE-001", "/ip4/127.0.0.1/tcp/4001")
    except ValueError:
        return
    raise AssertionError("local identity was registered as its own peer")


if __name__ == "__main__":
    test_identity_node_is_protocol_neutral()
    test_identity_node_rejects_cpg_association()
    test_peer_lifecycle_and_deterministic_snapshot()
    test_local_identity_cannot_be_its_own_peer()
    print("FN-024 identity-node networking substrate: PASS")
