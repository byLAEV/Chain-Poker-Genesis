# Cryptographic Core Engine — Architectural Specification

Protocol: Chain Poker Genesis by LAEV
Version: 0.1.0
Status: Architectural foundation — non-normative pending cryptographic profile approval

## Purpose
The Cryptographic Core Engine is the protocol's shared cryptographic infrastructure layer. It provides primitive cryptographic operations required by Chain Poker Genesis while remaining separate from the Cryptographic Connection Engine.

The Cryptographic Connection Engine manages credential acquisition, identity establishment, and Player Node activation. The Cryptographic Core Engine provides the cryptographic primitives consumed by that and other engines.

## Boundary
### Owns
- cryptographic hash functions;
- hash-domain separation;
- digest and commitment generation;
- commitment verification;
- signatures and signature verification;
- authenticated encryption and decryption where required;
- key-generation primitives where appropriate;
- key derivation primitives;
- cryptographically secure randomness interfaces;
- Merkle tree construction, root calculation, proof generation and proof verification;
- cryptographic encoding/decoding boundaries;
- algorithm/version profile selection;
- cryptographic parameter validation;
- cryptographic test vectors.

### Does not own
- Player Node identity lifecycle;
- hardware-wallet user interaction;
- table creation;
- poker rules;
- card dealing;
- settlement;
- reputation;
- P2P transport;
- application UI.

## Relationship to Cryptographic Connection Engine
Player Node → Cryptographic Connection Engine → credential/identity boundary → Cryptographic Core Engine → cryptographic primitives.

The Connection Engine decides which identity operation is requested. The Core Engine defines and executes how the cryptographic operation is performed.

A hardware wallet remains a separate trust/custody boundary. The Core Engine must not require extraction of hardware private keys.

## Primitive families
### Hash
Interface concept: hash(input, profile) → digest.
The exact hash algorithms are NOT frozen by this document.

### Domain-separated hash
Interface concept: domainHash(domain, input, profile) → digest.
Domain separation prevents semantically different protocol objects from accidentally sharing the same hash construction.

### Commitment
Interface concept: commit(message, nonce, profile) → commitment; verifyCommitment(message, nonce, commitment, profile) → boolean.
This is required by Commitment & Reveal and must remain compatible with deterministic replay.

### Signature
Interface concept: sign(message, signingAuthority, profile) → signature; verifySignature(message, signature, publicKey, profile) → boolean.
The signing authority may be software-held or an external hardware wallet.

### Encryption
Interface concept: encrypt(plaintext, keyReference, associatedData, profile) → ciphertext; decrypt(ciphertext, keyReference, associatedData, profile) → plaintext.
Encryption must provide authenticated encryption when the selected profile requires confidentiality plus integrity.

### Key derivation
Interface concept: deriveKey(parentKeyReference, context, profile) → derivedKeyReference.
Exact derivation paths and algorithms remain OPEN until the Cryptographic Profile is accepted.

### Secure randomness
Interface concept: randomBytes(length, profile) → bytes.
Cryptographic operations must use a cryptographically secure randomness source appropriate to the execution environment.

## Merkle subsystem
The Core Engine must define one common Merkle abstraction so protocol engines do not implement incompatible Merkle trees independently.

Required operations:
- merkleLeaf(data, profile)
- merkleParent(left, right, profile)
- merkleRoot(leaves, profile)
- merkleProof(leaves, index, profile)
- verifyMerkleProof(leaf, proof, root, profile)

The formal profile must define leaf hashing, parent hashing, domain separation, left/right ordering, odd-node handling, empty-tree behavior, single-leaf behavior, proof encoding, root representation, and serialization of leaves before hashing.

Until those rules are frozen, merkle_root remains an opaque cryptographic commitment.

## Protocol consumers
- Cryptographic Connection Engine
- Private Off-Chain Ledger Engine
- Commitment & Reveal Card Dealing Engine
- Table Creation Engine
- Table Wallet / settlement infrastructure
- P2P conflict resolution
- state anchoring infrastructure
- reputation/evidence infrastructure

Each consumer must call the Core Engine rather than implementing its own incompatible primitive.

## Cryptographic profile
A separate profile must freeze approved hash algorithms, signature algorithms, authenticated-encryption algorithms, key-derivation algorithms, key sizes, nonce/IV requirements, randomness requirements, public-key encoding, signature encoding, digest encoding, Merkle construction, domain-separation labels, canonical byte serialization, algorithm identifiers, profile versioning, and deprecation/compatibility rules.

This document deliberately does not choose those algorithms.

## Canonicalization dependency
Cryptographic operations operate on bytes. Therefore the Core Engine depends on Canonical Serialization for any protocol object that is hashed, signed, committed, encrypted, or inserted into a Merkle tree.

Canonical Object → Canonical Serialization → Bytes → Cryptographic Core → Digest / Signature / Commitment / Merkle Root

No implementation may silently hash an implementation-specific JSON representation and call it a protocol hash.

## Security boundaries
Private cryptographic material must be classified by custody: hardware-controlled, software secure-storage controlled, ephemeral in-memory, or public verification material.

The Core Engine must expose references and operation results without unnecessarily exposing private material. Logging must never record private keys, seeds, seed phrases, raw secret nonces, or decrypted secret material.

## Determinism
Operations used for protocol evidence, replay, commitments, hash verification, and Merkle construction must have deterministic definitions wherever deterministic output is required. Randomness must be explicit and auditable when randomness is part of protocol state.

## What remains OPEN
- exact hash algorithm;
- signature scheme;
- authenticated-encryption profile;
- key-derivation profile;
- key/address format;
- BIP-32/BIP-39/BIP-44 derivation policy;
- Merkle tree variant;
- canonical serialization format;
- protocol domain-separation labels.

These belong to the Formal Cryptographic Profile and must be selected through explicit protocol decisions and test vectors.

## Required next specifications
1. Formal Cryptographic Profile
2. Canonical Serialization Specification
3. Merkle Tree Specification
4. Cryptographic Test Vector Suite

## Architectural conclusion
The Cryptographic Connection Engine remains responsible for identity connection and credential lifecycle.

The Cryptographic Core Engine becomes responsible for cryptographic computation and verification.

This separation prevents identity management, cryptographic primitives, poker logic, ledger logic, and settlement logic from becoming coupled inside one engine.