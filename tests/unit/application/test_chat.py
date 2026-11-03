import pytest

from aikos.application.ports.language_model import ModelReply, ToolCall
from aikos.application.tools import NOTE_TOOLS
from aikos.application.use_cases.chat import Chat
from aikos.domain.conversation import Conversation, Role
from aikos.domain.errors import InvalidInput


def test_sends_system_prompt_and_history(model):
    model.answers = ["Hello!", "Sure."]
    chat = Chat(model, Conversation(), "You are AIKOs.")
    assert chat.execute("hi").text == "Hello!"
    assert chat.execute(" remind me later ").text == "Sure."

    last_call = model.calls[-1]
    assert last_call[0].role is Role.SYSTEM
    assert [m.content for m in last_call[1:]] == ["hi", "Hello!", "remind me later"]


def test_empty_input_is_rejected_without_calling_the_model(model):
    with pytest.raises(InvalidInput):
        Chat(model, Conversation(), "rules").execute("  ")
    assert model.calls == []


def test_offers_tools_and_returns_the_tool_call(model):
    call = ToolCall("take_note", {"text": "ซื้อนม"})
    model.answers = [ModelReply(tool_call=call), "You saved: ซื้อนม"]
    chat = Chat(model, Conversation(), "rules", tools=NOTE_TOOLS)

    assert chat.execute("จดไว้ว่าซื้อนม").tool_call == call
    assert model.tools_seen[0] == NOTE_TOOLS

    chat.remember("Saved note at 09:30: ซื้อนม")
    chat.execute("what did you save?")
    assert [m.content for m in model.calls[-1][1:]] == [
        "จดไว้ว่าซื้อนม",
        "Saved note at 09:30: ซื้อนม",
        "what did you save?",
    ]
