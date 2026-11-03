from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any, Protocol

from aikos.domain.conversation import Message


@dataclass(frozen=True)
class ToolSpec:
    """A tool the model may ask to use. `parameters` is a JSON Schema object."""

    name: str
    description: str
    parameters: Mapping[str, Any] = field(default_factory=lambda: {"type": "object", "properties": {}})


@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ModelReply:
    """Either a text answer or a request to use one tool."""

    text: str = ""
    tool_call: ToolCall | None = None


class LanguageModel(Protocol):
    """Anything that can answer a conversation: Ollama now, Claude in Phase 6."""

    def reply(self, messages: Sequence[Message], tools: Sequence[ToolSpec] = ()) -> ModelReply: ...
