from __future__ import annotations

import json
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from code_wiki.config import Settings
from code_wiki.tools.base import ToolSpec
from code_wiki.tools.filesystem import filesystem_tools
from code_wiki.tools.git_tools import git_tools
from code_wiki.tools.grep import grep_tools
from code_wiki.tools.symbols import symbol_tools


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]


@dataclass
class ToolResult:
    text: str
    elapsed: float


class ToolRegistry:
    def __init__(self, specs: list[ToolSpec], *, max_workers: int = 8, timeout: float = 30):
        self._by_name = {s.name: s for s in specs}
        self.max_workers = max_workers
        self.timeout = timeout

    @classmethod
    def from_settings(cls, settings: Settings) -> ToolRegistry:
        specs: list[ToolSpec] = []
        specs.extend(filesystem_tools())
        specs.extend(grep_tools())
        if settings.symbol_backend not in {"off", "none", "false"}:
            specs.extend(symbol_tools())
        if settings.git_enabled:
            specs.extend(git_tools(log_max=settings.git_log_max))
        return cls(
            specs,
            max_workers=settings.tool_max_workers,
            timeout=settings.tool_timeout,
        )

    def openai_tools(self) -> list[dict[str, Any]]:
        return [s.openai_schema() for s in self._by_name.values()]

    def run_one(self, workspace: Path, call: ToolCall) -> str:
        return self.run_one_timed(workspace, call).text

    def run_one_timed(self, workspace: Path, call: ToolCall) -> ToolResult:
        t0 = time.perf_counter()
        spec = self._by_name.get(call.name)
        if spec is None:
            text = f"ERROR: unknown tool '{call.name}'"
        else:
            try:
                text = spec.handler(workspace, call.arguments)
            except Exception as exc:  # noqa: BLE001 — isolate tool failures
                text = f"ERROR: {call.name} raised {type(exc).__name__}: {exc}"
        return ToolResult(text=text, elapsed=time.perf_counter() - t0)

    def execute_many(self, workspace: Path, calls: list[ToolCall]) -> list[ToolResult]:
        if not calls:
            return []
        if len(calls) == 1:
            return [self.run_one_timed(workspace, calls[0])]

        workers = min(self.max_workers, len(calls))
        results: list[ToolResult | None] = [None] * len(calls)

        def _run(idx: int, call: ToolCall) -> tuple[int, ToolResult]:
            return idx, self.run_one_timed(workspace, call)

        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = [pool.submit(_run, i, c) for i, c in enumerate(calls)]
            for fut in futures:
                try:
                    idx, result = fut.result(timeout=self.timeout)
                    results[idx] = result
                except FuturesTimeout:
                    for i, r in enumerate(results):
                        if r is None:
                            results[i] = ToolResult(
                                text="ERROR: tool timed out", elapsed=self.timeout
                            )
                except Exception as exc:  # noqa: BLE001
                    for i, r in enumerate(results):
                        if r is None:
                            results[i] = ToolResult(text=f"ERROR: {exc}", elapsed=0.0)
        return [
            r if r is not None else ToolResult(text="ERROR: tool failed", elapsed=0.0)
            for r in results
        ]


def parse_tool_arguments(raw: str | dict[str, Any] | None) -> dict[str, Any]:
    if raw is None:
        return {}
    if isinstance(raw, dict):
        return raw
    try:
        data = json.loads(raw)
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        return {}
