from datetime import datetime, timedelta

import pytest

from aikos.domain.errors import InvalidInput
from aikos.domain.note import Note
from aikos.domain.reminder import Reminder
from tests.conftest import BANGKOK


def test_note_needs_text_and_time_zone():
    with pytest.raises(InvalidInput):
        Note("", datetime(2026, 10, 16, tzinfo=BANGKOK))
    with pytest.raises(InvalidInput):
        Note("call Ann", datetime(2026, 10, 16))


def test_reminder_is_due_only_after_its_time_and_until_done():
    due = datetime(2026, 10, 16, 15, 0, tzinfo=BANGKOK)
    reminder = Reminder("call Ann", due)
    assert not reminder.is_due(due - timedelta(minutes=1))
    assert reminder.is_due(due)
    assert not Reminder("call Ann", due, done=True).is_due(due)
