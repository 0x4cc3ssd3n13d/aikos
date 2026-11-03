"""Tools the model can choose from natural language. Each maps to one use case."""

from aikos.application.ports.language_model import ToolSpec

TAKE_NOTE = ToolSpec(
    name="take_note",
    description="Save a short note for the user. Use when the user asks to note, remember or write something down "
    "(e.g. 'จดไว้ว่า...', 'note that...').",
    parameters={
        "type": "object",
        "properties": {"text": {"type": "string", "description": "The note text, in the user's language"}},
        "required": ["text"],
    },
)

LIST_NOTES = ToolSpec(
    name="list_notes",
    description="Show the user's most recent notes. Use when the user asks what they noted or saved "
    "(e.g. 'จดอะไรไว้บ้าง', 'what are my notes').",
)

NOTE_TOOLS = (TAKE_NOTE, LIST_NOTES)

# Tools that change something: the user must confirm before they run (safety.confirm_before_changes).
CHANGES_DATA = frozenset({TAKE_NOTE.name})
