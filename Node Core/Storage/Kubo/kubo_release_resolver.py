#!/usr/bin/env python3
"""Kubo release resolution for the Node Core managed provider.

Network retrieval is intentionally outside this module. The resolver consumes
official upstream release metadata supplied by a higher-level source adapter.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any


class KuboReleaseError(ValueError):
    pass


@dataclass(frozen=True)
class KuboRelease:
    version: str
    os: str
    architecture: str
    filename: str
    source_url: str
    expected_integrity: str
    resolved_at: str
    policy: str


_OS_ALIASES = {
    "linux": "linux",
    "linux2": "linux",
    "windows": "windows",
    "win32": "windows",
    "darwin": "macos",
}

_ARCH_ALIASES = {
    "x86_64": "amd64",
    "amd64": "amd64",
    "aarch64": "arm64",
    "arm64": "arm64",
}


class KuboReleaseResolver:
    """Select a compatible official Kubo release from upstream metadata."""

    def __init__(self, *, platform_os: str, architecture: str):
        os_name = _OS_ALIASES.get(platform_os.lower(), platform_os.lower())
        arch_name = _ARCH_ALIASES.get(architecture.lower(), architecture.lower())
        if os_name not in {"linux", "windows"}:
            raise KuboReleaseError(f"unsupported platform: {platform_os}")
        if arch_name not in {"amd64", "arm64"}:
            raise KuboReleaseError(f"unsupported architecture: {architecture}")
        self.platform_os = os_name
        self.architecture = arch_name

    def resolve(
        self,
        releases: list[dict[str, Any]],
        *,
        policy: str = "LATEST_COMPATIBLE_STABLE",
        exact_version: str | None = None,
    ) -> KuboRelease:
        if not releases:
            raise KuboReleaseError("release metadata is empty")
        if policy not in {"LATEST_COMPATIBLE_STABLE", "EXACT_VERSION"}:
            raise KuboReleaseError(f"unsupported release policy: {policy}")

        candidates = []
        for item in releases:
            self._validate_record(item)
            if item["os"] != self.platform_os or item["architecture"] != self.architecture:
                continue
            if item.get("channel", "stable") != "stable":
                continue
            if not item.get("official", True):
                continue
            if not item.get("expected_integrity"):
                continue
            if policy == "EXACT_VERSION" and item["version"] != exact_version:
                continue
            candidates.append(item)

        if not candidates:
            raise KuboReleaseError("no compatible verified release candidate")

        selected = max(candidates, key=lambda x: self._version_key(x["version"]))
        resolved_at = datetime.now(timezone.utc).isoformat()
        return KuboRelease(
            version=selected["version"],
            os=self.platform_os,
            architecture=self.architecture,
            filename=selected["filename"],
            source_url=selected["source_url"],
            expected_integrity=selected["expected_integrity"],
            resolved_at=resolved_at,
            policy=policy,
        )

    @staticmethod
    def _validate_record(item: dict[str, Any]) -> None:
        required = ("version", "os", "architecture", "filename", "source_url", "expected_integrity")
        missing = [field for field in required if not item.get(field)]
        if missing:
            raise KuboReleaseError(f"release metadata missing: {', '.join(missing)}")

    @staticmethod
    def _version_key(version: str) -> tuple:
        value = version.strip().lstrip("v")
        if "-" in value:
            value = value.split("-", 1)[0]
        parts = value.split(".")
        if not all(part.isdigit() for part in parts):
            raise KuboReleaseError(f"invalid stable version: {version}")
        return tuple(int(part) for part in parts)


def release_record(release: KuboRelease) -> dict[str, Any]:
    return asdict(release)
