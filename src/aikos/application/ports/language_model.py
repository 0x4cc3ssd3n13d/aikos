from collections.abc import Sequence
from typing import Protocol

from aikos.domain.conversation import Message


class LanguageModel(Protocol):
    """Anything that can answer a conversation: Ollama now, Claude in Phase 6."""

    def reply(self, messages: Sequence[Message]) -> str: ...
