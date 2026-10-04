# Node Core Production Cryptographic Security Requirements

**Status:** Normative security requirements v1.0

## 1. Production evidence
Production security status requires versioned accepted profiles, passing canonical/SHA-256/Ed25519 vectors, passing CSPRNG failure vectors, passing AEAD and Merkle vectors after implementation, no secret leakage, negative-path tests, reviewed dependencies/providers, independent review of security-sensitive changes, reproducible CI, and an explicit security review record.

## 2. Status claims
CI success alone MUST NOT be described as an independent security audit. IMPLEMENTED_VERIFIED is permitted only after implementation and conformance gates pass. PRODUCTION_SECURITY_REVIEWED requires explicit security-review evidence.

## 3. Algorithm policy
Approved algorithms MUST be identified by profile and version. Silent downgrade or implicit substitution is prohibited.

## 4. Secret handling
Private keys, seeds, raw secret nonces, plaintext secrets, and equivalent material MUST NOT be logged or committed.

## 5. Failure handling
Verification, authentication, malformed-input, and provider-failure paths MUST fail closed.

## 6. Review boundary
Security review covers implementation, profiles, vectors, providers, dependency versions, failure behavior, secret handling, and compatibility/versioning.

**Closure criterion:** required evidence exists, complete conformance CI passes, and an explicit security review record is approved.
