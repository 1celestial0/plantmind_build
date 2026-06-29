"""Agent base types. All agents return AgentResult; none are autonomous."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class AgentResult:
    agent: str
    asset_id: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    output: dict[str, Any] = field(default_factory=dict)
    model_used: str | None = None
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None
