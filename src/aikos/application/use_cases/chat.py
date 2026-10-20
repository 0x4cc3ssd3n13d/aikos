from aikos.application.ports.language_model import LanguageModel
from aikos.domain.conversation import Conversation, Message, Role
from aikos.domain.errors import InvalidInput


class Chat:
    """Answer the user with the language model, remembering the recent conversation."""

    def __init__(self, model: LanguageModel, conversation: Conversation, system_prompt: str) -> None:
        self._model = model
        self._conversation = conversation
        self._system = Message(Role.SYSTEM, system_prompt)

    def execute(self, user_text: str) -> str:
        if not user_text.strip():
            raise InvalidInput("Say or type something first.")
        self._conversation.add(Message(Role.USER, user_text.strip()))
        answer = self._model.reply([self._system, *self._conversation.recent()])
        self._conversation.add(Message(Role.ASSISTANT, answer))
        return answer
