# Rules for Claude working on AIKOs

## Architecture (Clean Architecture)

Code lives in `src/aikos/`, in four layers. Dependencies only point inward:

| Layer | Folder | May import | Holds |
| --- | --- | --- | --- |
| Domain | `domain/` | nothing else in aikos, no outside libraries | entities and rules: Conversation, Note, Reminder |
| Application | `application/` | domain | use cases (`use_cases/`) and ports (`ports/`, Protocols) |
| Infrastructure | `infrastructure/` | application, domain, outside libraries | adapters that implement ports: Ollama, files, Windows, speech |
| Interface | `interface/` | application, domain | how the user talks to AIKOs: CLI, voice loop, tray |
| Bootstrap | `bootstrap/` | everything | `settings.py` (config.yaml) and `container.py` (wiring) |

`lint-imports` enforces these rules; never weaken a contract in `pyproject.toml` to make code pass.

## Adding a feature

1. Domain: add or extend an entity if there is a new rule.
2. Application: add a port (Protocol) for anything outside, then a use case class with `execute()`.
3. Infrastructure: add an adapter that implements the port.
4. Bootstrap: wire it in `container.py`; add settings to `settings.py` and `config.yaml`.
5. Interface: call the use case from the CLI or voice loop.
6. Tests: unit tests with fakes from `tests/conftest.py`; integration tests for adapters; eval cases in `evals/`.

## Rules

- Python 3.12, type hints, small classes, one use case per file.
- All settings come from `config.yaml`; never hard-code model names, paths, hotkeys or keys.
- API keys come from environment variables only, never from files in this folder.
- No network calls unless `cloud.enabled` is true. Ollama on localhost is allowed.
- Any action that changes something (save, send, delete, overwrite, create an event) asks the user first.
- Email is draft-only.
- Build for the minimum profile (4 GB RAM, no GPU): one model loaded at a time, no heavy dependencies in core.
- Ask the user before installing packages or changing `config.yaml`.
- Claude's own experiments go in `sandbox/` on a separate Git branch, merged only after tests pass and the user says yes.
- Before finishing: `pytest` and `lint-imports` must both pass.
- Explain each step in plain words; the user may be a beginner.
