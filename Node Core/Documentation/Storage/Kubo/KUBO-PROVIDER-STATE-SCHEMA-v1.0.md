# Kubo Provider State Schema v1.0

**Status:** CANONICAL DESIGN

The Provider State record is Node Core management metadata. It does not replace Kubo's repository/configuration.

## Required state

- provider_id
- provider
- state_version
- installation_id
- lifecycle_state
- health_state
- synchronization_state
- kubo_version
- platform
- architecture
- release_source
- release_metadata_source
- expected_integrity
- observed_integrity
- executable_path
- repository_path
- ipfs_path
- installed_at
- last_transition_at
- last_health_check_at

## State rules

ipfs_path MUST equal the normalized absolute repository_path.

executable_path MUST resolve inside the selected immutable Kubo release directory.

kubo_version MUST agree with the executable's reported version.

lifecycle_state=READY requires:
- verified installation;
- initialized repository;
- valid configuration;
- healthy Kubo process;
- completed initial synchronization;
- successful coherence verification.

health_state and synchronization_state are separate dimensions.

A healthy Kubo process may still have synchronization state PENDING or FAILED.

## Persistence

State is stored under node-storage/providers/kubo/state/.

State updates are atomic and must preserve the last valid state if a write fails.

## Recovery

After Node Core restart, the Manager reconstructs provider state from:
1. persisted provider state;
2. active installation metadata;
3. filesystem existence;
4. controlled Kubo health check.

A stale PID is never treated as proof that Kubo is running.
