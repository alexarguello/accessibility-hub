"""List OpenRouter's free models that support tool calling.

  python -m site_agent.list_models            list them (needs no key)
  python -m site_agent.list_models --check    also send each one a tiny tool-calling
                                              request to see which respond right now
                                              (uses one free request per model)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.request

from .config import load_env_file
from .model_client import ChatClient, ModelError

MODELS_URL = "https://openrouter.ai/api/v1/models"

PROBE_TOOL = [{
    "type": "function",
    "function": {
        "name": "search_site",
        "description": "Search the site for pages about a topic.",
        "parameters": {"type": "object", "properties": {"query": {"type": "string"}},
                       "required": ["query"]},
    },
}]
PROBE_MESSAGES = [
    {"role": "system", "content": "Use the search_site tool to answer."},
    {"role": "user", "content": "Find pages about screen readers."},
]


def free_tool_models() -> list[dict]:
    with urllib.request.urlopen(MODELS_URL, timeout=30) as response:
        models = json.load(response)["data"]
    free = [m for m in models
            if m["id"].endswith(":free") and "tools" in (m.get("supported_parameters") or [])]
    free.sort(key=lambda m: m.get("created", 0), reverse=True)
    return free


def probe(model_id: str, api_key: str) -> str:
    """Send one small request. Says whether the model answered and whether it called the tool."""
    client = ChatClient(api_key, model_id, max_tokens=200, max_retries=0, timeout=60)
    started = time.monotonic()
    try:
        message = client.complete(PROBE_MESSAGES, PROBE_TOOL)["message"]
    except ModelError as error:
        return f"FAILED  {str(error)[:110]}"
    seconds = time.monotonic() - started
    called = bool(message.get("tool_calls"))
    return f"{'OK, called the tool' if called else 'OK, but answered without the tool'}  ({seconds:.1f}s)"


def main() -> int:
    parser = argparse.ArgumentParser(description="List free OpenRouter models with tool calling.")
    parser.add_argument("--check", action="store_true", help="Probe each model with one request.")
    args = parser.parse_args()
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")

    free = free_tool_models()
    api_key = ""
    if args.check:
        load_env_file()
        api_key = os.environ.get("OPENROUTER_API_KEY", "")
        if not api_key:
            print("No API key. Set OPENROUTER_API_KEY in agent/.env.local.", file=sys.stderr)
            return 1

    for model in free:
        line = f"{model['id']:<52} context {model.get('context_length', '?'):<8}"
        if args.check:
            line += f" {probe(model['id'], api_key)}"
        print(line, flush=True)
    print(f"\n{len(free)} free models with tool calling. Set AGENT_MODEL in .env.local to use one.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
