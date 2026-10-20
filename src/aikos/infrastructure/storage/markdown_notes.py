from datetime import datetime
from pathlib import Path

from aikos.domain.note import Note

_SEPARATOR = " | "


class MarkdownNoteRepository:
    """NoteRepository port that keeps one Markdown file per day, e.g. data/notes/2026-10-16.md.

    Each line is "- <ISO time> | <text>", so the files stay readable in any editor.
    """

    def __init__(self, folder: Path) -> None:
        self._folder = folder

    def save(self, note: Note) -> None:
        self._folder.mkdir(parents=True, exist_ok=True)
        text = " ".join(note.text.split())  # one note per line
        path = self._folder / f"{note.created_at:%Y-%m-%d}.md"
        with path.open("a", encoding="utf-8") as file:
            file.write(f"- {note.created_at.isoformat(timespec='seconds')}{_SEPARATOR}{text}\n")

    def list_recent(self, limit: int = 10) -> list[Note]:
        if not self._folder.exists():
            return []
        notes: list[Note] = []
        for path in sorted(self._folder.glob("*.md"), reverse=True):
            for line in reversed(path.read_text(encoding="utf-8").splitlines()):
                if not line.startswith("- ") or _SEPARATOR not in line:
                    continue
                stamp, text = line[2:].split(_SEPARATOR, 1)
                notes.append(Note(text=text, created_at=datetime.fromisoformat(stamp)))
                if len(notes) == limit:
                    return notes
        return notes
