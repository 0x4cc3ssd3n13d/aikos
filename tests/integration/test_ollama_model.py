import os

import pytest

from aikos.domain.conversation import Message, Role
from aikos.infrastructure.llm.ollama_model import OllamaLanguageModel


class FakeClient:
    def __init__(self, content: str) -> None:
        self.content = content
        self.sent: dict = {}

    def chat(self, model, messages):
        self.sent = {"model": model, "messages": messages}
        return {"message": {"content": self.content}}


def test_maps_messages_adds_no_think_and_strips_reasoning():
    client = FakeClient("<think>\nhmm\n</think>\n\nHello!")
    model = OllamaLanguageModel("qwen3:1.7b", "http://x", client=client)
    answer = model.reply([Message(Role.SYSTEM, "rules"), Message(Role.USER, "hi")])

    assert answer == "Hello!"
    assert client.sent["model"] == "qwen3:1.7b"
    assert client.sent["messages"] == [
        {"role": "system", "content": "rules"},
        {"role": "user", "content": "hi /no_think"},
    ]


def test_no_think_can_be_turned_off():
    client = FakeClient("Hi")
    OllamaLanguageModel("m", "h", no_think=False, client=client).reply([Message(Role.USER, "hi")])
    assert client.sent["messages"][-1]["content"] == "hi"


@pytest.mark.live
@pytest.mark.skipif(os.environ.get("AIKOS_LIVE") != "1", reason="set AIKOS_LIVE=1 with Ollama running")
def test_real_ollama_answers():
    model = OllamaLanguageModel(os.environ.get("AIKOS_MODEL", "qwen3:1.7b"), "http://127.0.0.1:11434")
    assert model.reply([Message(Role.USER, "Reply with one word: ready")])
