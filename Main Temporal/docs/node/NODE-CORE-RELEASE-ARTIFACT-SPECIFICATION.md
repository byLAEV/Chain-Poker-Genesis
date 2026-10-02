# Node Core Release Artifact Specification

**Project:** Chain Poker Genesis by LAEV
**Component:** Node Core
**Status:** Formal Release Definition

## Purpose

A Node Core release artifact is a reproducible package of the protocol-neutral installation layer.

## Required Contents

A release MUST identify:

- source implementation;
- installation bootstrap;
- verification tools;
- lifecycle implementation;
- health/readiness implementation;
- recovery implementation;
- storage specifications and schemas;
- test vectors;
- CI validation workflow;
- canonical installation manifest format.

## Exclusions

A Node Core release artifact MUST NOT contain an installed or activated Chain Poker Genesis protocol.

The release baseline remains:

    CPG = NOT_INSTALLED
    protocol_associations = []
    protocol_activation = NONE

## Verification

The release is accepted only when the End-to-End Node Installation test succeeds and the canonical installation manifest passes its schema invariants.
