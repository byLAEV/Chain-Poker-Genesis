#!/usr/bin/env python3
"""Minimal CPG deterministic execution-vector verifier.

This reference implementation is intentionally limited to the execution
vertical slice. It is not the Chain Poker Genesis production node.
"""

import hashlib
import json
import sys
from pathlib import Path


def canonical_json(value):
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256_prefixed(value):
    digest = hashlib.sha256(canonical_json(value)).hexdigest()
    return "sha256:" + digest


def verify_vector(path):
    vector = json.loads(Path(path).read_text(encoding="utf-8"))

    manifest = vector["manifest"]
    execution = vector["execution"]
    expected_result = vector["expected_result"]
    expected_state = vector["expected_state"]

    required_manifest = [
        "manifest_id",
        "version",
        "function_id",
        "function_version",
        "inputs",
        "required_state",
        "verification_rules",
    ]
    required_execution = [
        "execution_id",
        "manifest_id",
        "manifest_version",
        "function_id",
        "function_version",
        "input_reference",
        "state_reference",
        "result_reference",
        "result_hash",
        "evidence_reference",
        "execution_status",
    ]

    missing_manifest = [k for k in required_manifest if k not in manifest]
    missing_execution = [k for k in required_execution if k not in execution]

    if missing_manifest or missing_execution:
        raise ValueError(
            f"missing manifest fields={missing_manifest}; "
            f"missing execution fields={missing_execution}"
        )

    if execution["manifest_id"] != manifest["manifest_id"]:
        raise ValueError("manifest_id mismatch")

    if execution["manifest_version"] != manifest["version"]:
        raise ValueError("manifest_version mismatch")

    if execution["function_id"] != manifest["function_id"]:
        raise ValueError("function_id mismatch")

    if execution["function_version"] != manifest["function_version"]:
        raise ValueError("function_version mismatch")

    computed_hash = sha256_prefixed(expected_result)

    if computed_hash != execution["result_hash"]:
        raise ValueError(
            f"result hash mismatch: expected {computed_hash}, "
            f"recorded {execution['result_hash']}"
        )

    if expected_state["counter"] != vector["initial_state"]["counter"] + 1:
        raise ValueError("deterministic state transition failed")

    if execution["execution_status"] != "VERIFIED":
        raise ValueError("execution is not marked VERIFIED")

    return {
        "vector_id": vector["vector_id"],
        "status": "VERIFIED",
        "result_hash": computed_hash,
        "result": expected_result,
        "state": expected_state,
    }


if __name__ == "__main__":
    vector_path = (
        Path(sys.argv[1])
        if len(sys.argv) > 1
        else Path(__file__).parents[1] / "protocol/test-vectors/CPG-EXEC-0001.json"
    )

    print(json.dumps(verify_vector(vector_path), indent=2, ensure_ascii=False))
