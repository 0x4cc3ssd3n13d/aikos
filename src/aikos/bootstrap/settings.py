from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field


class AssistantSettings(BaseModel):
    name: str = "AIKOs"
    languages: list[str] = Field(default_factory=lambda: ["th", "en"])
    memory_turns: int = 10


class LlmSettings(BaseModel):
    provider: Literal["ollama"] = "ollama"
    host: str = "http://127.0.0.1:11434"
    model: str = "qwen3:1.7b"
    fast_model: str = "qwen3:1.7b"
    embed_model: str = "nomic-embed-text"
    no_think: bool = True


class SpeechSettings(BaseModel):
    stt_model: str = "base"
    push_to_talk_key: str = "ctrl+alt+space"
    wake_word: str = "hey_aikos"
    tts_english: str = "piper"
    tts_thai: str = "edge-tts"


class CloudSettings(BaseModel):
    enabled: bool = False
    provider: Literal["anthropic"] = "anthropic"
    model: str = "claude-opus-5-5"
    monthly_budget_usd: float = 10


class SafetySettings(BaseModel):
    confirm_before_changes: bool = True
    email_mode: Literal["draft_only"] = "draft_only"


class PathSettings(BaseModel):
    data_dir: Path = Path("data")


class Settings(BaseModel):
    assistant: AssistantSettings = Field(default_factory=AssistantSettings)
    profile: Literal["minimum", "standard", "high"] = "minimum"
    llm: LlmSettings = Field(default_factory=LlmSettings)
    speech: SpeechSettings = Field(default_factory=SpeechSettings)
    cloud: CloudSettings = Field(default_factory=CloudSettings)
    safety: SafetySettings = Field(default_factory=SafetySettings)
    paths: PathSettings = Field(default_factory=PathSettings)


def load_settings(path: Path) -> Settings:
    """Read config.yaml. Relative paths inside it are relative to the file's folder."""
    if not path.is_file():
        raise FileNotFoundError(f"Settings file not found: {path}. Run AIKOs from the project folder or pass --config.")
    data = yaml.safe_load(path.read_text(encoding="utf-8-sig")) or {}
    settings = Settings.model_validate(data)
    if not settings.paths.data_dir.is_absolute():
        settings.paths.data_dir = (path.parent / settings.paths.data_dir).resolve()
    return settings
