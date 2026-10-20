from dataclasses import dataclass

from aikos.application.ports.language_model import LanguageModel
from aikos.application.prompts import system_prompt
from aikos.application.use_cases.chat import Chat
from aikos.application.use_cases.take_note import TakeNote
from aikos.bootstrap.settings import Settings
from aikos.domain.conversation import Conversation
from aikos.infrastructure.llm.ollama_model import OllamaLanguageModel
from aikos.infrastructure.storage.markdown_notes import MarkdownNoteRepository
from aikos.infrastructure.system.clock import SystemClock


@dataclass(frozen=True)
class Container:
    chat: Chat
    take_note: TakeNote


def build_container(settings: Settings, model: LanguageModel | None = None) -> Container:
    """Wire the real adapters. Tests pass `model` to avoid needing Ollama."""
    if model is None:
        model = OllamaLanguageModel(settings.llm.model, settings.llm.host, no_think=settings.llm.no_think)
    chat = Chat(
        model,
        Conversation(max_turns=settings.assistant.memory_turns),
        system_prompt(settings.assistant.name),
    )
    notes = MarkdownNoteRepository(settings.paths.data_dir / "notes")
    return Container(chat=chat, take_note=TakeNote(notes, SystemClock()))
