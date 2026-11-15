"""Talks to any OpenAI-compatible chat completions endpoint (OpenRouter by default)."""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from typing import Callable

DEFAULT_BASE_URL = "https://openrouter.ai/api/v1"


class ModelError(Exception):
    def __init__(self, message: str, status: int | None = None, retryable: bool = False,
                 retry_after: float | None = None):
        super().__init__(message)
        self.status = status
        self.retryable = retryable
        self.retry_after = retry_after


def _http_post(url: str, headers: dict, body: bytes, timeout: float) -> tuple[int, dict, str]:
    """Send one POST. Returns (status, headers, text) for any HTTP status."""
    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status, dict(response.headers), response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        return error.code, dict(error.headers), error.read().decode("utf-8", errors="replace")


class ChatClient:
    def __init__(self, api_key: str, model: str, base_url: str = DEFAULT_BASE_URL,
                 temperature: float = 0.2, max_tokens: int = 900, max_retries: int = 3,
                 timeout: float = 90, transport: Callable = _http_post,
                 sleep: Callable[[float], None] = time.sleep):
        if not api_key:
            raise ModelError("No API key. Set OPENROUTER_API_KEY in agent/.env.local.")
        if not model:
            raise ModelError("No model id configured.")
        self.model = model
        self._endpoint = base_url.rstrip("/") + "/chat/completions"
        self._headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        self._temperature = temperature
        self._max_tokens = max_tokens
        self._max_retries = max_retries
        self._timeout = timeout
        self._transport = transport
        self._sleep = sleep

    def complete(self, messages: list[dict], tools: list[dict] | None = None) -> dict:
        """One model turn. Returns {"message": ..., "usage": ...}.

        Pass tools to let the model call them; pass none to force a text answer.
        """
        body = {
            "model": self.model,
            "messages": messages,
            "temperature": self._temperature,
            "max_tokens": self._max_tokens,
        }
        if tools:
            body["tools"] = tools
            body["tool_choice"] = "auto"
        payload = json.dumps(body).encode("utf-8")

        attempt = 0
        while True:
            try:
                return self._request_once(payload)
            except ModelError as error:
                if not error.retryable or attempt >= self._max_retries:
                    raise
                # Free models are rate limited; wait and try again.
                self._sleep(min(error.retry_after or 2 ** attempt * 2, 30))
                attempt += 1

    def _request_once(self, payload: bytes) -> dict:
        try:
            status, headers, text = self._transport(self._endpoint, self._headers, payload, self._timeout)
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            raise ModelError(f"Network error: {error}", retryable=True) from error

        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            data = None

        # Some gateways report a provider failure inside a 200 response.
        api_error = data.get("error") if isinstance(data, dict) else None
        if status >= 400 or api_error:
            code = status
            if status < 400:
                code = api_error.get("code") if isinstance(api_error.get("code"), int) else 502
            detail = api_error.get("message") if isinstance(api_error, dict) else text[:300]
            # OpenRouter puts the upstream provider's own message in error.metadata.
            metadata = api_error.get("metadata") if isinstance(api_error, dict) else None
            if isinstance(metadata, dict):
                extra = metadata.get("raw") or metadata.get("provider_name")
                if extra:
                    detail = f"{detail} | {str(extra)[:300]}"
            retry_after = None
            for key, value in headers.items():
                if key.lower() == "retry-after" and str(value).replace(".", "", 1).isdigit():
                    retry_after = float(value)
            raise ModelError(f"Model request failed ({code}): {detail}", status=code,
                             retryable=code == 429 or code >= 500, retry_after=retry_after)

        choices = data.get("choices") if isinstance(data, dict) else None
        if not choices or "message" not in choices[0]:
            raise ModelError("Model response had no message.", retryable=True)
        return {"message": choices[0]["message"], "usage": data.get("usage") or {}}
