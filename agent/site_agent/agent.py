"""The agent loop: ask the model, run the tools it asks for, repeat until it answers in text."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class AgentResult:
    answer: str
    tool_calls: list[dict] = field(default_factory=list)
    usage: dict = field(default_factory=dict)
    steps: int = 0
    # Earlier user and assistant turns plus this one; pass it back in for a follow-up question.
    history: list[dict] = field(default_factory=list)


class Agent:
    def __init__(self, client, tools, system_prompt: str, max_steps: int = 6,
                 on_event: Callable[[dict], None] | None = None):
        """
        client:  has complete(messages, tools) -> {"message", "usage"}  (see model_client.ChatClient)
        tools:   has .definitions and .execute(name, arguments)         (see tools.Tools)
        max_steps: model turns allowed before the agent must answer
        on_event: called once per tool call, for logging
        """
        self._client = client
        self._tools = tools
        self._system_prompt = system_prompt
        self._max_steps = max_steps
        self._on_event = on_event or (lambda event: None)

    def run(self, user_message: str, history: list[dict] | None = None) -> AgentResult:
        history = list(history or [])
        # The model has no memory between calls. Everything it knows is in this list,
        # and the whole list is sent again on every turn.
        messages = [
            {"role": "system", "content": self._system_prompt},
            *history,
            {"role": "user", "content": user_message},
        ]
        tool_calls: list[dict] = []
        usage = {"prompt_tokens": 0, "completion_tokens": 0}

        for step in range(1, self._max_steps + 1):
            # On the last allowed turn the model gets no tools, so it has to answer.
            last_turn = step == self._max_steps
            result = self._client.complete(messages, None if last_turn else self._tools.definitions)
            for key in usage:
                usage[key] += (result.get("usage") or {}).get(key, 0) or 0
            message = result["message"]
            calls = [] if last_turn else (message.get("tool_calls") or [])

            if not calls:
                answer = (message.get("content") or "").strip()
                history += [
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": answer},
                ]
                return AgentResult(answer, tool_calls, usage, step, history)

            # The model asked for tools. Record its request, run each tool, and add each
            # result as a "tool" message tied to the request by id. Then loop.
            messages.append({"role": "assistant", "content": message.get("content"), "tool_calls": calls})
            for call in calls:
                function = call.get("function") or {}
                name = function.get("name", "")
                output = self._tools.execute(name, function.get("arguments"))
                record = {
                    "name": name,
                    "arguments": function.get("arguments"),
                    "ok": "error" not in output,
                    "url": output.get("url"),
                    "error": output.get("error"),
                }
                tool_calls.append(record)
                self._on_event({"type": "tool", **record})
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.get("id"),
                    "content": json.dumps(output, ensure_ascii=False),
                })

        raise RuntimeError("Agent loop ended without an answer.")  # the last turn always returns
