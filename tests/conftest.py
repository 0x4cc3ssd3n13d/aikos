from collections.abc import Sequence
from datetime import datetime, timedelta, timezone

import pytest

from aikos.domain.conversation import Message
from aikos.domain.note import Note

BANGKOK = timezone(timedelta(hours=7))


class FakeLanguageModel:
    def __init__(self, answers: list[str] | None = None) -> None:
        self.answers = answers or ["OK"]
        self.calls: list[list[Message]] = []

    def reply(self, messages: Sequence[Message]) -> str:
        self.calls.append(list(messages))
        return self.answers[min(len(self.calls), len(self.answers)) - 1]


class FixedClock:
    def __init__(self, at: datetime) -> None:
        self.at = at

    def now(self) -> datetime:
        return self.at


class InMemoryNotes:
    def __init__(self) -> None:
        self.saved: list[Note] = []

    def save(self, note: Note) -> None:
        self.saved.append(note)

    def list_recent(self, limit: int = 10) -> list[Note]:
        return list(reversed(self.saved))[:limit]


@pytest.fixture
def model() -> FakeLanguageModel:
    return FakeLanguageModel()


@pytest.fixture
def clock() -> FixedClock:
    return FixedClock(datetime(2026, 10, 16, 9, 30, tzinfo=BANGKOK))


@pytest.fixture
def notes() -> InMemoryNotes:
    return InMemoryNotes()
