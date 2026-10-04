#!/usr/bin/env python3
"""Direct remote installer for the protocol-neutral Node Core.

This installer intentionally has no preflight subsystem. It performs the
minimum direct sequence required to obtain, stage, install, bootstrap and
verify Node Core from the Chain Poker Genesis repository.

Node Core remains protocol-neutral. CPG is not installed by this process.
"""
from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
from pathlib import Path

REPOSITORY = "byLAEV/Chain-Poker-Genesis"
DEFAULT_LINUX_TARGET = Path.home() / ".local" / "share" / "chain-poker-genesis" / "node-core"
DEFAULT_TERMUX_TARGET = Path.home() / ".chain-poker-genesis" / "node-core"


class InstallationError(RuntimeError):
    pass


def detect_platform() -> str:
    if os.environ.get("TERMUX_VERSION") or "com.termux" in os.environ.get("PREFIX", ""):
        return "TERMUX"
    if sys.platform.startswith("linux"):
        return "LINUX"
    raise InstallationError(f"Unsupported operating system: {sys.platform}")


def default_target(platform_name: str) -> Path:
    if platform_name == "TERMUX":
        return DEFAULT_TERMUX_TARGET
    return DEFAULT_LINUX_TARGET


def download_archive(destination: Path, source_ref: str) -> None:
    archive_url = (
        f"https://github.com/{REPOSITORY}/archive/{source_ref}.tar.gz"
    )
    print(f"Downloading Node Core package from {REPOSITORY}@{source_ref}...")
    request = urllib.request.Request(
        archive_url,
        headers={"User-Agent": "Chain-Poker-Genesis-Node-Core-Installer/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response, destination.open("wb") as output:
            shutil.copyfileobj(response, output)
    except Exception as exc:
        raise InstallationError(f"Unable to download Node Core package: {exc}") from exc


def extract_node_core(archive: Path, extraction_root: Path, staging: Path) -> None:
    try:
        with tarfile.open(archive, "r:gz") as package:
            members = package.getmembers()
            node_core_prefix = None
            for member in members:
                parts = Path(member.name).parts
                if len(parts) >= 2 and parts[1] == "Node Core":
                    node_core_prefix = Path(parts[0]) / "Node Core"
                    break

            if node_core_prefix is None:
                raise InstallationError("Downloaded repository does not contain Node Core")

            selected = []
            prefix = str(node_core_prefix).rstrip("/") + "/"
            for member in members:
                if member.name == str(node_core_prefix) or member.name.startswith(prefix):
                    relative = Path(member.name).relative_to(node_core_prefix)
                    member.name = str(relative)
                    selected.append(member)

            package.extractall(extraction_root, members=selected)

    except (tarfile.TarError, OSError) as exc:
        raise InstallationError(f"Unable to extract Node Core package: {exc}") from exc

    extracted = extraction_root / "Bootstrap" / "Installer" / "bootstrap_node.py"
    if not extracted.is_file():
        raise InstallationError("Downloaded package is missing the canonical Node Core installer")

    shutil.copytree(extraction_root, staging, dirs_exist_ok=True)



def prepare_python_environment(staging: Path, temp_root: Path) -> Path:
    requirements = staging / "Cryptography" / "requirements.txt"
    if not requirements.is_file():
        return Path(sys.executable)

    environment = temp_root / ".node-core-python"
    print("Preparing Node Core Python environment...")
    completed = subprocess.run(
        [sys.executable, "-m", "venv", str(environment)],
        text=True,
        capture_output=True,
    )
    if completed.returncode != 0:
        if completed.stdout:
            print(completed.stdout, end="")
        if completed.stderr:
            print(completed.stderr, file=sys.stderr, end="")
        raise InstallationError("Unable to create the Node Core Python environment")

    python_executable = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if not python_executable.is_file():
        raise InstallationError("Created Python environment is missing its interpreter")

    completed = subprocess.run(
        [str(python_executable), "-m", "pip", "install", "--disable-pip-version-check", "-r", str(requirements)],
        text=True,
        capture_output=True,
    )
    if completed.returncode != 0:
        if completed.stdout:
            print(completed.stdout, end="")
        if completed.stderr:
            print(completed.stderr, file=sys.stderr, end="")
        raise InstallationError("Unable to install Node Core Python dependencies")

    return python_executable


def bootstrap(staging: Path, python_executable: Path) -> None:
    installer = staging / "Bootstrap" / "Installer" / "bootstrap_node.py"
    print("Bootstrapping Node Core...")
    completed = subprocess.run(
        [str(python_executable), str(installer), str(staging)],
        text=True,
        capture_output=True,
    )
    if completed.returncode != 0:
        if completed.stdout:
            print(completed.stdout, end="")
        if completed.stderr:
            print(completed.stderr, file=sys.stderr, end="")
        raise InstallationError("Node Core bootstrap failed")

    if completed.stdout:
        print(completed.stdout, end="")


def verify(staging: Path, python_executable: Path) -> None:
    verifier = staging / "Bootstrap" / "Verification" / "bootstrap_verifier.py"
    print("Verifying Node Core...")
    completed = subprocess.run(
        [str(python_executable), str(verifier), str(staging)],
        text=True,
        capture_output=True,
    )
    if completed.returncode != 0:
        if completed.stdout:
            print(completed.stdout, end="")
        if completed.stderr:
            print(completed.stderr, file=sys.stderr, end="")
        raise InstallationError("Node Core verification failed")

    if completed.stdout:
        print(completed.stdout, end="")


def install(target: Path, source_ref: str = "main") -> None:
    platform_name = detect_platform()
    architecture = platform.machine()

    print(f"Platform: {platform_name}")
    print(f"Architecture: {architecture}")
    print(f"Target: {target}")

    target = target.expanduser().resolve()
    if target.exists():
        manifest = target / "node-installation-manifest.json"
        if manifest.exists():
            raise InstallationError(
                f"Node Core is already installed at {target}. "
                "The direct installer will not overwrite an existing installation."
            )
        if any(target.iterdir()):
            raise InstallationError(
                f"Installation target is not empty: {target}"
            )

    target.parent.mkdir(parents=True, exist_ok=True)
    staging = target.parent / f".{target.name}.staging-{os.getpid()}"
    if staging.exists():
        raise InstallationError(f"Installation staging path already exists: {staging}")

    target_created = False
    try:
        with tempfile.TemporaryDirectory(prefix="cpg-node-core-") as temp:
            temp_root = Path(temp)
            archive = temp_root / "repository.tar.gz"
            extracted = temp_root / "node-core"
            extracted.mkdir()

            download_archive(archive, source_ref)
            extract_node_core(archive, extracted, staging)

        staging.rename(target)
        target_created = True

        python_executable = prepare_python_environment(target, target)
        bootstrap(target, python_executable)
        verify(target, python_executable)
    except Exception:
        if target_created and target.exists():
            shutil.rmtree(target, ignore_errors=True)
        if staging.exists():
            shutil.rmtree(staging, ignore_errors=True)
        raise

    print("")
    print("Node Core installation completed.")
    print(f"Installed at: {target}")
    print("CPG Protocol: NOT INSTALLED")
    print("Protocol associations: []")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install Node Core directly from the Chain Poker Genesis repository."
    )
    parser.add_argument(
        "--target",
        type=Path,
        help="installation directory; defaults to a user-local Linux/Termux location",
    )
    parser.add_argument(
        "--ref",
        default="main",
        help="Git branch containing the Node Core package (default: main)",
    )
    args = parser.parse_args()

    try:
        platform_name = detect_platform()
        target = args.target or default_target(platform_name)
        install(target, args.ref)
    except InstallationError as exc:
        print(f"INSTALLATION FAILED: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
