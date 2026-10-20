from collections.abc import Callable

from aikos.application.use_cases.chat import Chat
from aikos.application.use_cases.take_note import TakeNote
from aikos.domain.errors import DomainError

HELP = "Type a message. Commands: /note <text> saves a note, /help, /quit."


def run_chat(
    chat: Chat,
    take_note: TakeNote,
    assistant_name: str = "AIKOs",
    read: Callable[[str], str] = input,
    write: Callable[[str], None] = print,
) -> None:
    write(f"{assistant_name} is ready. {HELP}")
    while True:
        try:
            text = read("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            write("")
            return
        if not text:
            continue
        if text in ("/quit", "/exit"):
            return
        if text == "/help":
            write(HELP)
            continue
        try:
            if text.startswith("/note"):
                note = take_note.execute(text.removeprefix("/note"))
                write(f"Saved note at {note.created_at:%H:%M}.")
            else:
                write(f"{assistant_name}> {chat.execute(text)}")
        except DomainError as exc:
            write(str(exc))
        except Exception as exc:  # e.g. Ollama is not running; keep the chat alive
            write(f"Sorry, something went wrong: {exc}")
