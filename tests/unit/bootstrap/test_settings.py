from pathlib import Path

import pytest

from aikos.bootstrap.container import build_container
from aikos.bootstrap.settings import load_settings

PROJECT_CONFIG = Path(__file__).resolve().parents[3] / "config.yaml"


def test_project_config_loads():
    settings = load_settings(PROJECT_CONFIG)
    assert settings.assistant.name == "Aiko"
    assert settings.assistant.name_th == "ไอโกะ"
    assert settings.assistant.self_pronoun_th == "ฉัน"
    assert settings.speech.wake_words == ["ไอโกะ", "Aiko", "สวัสดี ไอโกะ"]
    assert settings.profile == "minimum"
    assert settings.llm.model == "qwen3:1.7b"
    assert settings.cloud.enabled is False
    assert settings.paths.data_dir == PROJECT_CONFIG.parent / "data"


def test_phase0_config_without_new_keys_still_loads(tmp_path):
    config = tmp_path / "config.yaml"
    config.write_text("assistant:\n  name: AIKOs\nllm:\n  model: qwen3:4b\n", encoding="utf-8")
    settings = load_settings(config)
    assert settings.llm.model == "qwen3:4b"
    assert settings.assistant.memory_turns == 10


def test_missing_config_explains_what_to_do(tmp_path):
    with pytest.raises(FileNotFoundError, match="--config"):
        load_settings(tmp_path / "nope.yaml")


def test_container_wires_use_cases(tmp_path, model):
    config = tmp_path / "config.yaml"
    config.write_text("paths:\n  data_dir: mydata\n", encoding="utf-8")
    container = build_container(load_settings(config), model=model)
    assert container.chat.execute("hi") == "OK"
    system = model.calls[0][0].content
    assert "ไอโกะ" in system and '"ฉัน"' in system
    container.take_note.execute("from the container")
    assert list((tmp_path / "mydata" / "notes").glob("*.md"))
