"""Speech ports, implemented in Phase 2 (faster-whisper, Piper, Edge TTS) and Phase 3 (openWakeWord)."""

from typing import Protocol


class SpeechToText(Protocol):
    def transcribe(self, audio: bytes, sample_rate: int) -> str: ...


class TextToSpeech(Protocol):
    def speak(self, text: str, language: str) -> None: ...


class WakeWordDetector(Protocol):
    def wait_for_wake_word(self) -> None: ...
