#!/usr/bin/env python3
"""Canonical path and IPFS_PATH handling for the managed Kubo provider."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


class KuboPathError(ValueError):
    pass


@dataclass(frozen=True)
class KuboPaths:
    node_root: Path
    release_root: Path
    active_root: Path
    repository: Path
    runtime: Path
    logs: Path
    state: Path
    synchronization: Path

    @property
    def ipfs_path(self) -> Path:
        return self.repository


class KuboPathManager:
    def __init__(self, node_core_root: str | Path):
        root = Path(node_core_root).expanduser()
        if not root.is_absolute():
            root = root.resolve()
        self.node_root = root.resolve()

    def paths(self, version: str) -> KuboPaths:
        if not version or "/" in version or chr(92) in version or ".." in version:
            raise KuboPathError("invalid Kubo version")
        external = self.node_root / "External Providers" / "Kubo"
        provider = self.node_root / "node-storage" / "providers" / "kubo"
        return KuboPaths(
            node_root=self.node_root,
            release_root=(external / version).resolve(),
            active_root=(external / "active").resolve(),
            repository=(provider / "repository").resolve(),
            runtime=(provider / "runtime").resolve(),
            logs=(provider / "logs").resolve(),
            state=(provider / "state").resolve(),
            synchronization=(provider / "synchronization").resolve(),
        )

    def validate(self, paths: KuboPaths) -> None:
        root = self.node_root
        for candidate in (
            paths.release_root,
            paths.active_root,
            paths.repository,
            paths.runtime,
            paths.logs,
            paths.state,
            paths.synchronization,
        ):
            try:
                candidate.relative_to(root)
            except ValueError as exc:
                raise KuboPathError("managed Kubo path escapes Node Core root") from exc
        if not paths.ipfs_path.is_absolute():
            raise KuboPathError("IPFS_PATH must be absolute")

    def environment(self, paths: KuboPaths) -> dict[str, str]:
        self.validate(paths)
        return {"IPFS_PATH": str(paths.ipfs_path)}
