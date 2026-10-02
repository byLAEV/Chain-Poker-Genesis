# CPG Protocol — Implementation Readiness

## Purpose

This document bridges the existing Chain Poker Genesis specifications and a future reference implementation.

## Current implementation posture

CPG contains substantial architectural and engine-level specifications. The implementation phase should proceed without allowing developers to silently invent missing protocol rules.

## Readiness requirements

Before an integrated reference implementation is considered protocol-conformant, the project should establish:

1. canonical data structures;
2. canonical serialization;
3. formal state machines;
4. engine-to-engine interfaces;
5. cryptographic algorithm profiles;
6. deterministic test vectors;
7. P2P message schemas;
8. synchronization rules;
9. consensus and conflict-resolution rules;
10. settlement state definitions;
11. recovery and failure procedures;
12. security threat model;
13. cross-implementation tests.

## Definition of implementation readiness

An engine is implementation-ready when an independent engineering team can implement it from the published specification without private clarification of normative behavior.

The integrated protocol is implementation-ready when independent implementations can exchange valid protocol data and converge on identical deterministic results under the same defined conditions.

## Prohibition

Implementation convenience must not become an undocumented protocol rule.

If an implementation requires a decision that is not specified, the decision must be surfaced as a specification issue before it becomes normative behavior.
