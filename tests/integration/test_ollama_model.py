import os

import pytest

from aikos.application.ports.language_model import ToolCall
from aikos.application.tools import NOTE_TOOLS
from aikos.domain.conversation import Message, Role
from aikos.infrastructure.llm.ollama_model import OllamaLanguageModel


class FakeClient:
    def __init__(self, message: dict) -> None:
        self.message = message
        self.sent: dict = {}

    def chat(self, **request):
        self.sent = request
        return {"message": self.message}


def test_maps_messages_turns_thinking_off_and_strips_reasoning():
    client = FakeClient({"content": "<think>\nhmm\n</think>\n\nHello!"})
    model = OllamaLanguageModel("qwen3:1.7b", "http://x", client=client)
    reply = model.reply([Message(Role.SYSTEM, "rules"), Message(Role.USER, "hi")])

    assert reply.text == "Hello!" and reply.tool_call is None
    assert client.sent["model"] == "qwen3:1.7b"
    assert client.sent["think"] is False
    assert "tools" not in client.sent
    assert client.sent["messages"] == [
        {"role": "system", "content": "rules"},
        {"role": "user", "content": "hi"},
    ]


def test_thinking_can_be_left_on():
    client = FakeClient({"content": "Hi"})
    OllamaLanguageModel("m", "h", no_think=False, client=client).reply([Message(Role.USER, "hi")])
    assert "think" not in client.sent


def test_sends_tools_and_reads_the_tool_call():
    client = FakeClient({"content": "", "tool_calls": [{"function": {"name": "take_note", "arguments": {"text": "ซื้อนม"}}}]})
    reply = OllamaLanguageModel("m", "h", client=client).reply([Message(Role.USER, "จดไว้ว่าซื้อนม")], NOTE_TOOLS)

    assert reply.tool_call == ToolCall("take_note", {"text": "ซื้อนม"})
    assert [t["function"]["name"] for t in client.sent["tools"]] == ["take_note", "list_notes"]
    assert client.sent["tools"][0]["function"]["parameters"]["required"] == ["text"]


@pytest.mark.live
@pytest.mark.skipif(os.environ.get("AIKOS_LIVE") != "1", reason="set AIKOS_LIVE=1 with Ollama running")
def test_real_ollama_answers_and_picks_a_tool():
    model = OllamaLanguageModel(os.environ.get("AIKOS_MODEL", "qwen3:1.7b"), "http://127.0.0.1:11434")
    assert model.reply([Message(Role.USER, "Reply with one word: ready")]).text
    reply = model.reply([Message(Role.USER, "จดไว้หน่อยว่าพรุ่งนี้ต้องซื้อนม")], NOTE_TOOLS)
    assert reply.tool_call and reply.tool_call.name == "take_note"
