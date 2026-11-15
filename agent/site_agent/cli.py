"""Chat with the agent in a terminal.

  python -m site_agent.cli                     interactive
  python -m site_agent.cli "your question"     one question
  python -m site_agent.cli --verbose           also show each tool call
"""
from __future__ import annotations

import argparse
import sys

from .config import build_agent, load_config, load_site_index
from .model_client import ModelError


def main() -> int:
    parser = argparse.ArgumentParser(description="Chat with the site agent.")
    parser.add_argument("question", nargs="?", help="Ask one question and exit.")
    parser.add_argument("--model", help="Model id to use instead of the configured one.")
    parser.add_argument("--verbose", action="store_true", help="Show tool calls and token use.")
    args = parser.parse_args()

    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")

    def show_tool_call(event: dict) -> None:
        if args.verbose:
            status = "ok" if event["ok"] else f"error: {event['error']}"
            print(f"  [tool] {event['name']} {event['arguments']} -> {status}", file=sys.stderr)

    try:
        config = load_config()
        agent = build_agent(config, load_site_index(config), model=args.model, on_event=show_tool_call)
    except (ModelError, FileNotFoundError) as error:
        print(f"Cannot start: {error}", file=sys.stderr)
        return 1

    def ask(question: str, history: list[dict]) -> list[dict]:
        try:
            result = agent.run(question, history)
        except ModelError as error:
            print(f"Model error: {error}", file=sys.stderr)
            return history
        print(result.answer)
        if args.verbose:
            print(f"  [steps {result.steps}, tokens in {result.usage['prompt_tokens']}, "
                  f"out {result.usage['completion_tokens']}]", file=sys.stderr)
        return result.history

    if args.question:
        ask(args.question, [])
        return 0

    print(f"{config['name']} guide. Type a question, or press Enter on an empty line to quit.")
    history: list[dict] = []
    while True:
        try:
            question = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not question:
            break
        print()
        history = ask(question, history)
    return 0


if __name__ == "__main__":
    sys.exit(main())
