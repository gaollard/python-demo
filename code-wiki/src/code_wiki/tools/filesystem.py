from __future__ import annotations

from pathlib import Path
from typing import Any

from code_wiki.outline import format_outline, format_symbol_body
from code_wiki.safety import (
    PathEscapeError,
    is_probably_text_file,
    resolve_under_root,
    should_skip_dir,
    truncate,
    truncate_lines,
)
from code_wiki.tools.base import ToolSpec

LIST_DIR_MAX = 200
GLOB_MAX = 100
BODY_MAX_LINES = 200
BODY_MAX_CHARS = 20_000


def _rel(workspace: Path, path: Path) -> str:
    return path.relative_to(workspace.resolve()).as_posix()


def list_dir(workspace: Path, args: dict[str, Any]) -> str:
    rel = args.get("path") or "."
    try:
        target = resolve_under_root(workspace, rel)
    except PathEscapeError as e:
        return f"ERROR: {e}"
    if not target.exists():
        return f"ERROR: path not found: {rel}"
    if not target.is_dir():
        return f"ERROR: not a directory: {rel}"

    entries: list[str] = []
    try:
        children = sorted(target.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
    except OSError as e:
        return f"ERROR: {e}"

    for child in children:
        if should_skip_dir(child) and child.is_dir():
            continue
        if child.name.startswith(".") and child.name not in {".github", ".env.example"}:
            # skip most dotfiles/dirs except common useful ones
            if child.is_dir() and child.name not in {".github"}:
                continue
        suffix = "/" if child.is_dir() else ""
        entries.append(child.name + suffix)
        if len(entries) >= LIST_DIR_MAX:
            entries.append("[truncated]")
            break
    return f"{_rel(workspace, target)}/\n" + "\n".join(entries) if entries else "(empty)"


def glob_files(workspace: Path, args: dict[str, Any]) -> str:
    pattern = args.get("pattern")
    if not pattern:
        return "ERROR: pattern is required"
    root = workspace.resolve()
    matches: list[str] = []
    for path in root.glob(pattern):
        try:
            path.resolve().relative_to(root)
        except ValueError:
            continue
        if any(part in {".git", "node_modules", ".venv", "venv", "__pycache__"} for part in path.parts):
            continue
        if path.is_file():
            matches.append(path.relative_to(root).as_posix())
        if len(matches) >= GLOB_MAX:
            matches.append("[truncated]")
            break
    if not matches:
        return f"No matches for pattern: {pattern}"
    return "\n".join(matches)


def _read_lines(path: Path) -> list[str] | str:
    if not is_probably_text_file(path):
        return f"ERROR: refusing to read binary/non-text file: {path.name}"
    try:
        # size guard
        if path.stat().st_size > 2_000_000:
            return "ERROR: file too large (>2MB)"
        return path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as e:
        return f"ERROR: {e}"


def read_file(workspace: Path, args: dict[str, Any]) -> str:
    rel = args.get("path")
    if not rel:
        return "ERROR: path is required"
    mode = (args.get("mode") or "outline").lower()
    try:
        target = resolve_under_root(workspace, rel)
    except PathEscapeError as e:
        return f"ERROR: {e}"
    if not target.exists() or not target.is_file():
        return f"ERROR: file not found: {rel}"

    lines_or_err = _read_lines(target)
    if isinstance(lines_or_err, str):
        return lines_or_err
    lines = lines_or_err
    rel_posix = _rel(workspace, target)

    if mode == "outline":
        return format_outline(rel_posix, lines)

    if mode == "symbol":
        symbol = args.get("symbol")
        if not symbol:
            return "ERROR: symbol is required when mode=symbol"
        body = format_symbol_body(rel_posix, lines, symbol)
        return truncate(body, BODY_MAX_CHARS)

    if mode != "body":
        return f"ERROR: unknown mode '{mode}' (use outline|body|symbol)"

    start = args.get("start_line")
    end = args.get("end_line")
    start_i = int(start) if start is not None else 1
    end_i = int(end) if end is not None else len(lines)
    start_i = max(1, start_i)
    end_i = min(len(lines), end_i)
    if start_i > end_i:
        return "ERROR: start_line > end_line"

    chunk = lines[start_i - 1 : end_i]
    if len(chunk) > BODY_MAX_LINES:
        chunk = truncate_lines(chunk, BODY_MAX_LINES)
    numbered = []
    for i, line in enumerate(chunk):
        if line == "[truncated]":
            numbered.append(line)
        else:
            numbered.append(f"{start_i + i}|{line.rstrip()}")
    text = f"# {rel_posix}  L{start_i}-{min(end_i, start_i + len(chunk) - 1)}\n" + "\n".join(
        numbered
    )
    return truncate(text, BODY_MAX_CHARS)


def filesystem_tools() -> list[ToolSpec]:
    return [
        ToolSpec(
            name="list_dir",
            description="List files and subdirectories under a path (relative to workspace).",
            parameters={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Directory relative to workspace. Default '.'",
                    }
                },
            },
            handler=list_dir,
        ),
        ToolSpec(
            name="glob",
            description="Find files by glob pattern (e.g. '**/*auth*.py').",
            parameters={
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "Glob pattern"},
                },
                "required": ["pattern"],
            },
            handler=glob_files,
        ),
        ToolSpec(
            name="read_file",
            description=(
                "Read a file. Prefer mode=outline for large/unknown files; "
                "then mode=symbol or mode=body with line range for details."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "mode": {
                        "type": "string",
                        "enum": ["outline", "body", "symbol"],
                        "description": "outline (default) | body | symbol",
                    },
                    "symbol": {
                        "type": "string",
                        "description": "Required for mode=symbol, e.g. AuthService.login",
                    },
                    "start_line": {"type": "integer"},
                    "end_line": {"type": "integer"},
                },
                "required": ["path"],
            },
            handler=read_file,
        ),
    ]
