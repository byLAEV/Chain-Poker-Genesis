# Node Installation Contract

**Project:** Chain Poker Genesis by LAEV  
**Layer:** Node Core  
**Version:** 0.1.0  
**Status:** SUPPORTING / RECONCILED  
**Protocol:** Not installed

## Contract

A compliant baseline installer MUST produce a Node Core installation that satisfies:

```text
NODE_CORE_READY
+
CPG_PROTOCOL = NOT_INSTALLED
+
PROTOCOL_ASSOCIATIONS = []
```

## Required outputs

1. Node identity metadata.
2. Node configuration.
3. Canonical local storage structure.
4. Storage manifest.
5. Node lifecycle state.
6. Recovery metadata.
7. Installation manifest.
8. Deterministic verification result.

## Required canonical storage paths

```text
node-storage/
├── identity/
├── cryptography/
├── configuration/
├── state/
├── records/
├── recovery/
└── protocol/
```

## Provider boundary

A decentralized-storage provider is optional at this baseline.

The installer MUST NOT silently install Kubo/IPFS or any other external storage daemon.

If no provider is provisioned, the node records:

`decentralized_storage.status = NOT_PROVISIONED`

This is not an installation failure for Node Core 0.1.0.

## Protocol isolation

The baseline installer MUST NOT:

- download CPG packages;
- import CPG engines;
- create CPG table state;
- create CPG ledger state;
- create CPG protocol membership;
- activate CPG networking.

## Failure behavior

Any malformed manifest, missing required path, unexpected protocol association, or invalid CPG status MUST cause verification failure.

## Version boundary

This contract defines the 0.1.0 baseline only. Changes to required paths, readiness semantics, protocol isolation, or manifest fields require a versioned contract update.


## Managed Kubo Provisioning

The baseline Node Core installation remains protocol-neutral and does not silently install Kubo.

A subsequent explicit storage-provider provisioning action MAY install the complete official Kubo distribution for the host platform.

For Linux, the first supported platform, the installer MUST:
1. select a compatible stable Kubo release;
2. download the complete official distribution;
3. verify package integrity;
4. install the Kubo executable under the Node Core-managed External Providers/Kubo version directory;
5. initialize the Kubo repository under Node Core's provider storage directory;
6. set an absolute `IPFS_PATH` for every Kubo process;
7. record the installed Kubo version and repository path;
8. perform initial local-to-Kubo synchronization;
9. verify coherence and integrity;
10. only then permit `DUAL_STORAGE`.

Windows follows the same logical contract with platform-specific installation mechanics.

iOS is a later platform target and MUST NOT be treated as equivalent to the Linux Kubo daemon model without a separate platform-specific implementation contract.
