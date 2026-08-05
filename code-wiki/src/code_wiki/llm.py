from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Protocol

from code_wiki.tools import ToolCall, parse_tool_arguments


@dataclass
class LLMResponse:
    content: str | None
    tool_calls: list[ToolCall] = field(default_factory=list)
    raw_message: dict[str, Any] | None = None


class LLMClient(Protocol):
    def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
    ) -> LLMResponse: ...


class OpenAICompatibleClient:
    def __init__(self, *, api_key: str, model: str, base_url: str | None = None):
        from openai import OpenAI

        kwargs: dict[str, Any] = {"api_key": api_key}
        if base_url:
            kwargs["base_url"] = base_url
        self._client = OpenAI(**kwargs)
        self.model = model

    def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
    ) -> LLMResponse:
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
        }
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"

        resp = self._client.chat.completions.create(**kwargs)
        msg = resp.choices[0].message
        tool_calls: list[ToolCall] = []
        if msg.tool_calls:
            for tc in msg.tool_calls:
                tool_calls.append(
                    ToolCall(
                        id=tc.id,
                        name=tc.function.name,
                        arguments=parse_tool_arguments(tc.function.arguments),
                    )
                )
        raw = {
            "role": "assistant",
            "content": msg.content,
        }
        if msg.tool_calls:
            raw["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                        if isinstance(tc.function.arguments, str)
                        else json.dumps(tc.function.arguments),
                    },
                }
                for tc in msg.tool_calls
            ]
        return LLMResponse(content=msg.content, tool_calls=tool_calls, raw_message=raw)


class MockLLMClient:
    """Deterministic client for tests: scripted responses."""

    def __init__(self, script: list[LLMResponse]):
        self._script = list(script)
        self.calls = 0

    def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
    ) -> LLMResponse:
        if not self._script:
            return LLMResponse(content="(mock: no more scripted responses)")
        self.calls += 1
        return self._script.pop(0)
