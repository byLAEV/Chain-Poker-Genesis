#!/usr/bin/env python3
"""Initialize and verify a managed Kubo repository without starting the daemon."""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


class KuboRepositoryError(RuntimeError):
    pass


class KuboRepositoryInitializer:
    """Owns repository initialization only; process lifecycle is separate."""

    def initialize(self, *, executable: str | Path, paths, version: str) -> dict:
        executable = Path(executable).resolve()
        if not executable.is_file():
            raise KuboRepositoryError("Kubo executable does not exist")
        if not os.access(executable, os.X_OK):
            raise KuboRepositoryError("Kubo executable is not executable")

        paths.repository.mkdir(parents=True, exist_ok=True)
        config = paths.repository / "config"

        if config.exists():
            raise KuboRepositoryError("repository already initialized")

        env = os.environ.copy()
        env["IPFS_PATH"] = str(paths.ipfs_path)

        try:
            completed = subprocess.run(
                [str(executable), "init"],
                env=env,
                capture_output=True,
                text=True,
                timeout=120,
                check=False,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            raise KuboRepositoryError("Kubo initialization process failed") from exc

        if completed.returncode != 0:
            raise KuboRepositoryError(
                f"Kubo init failed with exit code {completed.returncode}"
            )

        self._verify_repository(paths.repository, version)

        return {
            "repository_path": str(paths.repository),
            "ipfs_path": str(paths.ipfs_path),
            "config_path": str(config),
            "version": version,
            "repository_initialized": True,
            "node_core_identity": "UNRELATED",
        }

    @staticmethod
    def _verify_repository(repository: Path, version: str) -> None:
        config = repository / "config"
        if not config.is_file():
            raise KuboRepositoryError("Kubo init did not create repository config")

        try:
            data = json.loads(config.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise KuboRepositoryError("Kubo repository config is invalid") from exc

        if not isinstance(data, dict):
            raise KuboRepositoryError("Kubo repository config is not an object")
        identity = data.get("Identity")
        if not isinstance(identity, dict) or not identity.get("PeerID"):
            raise KuboRepositoryError("Kubo repository has no PeerID")

        repo_version = repository / "version"
        if not repo_version.is_file():
            raise KuboRepositoryError("Kubo repository version marker is missing")

        observed = repo_version.read_text(encoding="utf-8").strip()
        if not observed:
            raise KuboRepositoryError("Kubo repository version marker is empty")
