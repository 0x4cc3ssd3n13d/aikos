from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_clean_architecture_contracts_hold(monkeypatch, capsys):
    """Runs the import-linter contracts from pyproject.toml (same as `lint-imports`)."""
    cli = pytest.importorskip("importlinter.cli", reason="import-linter not installed (pip install -e .[dev])")
    monkeypatch.chdir(ROOT)
    exit_code = cli.lint_imports(no_cache=True, no_logo=True)
    assert exit_code == 0, capsys.readouterr().out
