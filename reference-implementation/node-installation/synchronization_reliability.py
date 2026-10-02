#!/usr/bin/env python3
"""Protocol-neutral retry, backoff, and circuit-breaker controls.

This layer governs synchronization attempts only. It does not define
replication, peer networking, conflict resolution, or storage policy.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable, TypeVar

T = TypeVar("T")


class SynchronizationCircuitOpenError(RuntimeError):
    """Raised when the circuit refuses a new synchronization attempt."""


@dataclass
class RetryBackoffCircuitBreaker:
    max_retries: int = 2
    base_delay: float = 1.0
    backoff_multiplier: float = 2.0
    failure_threshold: int = 3
    recovery_timeout: float = 30.0
    sleep: Callable[[float], None] = time.sleep
    clock: Callable[[], float] = time.monotonic

    def __post_init__(self) -> None:
        if self.max_retries < 0:
            raise ValueError("max_retries must be non-negative")
        if self.base_delay < 0 or self.backoff_multiplier < 1:
            raise ValueError("invalid backoff configuration")
        if self.failure_threshold < 1 or self.recovery_timeout < 0:
            raise ValueError("invalid circuit-breaker configuration")
        self._consecutive_failures = 0
        self._opened_at: float | None = None

    @property
    def state(self) -> str:
        if self._opened_at is None:
            return "CLOSED"
        if self.clock() - self._opened_at >= self.recovery_timeout:
            return "HALF_OPEN"
        return "OPEN"

    def _allow(self) -> None:
        if self.state == "OPEN":
            raise SynchronizationCircuitOpenError("synchronization circuit is open")

    def execute(self, operation: Callable[[], T]) -> T:
        self._allow()
        attempts = self.max_retries + 1
        last_error: Exception | None = None
        for attempt in range(attempts):
            try:
                result = operation()
            except Exception as exc:
                last_error = exc
                self._consecutive_failures += 1
                if self._consecutive_failures >= self.failure_threshold:
                    self._opened_at = self.clock()
                    break
                if attempt < attempts - 1:
                    self.sleep(self.base_delay * (self.backoff_multiplier ** attempt))
            else:
                self._consecutive_failures = 0
                self._opened_at = None
                return result
        assert last_error is not None
        raise last_error
