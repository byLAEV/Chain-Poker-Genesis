#!/usr/bin/env python3
"""Verify the Node Core specification coverage artifact."""

from pathlib import Path

REQUIRED = [
    "Bootstrap", "Identity", "Configuration", "Storage Manager",
    "Storage Provider", "Storage Coherence", "Object Registry",
    "Storage Locator", "Synchronization State", "Runtime Lifecycle",
    "Health / Readiness", "Recovery", "Installation Manifest",
    "Manifest Schema", "Final Audit", "Completion Gate",
    "Release Artifact", "Protocol Boundary",
]

def main():
    path = Path(__file__).resolve().parents[2] / "docs/node/NODE-CORE-SPECIFICATION-COVERAGE-AUDIT.md"
    text = path.read_text(encoding="utf-8")
    missing = [item for item in REQUIRED if item not in text]
    if missing:
        raise AssertionError(f"coverage entries missing: {missing}")
    print("coverage_audit = PASS")
    print(f"coverage_entries = {len(REQUIRED)}")

if __name__ == "__main__":
    main()
