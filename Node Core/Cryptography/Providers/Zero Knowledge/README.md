# Zero Knowledge Provider

**Status:** IMPLEMENTED

Node Core exposes a protocol-neutral zero-knowledge verification boundary.

The implemented adapter uses RISC Zero as an external proof-verification backend through an explicit process boundary. Node Core does not embed the Rust runtime or define a CPG-specific circuit.

Capabilities:
- proof verification;
- receipt verification.

A concrete verifier executable must be supplied by deployment. This prevents Node Core from silently selecting a circuit, guest program, proving system, or application-specific statement.

Upstream: RISC Zero — https://github.com/risc0/risc0
