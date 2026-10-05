#!/usr/bin/env python3
"""Node Core OS Linux installer.

Installs the Node Core OS terminal bootstrap locally without requiring sudo.
"""

from __future__ import annotations

import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

MIN_PYTHON = (3, 9)
DEFAULT_INSTALL_ROOT = Path.home() / ".local" / "share" / "chain-poker-genesis" / "node-core-os"
BOOTSTRAP_RELATIVE = Path("Node Core OS") / "Bootstrap" / "node_core_os_bootstrap.py"
INSTALLER_VERSION = "1.0.0"


class InstallerError(RuntimeError):
    pass


def check_linux() -> None:
    if not sys.platform.startswith("linux"):
        raise InstallerError("This installer currently supports Linux only.")


def check_python() -> None:
    if sys.version_info < MIN_PYTHON:
        raise InstallerError(
            f"Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]} or newer is required; "
            f"detected {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}."
        )


def check_dependencies() -> None:
    # The first Node Core OS bootstrap uses only Python's standard library.
    # No pip package is required for this first installation stage.
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
    launcher.write_text(
        "#!/bin/sh\n"
        'exec python3 "$HOME/.local/share/chain-poker-genesis/node-core-os/'
        'Bootstrap/node_core_os_bootstrap.py" "$@"\n',
        encoding="utf-8",
    )
    mode = launcher.stat().st_mode
    launcher.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return launcher


def main() -> int:
    try:
        check_linux()
        check_python()
        check_dependencies()

        target_root = Path(
            os.environ.get("NODE_CORE_OS_INSTALL_ROOT", str(DEFAULT_INSTALL_ROOT))
        ).expanduser().resolve()

        print("Node Core OS Linux Installer")
        print("============================")
        print(f"Python: {sys.version.split()[0]}")
        print(f"Install root: {target_root}")
        print()
        print("[1/3] Checking Linux and Python environment... OK")
        print("[2/3] Installing Node Core OS Bootstrap...")
        bootstrap = install_bootstrap(target_root)
        print(f"      Installed: {bootstrap}")
        print("[3/3] Creating terminal launcher...")
        launcher = create_launcher(target_root)
        print(f"      Created: {launcher}")
        print()
        print("Node Core OS installed successfully.")
        print()
        print("Run:")
        print(f"  {launcher}")
        print()
        print("Or run the Bootstrap directly:")
        print(f"  python3 {bootstrap}")
        return 0

    except InstallerError as exc:
        print(f"INSTALLATION FAILED: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"INSTALLATION FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
