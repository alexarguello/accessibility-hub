"""Reads site.config.json and .env.local, and wires the pieces into an agent."""
from __future__ import annotations

import json
import os
from pathlib import Path

from .agent import Agent
from .model_client import DEFAULT_BASE_URL, ChatClient
from .prompt import build_system_prompt
from .site_index import SiteIndex, load_from_directory
from .tools import Tools

AGENT_DIR = Path(__file__).resolve().parent.parent


def load_env_file(path: Path = AGENT_DIR / ".env.local") -> None:
    """Load KEY=value lines into the environment. Existing variables win."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


def load_config(path: Path = AGENT_DIR / "site.config.json") -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_site_index(config: dict) -> SiteIndex:
    directory = (AGENT_DIR / config["indexDir"]).resolve()
    if not (directory / "site-index.json").exists():
        raise FileNotFoundError(
            f"No site index at {directory}. Run the site's index generator first."
        )
    return load_from_directory(directory)


def build_agent(config: dict, site_index: SiteIndex, model: str | None = None, on_event=None) -> Agent:
    load_env_file()
    client = ChatClient(
        api_key=os.environ.get("OPENROUTER_API_KEY", ""),
        model=model or os.environ.get("AGENT_MODEL") or config.get("defaultModel", ""),
        base_url=os.environ.get("AGENT_BASE_URL") or DEFAULT_BASE_URL,
    )
    return Agent(client, Tools(site_index), build_system_prompt(config, site_index), on_event=on_event)
