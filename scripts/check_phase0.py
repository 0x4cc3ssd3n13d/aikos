"""Phase 0 check: Python 3.12, the ollama package, and the model answering in English and Thai."""

import argparse
import platform
import re
import sys
import time


def ask(ollama, model: str, text: str) -> tuple[str, float, float | None]:
    """Send one message; return (answer, seconds, tokens per second)."""
    start = time.perf_counter()
    # "/no_think" asks Qwen3 to skip its long reasoning so answers come back faster.
    resp = ollama.chat(model=model, messages=[{"role": "user", "content": text + " /no_think"}])
    seconds = time.perf_counter() - start
    answer = re.sub(r"<think>.*?</think>", "", resp["message"]["content"], flags=re.S).strip()
    try:
        speed = resp["eval_count"] / (resp["eval_duration"] / 1e9)
    except (KeyError, TypeError, ZeroDivisionError):
        speed = None
    return answer, seconds, speed


def main() -> int:
    # Thai text must print correctly even when the output is piped or logged.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="qwen3:1.7b")
    args = parser.parse_args()

    print(f"Python {platform.python_version()} at {sys.executable}")
    if sys.version_info[:2] != (3, 12):
        print("WARNING: AIKOs expects Python 3.12")

    try:
        import ollama
    except ImportError:
        print("FAIL: the ollama package is missing. Run: .venv\\Scripts\\python.exe -m pip install -r requirements.txt")
        return 1

    tests = [
        ("English", "In one short sentence, introduce yourself as AIKOs, a personal secretary."),
        ("Thai", "\u0e41\u0e19\u0e30\u0e19\u0e33\u0e15\u0e31\u0e27\u0e40\u0e2d\u0e07\u0e2a\u0e31\u0e49\u0e19\u0e46 \u0e2b\u0e19\u0e36\u0e48\u0e07\u0e1b\u0e23\u0e30\u0e42\u0e22\u0e04\u0e27\u0e48\u0e32\u0e04\u0e38\u0e13\u0e04\u0e37\u0e2d AIKOs \u0e40\u0e25\u0e02\u0e32\u0e2a\u0e48\u0e27\u0e19\u0e15\u0e31\u0e27 \u0e15\u0e2d\u0e1a\u0e40\u0e1b\u0e47\u0e19\u0e20\u0e32\u0e29\u0e32\u0e44\u0e17\u0e22"),
        ("English, model already loaded", "Reply with one word: ready"),
    ]
    passed = 0
    for label, text in tests:
        try:
            answer, seconds, speed = ask(ollama, args.model, text)
        except Exception as exc:  # connection refused, model not pulled, out of memory...
            print(f"FAIL [{label}]: {exc}")
            print("Is Ollama running? Try: ollama run " + args.model)
            continue
        rate = f", {speed:.1f} tokens/s" if speed else ""
        print(f"OK   [{label}] {seconds:.1f}s{rate}: {answer}")
        passed += 1

    print("\nThe first answer includes loading the model into memory, so it is the slowest.")
    print(f"Result: {passed}/{len(tests)} checks passed")
    return 0 if passed == len(tests) else 1


if __name__ == "__main__":
    sys.exit(main())