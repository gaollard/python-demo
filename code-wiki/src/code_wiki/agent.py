from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Callable

from code_wiki.config import Settings
from code_wiki.llm import LLMClient, LLMResponse, OpenAICompatibleClient
from code_wiki.prompts import bootstrap_context, system_prompt, user_prompt
from code_wiki.tools import ToolRegistry


LogFn = Callable[[str], None]


def run_agent(
    workspace: Path,
    question: str,
    *,
    settings: Settings | None = None,
    llm: LLMClient | None = None,
    verbose: bool = False,
    max_steps: int | None = None,
    log: LogFn | None = None,
) -> str:
    """Run the analysis agent and return the final answer text."""
    settings = settings or Settings.from_env()
    workspace = workspace.resolve()
    if not workspace.is_dir():
        raise FileNotFoundError(f"workspace is not a directory: {workspace}")

    steps = max_steps if max_steps is not None else settings.max_steps
    registry = ToolRegistry.from_settings(settings)
    client = llm or OpenAICompatibleClient(
        api_key=settings.api_key,
        model=settings.model,
        base_url=settings.base_url,
    )
    if not settings.api_key and llm is None:
        raise RuntimeError(
            "Missing API key. Set CODE_WIKI_API_KEY or DEEPSEEK_API_KEY."
        )

    def _emit(msg: str) -> None:
        if log:
            log(msg)
        else:
            print(msg, flush=True)

    def _log(msg: str) -> None:
        if verbose:
            _emit(msg)

    messages: list[dict[str, Any]] = [
        {"role": "system", "content": system_prompt(workspace)},
        {
            "role": "user",
            "content": bootstrap_context(workspace) + "\n\n" + user_prompt(workspace, question),
        },
    ]
    tools = registry.openai_tools()
    seen_calls: dict[str, int] = {}

    for step in range(1, steps + 1):
        _log(f"\n── step {step}/{steps} ──")
        resp: LLMResponse = client.chat(messages, tools)

        if resp.raw_message:
            messages.append(resp.raw_message)
        elif resp.tool_calls:
            messages.append(
                {
                    "role": "assistant",
                    "content": resp.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.name,
                                "arguments": __import__("json").dumps(tc.arguments),
                            },
                        }
                        for tc in resp.tool_calls
                    ],
                }
            )
        else:
            messages.append({"role": "assistant", "content": resp.content or ""})

        if not resp.tool_calls:
            answer = (resp.content or "").strip()
            if not answer:
                return "(empty response from model)"
            return answer

        if resp.content and resp.content.strip():
            _emit(f"assistant: {resp.content.strip()}")

        # duplicate-call soft fuse
        for tc in resp.tool_calls:
            key = f"{tc.name}:{sorted(tc.arguments.items())}"
            seen_calls[key] = seen_calls.get(key, 0) + 1
            if seen_calls[key] >= 3:
                _emit(f"warn: repeated tool call {tc.name} x{seen_calls[key]}")

        parallel = len(resp.tool_calls) > 1
        mode = "parallel" if parallel else "serial"
        _emit(f"tool_calls ({mode}):")
        for tc in resp.tool_calls:
            _emit(f"  → {tc.name}({tc.arguments})")

        t0 = time.perf_counter()
        results = registry.execute_many(workspace, resp.tool_calls)
        elapsed = time.perf_counter() - t0
        _emit(f"tools finished in {elapsed:.2f}s")

        for tc, result in zip(resp.tool_calls, results):
            preview = result.text if len(result.text) <= 300 else result.text[:300] + "…"
            _emit(f"  ← {tc.name} ({result.elapsed:.2f}s): {preview}")
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result.text,
                }
            )

    # Force summary
    _log("\n── max steps reached; requesting summary ──")
    messages.append(
        {
            "role": "user",
            "content": (
                "You have reached the maximum number of tool steps. "
                "Based on the information gathered so far, provide the best possible answer "
                "with citations. Do not call any more tools."
            ),
        }
    )
    final = client.chat(messages, tools=[])
    return (final.content or "Reached max steps without a final answer.").strip()
