# Chain Poker Genesis — Direct Node Core Installer

This directory contains the direct remote installer for the protocol-neutral
Node Core.

## Purpose

The installer allows a Linux or Termux user to start installation from a
single repository-hosted link.

The installer:

1. obtains the installer bootstrap;
2. detects Linux or Termux;
3. downloads the repository archive;
4. extracts the Node Core component;
5. stages the component locally;
6. executes the canonical Node Core Bootstrap installer;
7. verifies the resulting Node Core installation;
8. commits the staged installation to the local target.

## Entry point

The shell launcher is:

`Installer/install.sh`

It is intentionally small. The installation logic lives in:

`Installer/install.py`

## Direct execution

Linux or Termux can obtain the launcher from the repository and execute it
with a POSIX shell.

The installer requires Python 3. On Termux, when Python is absent, the
launcher attempts to install it through the native Termux package manager.

## Installation boundary

This installer installs Node Core only.

It does not:

- install CPG Protocol;
- create a CPG ledger;
- create CPG table state;
- install poker rules;
- associate a protocol with the node.

The architectural rule remains:

**Node Core provides the node. Protocols provide their protocols.**

## Existing installations

The installer does not overwrite an existing Node Core installation. A
future repair/recovery command can be introduced separately without turning
the direct installer into an updater.

## Current status

This is the first direct installer implementation and must be exercised on
real Linux and Termux environments before being promoted to a stable release.
