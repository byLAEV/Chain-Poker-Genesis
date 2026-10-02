#!/usr/bin/env python3
"""Tests for FN-024A protocol-neutral data networking / transport substrate."""

from identity_node_network import IdentityNode
from node_data_transport import NodeDataTransport, TransportState


def test_endpoint_is_not_identity() -> None:
    node = IdentityNode(
        node_id="NODE-001", public_identity_reference="PUB-001", node_instance_id="INSTANCE-001"
    )
    transport = NodeDataTransport(node.node_id)
    session = transport.open_session("NODE-002", "/ip4/203.0.113.20/tcp/4002")
    assert session.remote_node_id == "NODE-002"
    assert session.endpoint.value == "/ip4/203.0.113.20/tcp/4002"
    assert session.remote_node_id != session.endpoint.value


def test_connection_lifecycle_and_data_exchange() -> None:
    transport = NodeDataTransport("NODE-001")
    transport.open_session("NODE-002", "/ip4/127.0.0.1/tcp/4002")
    transport.set_state("NODE-002", TransportState.CONNECTING)
    try:
        transport.send("NODE-002", b"hello")
    except ConnectionError:
        pass
    else:
        raise AssertionError("data exchange occurred before connection")
    transport.set_state("NODE-002", TransportState.CONNECTED)
    message = transport.send("NODE-002", b"hello")
    assert message.source_node_id == "NODE-001"
    assert message.destination_node_id == "NODE-002"
    assert message.payload == b"hello"
    assert len(transport.receive_all()) == 1
    assert transport.receive_all() == ()


def test_degraded_connection_remains_data_capable() -> None:
    transport = NodeDataTransport("NODE-001")
    transport.open_session("NODE-002", "/ip4/127.0.0.1/tcp/4002")
    transport.set_state("NODE-002", TransportState.DEGRADED)
    transport.send("NODE-002", b"degraded")
    assert len(transport.receive_all()) == 1


def test_network_conditions_are_infrastructure_metadata() -> None:
    transport = NodeDataTransport("NODE-001")
    transport.open_session("NODE-002", "/ip4/127.0.0.1/tcp/4002")
    transport.set_network_conditions("NODE-002", latency_ms=12.5, capacity_bps=1_000_000)
    snapshot = transport.snapshot()
    session = snapshot["sessions"][0]
    assert session["latency_ms"] == 12.5
    assert session["capacity_bps"] == 1_000_000


def test_identity_cannot_be_its_own_transport_peer() -> None:
    transport = NodeDataTransport("NODE-001")
    try:
        transport.open_session("NODE-001", "/ip4/127.0.0.1/tcp/4001")
    except ValueError:
        return
    raise AssertionError("local identity was accepted as its own transport peer")


if __name__ == "__main__":
    test_endpoint_is_not_identity()
    test_connection_lifecycle_and_data_exchange()
    test_degraded_connection_remains_data_capable()
    test_network_conditions_are_infrastructure_metadata()
    test_identity_cannot_be_its_own_transport_peer()
    print("FN-024A node data networking / transport substrate: PASS")
