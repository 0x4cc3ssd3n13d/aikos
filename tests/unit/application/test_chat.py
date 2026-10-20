import pytest

from aikos.application.use_cases.chat import Chat
from aikos.domain.conversation import Conversation, Role
from aikos.domain.errors import InvalidInput


def test_sends_system_prompt_and_history(model):
    model.answers = ["Hello!", "Sure."]
    chat = Chat(model, Conversation(), "You are AIKOs.")
    assert chat.execute("hi") == "Hello!"
    assert chat.execute(" remind me later ") == "Sure."

    last_call = model.calls[-1]
    assert last_call[0].role is Role.SYSTEM
    assert [m.content for m in last_call[1:]] == ["hi", "Hello!", "remind me later"]


def test_empty_input_is_rejected_without_calling_the_model(model):
    with pytest.raises(InvalidInput):
        Chat(model, Conversation(), "rules").execute("  ")
    assert model.calls == []
