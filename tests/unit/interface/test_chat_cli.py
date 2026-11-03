from aikos.application.ports.language_model import ModelReply, ToolCall
from aikos.application.use_cases.chat import Chat
from aikos.application.use_cases.list_notes import ListNotes
from aikos.application.use_cases.take_note import TakeNote
from aikos.domain.conversation import Conversation
from aikos.interface.cli.chat_cli import run_chat


def run(lines, chat, notes, clock, **kwargs):
    inputs, outputs = iter(lines), []
    run_chat(
        chat,
        TakeNote(notes, clock),
        ListNotes(notes),
        read=lambda _prompt: next(inputs),
        write=outputs.append,
        **kwargs,
    )
    return outputs


def note_call(text):
    return ModelReply(tool_call=ToolCall("take_note", {"text": text}))


def test_chat_note_and_quit(model, notes, clock):
    model.answers = ["Hi, I am Aiko."]
    out = run(["hello", "/note buy milk", "/quit"], Chat(model, Conversation(), "rules"), notes, clock)
    assert "Aiko> Hi, I am Aiko." in out
    assert "Saved note at 09:30: buy milk" in out
    assert notes.saved[0].text == "buy milk"


def test_model_asks_to_save_note_and_user_confirms(model, notes, clock):
    model.answers = [note_call("ซื้อนม")]
    out = run(["จดไว้ว่าซื้อนม", "ได้", "/quit"], Chat(model, Conversation(), "rules"), notes, clock)
    assert [n.text for n in notes.saved] == ["ซื้อนม"]
    assert "Aiko> Saved note at 09:30: ซื้อนม" in out


def test_declining_saves_nothing(model, notes, clock):
    model.answers = [note_call("ซื้อนม")]
    out = run(["จดไว้ว่าซื้อนม", "n", "/quit"], Chat(model, Conversation(), "rules"), notes, clock)
    assert notes.saved == []
    assert "Aiko> Cancelled, nothing was saved." in out


def test_confirmation_can_be_turned_off(model, notes, clock):
    model.answers = [note_call("ซื้อนม")]
    run(["จดไว้ว่าซื้อนม", "/quit"], Chat(model, Conversation(), "rules"), notes, clock, confirm_changes=False)
    assert [n.text for n in notes.saved] == ["ซื้อนม"]


def test_list_notes_by_tool_and_command(model, notes, clock):
    TakeNote(notes, clock).execute("ซื้อนม")
    model.answers = [ModelReply(tool_call=ToolCall("list_notes"))]
    out = run(["จดอะไรไว้บ้าง", "/notes", "/quit"], Chat(model, Conversation(), "rules"), notes, clock)
    assert out.count("- 2026-10-16 09:30 ซื้อนม") == 1
    assert "Aiko> - 2026-10-16 09:30 ซื้อนม" in out


def test_unknown_tool_is_refused(model, notes, clock):
    model.answers = [ModelReply(tool_call=ToolCall("delete_everything"))]
    out = run(["wipe it", "/quit"], Chat(model, Conversation(), "rules"), notes, clock)
    assert "Aiko> Sorry, I can't do 'delete_everything' yet." in out


def test_errors_are_shown_and_chat_continues(notes, clock):
    class OfflineModel:
        def reply(self, messages, tools=()):
            raise ConnectionError("Ollama is not running")

    out = run(["hello", "/note", "/quit"], Chat(OfflineModel(), Conversation(), "rules"), notes, clock)
    assert any("Ollama is not running" in line for line in out)
    assert "A note cannot be empty." in out


def test_end_of_input_exits(model, notes, clock):
    def read(_prompt):
        raise EOFError

    run_chat(
        Chat(model, Conversation(), "rules"), TakeNote(notes, clock), ListNotes(notes), read=read, write=lambda _t: None
    )
