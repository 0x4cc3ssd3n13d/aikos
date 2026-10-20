from aikos.application.use_cases.chat import Chat
from aikos.application.use_cases.take_note import TakeNote
from aikos.domain.conversation import Conversation
from aikos.interface.cli.chat_cli import run_chat


def run(lines, chat, take_note):
    inputs, outputs = iter(lines), []
    run_chat(chat, take_note, read=lambda _prompt: next(inputs), write=outputs.append)
    return outputs


def test_chat_note_and_quit(model, notes, clock):
    model.answers = ["Hi, I am AIKOs."]
    out = run(["hello", "/note buy milk", "/quit"], Chat(model, Conversation(), "rules"), TakeNote(notes, clock))
    assert "AIKOs> Hi, I am AIKOs." in out
    assert "Saved note at 09:30." in out
    assert notes.saved[0].text == "buy milk"


def test_errors_are_shown_and_chat_continues(notes, clock):
    class OfflineModel:
        def reply(self, messages):
            raise ConnectionError("Ollama is not running")

    out = run(["hello", "/note", "/quit"], Chat(OfflineModel(), Conversation(), "rules"), TakeNote(notes, clock))
    assert any("Ollama is not running" in line for line in out)
    assert "A note cannot be empty." in out


def test_end_of_input_exits(model, notes, clock):
    def read(_prompt):
        raise EOFError

    run_chat(Chat(model, Conversation(), "rules"), TakeNote(notes, clock), read=read, write=lambda _t: None)
