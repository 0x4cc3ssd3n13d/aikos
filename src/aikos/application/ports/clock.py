from datetime import datetime
from typing import Protocol


class Clock(Protocol):
    """Current time with a time zone. A port so tests can freeze time."""

    def now(self) -> datetime: ...
