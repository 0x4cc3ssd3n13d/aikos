import re
from collections.abc import Sequence
from typing import Any

from aikos.domain.conversation import Message, Role

_THINK_BLOCK = re.compile(r"<think>.*?</think>", re.S)


class OllamaLanguageModel:
    """LanguageModel port backed by a local Ollama server."""

    def __init__(self, model: str, host: str, no_think: bool = True, client: Any | None = None) -> None:
        if client is None:
            import ollama  # imported here so the rest of AIKOs loads without it

            client = ollama.Client(host=host)
        self._client = client
        self._model = model
        self._no_think = no_think

    def reply(self, messages: Sequence[Message]) -> str:
        payload = [{"role": m.role.value, "content": m.content} for m in messages]
        if self._no_think and payload and payload[-1]["role"] == Role.USER.value:
            # Qwen3 soft switch: skip the long reasoning step, much faster on low-spec CPUs.
            payload[-1]["content"] += " /no_think"
        response = self._client.chat(model=self._model, messages=payload)
        return _THINK_BLOCK.sub("", response["message"]["content"]).strip()
