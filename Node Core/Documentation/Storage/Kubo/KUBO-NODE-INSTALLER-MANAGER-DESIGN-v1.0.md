# Kubo Node Installer / Manager — Canonical Design v1.0

**Status:** CANONICAL DESIGN — NO INSTALLATION CODE YET

## 1. Purpose

The Kubo Node Installer / Manager is a Node Core provider-management subsystem. It is not a Kubo reimplementation and it is not a generic downloader.

It has two responsibilities:

1. provision a complete official Kubo node distribution;
2. manage the resulting Kubo node as an external storage provider.

The existing Kubo Adapter remains a separate boundary. The Installer / Manager owns lifecycle and environment; the Adapter owns provider API translation.

## 2. Canonical directory model

Given:

`NODE_CORE_ROOT`

the Linux reference layout is:

```text
<NODE_CORE_ROOT>/
├── External Providers/
│   └── Kubo/
│       └── <kubo-version>/
│           ├── bin/
│           │   └── ipfs
│           ├── release/
│           └── metadata/
│
└── node-storage/
    └── providers/
        └── kubo/
            ├── repository/
            ├── runtime/
            ├── logs/
            ├── state/
            └── synchronization/
```

The versioned installation directory contains the Kubo distribution. The repository is deliberately outside that directory.

Kubo's internal repository layout is Kubo-owned and MUST NOT be recreated or renamed by Node Core.

## 3. IPFS_PATH contract

Node Core derives one absolute repository path:

`<NODE_CORE_ROOT>/node-storage/providers/kubo/repository/`

Every managed Kubo process receives:

`IPFS_PATH=<absolute-kubo-repository-path>`

The Manager MUST NOT depend on the operator's `~/.ipfs`, current working directory, shell profile, or implicit relative paths.

The selected `IPFS_PATH` is persisted in provider state and verified before every managed process start.

## 4. Release selection

The Manager does not hard-code a release into the repository architecture.

At explicit provisioning time it resolves:

`latest compatible stable release → platform → architecture → official distribution`

The resolved release becomes an immutable installation record.

An upgrade is a separate explicit lifecycle operation. A new Kubo version MUST receive a new versioned installation directory rather than overwriting the active installation.

## 5. Package verification

The lifecycle cannot progress to installation until the downloaded distribution passes integrity verification.

Minimum verification evidence:

- official release identity;
- selected platform;
- selected architecture;
- expected package;
- package hash/integrity evidence;
- extracted executable presence;
- executable identity/version check.

A failed verification MUST transition to `FAILED` and MUST NOT activate the provider.

## 6. Initialization

Initialization is explicitly separated:

```text
PACKAGE_VERIFIED
      ↓
INSTALLING
      ↓
INSTALLED
      ↓
REPOSITORY_INITIALIZING
      ↓
REPOSITORY_INITIALIZED
      ↓
CONFIGURING
      ↓
CONFIGURED
```

The Manager invokes Kubo's supported initialization mechanism with the explicit `IPFS_PATH`.

Node Core does not manufacture Kubo's repository files.

## 7. Runtime lifecycle

```text
NOT_PROVISIONED
  → RELEASE_SELECTED
  → PACKAGE_DOWNLOADING
  → PACKAGE_DOWNLOADED
  → PACKAGE_VERIFIED
  → INSTALLING
  → INSTALLED
  → REPOSITORY_INITIALIZING
  → REPOSITORY_INITIALIZED
  → CONFIGURING
  → CONFIGURED
  → STARTING
  → HEALTHY
  → INITIAL_SYNC_PENDING
  → INITIAL_SYNCING
  → COHERENCE_VERIFICATION
  → READY
```

Runtime exceptions may enter `DEGRADED` or `FAILED`.

`READY` means the managed Kubo provider is ready for Node Core Storage integration. It does not mean Dual Storage is active by itself.

## 8. Stop / restart

A controlled stop:

`HEALTHY/READY → STOPPING → STOPPED`

A restart must verify the persisted installation manifest and `IPFS_PATH` before starting the executable.

The Manager MUST never start an unverified or unregistered Kubo installation.

## 9. Provider state

The Manager persists state under:

`node-storage/providers/kubo/state/`

At minimum:

- installed version;
- platform;
- architecture;
- executable path;
- repository path;
- `IPFS_PATH`;
- lifecycle state;
- health status;
- installation timestamp;
- last transition;
- release verification evidence;
- active installation identifier.

The state record is Node Core metadata. It is not a replacement for Kubo's repository.

## 10. Synchronization boundary

Once Kubo reaches `HEALTHY`, Storage Manager may initiate:

```text
INITIAL_SYNC_PENDING
      ↓
INITIAL_SYNCING
      ↓
COHERENCE_VERIFICATION
      ↓
READY
```

The Installer / Manager does not decide which logical objects should be mirrored. Storage Manager / Storage Policy decides that.

The Installer / Manager only provides the healthy Kubo target and reports provider state.

## 11. Dual Storage gate

`DUAL_STORAGE` is permitted only when:

- installation is verified;
- repository is initialized;
- configuration is valid;
- Kubo is healthy;
- initial synchronization has completed;
- integrity/coherence verification succeeds;
- no unresolved synchronization conflict exists.

Therefore:

`KUBO READY ≠ DUAL STORAGE READY`

## 12. Failure rules

The Manager MUST fail closed for:

- unknown release;
- unsupported platform/architecture;
- failed package verification;
- missing executable;
- executable/version mismatch;
- invalid repository path;
- repository initialized at an unexpected location;
- invalid `IPFS_PATH`;
- failed health check;
- unresolved installation state.

Failed installation artifacts MUST NOT be promoted to active provider state.

## 13. Upgrade model

The architecture supports explicit provider upgrades:

```text
ACTIVE KUBO vA
      ↓
INSTALL vB beside vA
      ↓
VERIFY vB
      ↓
INITIALIZE vB repository if required
      ↓
MIGRATION / PROVIDER-SPECIFIC VALIDATION
      ↓
ACTIVATE vB
```

The exact repository migration mechanism remains provider-specific and is not invented in this contract.

## 14. Security boundary

Node Core manages paths, process environment and lifecycle.

Node Core does not assume custody of Kubo private keys merely because it manages the Kubo process.

Protocol private keys, wallet keys and CPG cryptographic identity remain outside this provider manager unless a separate canonical contract explicitly assigns a credential adapter.

## 15. Platform policy

Linux is the reference implementation target.

Windows reuses the logical contract with platform-specific executable/process/path mechanics.

iOS is a later target and requires a separate platform contract before implementation. The Linux daemon model MUST NOT simply be copied to iOS.

## 16. Non-responsibilities

The Kubo Node Installer / Manager does not:

- implement IPFS;
- implement CPG consensus;
- modify the CPG ledger;
- define poker state;
- administer Table Wallet;
- perform settlement/rake;
- decide Storage Policy;
- become a second Storage Registry;
- replace the Kubo Adapter.

## 17. Design gate

This document is complete enough to begin implementation only after the release-source contract, platform architecture matrix, provider-state schema and installation test vectors are separately frozen.
