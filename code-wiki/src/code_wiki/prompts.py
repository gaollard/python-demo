from __future__ import annotations

from pathlib import Path


def system_prompt(workspace: Path) -> str:
    return f"""You are Code Wiki, a read-only code analysis assistant.

Workspace root: {workspace.resolve()}

## Strategy
1. Start with list_dir / glob to understand structure when needed.
2. Prefer find_definition / find_references when you know a symbol name; use grep for concepts or as fallback.
3. For large/unknown files, read_file with mode=outline first, then mode=symbol or mode=body with line ranges.
4. For authorship / when something was introduced / recent changes, use read-only git tools (git_blame, git_log, git_show, git_diff, git_status). Never invent commit hashes.
5. If you need multiple independent searches or file reads, issue multiple tool_calls in the same turn.
6. Answer with a clear conclusion, key steps/modules, and citations as path:line (and commit when from git).
7. Only cite paths you actually observed via tools. If unsure, say so.

## Constraints
- Read-only: do not attempt to modify the repository.
- Do not ask the user to run commands; use tools.
- Match the user's language in the final answer.
"""


def user_prompt(workspace: Path, question: str) -> str:
    return f"工作空间: {workspace.resolve()}\n问题: {question}"


def bootstrap_context(workspace: Path, max_entries: int = 40) -> str:
    """Cheap first-turn context: top-level listing + README snippet."""
    root = workspace.resolve()
    lines = ["## Workspace snapshot (auto)", f"root: {root}", "top-level:"]
    try:
        children = sorted(root.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
    except OSError as e:
        return f"## Workspace snapshot\nERROR: {e}"

    count = 0
    for child in children:
        if child.name in {".git", ".venv", "venv", "node_modules", "__pycache__"}:
            continue
        if child.name.startswith(".") and child.name not in {".github"}:
            continue
        mark = "/" if child.is_dir() else ""
        lines.append(f"- {child.name}{mark}")
        count += 1
        if count >= max_entries:
            lines.append("- …")
            break

    for name in ("README.md", "readme.md", "README.rst", "pyproject.toml", "package.json"):
        path = root / name
        if path.is_file():
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            snippet = "\n".join(text.splitlines()[:40])
            lines.append(f"\n### {name} (first lines)\n```\n{snippet}\n```")
            break
    return "\n".join(lines)
