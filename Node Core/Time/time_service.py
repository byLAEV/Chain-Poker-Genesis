"""Protocol-neutral Node Core time reference service."""
from __future__ import annotations
import hashlib
import json
import time
from dataclasses import dataclass

@dataclass(frozen=True)
class TimeRecord:
    sequence: int
    timestamp: int
    previous_hash: str | None
    record_hash: str

class TimeService:
    def __init__(self) -> None:
        self.sequence = 0
        self.previous_hash: str | None = None

    def now(self) -> int:
        return int(time.time())

    def timestamp(self, value: int | None = None) -> int:
        ts = self.now() if value is None else value
        self.validate_timestamp(ts)
        return ts

    @staticmethod
    def validate_timestamp(timestamp: int) -> bool:
        if not isinstance(timestamp, int) or isinstance(timestamp, bool):
            raise ValueError("timestamp must be an integer Unix-second value")
        if timestamp < 0:
            raise ValueError("timestamp must not be negative")
        return True

    def logical_tick(self) -> int:
        value = self.sequence
        self.sequence += 1
        return value

    def record(self, timestamp: int | None = None) -> TimeRecord:
        ts = self.timestamp(timestamp)
        sequence = self.sequence
        previous = self.previous_hash
        body = {
            "sequence": sequence,
            "timestamp": ts,
            "previous_hash": previous,
        }
        digest = hashlib.sha256(
            json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        self.sequence += 1
        self.previous_hash = digest
        return TimeRecord(sequence, ts, previous, digest)

    @staticmethod
    def verify_record(record: TimeRecord, expected_previous_hash: str | None = None) -> bool:
        if not isinstance(record, TimeRecord):
            raise ValueError("record must be a TimeRecord")
        if record.previous_hash != expected_previous_hash:
            return False
        body = {
            "sequence": record.sequence,
            "timestamp": record.timestamp,
            "previous_hash": record.previous_hash,
        }
        digest = hashlib.sha256(
            json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        return digest == record.record_hash

    def reference_status(self) -> dict:
        return {
            "clock": "system",
            "trust": "LOCAL_OBSERVATION",
            "consensus_authority": False,
        }
