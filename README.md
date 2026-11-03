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
evals/             message -> expected tool cases (scored by scripts/run_evals.py)
scripts/           setup check and evals
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
Score tool choice in Thai and English: `.venv\Scripts\python.exe scripts\run_evals.py`

In the chat, just ask: "จดไว้ว่าพรุ่งนี้ซื้อนม" saves a note after you confirm, "จดอะไรไว้บ้าง" lists notes.
Commands: `/note buy milk` saves directly to `data/notes/`, `/notes` lists notes, `/quit` exits.
