"""Protocol readiness evaluation for the protocol-neutral Node Core."""

from __future__ import annotations

MINIMUM_PROTOCOL_NODES = 5


def evaluate_protocol_readiness(connected_nodes: int) -> dict:
    if connected_nodes < 0:
        raise ValueError("connected_nodes cannot be negative")
    ready = connected_nodes >= MINIMUM_PROTOCOL_NODES
    return {
        "ready": ready,
        "status": "READY" if ready else "NOT_READY",
        "minimum_nodes_required": MINIMUM_PROTOCOL_NODES,
        "connected_nodes": connected_nodes,
    }


__all__ = ["MINIMUM_PROTOCOL_NODES", "evaluate_protocol_readiness"]
