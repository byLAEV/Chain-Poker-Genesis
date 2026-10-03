"""Node Core recovery state and records."""
from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass
class RecoveryRecord:
    operation: str
    status: str
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: str | None = None
    details: dict = field(default_factory=dict)
