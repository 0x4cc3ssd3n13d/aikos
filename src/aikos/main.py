"""Entry point: load settings, wire the app, start the chosen interface."""

import argparse
import sys
from pathlib import Path

from aikos.bootstrap.container import build_container
from aikos.bootstrap.settings import load_settings
from aikos.interface.cli.chat_cli import run_chat


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="aikos", description="AIKOs voice secretary")
    parser.add_argument("--config", type=Path, default=Path("config.yaml"), help="path to config.yaml")
    args = parser.parse_args(argv)

    # Thai text must print correctly in any Windows console.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    settings = load_settings(args.config)
    container = build_container(settings)
    run_chat(container.chat, container.take_note, assistant_name=settings.assistant.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
