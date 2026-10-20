from dataclasses import dataclass, field
from enum import Enum

from aikos.domain.errors import InvalidInput


class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass(frozen=True)
class Message:
    role: Role
    content: str

    def __post_init__(self) -> None:
        if not self.content.strip():
            raise InvalidInput("A message cannot be empty.")


@dataclass
class Conversation:
    """Short-term memory: keeps only the last `max_turns` user/assistant pairs."""

    max_turns: int = 10
    _messages: list[Message] = field(default_factory=list)

    def add(self, message: Message) -> None:
        if message.role is Role.SYSTEM:
            raise InvalidInput("System instructions are not part of the conversation history.")
        self._messages.append(message)
        overflow = len(self._messages) - self.max_turns * 2
        if overflow > 0:
            del self._messages[:overflow]

    def recent(self) -> list[Message]:
        return list(self._messages)
