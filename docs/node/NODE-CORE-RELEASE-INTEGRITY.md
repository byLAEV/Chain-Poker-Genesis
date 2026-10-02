# Node Core Release Integrity

**Project:** Chain Poker Genesis by LAEV  
**Component:** Node Core

## Purpose

Release integrity binds a Node Core release declaration to deterministic SHA-256 file digests.

The release manifest is provenance metadata. It does not install or activate Chain Poker Genesis.

## Required Properties

A valid release integrity manifest MUST contain:

- release manifest version;
- Node Core version;
- ordered artifact entries;
- SHA-256 digest for every artifact entry;
- protocol boundary state;
- CPG status as NOT_INSTALLED.

The ordered artifact list is part of the canonical release definition.

## Acceptance

Release integrity is valid only when every declared artifact exists and its SHA-256 digest matches the recorded value.
