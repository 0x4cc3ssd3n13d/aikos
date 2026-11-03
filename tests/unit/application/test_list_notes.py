from aikos.application.use_cases.list_notes import ListNotes
from aikos.application.use_cases.take_note import TakeNote


def test_lists_newest_first_with_limit(notes, clock):
    for text in ("one", "two", "three"):
        TakeNote(notes, clock).execute(text)
    assert [n.text for n in ListNotes(notes).execute(limit=2)] == ["three", "two"]
