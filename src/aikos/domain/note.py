from dataclasses import dataclass
from datetime import datetime

from aikos.domain.errors import InvalidInput


@dataclass(frozen=True)
class Note:
    text: str
    created_at: datetime

    def __post_init__(self) -> None:
        if not self.text.strip():
            raise InvalidInput("A note cannot be empty.")
        if self.created_at.tzinfo is None:
            raise InvalidInput("Note times must include a time zone.")
