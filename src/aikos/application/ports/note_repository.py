from typing import Protocol

from aikos.domain.note import Note


class NoteRepository(Protocol):
    def save(self, note: Note) -> None: ...

    def list_recent(self, limit: int = 10) -> list[Note]: ...
