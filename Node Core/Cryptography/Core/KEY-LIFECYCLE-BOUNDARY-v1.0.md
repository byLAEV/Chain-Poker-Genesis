# Node Core Cryptographic Key Lifecycle Boundary

**Status:** Normative boundary v1.0

## 1. Principle
Cryptography Core performs cryptographic computation. It does not become the long-term custodian of private keys merely because it consumes a key reference.

## 2. Custody
Private keys MAY be controlled by an approved hardware signer, approved secure software custody layer, or ephemeral in-memory operation. Private keys MUST NOT be stored in manifests, ordinary logs, test fixtures, or persistent protocol state.

## 3. Responsibilities
Custody owns generation, import, persistent storage, backup/recovery, rotation, revocation, and destruction. Cryptography Core owns parameter validation, cryptographic execution, verification, and operation-result semantics.

## 4. Interface
Core operations SHOULD consume opaque key references or provider interfaces. Core MUST NOT require extraction of private keys from hardware custody.

## 5. Exposure
Private material MUST NOT appear in logs, manifests, errors, telemetry, or test reports. Temporary secret material MUST have the shortest practical lifetime.

## 6. Recovery
Cryptography Core MUST NOT define private-key recovery. Recovery belongs to the custody authority.

**Closure criterion:** custody boundary accepted, provider interface defined, and tests prove no private-key leakage.

## Current verification gap
The boundary is contractually closed but is not yet implementation-verified. The repository must provide an explicit custody/provider interface and automated evidence that private material is absent from manifests, ordinary logs, errors, telemetry, and test reports. Until those artifacts and tests pass CI, this boundary remains IMPLEMENTED / PARTIAL.


## Minimal custody/provider interface
The Node Core custody boundary is reference-based. Cryptography Core MUST NOT require a private-key byte value from a custody provider. The minimum provider surface is:
- `sign_ed25519(message: bytes, key_ref: str) -> bytes`
- `public_key(key_ref: str) -> bytes`

The provider owns private-key material and returns only the operation result or public material explicitly requested by the contract. The existing direct `sign(message, private_key)` primitive remains an internal/low-level primitive until the provider integration is separately reconciled and verified.


## Leakage audit finding
The identity credential verification boundary was found to propagate raw exception text through `VerificationResult.reason`. This was reconciled to the stable value `verification_failed`; the raw exception is no longer part of the result surface. A regression test now verifies sanitized failure output.
