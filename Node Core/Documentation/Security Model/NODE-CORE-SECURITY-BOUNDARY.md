# Node Core Security Boundary

**Status:** Normative design baseline  
**Scope:** Protocol-neutral Node Core

## Security domains
1. Identity boundary
2. Credential boundary
3. Configuration boundary
4. Storage boundary
5. Runtime/process boundary
6. Engine boundary
7. Protocol boundary
8. Network boundary
9. Recovery boundary
10. Audit boundary

## Required controls
- least privilege;
- fail-closed validation;
- path traversal prevention;
- protocol isolation;
- sensitive-data non-disclosure;
- integrity verification;
- explicit trust configuration;
- recovery authorization;
- auditable state transitions.

## Credential rule
Node Core MUST NOT assume ownership of private keys merely because an identity exists. Private-key custody and signing authority require an explicit credential profile.

## Protocol isolation
Node Core MUST reject attempts to write protocol-reserved storage through Node Core storage APIs and MUST NOT activate CPG during bootstrap.

## Trust model
Trust anchors, signing authorities, revocation, rotation, and anti-rollback remain explicit configuration/specification domains; they are not silently inferred.

## Failure rule
Malformed configuration, invalid manifests, failed integrity checks, unauthorized state transitions, and protocol-boundary violations MUST fail closed.

## Security non-goals
This document does not select cryptographic algorithms. Algorithm selection belongs to the Formal Cryptographic Profile.
