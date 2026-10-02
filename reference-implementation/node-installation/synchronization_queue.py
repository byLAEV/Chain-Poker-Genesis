#!/usr/bin/env python3
"""Durable local synchronization queue for the Node Core.

This queue persists synchronization intent before remote work begins and
recovers interrupted entries after a process restart. It does not implement
retry policy, backoff, circuit breakers, replication, or peer networking.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

QUEUE_PATH = "node-storage/state/synchronization-queue.json"


class SynchronizationQueueError(RuntimeError):
    pass


class DurableSynchronizationQueue:
    """Persist pending synchronization work in Node Core local storage."""

    def __init__(self, node_root: Path) -> None:
        self.node_root = Path(node_root).resolve()
        self.path = self.node_root / QUEUE_PATH
        if not self.path.parent.is_dir():
            raise SynchronizationQueueError("queue storage does not exist")
        self.entries = self._load()
        self._recover_processing_entries()

    def _load(self) -> dict[str, dict[str, Any]]:
        if not self.path.exists():
            return {}
        try:
            value = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise SynchronizationQueueError("invalid synchronization queue") from exc
        if not isinstance(value, dict):
            raise SynchronizationQueueError("synchronization queue must be an object")
        return value

    def _persist(self) -> None:
        payload = json.dumps(self.entries, indent=2, sort_keys=True) + "\n"
        temporary = self.path.with_name(self.path.name + ".tmp")
        try:
            temporary.write_text(payload, encoding="utf-8")
            with temporary.open("rb") as handle:
                os.fsync(handle.fileno())
            os.replace(temporary, self.path)
        except OSError as exc:
            try:
                temporary.unlink()
            except OSError:
                pass
            raise SynchronizationQueueError("unable to persist synchronization queue") from exc

    def _recover_processing_entries(self) -> None:
        changed = False
        for entry in self.entries.values():
            if entry.get("status") == "PROCESSING":
                entry["status"] = "PENDING"
                changed = True
        if changed:
            self._persist()

    def enqueue(self, object_id: str, *, content_hash: str, storage_version: str) -> dict[str, Any]:
        if not object_id:
            raise SynchronizationQueueError("object_id is required")
        existing = self.entries.get(object_id)
        if existing is not None and existing.get("status") in {"PENDING", "PROCESSING"}:
            return dict(existing)
        entry = {
            "object_id": object_id,
            "content_hash": content_hash,
            "storage_version": storage_version,
            "status": "PENDING",
        }
        self.entries[object_id] = entry
        self._persist()
        return dict(entry)

    def mark_processing(self, object_id: str) -> dict[str, Any]:
        entry = self._get(object_id)
        if entry["status"] != "PENDING":
            raise SynchronizationQueueError("queue entry is not pending")
        entry["status"] = "PROCESSING"
        self._persist()
        return dict(entry)

    def mark_completed(self, object_id: str) -> dict[str, Any]:
        entry = self._get(object_id)
        if entry["status"] != "PROCESSING":
            raise SynchronizationQueueError("queue entry is not processing")
        entry["status"] = "COMPLETED"
        self._persist()
        return dict(entry)

    def pending(self) -> list[dict[str, Any]]:
        return [
            dict(self.entries[object_id])
            for object_id in sorted(self.entries)
            if self.entries[object_id].get("status") == "PENDING"
        ]

    def _get(self, object_id: str) -> dict[str, Any]:
        try:
            return self.entries[object_id]
        except KeyError as exc:
            raise SynchronizationQueueError("object is not queued") from exc
