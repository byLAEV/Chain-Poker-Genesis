#!/usr/bin/env python3
"""Integration gate for the Node Core monetary reference layer."""

from __future__ import annotations

import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
REFERENCES = BASE / "Monetary References"
sys.path.insert(0, str(REFERENCES))

from reference_registry import MonetaryReferenceRegistry


def main() -> int:
    registry = MonetaryReferenceRegistry()

    bitcoin = registry.get("bitcoin")
    ethereum = registry.get("ethereum")
    banking = registry.get("traditional-banking")

    assert bitcoin["reference_repository"] == "bitcoin/bitcoin"
    assert ethereum["reference_repository"] == "ethereum/go-ethereum"
    assert banking["reference_type"] == "provider_interface"

    assert registry.settlement_execution_enabled() is False
    assert registry.custody_enabled() is False

    for reference in registry.all():
        assert reference["reference_status"] == "REFERENCE_ONLY"
        assert reference["protocol_execution"] is False

    print("Node Core monetary reference registry: PASS")
    print("bitcoin_reference = AVAILABLE")
    print("ethereum_reference = AVAILABLE")
    print("traditional_banking_reference = AVAILABLE")
    print("settlement_execution = DISABLED")
    print("custody = DISABLED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
