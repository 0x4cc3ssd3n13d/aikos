import re
from collections.abc import Sequence
from typing import Any

from aikos.application.ports.language_model import ModelReply, ToolCall, ToolSpec
from aikos.domain.conversation import Message

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

    def reply(self, messages: Sequence[Message], tools: Sequence[ToolSpec] = ()) -> ModelReply:
        request: dict[str, Any] = {
            "model": self._model,
            "messages": [{"role": m.role.value, "content": m.content} for m in messages],
        }
        if self._no_think:
            # Qwen3 skips its hidden reasoning: "ready" took 22 s with the old "/no_think" text, 0.5 s with this.
            request["think"] = False
        if tools:
            request["tools"] = [
                {
                    "type": "function",
                    "function": {"name": t.name, "description": t.description, "parameters": dict(t.parameters)},
                }
                for t in tools
            ]
        message = self._client.chat(**request)["message"]
        calls = message.get("tool_calls") or []
        if calls:
            function = calls[0]["function"]  # one action at a time; the user confirms each
            return ModelReply(tool_call=ToolCall(function["name"], dict(function.get("arguments") or {})))
        return ModelReply(text=_THINK_BLOCK.sub("", message.get("content") or "").strip())
