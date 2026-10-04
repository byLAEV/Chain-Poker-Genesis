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

The shell launcher installs Python and the native cryptography dependency through
the Termux package manager when Python is absent. If Python is already present,
the Python installer path still installs the native cryptography package before
creating the Node Core environment. It uses Python's standard library to retrieve the installer,
so `curl` or `wget` is not required by the launcher.

### Termux cryptography dependency

Node Core Cryptography currently declares `cryptography==46.0.4` for the
canonical Linux/Python dependency environment. Termux is different: Android
does not receive the same PyPI binary-wheel set as the supported Linux
platforms, so installing that pinned package with pip can fall back to a
local Rust/C build. Current Termux Rust packaging has documented cases where
Rust-based Python extensions such as `cryptography` cannot be built reliably.

For Termux, the installer therefore uses the native Termux package:

`python-cryptography`

The installer:

1. installs `python-cryptography` through `pkg`;
2. creates the Node Core virtual environment with
   `--system-site-packages`;
3. verifies that the native `cryptography` installation is visible;
4. verifies that its version is compatible with the current Node Core
   cryptography API boundary (`>=46,<49`);
5. verifies the Ed25519 and AES-GCM primitives required by the Node Core
   implementation;
6. does **not** attempt to compile `cryptography` from PyPI source on
   Termux.

This deliberately avoids making Rust, clang, OpenSSL headers, libffi, or
pkg-config a mandatory Termux build chain for the Node Core installer.
Those tools are relevant when compiling `cryptography` from source, but the
installer's Termux path uses the native packaged cryptography implementation
instead.

If the native Termux package is unavailable or outside the compatibility
range, installation fails explicitly rather than silently substituting an
unverified cryptographic implementation.

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

## Verification status

The Installer is **IMPLEMENTED_AND_CI_VERIFIED**.

CI verifies:

- interactive two-option CLI behavior;
- fresh installation flow;
- existing/incomplete target protection;
- interrupted installation rollback;
- rollback after target creation;
- archive extraction safety;
- immutable source resolution;
- Node Core Bootstrap;
- Node Core Verification;
- POSIX shell launcher syntax.

Real-environment validation remains explicitly separate:

- Linux real-device/host validation: not verified in the release environment used for this repository review.
- Termux real-device validation: not verified.

The Termux installer path is implemented, including native Python and
`python-cryptography` dependency handling, system-site-packages environment
creation, cryptography primitive verification, and the Node Core network
readiness baseline. Physical Termux-device certification remains pending.

Therefore this status means **implementation and CI verification**, not a claim of physical Termux certification.
