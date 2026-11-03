from aikos.application.ports.note_repository import NoteRepository
from aikos.domain.note import Note


class ListNotes:
    def __init__(self, notes: NoteRepository) -> None:
        self._notes = notes

    def execute(self, limit: int = 10) -> list[Note]:
        return self._notes.list_recent(limit)
