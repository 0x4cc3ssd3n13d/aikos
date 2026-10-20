# Rules for Claude working on AIKOs

- Python 3.12, type hints, one tool per file in `aikos/tools/`, every tool has tests in `tests/`.
- All settings come from `config.yaml`; never hard-code model names, paths, hotkeys or keys.
- API keys come from environment variables only, never from files in this folder.
- No network calls unless `cloud.enabled` is true in `config.yaml`. Ollama on localhost is allowed.
- Any action that changes something (save, send, delete, overwrite, create an event) asks the user first.
- Email is draft-only.
- Ask the user before installing packages or changing `config.yaml`.
- Claude's own experiments go in `sandbox/` on a separate Git branch, merged only after tests pass and the user says yes.
- Explain each step in plain words; the user may be a beginner.