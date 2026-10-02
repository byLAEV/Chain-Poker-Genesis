# 06 — Commitment and Reveal Card Dealing Engine — Historical Source

**Chain Poker Genesis by LAEV (peroqtdigo)**  
**Official Technical Specification v1.0**  
**Historical source:** 6.0 Commitment and Reveal Card Dealing Engine__.pdf

This file preserves the supplied historical specification as the source record for Engine 06.

## Purpose

The Commitment and Reveal Card Dealing Engine is described as the cryptographic component responsible for assigning private player cards through a Commit-Reveal scheme. The historical specification states that private cards remain hidden until protocol-authorized revelation.

## Historical functional requirements

- Secure distribution of private cards.
- Association of each hand with a signed cryptographic commitment.
- Private visualization by the legitimate player.
- Prevention of premature disclosure.
- Cryptographically verifiable evidence throughout the hand.
- Reveal only when authorized by protocol rules.
- Verification that revealed information matches the original commitment.
- Rejection of inconsistent reveals.

## Historical dependencies

The document references:

- Poker Rules Engine
- Requests and Permissions Engine
- Player wallets
- Viewer Engine

## Important reconstruction note

The historical document describes a commitment signature as the cryptographic link to the private cards. For an implementation-safe reconstruction, **authentication/signature and confidentiality/encryption must be treated as separate mechanisms**.

A digital signature can prove authorization or ownership of an action, but a signature alone does not encrypt or hide card data. The implementation specification therefore introduces an explicit encrypted-card payload plus a commitment over canonical card material and a secret nonce.

The original PDF remains the historical source record; the implementation-facing specification below makes this distinction explicit without changing the intended privacy model.

---

© 2026 Lerry Alexander Elizondo Villalobos (LAEV).  
Chain Poker Genesis by LAEV.
