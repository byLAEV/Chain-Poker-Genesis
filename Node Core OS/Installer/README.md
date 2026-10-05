# Node Core OS Linux Installer

This directory contains the first Linux installer for **Node Core OS**.

## Purpose

The installer prepares a local Node Core OS terminal entry point and installs the Python Bootstrap.

The first stage intentionally has no third-party Python dependencies. The Bootstrap uses only the Python standard library because its current responsibility is to display and operate the Node Core OS main menu.

## Requirements

- Linux
- Python 3.9 or newer
- `python3` available in `PATH`
- No `sudo`
- No `pip`
- No external Python package

## Installation

From the repository root:

```bash
python3 "Node Core OS/Installer/install.py"
```

The default installation target is:

```text
~/.local/share/chain-poker-genesis/node-core-os/
```

A different target may be selected with:

```bash
NODE_CORE_OS_INSTALL_ROOT=/path/to/node-core-os python3 "Node Core OS/Installer/install.py"
```

## Installed entry point

The installer creates:

```text
~/.local/share/chain-poker-genesis/node-core-os/
├── Bootstrap/
│   └── node_core_os_bootstrap.py
└── node-core-os
```

Run the menu with:

```bash
~/.local/share/chain-poker-genesis/node-core-os/node-core-os
```

or directly:

```bash
python3 ~/.local/share/chain-poker-genesis/node-core-os/Bootstrap/node_core_os_bootstrap.py
```

## Dependency policy

No external library is introduced at this stage.

The Bootstrap requires only:

- Python standard library
- Linux terminal
- standard POSIX filesystem access

Later Node Core OS components may introduce additional dependencies, but those belong to the corresponding implementation stage and must not be added speculatively to this first Bootstrap installer.
