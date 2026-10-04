# Chain Poker Genesis — Node Core CLI Installer

This directory contains the minimal command-line installer for the
protocol-neutral Node Core.

## Interface

The installer is designed for a command window, POSIX shell, or Termux.

The interactive menu intentionally has only two options:

```
1. Install Node Core
2. Exit
```

It is not a GUI and it is not a Node Manager.

## Entry points

- `Installer/install.sh` — shell/Termux launcher.
- `Installer/install.py` — CLI and installation engine.

When launched from an interactive terminal, `install.py` presents the
minimal menu. CI and automation use `--non-interactive`.

## Installation flow

The user-facing flow is:

```
Menu
  ↓
Install Node Core
  ↓
Confirm
  ↓
Download
  ↓
Prepare local environment
  ↓
Node Core Bootstrap
  ↓
Node Core Verification
  ↓
NODE_CORE_READY
```

The installer engine keeps the existing installation boundary:

- downloads only the Node Core component;
- creates the local `.node-core-python` environment when Node Core declares Python dependencies;
- invokes the canonical Node Core Bootstrap;
- verifies the resulting installation;
- does not overwrite an existing Node Core installation.

## Architectural boundary

This installer installs **Node Core only**.

It does not:

- install CPG Protocol;
- create a CPG ledger;
- create CPG table state;
- install poker rules;
- create protocol associations;
- create cryptographic player identity;
- act as Node Manager;
- update an existing Node Core installation.

The architectural rule remains:

**Node Core provides the node. Protocols provide their protocols.**

## Platform behavior

Supported targets are Linux and Termux.

The shell launcher installs Python through the native Termux package manager when
Python is absent. It uses Python's standard library to retrieve the installer,
so `curl` or `wget` is not required by the launcher.

Default installation targets:

- Linux: `~/.local/share/chain-poker-genesis/node-core`
- Termux: `~/.chain-poker-genesis/node-core`

## Automation

For CI or scripts:

```sh
python Installer/install.py --non-interactive --ref <ref> --target <target>
```

The non-interactive mode uses the same installation engine as the interactive
menu.

## No Preflight subsystem

The installer intentionally has no Preflight subsystem. Required validation
belongs to the installation, Bootstrap, and Verification stages.

## Status

This CLI implementation must be exercised on real Linux and Termux
environments before promotion to a stable installer release.
