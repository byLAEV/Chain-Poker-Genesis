# Cryptographic Architecture — Three-Layer Model

Protocol: Chain Poker Genesis by LAEV
Version: 0.2.0
Status: Architectural clarification

## 1. Principle
The cryptographic architecture is intentionally divided into three layers.

**Cryptographic Core** = primitive cryptographic capability.

**Cryptographic Engine** = protocol-level cryptographic operations and orchestration built on the Core.

**Cryptographic Connection Engine** = identity, credential and connection lifecycle that consumes the Cryptographic Engine.

The layers must not be collapsed into one engine.

## 2. Layer A — Cryptographic Core
The Core provides the lowest-level cryptographic primitives. It does not decide how Chain Poker Genesis uses those primitives.

Core responsibilities:
- primitive hash execution;
- primitive encryption/decryption execution;
- primitive signature operations and verification;
- primitive key derivation;
- secure randomness;
- primitive Merkle operations;
- low-level cryptographic encoding/decoding;
- constant-time/security-sensitive primitive implementations where applicable.

The Core does not own CPG identity, table identity, poker commitments, ledger policy, settlement policy, authentication workflows, or protocol semantics.

## 3. Layer B — Cryptographic Engine
The Cryptographic Engine is the protocol cryptography layer. It uses the Core to implement the cryptographic behavior required by Chain Poker Genesis.

Cryptographic Engine responsibilities:
- define and apply CPG cryptographic profiles;
- select approved algorithms for each protocol operation;
- apply domain separation;
- construct protocol-specific hashes;
- construct and verify protocol commitments;
- construct and verify CPG signatures;
- provide encryption/decryption services according to CPG security policy;
- manage cryptographic operation contexts;
- construct and verify CPG Merkle trees and Merkle roots;
- create and verify Merkle proofs;
- bind cryptographic operations to canonical serialization;
- enforce algorithm/version compatibility;
- expose safe cryptographic services to other CPG engines;
- provide cryptographic error classification;
- maintain deterministic cryptographic behavior required for replay and verification.

The Cryptographic Engine therefore answers: **how does Chain Poker Genesis use cryptography?**

The Core answers: **how is the underlying cryptographic primitive computed?**

## 4. Layer C — Cryptographic Connection Engine
The Cryptographic Connection Engine consumes the Cryptographic Engine for identity-related workflows.

Responsibilities:
- select credential/identity connection method;
- connect compatible hardware wallets;
- generate or import supported credentials;
- establish cryptographic identity;
- validate identity credentials;
- request signatures through the cryptographic service boundary;
- associate identity with the Player Node;
- activate the Player Node;
- manage credential lifecycle and connection state.

It must not independently implement CPG hash, Merkle, encryption, signature or commitment logic.

## 5. Dependency direction
Player Node / protocol engines
→ Cryptographic Connection Engine for identity workflows
→ Cryptographic Engine for protocol cryptography
→ Cryptographic Core for primitive computation

Other protocol engines may call the Cryptographic Engine directly when they require protocol cryptography.

They should not bypass the Cryptographic Engine merely to call primitives with their own parameters.

## 6. Example: Merkle Root
Ledger Engine requests a CPG Merkle root.

Ledger → Cryptographic Engine: createMerkleRoot(canonicalLeaves, profile)

Cryptographic Engine:
1. validates the selected CPG cryptographic profile;
2. obtains canonical bytes;
3. applies CPG domain separation;
4. defines leaf/parent construction according to the profile;
5. delegates primitive hashing to Cryptographic Core;
6. constructs the tree;
7. returns the Merkle root and required proof metadata.

The Core does not decide what a CPG ledger Merkle tree means.

## 7. Example: commitment
Commitment & Reveal Engine → Cryptographic Engine: createCommitment(message, nonce, context)

Cryptographic Engine determines the CPG commitment construction and domain context.

Cryptographic Core performs the underlying primitive operation.

## 8. Example: identity signature
Cryptographic Connection Engine → Cryptographic Engine: requestIdentitySignature(message, identityContext)

Cryptographic Engine validates the protocol context and signature profile.

The signing operation may then be delegated to:
- Cryptographic Core for software-controlled keys; or
- hardware wallet boundary for hardware-controlled keys.

The private key does not need to cross the hardware boundary.

## 9. What belongs where
| Concern | Core | Cryptographic Engine | Connection Engine |
|---|---|---|---|
| Primitive hash | YES | uses | no |
| CPG hash construction | no | YES | no |
| Primitive encryption | YES | uses | no |
| CPG encryption policy | no | YES | no |
| Primitive signature | YES | uses | requests |
| CPG signature profile | no | YES | identity workflow |
| Primitive Merkle operation | YES | uses | no |
| CPG Merkle tree | no | YES | no |
| Commitment primitive | YES if primitive required | CPG commitment | consumes |
| Identity lifecycle | no | no | YES |
| Hardware wallet connection | no | cryptographic service boundary | YES |
| Player Node activation | no | no | YES |
| Poker rules | no | no | no |
| Settlement | no | no | no |

## 10. Architectural consequence
The previous two-layer description is therefore corrected.

The intended architecture is:

Cryptographic Core
↓
Cryptographic Engine
↓
Cryptographic Connection Engine / other protocol engines

Support flows may exist in both directions at the interface level, but ownership must remain separated.

## 11. Required specifications
This clarification creates the following distinct specifications:

1. Cryptographic Core Specification
2. Cryptographic Engine Specification
3. Formal Cryptographic Profile
4. Merkle Tree Specification
5. Cryptographic Test Vector Suite
6. Cryptographic Connection Engine Specification

These should be reconciled before cryptographic Canonical Schemas become normative.