#!/usr/bin/env python3
"""Direct CLI installer for the protocol-neutral Node Core.

The interactive interface is intentionally minimal: install Node Core or exit.
The installation engine remains protocol-neutral and never installs CPG.
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
    return DEFAULT_TERMUX_TARGET if platform_name == "TERMUX" else DEFAULT_LINUX_TARGET


def resolve_commit_sha(source_ref: str) -> str:
    """Resolve a branch/tag/ref to an immutable commit SHA before downloading."""
    if len(source_ref) == 40 and all(c in "0123456789abcdefABCDEF" for c in source_ref):
        return source_ref.lower()

    api_url = f"https://api.github.com/repos/{REPOSITORY}/commits/{source_ref}"
    request = urllib.request.Request(
        api_url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "Chain-Poker-Genesis-Node-Core-Installer/1.0",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            import json
            payload = json.load(response)
        sha = payload.get("sha")
    except Exception as exc:
        raise InstallationError(f"Unable to resolve installer source reference: {exc}") from exc

    if not isinstance(sha, str) or len(sha) != 40:
        raise InstallationError("GitHub did not return a valid commit SHA for the requested source")
    return sha.lower()


def download_archive(destination: Path, source_ref: str) -> str:
    resolved_sha = resolve_commit_sha(source_ref)
    archive_url = f"https://github.com/{REPOSITORY}/archive/{resolved_sha}.tar.gz"
    request = urllib.request.Request(
        archive_url,
        headers={"User-Agent": "Chain-Poker-Genesis-Node-Core-Installer/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response, destination.open("wb") as output:
            shutil.copyfileobj(response, output)
    except Exception as exc:
        raise InstallationError(f"Unable to download Node Core package: {exc}") from exc
    return resolved_sha


def _safe_archive_member(member: tarfile.TarInfo, node_core_prefix: Path) -> Path:
    """Validate a remote tar member before extraction."""
    if member.issym() or member.islnk() or member.isdev() or member.isfifo():
        raise InstallationError(f"Unsupported archive member type: {member.name}")
    try:
        relative = Path(member.name).relative_to(node_core_prefix)
    except ValueError as exc:
        raise InstallationError(f"Archive member is outside Node Core: {member.name}") from exc
    if relative.is_absolute() or ".." in relative.parts:
        raise InstallationError(f"Unsafe archive path: {member.name}")
    return relative



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
                    relative = _safe_archive_member(member, node_core_prefix)
                    member.name = str(relative)
                    selected.append(member)
            package.extractall(extraction_root, members=selected)
    except (tarfile.TarError, OSError) as exc:
        raise InstallationError(f"Unable to extract Node Core package: {exc}") from exc

    extracted = extraction_root / "Bootstrap" / "Installer" / "bootstrap_node.py"
    if not extracted.is_file():
        raise InstallationError("Downloaded package is missing the canonical Node Core installer")
    shutil.copytree(extraction_root, staging, dirs_exist_ok=True)


def _termux_install_native_cryptography() -> None:
    """Install the Termux-native cryptography package instead of compiling it with pip."""
    pkg = shutil.which("pkg")
    if pkg is None:
        raise InstallationError("Termux package manager 'pkg' is required for the native cryptography dependency")

    completed = subprocess.run(
        [pkg, "install", "-y", "python-cryptography"],
        text=True, capture_output=True,
    )
    if completed.returncode != 0:
        if completed.stdout:
            print(completed.stdout, file=sys.stderr, end="")
        if completed.stderr:
            print(completed.stderr, file=sys.stderr, end="")
        raise InstallationError(
            "Unable to install the Termux-native python-cryptography package"
        )


def _verify_termux_cryptography(python_executable: Path) -> None:
    """Verify the native Termux package is visible and importable in the local venv."""
    probe = (
        "import importlib.metadata as m; "
        "v=m.version('cryptography'); "
        "import platform, ssl; "
        "from cryptography.hazmat.primitives.ciphers.aead import AESGCM; "
        "from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey; "
        "key=AESGCM.generate_key(bit_length=128); "
        "nonce=b'\\x00'*12; "
        "cipher=AESGCM(key); "
        "cipher.decrypt(nonce, cipher.encrypt(nonce, b'node-core-cryptography-check', None), None); "
        "Ed25519PrivateKey.generate(); "
        "print(f'{v}|{platform.machine()}|{ssl.OPENSSL_VERSION}')"
    )
    completed = subprocess.run(
        [str(python_executable), "-c", probe],
        text=True, capture_output=True,
    )
    if completed.returncode != 0:
        if completed.stderr:
            print(completed.stderr, file=sys.stderr, end="")
        raise InstallationError(
            "Termux cryptography dependency is unavailable, incompatible, or not importable"
        )


def prepare_python_environment(staging: Path, temp_root: Path) -> Path:
    requirements = staging / "Cryptography" / "requirements.txt"
    if not requirements.is_file():
        return Path(sys.executable)

    environment = temp_root / ".node-core-python"
    print("[2/5] Preparing Node Core environment...", flush=True)

    if detect_platform() == "TERMUX":
        _termux_install_native_cryptography()
        completed = subprocess.run(
            [sys.executable, "-m", "venv", "--system-site-packages", str(environment)],
            text=True, capture_output=True,
        )
    else:
        completed = subprocess.run(
            [sys.executable, "-m", "venv", str(environment)],
            text=True, capture_output=True,
        )

    if completed.returncode != 0:
        if completed.stderr:
            print(completed.stderr, file=sys.stderr, end="")
        raise InstallationError("Unable to create the Node Core Python environment")

    python_executable = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if not python_executable.is_file():
        raise InstallationError("Created Python environment is missing its interpreter")

    if detect_platform() == "TERMUX":
        _verify_termux_cryptography(python_executable)
        return python_executable

    completed = subprocess.run(
        [str(python_executable), "-m", "pip", "install", "--disable-pip-version-check", "-r", str(requirements)],
        text=True, capture_output=True,
    )
    if completed.returncode != 0:
        if completed.stderr:
            print(completed.stderr, file=sys.stderr, end="")
        raise InstallationError("Unable to install Node Core Python dependencies")
    return python_executable


def bootstrap(staging: Path, python_executable: Path) -> None:
    print("[3/5] Running Node Core Bootstrap...", flush=True)
    installer = staging / "Bootstrap" / "Installer" / "bootstrap_node.py"
    completed = subprocess.run(
        [str(python_executable), str(installer), str(staging)],
        text=True, capture_output=True,
    )
    if completed.returncode != 0:
        if completed.stderr:
            print(completed.stderr, file=sys.stderr, end="")
        raise InstallationError("Node Core bootstrap failed")


def verify(staging: Path, python_executable: Path) -> None:
    print("[4/5] Verifying Node Core...", flush=True)
    verifier = staging / "Bootstrap" / "Verification" / "bootstrap_verifier.py"
    completed = subprocess.run(
        [str(python_executable), str(verifier), str(staging)],
        text=True, capture_output=True,
    )
    if completed.returncode != 0:
        if completed.stderr:
            print(completed.stderr, file=sys.stderr, end="")
        raise InstallationError("Node Core verification failed")


def install(target: Path, source_ref: str = "main") -> None:
    platform_name = detect_platform()
    target = target.expanduser().resolve()

    if target.exists():
        manifest = target / "node-installation-manifest.json"
        if manifest.exists():
            raise InstallationError("An existing Node Core installation was detected; it will not be overwritten.")
        if any(target.iterdir()):
            raise InstallationError(
                "An existing or incomplete installation target was detected; "
                "it will not be overwritten. Remove it manually or choose another target."
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

            print("[1/5] Downloading Node Core...", flush=True)
            resolved_sha = download_archive(archive, source_ref)
            print(f"Source commit: {resolved_sha}", flush=True)
            extract_node_core(archive, extracted, staging)

        staging.rename(target)
        target_created = True
        python_executable = prepare_python_environment(target, target)
        bootstrap(target, python_executable)
        verify(target, python_executable)
        print("[5/5] Finalizing installation...", flush=True)
    except BaseException:
        # Installation is transactional: failures and user interruptions remove
        # any incomplete Node Core installation.
        if target_created and target.exists():
            shutil.rmtree(target, ignore_errors=True)
        if staging.exists():
            shutil.rmtree(staging, ignore_errors=True)
        raise

    print()
    print("Node Core installed successfully.")
    print()
    print(f"Status: NODE_CORE_READY")
    print("CPG Protocol: NOT INSTALLED")
    print("Protocol associations: []")


def print_menu() -> None:
    print()
    print("Trilema Project Presents")
    print("Node Core Network by LAEV")
    print("& The Chain Poker Genesis Protocol")
    print()
    print("[In Memory of Satoshi Nakamoto's Legacy,")
    print(" Trilema.com (MP), Hannah Wiggins (Hanbot),")
    print(" Lerry Alexander (LAEV) & The Bitcoin Network]")
    print()
    print("--------------------------------------------------")
    print()
    print("1. Install Node Core")
    print("2. Exit")
    print()


def confirm_install(target: Path) -> bool:
    print("Node Core Installation")
    print()
    print(f"Target: {target}")
    print("Source: Chain Poker Genesis by LAEV")
    print()
    answer = input("Proceed with installation? [Y/n]: ").strip().lower()
    return answer in ("", "y", "yes")


def interactive(source_ref: str, target: Path) -> int:
    while True:
        print_menu()
        choice = input("Select an option: ").strip()

        if choice == "2":
            print("Exiting.")
            return 0
        if choice != "1":
            print("Please select 1 or 2.")
            continue

        try:
            target = target.expanduser().resolve()
            if target.exists() and (target / "node-installation-manifest.json").exists():
                print()
                print("Existing Node Core installation detected.")
                print("The existing installation will not be overwritten.")
                print()
                input("Press Enter to return to the menu.")
                continue

            print()
            if not confirm_install(target):
                print("Installation cancelled.")
                continue
            print()
            install(target, source_ref)
            print()
            input("Press Enter to return to the menu.")
        except (InstallationError, EOFError, KeyboardInterrupt) as exc:
            if isinstance(exc, InstallationError):
                print()
                print("Installation failed.")
                print(f"Reason: {exc}")
            else:
                print()
                print("Exiting.")
                return 0
            print()
            input("Press Enter to return to the menu.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install Node Core directly from the Chain Poker Genesis repository."
    )
    parser.add_argument("--target", type=Path, help="installation directory")
    parser.add_argument("--ref", default="main", help="repository branch, tag, or commit SHA")
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="run the installation engine without the interactive CLI",
    )
    args = parser.parse_args()

    try:
        platform_name = detect_platform()
        target = args.target or default_target(platform_name)
        if not args.non_interactive and sys.stdin.isatty() and sys.stdout.isatty():
            return interactive(args.ref, target)
        install(target, args.ref)
    except InstallationError as exc:
        print(f"INSTALLATION FAILED: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
