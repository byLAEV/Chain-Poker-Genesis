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
