# Open Specifications

This document tracks areas that require explicit specification before they can be treated as implementation-defined behavior.

Examples include:

- canonical serialization;
- cryptographic algorithm profiles;
- key hierarchy and lifecycle;
- exact engine interfaces;
- state-machine transition tables;
- P2P message schemas;
- synchronization rules;
- consensus thresholds and failure modes;
- conflict-resolution procedures;
- settlement failure handling;
- recovery procedures;
- update and version-selection mechanisms;
- interoperable test vectors.

## Rule

Unspecified behavior must not be invented by an implementation and then treated as protocol law.

Each item should eventually become one of:

- **SPECIFIED**
- **UNDER REVIEW**
- **DEFERRED**
- **IMPLEMENTATION-DEFINED**, when the protocol explicitly permits independent choice without affecting interoperability.

## Change control

Any transition from unspecified to specified behavior should be documented in the relevant formal specification.
