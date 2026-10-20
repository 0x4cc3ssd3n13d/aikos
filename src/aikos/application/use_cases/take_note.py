from aikos.application.ports.clock import Clock
from aikos.application.ports.note_repository import NoteRepository
from aikos.domain.note import Note


class TakeNote:
    def __init__(self, notes: NoteRepository, clock: Clock) -> None:
        self._notes = notes
        self._clock = clock

    def execute(self, text: str) -> Note:
        note = Note(text=text.strip(), created_at=self._clock.now())
        self._notes.save(note)
        return note
