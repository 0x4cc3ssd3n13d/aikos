from collections.abc import Callable, Sequence
from dataclasses import replace

from aikos.application.ports.language_model import LanguageModel, ModelReply, ToolSpec
from aikos.domain.conversation import Conversation, Message, Role
from aikos.domain.errors import InvalidInput


class Chat:
    """Answer the user with the language model, remembering the recent conversation.

    The model may answer with text or ask to use one of `tools`; the caller runs the tool.
    """

    def __init__(
        self,
        model: LanguageModel,
        conversation: Conversation,
        system_prompt: str,
        tools: Sequence[ToolSpec] = (),
        polish: Callable[[str], str] = str,
    ) -> None:
        self._model = model
        self._conversation = conversation
        self._system = Message(Role.SYSTEM, system_prompt)
        self._tools = tuple(tools)
        self._polish = polish  # e.g. female_thai: fixes wording the model gets wrong

    def execute(self, user_text: str) -> ModelReply:
        if not user_text.strip():
            raise InvalidInput("Say or type something first.")
        self._conversation.add(Message(Role.USER, user_text.strip()))
        reply = self._model.reply([self._system, *self._conversation.recent()], self._tools)
        reply = replace(reply, text=self._polish(reply.text))
        if reply.text.strip():
            self._conversation.add(Message(Role.ASSISTANT, reply.text))
        return reply

    def remember(self, outcome: str) -> None:
        """Record what a tool did, so follow-up questions ("what did you save?") make sense."""
        self._conversation.add(Message(Role.ASSISTANT, outcome))
