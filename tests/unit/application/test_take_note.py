from aikos.application.use_cases.take_note import TakeNote


def test_saves_note_with_current_time(notes, clock):
    note = TakeNote(notes, clock).execute("  ซื้อนม  ")
    assert note.text == "ซื้อนม"
    assert note.created_at == clock.at
    assert notes.saved == [note]
