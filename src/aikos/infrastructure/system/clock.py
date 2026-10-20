from datetime import datetime


class SystemClock:
    """Clock port using the PC's local time zone."""

    def now(self) -> datetime:
        return datetime.now().astimezone()
