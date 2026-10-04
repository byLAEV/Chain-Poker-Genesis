# Node Core Installer — Real Environment Validation

## Purpose

This procedure validates the Node Core CLI Installer outside CI without changing installer behavior.

CI verification is already recorded as `IMPLEMENTED_AND_CI_VERIFIED`. This procedure is required before claiming physical Linux or Termux validation.

## Required test environments

- Linux host with network access and Python 3.9+.
- Termux on a real Android device with network access and Python available through Termux.

Each environment must record:
- OS and version;
- architecture;
- Python version;
- installer source reference;
- resolved source commit SHA;
- target path used;
- final result.

## Test 1 — Fresh installation

1. Start from a target path that does not exist.
2. Launch `Installer/install.sh`.
3. Select `1. Install Node Core`.
4. Accept the installation confirmation.
5. Record the displayed source commit SHA.
6. Confirm the process ends with `NODE_CORE_READY`.
7. Confirm CPG Protocol is `NOT INSTALLED`.
8. Run the Node Core verification command used by the installer.
9. Record PASS/FAIL.

Expected: PASS and a complete Node Core installation.

## Test 2 — Existing installation

1. Repeat the installer against the same target.
2. Confirm it detects the existing installation.
3. Confirm it does not overwrite the target.
4. Confirm the existing installation remains functional.

Expected: PASS with no destructive modification.

## Test 3 — Interrupted installation

1. Start a fresh installation target.
2. Interrupt the process with `Ctrl+C` during installation.
3. Confirm the process terminates.
4. Confirm no incomplete target remains.
5. Confirm a subsequent fresh installation can proceed.

Expected: PASS with clean rollback.

## Test 4 — Non-interactive mode

Run the installer with the same source reference and explicit target arguments used by CI.

Expected: PASS without presenting the interactive menu.

## Test 5 — Final verification

Run the Node Core verification after installation.

Confirm:
- Node Core is ready;
- storage/provider state is coherent;
- Bootstrap verification succeeds;
- CPG Protocol remains not installed;
- no protocol-specific state was created by the Installer.

## Result classification

Use only these values:

- `PASS`
- `FAIL`
- `BLOCKED`

Do not mark Linux or Termux as verified without actually executing the procedure in that environment.

## Evidence record

For every completed environment, preserve the terminal output or an equivalent test record containing the environment, source SHA, target, tests, and result.

## Scope boundary

This procedure validates the Installer only. It does not authorize adding Node Manager, Preflight, updater behavior, CPG Protocol installation, poker logic, ledger creation, or identity provisioning to the Installer.
