#!/usr/bin/env python3
"""Protocol-neutral dual-storage bootstrap for the Full Node Core.

This module does not install Kubo. It verifies/initializes the protocol-controlled
logical namespace through a Kubo HTTP API endpoint when one is explicitly supplied.
The CPG protocol remains uninstalled and unassociated.
"""

from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

STORAGE_STRUCTURE_VERSION = "0.1.0"
REQUIRED_PATHS = (
    "node-storage",
    "node-storage/identity",
    "node-storage/cryptography",
    "node-storage/configuration",
    "node-storage/state",
    "node-storage/records",
    "node-storage/recovery",
    "node-storage/protocol",
)


class BootstrapError(RuntimeError):
    """Raised when the dual-storage bootstrap contract cannot be satisfied."""


@dataclass(frozen=True)
class BootstrapResult:
    local_ready: bool
    ipfs_ready: bool
    synchronization_state: str


def initialize_local(root: Path) -> None:
    """Create and verify the canonical logical local namespace."""
    for relative in REQUIRED_PATHS:
        (root / relative).mkdir(parents=True, exist_ok=True)
    manifest = {
        "storage_structure_version": STORAGE_STRUCTURE_VERSION,
        "root": "node-storage",
        "required_paths": list(REQUIRED_PATHS),
    }
    path = root / "node-storage/state/storage-manifest.json"
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    verify_local(root)


def verify_local(root: Path) -> None:
    for relative in REQUIRED_PATHS:
        if not (root / relative).is_dir():
            raise BootstrapError(f"local required path missing: {relative}")
    manifest_path = root / "node-storage/state/storage-manifest.json"
    if not manifest_path.is_file():
        raise BootstrapError("local storage manifest missing")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("storage_structure_version") != STORAGE_STRUCTURE_VERSION:
        raise BootstrapError("local storage structure version mismatch")
    if manifest.get("required_paths") != list(REQUIRED_PATHS):
        raise BootstrapError("local canonical path set mismatch")


class KuboMFSAdapter:
    """Minimal adapter for Kubo's MFS API; Kubo itself is never installed here."""

    def __init__(self, api_base: str, timeout: float = 5.0) -> None:
        self.api_base = api_base.rstrip("/")
        self.timeout = timeout

    def _post(self, endpoint: str, params: dict[str, str]) -> None:
        query = urllib.parse.urlencode(params)
        request = urllib.request.Request(
            f"{self.api_base}/api/v0/{endpoint}?{query}",
            data=b"",
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                if response.status >= 300:
                    raise BootstrapError(f"Kubo API returned HTTP {response.status}")
        except (urllib.error.URLError, TimeoutError) as exc:
            raise BootstrapError(f"Kubo API unavailable: {exc}") from exc

    def initialize_namespace(self) -> None:
        for relative in REQUIRED_PATHS:
            path = "/" + relative
            self._post("files/mkdir", {"arg": path, "parents": "true"})

    def verify_namespace(self) -> None:
        # MFS stat is used as the structural existence check for each canonical path.
        for relative in REQUIRED_PATHS:
            path = "/" + relative
            query = urllib.parse.urlencode({"arg": path})
            request = urllib.request.Request(
                f"{self.api_base}/api/v0/files/stat?{query}", method="POST", data=b""
            )
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    if response.status >= 300:
                        raise BootstrapError(f"Kubo stat returned HTTP {response.status}")
            except (urllib.error.URLError, TimeoutError) as exc:
                raise BootstrapError(f"Kubo namespace verification failed: {exc}") from exc


def bootstrap(root: Path, kubo_api: str | None = None) -> BootstrapResult:
    """Bootstrap local storage and, when configured, the Kubo logical namespace."""
    root = root.resolve()
    root.mkdir(parents=True, exist_ok=True)
    initialize_local(root)

    if kubo_api is None:
        return BootstrapResult(True, False, "NOT_EVALUATED")

    adapter = KuboMFSAdapter(kubo_api)
    adapter.initialize_namespace()
    adapter.verify_namespace()
    return BootstrapResult(True, True, "STRUCTURE_VERIFIED")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target_directory")
    parser.add_argument("--kubo-api", help="Kubo API base URL; Kubo is not installed by this command")
    args = parser.parse_args()
    try:
        result = bootstrap(Path(args.target_directory), args.kubo_api)
    except (BootstrapError, OSError, json.JSONDecodeError) as exc:
        print("status = FAILED")
        print(f"reason = {exc}")
        return 1
    print("status = BOOTSTRAP_READY")
    print(f"local_storage = {result.local_ready}")
    print(f"ipfs_storage = {result.ipfs_ready}")
    print(f"synchronization = {result.synchronization_state}")
    print("cpg_protocol = NOT_INSTALLED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
