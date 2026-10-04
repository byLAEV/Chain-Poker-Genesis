#!/usr/bin/env python3
"""Atomic persistent state for the managed Kubo provider."""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any


class KuboStateError(ValueError):
    pass


class KuboProviderState:
    REQUIRED = {
        "provider_id", "provider", "state_version", "installation_id",
        "lifecycle_state", "health_state", "synchronization_state",
        "kubo_version", "platform", "architecture", "release_source",
        "release_metadata_source", "expected_integrity", "observed_integrity",
        "executable_path", "repository_path", "ipfs_path",
        "installed_at", "last_transition_at", "last_health_check_at",
    }

    def __init__(self, path: str | Path):
        self.path = Path(path).resolve()

    def write(self, record: dict[str, Any]) -> None:
        missing = self.REQUIRED - set(record)
        if missing:
            raise KuboStateError("missing state fields: " + ", ".join(sorted(missing)))
        if record["ipfs_path"] != str(Path(record["repository_path"]).resolve()):
            raise KuboStateError("ipfs_path must equal normalized repository_path")
        if record["lifecycle_state"] == "READY":
            if record["health_state"] != "HEALTHY":
                raise KuboStateError("READY requires HEALTHY state")
            if record["synchronization_state"] != "SYNCHRONIZED":
                raise KuboStateError("READY requires synchronized state")

        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, temporary = tempfile.mkstemp(prefix=".kubo-state-", dir=self.path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(record, handle, sort_keys=True, indent=2)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, self.path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)

    def read(self) -> dict[str, Any]:
        if not self.path.is_file():
            raise KuboStateError("provider state does not exist")
        with self.path.open("r", encoding="utf-8") as handle:
            record = json.load(handle)
        missing = self.REQUIRED - set(record)
        if missing:
            raise KuboStateError("provider state is incomplete")
        return record
