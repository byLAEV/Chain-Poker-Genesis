# Zero-Knowledge Reference Test Matrix v0.1

## External reference

Repository:

`candrea-rares/Decentralized-Zero-Knowledge-Poker`

Pinned commit:

`c6ca40add20945615eb1442c9ef41cf2c03e82d5`

## Matrix

| Test ID | Category | Expected Node Core behavior | Status |
|---|---|---|---|
| ZK-ENV-001 | missing proof field | reject as MALFORMED_REQUEST | vector pending |
| ZK-ENV-002 | unsupported proof system | reject as UNSUPPORTED_PROOF_SYSTEM | vector pending |
| ZK-VK-001 | unknown verification key | reject as UNKNOWN_VERIFICATION_KEY | vector pending |
| ZK-VK-002 | altered verification key | reject verification | vector pending |
| ZK-IN-001 | valid public inputs | accept input envelope | vector pending |
| ZK-IN-002 | altered public inputs | reject as PUBLIC_INPUT_INVALID | vector pending |
| ZK-PR-001 | valid proof | VERIFIED | vector pending |
| ZK-PR-002 | invalid proof | INVALID_PROOF | vector pending |
| ZK-PR-003 | wrong statement | reject verification | vector pending |
| ZK-REQ-001 | valid request binding | verify | vector pending |
| ZK-REQ-002 | replayed request | REPLAY_DETECTED | vector pending |
| ZK-REQ-003 | expired request | EXPIRED_REQUEST | vector pending |
| ZK-CTX-001 | context mismatch | CONTEXT_MISMATCH | vector pending |

## Reference-circuit mapping

The external repository contains poker-specific circuits for:

- public key handling;
- 52-card deck encryption;
- shuffle and re-encryption;
- partial decryption;
- final reveal.

Those circuits remain outside Node Core.

The test suite for Node Core validates the generic proof verification boundary that can later consume proofs produced by a protocol-specific circuit.
