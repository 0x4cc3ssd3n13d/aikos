# AIKOs

Artificial Intelligence Kontrol (Control) Operating System: a voice secretary that runs on your own low-spec Windows PC.

Full guide (Thai): what is installed, how the code is organised and what each file does: [docs/PROJECT_GUIDE.md](docs/PROJECT_GUIDE.md).

## Project structure (Clean Architecture)

```text
src/aikos/
  domain/          rules and data, pure Python (Conversation, Note, Reminder)
  application/
    ports/         interfaces the use cases need (LanguageModel, NoteRepository, Clock, speech)
    use_cases/     what AIKOs can do (Chat, TakeNote, ...)
  infrastructure/  real tools behind the ports (Ollama, Markdown files, clock; speech, calendar, email later)
  interface/       how you talk to AIKOs (terminal chat now; voice and tray icon later)
  bootstrap/       reads config.yaml and wires everything together
  main.py          starts AIKOs
tests/             unit tests (fakes, no Ollama needed) and integration tests
evals/             command -> expected tool cases (from Phase 4)
scripts/           setup checks
config.yaml        all settings
```

Dependencies only point inward (interface and infrastructure -> application -> domain), so the core logic never depends on Ollama, Windows or any library. `lint-imports` checks this.

## Run

```powershell
.venv\Scripts\python.exe -m pip install -e ".[dev]"
.venv\Scripts\python.exe -m aikos            # chat in the terminal
.venv\Scripts\python.exe -m pytest           # tests
.venv\Scripts\lint-imports.exe               # architecture rules
```

Check that Ollama and the model work: `.venv\Scripts\python.exe scripts\check_phase0.py`

In the chat, `/note buy milk` saves a note to `data/notes/`, `/quit` exits.
