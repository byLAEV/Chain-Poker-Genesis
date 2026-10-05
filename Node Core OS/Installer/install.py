#!/usr/bin/env python3
"""Node Core OS installer for Linux and Termux."""

from __future__ import annotations

import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

MIN_PYTHON = (3, 9)
DEFAULT_INSTALL_ROOT = Path.home() / "Node Core OS"
BOOTSTRAP_RELATIVE = Path("Node Core OS") / "Bootstrap" / "node_core_os_bootstrap.py"
INSTALLER_VERSION = "1.1.1"


class InstallerError(RuntimeError):
    pass


def check_platform() -> None:
    if not (sys.platform.startswith("linux") or sys.platform == "android"):
        raise InstallerError(
            "This installer currently supports Linux and Termux on Android."
        )


def check_python() -> None:
    if sys.version_info < MIN_PYTHON:
        raise InstallerError(
            f"Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]} or newer is required; "
            f"detected {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}."
        )


def check_dependencies() -> None:
    if shutil.which("python3") is None:
        raise InstallerError("python3 was not found in PATH.")


def repository_root() -> Path:
    current = Path(__file__).resolve()
    for parent in (current, *current.parents):
        candidate = parent / BOOTSTRAP_RELATIVE
        if candidate.is_file():
            return parent
    raise InstallerError(
        "Cannot locate the Node Core OS Bootstrap in the repository."
    )


def install_bootstrap(target_root: Path) -> Path:
    source_root = repository_root()
    source = source_root / BOOTSTRAP_RELATIVE
    target = target_root / "Bootstrap" / "node_core_os_bootstrap.py"

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)

    mode = target.stat().st_mode
    target.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return target


def create_launcher(target_root: Path) -> Path:
    launcher = target_root / "node-core-os"
    bootstrap = target_root / "Bootstrap" / "node_core_os_bootstrap.py"
    launcher.write_text(
        "#!/bin/sh\n"
        f'exec python3 "{bootstrap}" "$@"\n',
        encoding="utf-8",
    )
    mode = launcher.stat().st_mode
    launcher.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return launcher


def main() -> int:
    try:
        check_platform()
        check_python()
        check_dependencies()

        target_root = Path(
            os.environ.get("NODE_CORE_OS_INSTALL_ROOT", str(DEFAULT_INSTALL_ROOT))
        ).expanduser().resolve()

        print("Node Core OS Installer")
        print("======================")
        print(f"Version: {INSTALLER_VERSION}")
        print(f"Python: {sys.version.split()[0]}")
        print(f"Install root: {target_root}")
        print()
        print("[1/3] Checking Linux/Termux and Python environment... OK")
        print("[2/3] Installing Node Core OS Bootstrap...")
        bootstrap = install_bootstrap(target_root)
        print(f"      Installed: {bootstrap}")
        print("[3/3] Creating terminal launcher...")
        launcher = create_launcher(target_root)
        print(f"      Created: {launcher}")
        print()
        print("Node Core OS installed successfully.")
        print()
        print("Starting Node Core OS...")
        print()

        return subprocess.call([sys.executable, str(bootstrap)])

    except InstallerError as exc:
        print(f"INSTALLATION FAILED: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"INSTALLATION FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
