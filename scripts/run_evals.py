"""Score how often Aiko picks the right tool (evals/commands.yaml) and how fast, with the model in config.yaml."""

import argparse
import sys
import time
from pathlib import Path

import yaml

from aikos.application.prompts import system_prompt
from aikos.application.tools import NOTE_TOOLS
from aikos.bootstrap.settings import load_settings
from aikos.domain.conversation import Message, Role
from aikos.infrastructure.llm.ollama_model import OllamaLanguageModel

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", help="override llm.model from config.yaml")
    args = parser.parse_args()

    settings = load_settings(ROOT / "config.yaml")
    name = args.model or settings.llm.model
    model = OllamaLanguageModel(name, settings.llm.host, no_think=settings.llm.no_think)
    a = settings.assistant
    system = Message(Role.SYSTEM, system_prompt(a.name, a.name_th, a.self_pronoun_th))
    cases = yaml.safe_load((ROOT / "evals" / "commands.yaml").read_text(encoding="utf-8"))

    model.reply([Message(Role.USER, "hi")])  # load the model so the first case is not penalised
    passed, total_time = 0, 0.0
    for case in cases:
        start = time.perf_counter()
        reply = model.reply([system, Message(Role.USER, case["say"])], NOTE_TOOLS)
        seconds = time.perf_counter() - start
        total_time += seconds
        got = reply.tool_call.name if reply.tool_call else "none"
        ok = got == case["tool"]
        passed += ok
        print(f"{'OK  ' if ok else 'FAIL'} {seconds:4.1f}s want={case['tool']:<10} got={got:<10} {case['say']}")

    print(f"\nModel {name}: {passed}/{len(cases)} correct ({passed / len(cases):.0%}), "
          f"average {total_time / len(cases):.1f}s per message")
    return 0 if passed == len(cases) else 1


if __name__ == "__main__":
    sys.exit(main())
