from dataclasses import dataclass
from datetime import datetime

from aikos.domain.errors import InvalidInput


@dataclass(frozen=True)
class Reminder:
    """Used from Phase 4 (secretary tools)."""

    text: str
    due_at: datetime
    done: bool = False

    def __post_init__(self) -> None:
        if not self.text.strip():
            raise InvalidInput("A reminder needs some text.")
        if self.due_at.tzinfo is None:
            raise InvalidInput("Reminder times must include a time zone.")

    def is_due(self, now: datetime) -> bool:
        return not self.done and now >= self.due_at
