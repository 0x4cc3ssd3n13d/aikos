from dataclasses import dataclass

from aikos.application.ports.language_model import LanguageModel
from aikos.application.prompts import female_thai, system_prompt
from aikos.application.tools import NOTE_TOOLS
from aikos.application.use_cases.chat import Chat
from aikos.application.use_cases.list_notes import ListNotes
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
    list_notes: ListNotes


def build_container(settings: Settings, model: LanguageModel | None = None) -> Container:
    """Wire the real adapters. Tests pass `model` to avoid needing Ollama."""
    if model is None:
        model = OllamaLanguageModel(settings.llm.model, settings.llm.host, no_think=settings.llm.no_think)
    chat = Chat(
        model,
        Conversation(max_turns=settings.assistant.memory_turns),
        system_prompt(settings.assistant.name, settings.assistant.name_th, settings.assistant.self_pronoun_th),
        tools=NOTE_TOOLS,
        polish=female_thai,
    )
    notes = MarkdownNoteRepository(settings.paths.data_dir / "notes")
    return Container(chat=chat, take_note=TakeNote(notes, SystemClock()), list_notes=ListNotes(notes))
