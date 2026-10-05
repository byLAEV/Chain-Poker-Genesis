# Chain Poker Genesis — Node Core CLI Installer

This directory contains the minimal command-line installer for the
protocol-neutral Node Core.

## Interface

The installer is designed for Linux shells and Termux.

The interactive installer follows the Node Core OS architecture:

```
1. Node Core BIOS
2. Node Core
3. Protocols
0. Exit
```

The BIOS menu contains the Node Core installation action. Node Core and Protocols are
separate architectural instances and are not collapsed into the BIOS installation
action.

It is not a GUI and it is not a Node Manager.

## Entry points

- `Installer/install.sh` — Linux/Termux launcher.
- `Installer/install.py` — CLI and installation engine.

When launched from an interactive terminal, `install.py` presents the
minimal menu. CI and automation use `--non-interactive`.

## Platform requirements

- Linux: Python 3.9 or newer, with the distribution's `venv` support available.
- Termux: Python and `python-cryptography` are installed through `pkg`.
- Network access is required to resolve the source ref, download Node Core, and
  install Linux Python dependencies.

The installer does not use `sudo` automatically and does not modify system
packages on Linux. If Linux Python or its `venv` support is missing, install
the appropriate packages using the distribution package manager and rerun the
installer.

## Installation flow

```
Platform detection
  ↓
Python runtime validation
  ↓
Download immutable Node Core source
  ↓
Prepare platform-specific Python environment
  ↓
Node Core Bootstrap
  ↓
Node Core Verification
  ↓
NODE_CORE_READY
```

The installation engine:

- downloads only the Node Core component;
- resolves the requested source ref to a commit SHA before downloading;
- creates the local `.node-core-python` environment when Node Core declares
  Python dependencies;
- invokes the canonical Node Core Bootstrap;
- verifies the resulting installation;
- does not overwrite an existing Node Core installation.

## Linux behavior

Linux creates an isolated virtual environment under the installed Node Core
directory and installs the canonical Node Core requirements.

The dependency installation uses compatible binary packages only. This avoids
silently introducing a compiler/Rust build chain for cryptography. If the
selected Linux architecture/Python combination has no compatible binary
package, installation fails explicitly rather than performing an unreviewed
source build.

## Termux behavior

Termux uses the native packages:

`python` and `python-cryptography`.

The Node Core environment is created with `--system-site-packages`, so the
native cryptography implementation is reused instead of compiling
`cryptography` from PyPI source.

The installer verifies:

1. the native `cryptography` package is visible;
2. its version is within the Node Core compatibility boundary (`>=46,<49`);
3. AES-GCM encryption/decryption works;
4. Ed25519 key generation works.

If these checks fail, installation stops explicitly.

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

## Verification status

The Installer is **IMPLEMENTED_AND_CI_VERIFIED**.

CI verification covers the installer logic, fresh installation, protection of
existing installations, rollback behavior, archive safety, immutable source
resolution, Bootstrap, Verification, and POSIX launcher syntax.

Real-environment validation remains explicitly separate:

- Linux real-host validation: not verified in the release environment used for
  this repository review.
- Termux real-device validation: not verified.

Therefore this status means implementation and repository/CI verification,
not physical Termux certification.
