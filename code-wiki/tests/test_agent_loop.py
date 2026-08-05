from pathlib import Path

from code_wiki.agent import run_agent
from code_wiki.config import Settings
from code_wiki.llm import LLMResponse, MockLLMClient
from code_wiki.tools import ToolCall


def _settings(**overrides) -> Settings:
    base = dict(
        api_key="test",
        base_url=None,
        model="mock",
        max_steps=5,
        tool_max_workers=4,
        tool_timeout=10,
        git_enabled=False,
        git_log_max=10,
        symbol_backend="heuristic",
    )
    base.update(overrides)
    return Settings(**base)


def test_agent_uses_tools_then_answers(tmp_path: Path):
    (tmp_path / "hello.py").write_text("def greet():\n    return 'hi'\n")

    script = [
        LLMResponse(
            content=None,
            tool_calls=[
                ToolCall(
                    id="1",
                    name="grep",
                    arguments={"pattern": "greet"},
                )
            ],
        ),
        LLMResponse(
            content="`greet` is defined in hello.py:1.",
            tool_calls=[],
        ),
    ]
    logs: list[str] = []
    answer = run_agent(
        tmp_path,
        "Where is greet?",
        settings=_settings(),
        llm=MockLLMClient(script),
        verbose=False,
        log=logs.append,
    )
    assert "hello.py" in answer
    joined = "\n".join(logs)
    assert "tool_calls (serial):" in joined
    assert "→ grep(" in joined
    assert "← grep (" in joined


def test_agent_prints_assistant_content_with_tool_calls(tmp_path: Path):
    (tmp_path / "a.py").write_text("x = 1\n")
    script = [
        LLMResponse(
            content="Looking up the symbol…",
            tool_calls=[
                ToolCall(id="1", name="list_dir", arguments={"path": "."}),
            ],
        ),
        LLMResponse(content="done", tool_calls=[]),
    ]
    logs: list[str] = []
    run_agent(
        tmp_path,
        "list files",
        settings=_settings(),
        llm=MockLLMClient(script),
        log=logs.append,
    )
    assert any("assistant: Looking up the symbol…" in m for m in logs)
