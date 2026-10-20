import pytest

from aikos.domain.conversation import Conversation, Message, Role
from aikos.domain.errors import InvalidInput


def test_keeps_only_recent_turns():
    conversation = Conversation(max_turns=2)
    for i in range(3):
        conversation.add(Message(Role.USER, f"question {i}"))
        conversation.add(Message(Role.ASSISTANT, f"answer {i}"))
    assert [m.content for m in conversation.recent()] == ["question 1", "answer 1", "question 2", "answer 2"]


def test_rejects_empty_message():
    with pytest.raises(InvalidInput):
        Message(Role.USER, "   ")


def test_system_messages_are_not_history():
    with pytest.raises(InvalidInput):
        Conversation().add(Message(Role.SYSTEM, "rules"))
