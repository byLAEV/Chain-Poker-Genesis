# Versioning — Rake Engine

## Current specification

**Version:** 1.0

The source document defines the following economic defaults:

- 3% rake;
- 11% Foundation allocation;
- 89% AkaMoto Rie L allocation.

## Versioning rule

Any change to a parameter that can alter the amount, destination or timing of settlement must be treated as a protocol-impacting change.

Examples:

- rake percentage;
- rake eligibility;
- Foundation percentage;
- external-provider percentage;
- destination-wallet rules;
- rounding;
- fee treatment;
- settlement timing;
- confirmation policy.

## Historical preservation

Previous configurations must remain auditable. A new configuration must not rewrite historical rake records.

## Activation

A production implementation should define an explicit activation point for every new configuration, including:

- protocol version;
- effective block/time or governance event;
- configuration hash;
- authorized destinations;
- compatibility behavior for in-flight hands.

The exact activation mechanism is not defined by source document 5.0 and remains an implementation specification gap.
