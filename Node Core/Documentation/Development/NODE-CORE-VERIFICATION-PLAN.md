# Node Core Verification Plan

## Verification layers

| Layer | Purpose |
|---|---|
| Structural | Canonical files, directories, boundaries, and migration state |
| Static | JSON/schema validity and source compilation |
| Unit | Individual component behavior |
| Integration | Cross-component behavior |
| Failure | Invalid input, unavailable dependencies, interruption, and recovery |
| Operational | Install, initialize, start, readiness, stop, restart |
| Fresh-environment | Reproducibility from a clean environment |
| CI | Automated execution and recorded GitHub evidence |

## Verification matrix

| Area | Structural | Static | Unit | Integration | Failure | Operational | Fresh environment |
|---|---:|---:|---:|---:|---:|---:|---:|
| Bootstrap | ✓ | ✓ | ☐ | ☐ | ☐ | ☐ | ☐ |
| Identity | ✓ | ✓ | ☐ | ☐ | ☐ | ☐ | ☐ |
| Cryptography | ✓ | ✓ | ☐ | ☐ | ☐ | ☐ | ☐ |
| Storage | ✓ | ✓ | ☐ | ☐ | ☐ | ☐ | ☐ |
| Runtime | ✓ | ✓ | ☐ | ☐ | ☐ | ☐ | ☐ |
| Network | ✓ | ✓ | ☐ | ☐ | ☐ | ☐ | ☐ |
| Recovery | ✓ | ✓ | ☐ | ☐ | ☐ | ☐ | ☐ |
| Protocol Interface | ✓ | ✓ | ☐ | ☐ | ☐ | ☐ | ☐ |
| Configuration / Manifest | ✓ | ✓ | ☐ | ☐ | ☐ | ☐ | ☐ |
| Release Integrity | ✓ | ✓ | ☐ | ☐ | ☐ | ☐ | ☐ |

The unchecked cells are implementation work, not claims of completion.

## Evidence rule

A green CI run proves only the checks executed by that run. Each completion record must identify the commit, workflow run, tests executed, and remaining limitations.
