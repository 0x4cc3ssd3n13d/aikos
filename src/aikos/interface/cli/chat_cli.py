from collections.abc import Callable

from aikos.application.ports.language_model import ToolCall
from aikos.application.tools import CHANGES_DATA, LIST_NOTES, TAKE_NOTE
from aikos.application.use_cases.chat import Chat
from aikos.application.use_cases.list_notes import ListNotes
from aikos.application.use_cases.take_note import TakeNote
from aikos.domain.errors import DomainError

HELP = (
    "Type a message, e.g. 'จดไว้ว่าพรุ่งนี้ซื้อนม' or 'what are my notes?'. "
    "Commands: /note <text> saves a note, /notes lists notes, /help, /quit."
)
YES = {"y", "yes", "ใช่", "ได้", "ok", "ตกลง"}


def run_chat(
    chat: Chat,
    take_note: TakeNote,
    list_notes: ListNotes,
    assistant_name: str = "Aiko",
    confirm_changes: bool = True,
    read: Callable[[str], str] = input,
    write: Callable[[str], None] = print,
) -> None:
    def save(text: str) -> str:
        note = take_note.execute(text)
        return f"Saved note at {note.created_at:%H:%M}: {note.text}"

    def show_notes() -> str:
        notes = list_notes.execute()
        if not notes:
            return "No notes yet."
        return "\n".join(f"- {n.created_at:%Y-%m-%d %H:%M} {n.text}" for n in notes)

    def run_tool(call: ToolCall) -> str:
        if call.name == TAKE_NOTE.name:
            text = str(call.arguments.get("text", "")).strip()
            if confirm_changes and call.name in CHANGES_DATA:
                if read(f'Save note "{text}"? (y/n) ').strip().lower() not in YES:
                    return "Cancelled, nothing was saved."
            return save(text)
        if call.name == LIST_NOTES.name:
            return show_notes()
        return f"Sorry, I can't do '{call.name}' yet."

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
            if text.startswith("/notes"):
                write(show_notes())
            elif text.startswith("/note"):
                write(save(text.removeprefix("/note")))  # typed command = explicit consent
            else:
                reply = chat.execute(text)
                if reply.tool_call:
                    outcome = run_tool(reply.tool_call)
                    chat.remember(outcome)
                    write(f"{assistant_name}> {outcome}")
                else:
                    write(f"{assistant_name}> {reply.text}")
        except DomainError as exc:
            write(str(exc))
        except (EOFError, KeyboardInterrupt):
            write("")
            return
        except Exception as exc:  # e.g. Ollama is not running; keep the chat alive
            write(f"Sorry, something went wrong: {exc}")
