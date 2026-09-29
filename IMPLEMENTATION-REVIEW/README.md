# Chain Poker Genesis — Implementation Review

## Purpose

This directory is the formal entry point for independent technical review of the Chain Poker Genesis (CPG) protocol by LAEV.

The objective is to allow experienced protocol engineers, cryptographers, distributed-systems researchers, Bitcoin/Lightning engineers, poker-engine specialists, and security reviewers to evaluate the specification before or during reference implementation.

This directory does not delegate protocol authority to reviewers. Reviews are technical inputs; protocol decisions remain part of the project's documented governance and specification process.

## Review principle

Reviewers are invited to identify:

- inconsistencies;
- missing normative specifications;
- ambiguous requirements;
- security assumptions;
- interoperability risks;
- deterministic-execution risks;
- implementation dependencies;
- testability gaps;
- recovery and failure-mode gaps.

Reviewers should not invent unspecified protocol behavior. Where the specification is incomplete, the correct result is to identify the missing specification.

## Repository

[Chain Poker Genesis by LAEV](https://github.com/byLAEV/Chain-Poker-Genesis)

## Documents

- [Implementation Review Invitation](INVITATION.md)
- [Review Questions](REVIEW-QUESTIONS.md)
- [Reviewer Matrix](REVIEWER-MATRIX.md)
- [Implementation Readiness](CPG-PROTOCOL-IMPLEMENTATION-READINESS.md)
- [Review Process](REVIEW-PROCESS.md)
- [Open Specifications](OPEN-SPECIFICATIONS.md)

## Review areas

1. Deterministic protocol execution
2. Poker and betting state machines
3. Cryptography and key management
4. Dealer / Mental Poker / private-card security
5. CID and cryptographic event-log architecture
6. Ledger and replay
7. P2P communication and synchronization
8. Consensus and conflict resolution
9. Bitcoin / Lightning settlement
10. Security and adversarial analysis
11. Testing and formal verification
12. Reference implementation architecture

## Status

This directory is an implementation-review framework. Individual specifications remain authoritative only where explicitly defined by the protocol documentation.
