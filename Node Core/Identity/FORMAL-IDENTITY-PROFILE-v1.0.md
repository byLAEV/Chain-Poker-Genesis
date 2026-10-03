# Node Core Formal Identity Profile

**Status:** Normative profile v1.0  
**Scope:** Node identity and activation boundary

## 1. Identity model
A Node Identity is a cryptographically verifiable identifier bound to a public verification key and its registration metadata.

Identity is distinct from:
- human account identity;
- protocol membership;
- wallet ownership;
- CPG player identity.

## 2. Identity lifecycle
`UNINITIALIZED → GENERATED_OR_IMPORTED → VALIDATED → REGISTERED → ACTIVE`

Failure or revocation must prevent ACTIVE state.

## 3. Credential boundary
Node Core may receive a public key or an authorized signing capability from an external credential provider.

Private keys remain outside Node Core unless a future explicit custody profile states otherwise.

## 4. Identity record
The canonical identity record contains:
- identity version;
- identity identifier;
- public-key algorithm;
- public key;
- creation timestamp;
- status;
- registration metadata;
- verification metadata.

Private key material MUST NOT be present.

## 5. Derivation
Identity identifiers MUST be deterministically derived from the canonical public identity material using the Node Core cryptographic profile.

No password-derived or hardware-wallet-specific identity derivation is assumed unless separately specified.

## 6. Validation
Validation MUST verify:
1. schema;
2. canonical serialization;
3. public-key format;
4. identifier derivation;
5. signature where applicable;
6. lifecycle status;
7. trust/registration state.

## 7. Activation
A node may become ACTIVE only after identity validation and Node Core readiness requirements pass.

Identity activation does not install or activate a protocol.

## 8. Recovery
Recovery MUST preserve identity continuity unless an explicit identity replacement procedure is authorized.

Identity replacement is a separate security event and must be auditable.

## 9. Revocation
A revoked identity MUST NOT be activated. Revocation state and authority require an explicit trust/registration mechanism.

## 10. CPG boundary
CPG protocol identity, player identity, table membership, and cryptographic player authorization are outside this Node Core identity profile.
