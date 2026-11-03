from collections.abc import Sequence
from datetime import datetime, timedelta, timezone

import pytest

from aikos.application.ports.language_model import ModelReply, ToolSpec
from aikos.domain.conversation import Message
from aikos.domain.note import Note

BANGKOK = timezone(timedelta(hours=7))


class FakeLanguageModel:
    """Returns `answers` in order (the last one repeats); a str becomes a text reply."""

    def __init__(self, answers: list[str | ModelReply] | None = None) -> None:
        self.answers = answers or ["OK"]
        self.calls: list[list[Message]] = []
        self.tools_seen: list[tuple[ToolSpec, ...]] = []

    def reply(self, messages: Sequence[Message], tools: Sequence[ToolSpec] = ()) -> ModelReply:
        self.calls.append(list(messages))
        self.tools_seen.append(tuple(tools))
        answer = self.answers[min(len(self.calls), len(self.answers)) - 1]
        return answer if isinstance(answer, ModelReply) else ModelReply(text=answer)


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
