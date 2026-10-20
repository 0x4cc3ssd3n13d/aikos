---
name: aikos-guide
description: Explain and extend the AIKOs voice-secretary project (Clean Architecture, Python 3.12, Ollama). Use when the user asks how AIKOs works, where some code lives, what is installed, how to run or test it, or wants to add a feature, tool, adapter or use case to AIKOs; also for "อธิบายโปรเจกต์", "โค้ดนี้ทำอะไร", "เพิ่มฟีเจอร์".
---

# AIKOs guide

Full reference (Thai): `docs/PROJECT_GUIDE.md`. Read the section you need instead of guessing:
installed tools (section 3), layers (4), file map (5), commands (6), adding a feature (7), roadmap (9).
Rules for working here: `CLAUDE.md`. The user is a beginner and reads Thai: explain in plain Thai, keep English code terms.

## Explaining

- Answer with the file path and the layer it belongs to, e.g. "`application/use_cases/chat.py` (Application): ...".
- Follow a message through the layers when it helps: interface → use case → port → adapter → back.
- If the guide and the code disagree, trust the code and update the guide.

## Adding a feature

Work inward-out, one step at a time, and say which layer each step touches:

1. Domain: new rule or entity only if needed, pure Python.
2. Application: a port (`Protocol`) for anything outside, then one use case class per file with `execute()`.
3. Infrastructure: an adapter that implements the port; outside libraries are allowed only here.
4. Bootstrap: wire it in `bootstrap/container.py`; new settings go in `settings.py` and `config.yaml` (ask first).
5. Interface: call the use case from the CLI (later the voice loop).
6. Tests: unit tests with fakes from `tests/conftest.py`, integration tests for adapters.

Ask the user before installing packages, editing `config.yaml`, or any action that saves, sends, deletes or overwrites.

## Done means

```powershell
.venv\Scripts\python.exe -m pytest
.venv\Scripts\lint-imports.exe
```

Both pass. Never loosen an import-linter contract in `pyproject.toml` to make code pass.
If the change adds files, layers, commands or installs, update `docs/PROJECT_GUIDE.md` in the same change.
For bigger tasks use the `feature-dev` or `ralph-loop` plugin (always set a max iteration count);
review with `pr-review-toolkit`, and run `claude-security` before opening a PR.
