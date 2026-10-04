# Kubo Process and Health Management

The Node Core Kubo manager owns the Linux daemon lifecycle.

## Process boundary

The manager starts the installed Kubo executable with:
- explicit absolute `IPFS_PATH`;
- `daemon` command;
- Node Core-managed runtime and log paths;
- persisted PID/process metadata.

A PID is never considered proof of health.

## Health boundary

Health is established through Kubo's local RPC API:
- `/api/v0/id` verifies the repository identity is available;
- `/api/v0/version` verifies the daemon reports its version.

A healthy process is not automatically synchronized or READY.

Initial synchronization and Dual Storage activation remain separate lifecycle stages.