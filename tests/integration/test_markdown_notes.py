from datetime import datetime, timedelta

from aikos.domain.note import Note
from aikos.infrastructure.storage.markdown_notes import MarkdownNoteRepository
from tests.conftest import BANGKOK


def test_round_trip_keeps_order_time_zone_and_thai(tmp_path):
    repo = MarkdownNoteRepository(tmp_path / "notes")
    first = Note("ซื้อนม", datetime(2026, 10, 15, 8, 0, tzinfo=BANGKOK))
    second = Note("call Ann\nabout the invoice", datetime(2026, 10, 16, 9, 30, tzinfo=BANGKOK))
    repo.save(first)
    repo.save(second)

    recent = repo.list_recent()
    assert [n.text for n in recent] == ["call Ann about the invoice", "ซื้อนม"]
    assert recent[0].created_at.utcoffset() == timedelta(hours=7)
    assert repo.list_recent(limit=1) == [recent[0]]
    assert (tmp_path / "notes" / "2026-10-16.md").read_text(encoding="utf-8").startswith("- 2026-10-16T09:30:00+07:00 | ")


def test_empty_folder_has_no_notes(tmp_path):
    assert MarkdownNoteRepository(tmp_path / "missing").list_recent() == []
