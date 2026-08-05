from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from code_wiki.safety import (
    DEFAULT_IGNORE_DIRS,
    PathEscapeError,
    resolve_under_root,
    should_skip_dir,
    truncate,
)
from code_wiki.tools.base import ToolSpec

GREP_MAX = 50
LINE_MAX = 200


def _rg_available() -> bool:
    return shutil.which("rg") is not None


def _grep_rg(
    workspace: Path,
    pattern: str,
    *,
    path: str | None,
    glob: str | None,
    case_insensitive: bool,
) -> str:
    root = workspace.resolve()
    search_path = root
    if path:
        try:
            search_path = resolve_under_root(workspace, path)
        except PathEscapeError as e:
            return f"ERROR: {e}"

    cmd = [
        "rg",
        "--line-number",
        "--no-heading",
        "--color",
        "never",
        "--max-count",
        str(GREP_MAX),
    ]
    for d in sorted(DEFAULT_IGNORE_DIRS):
        cmd.extend(["--glob", f"!{d}/**"])
    if case_insensitive:
        cmd.append("-i")
    if glob:
        cmd.extend(["--glob", glob])
    cmd.append("--")
    cmd.append(pattern)
    cmd.append(str(search_path))

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return "ERROR: rg timed out"
    except OSError as e:
        return f"ERROR: {e}"

    if proc.returncode not in (0, 1):
        err = (proc.stderr or "").strip()
        return f"ERROR: rg failed: {err or proc.returncode}"

    lines = []
    for line in (proc.stdout or "").splitlines():
        # make paths relative
        if line.startswith(str(root)):
            line = line[len(str(root)) :].lstrip("/\\")
        if len(line) > LINE_MAX:
            line = line[:LINE_MAX] + "…"
        lines.append(line)
        if len(lines) >= GREP_MAX:
            break

    if not lines:
        return f"No matches for: {pattern}"
    out = "\n".join(lines)
    if len((proc.stdout or "").splitlines()) > GREP_MAX:
        out += "\n[truncated]"
    return out


def _grep_python(
    workspace: Path,
    pattern: str,
    *,
    path: str | None,
    glob: str | None,
    case_insensitive: bool,
) -> str:
    flags = re.IGNORECASE if case_insensitive else 0
    try:
        regex = re.compile(pattern, flags)
    except re.error as e:
        return f"ERROR: invalid regex: {e}"

    root = workspace.resolve()
    start = root
    if path:
        try:
            start = resolve_under_root(workspace, path)
        except PathEscapeError as e:
            return f"ERROR: {e}"

    matches: list[str] = []
    paths: list[Path]
    if start.is_file():
        paths = [start]
    else:
        if glob:
            paths = [p for p in start.glob(glob) if p.is_file()]
        else:
            paths = [p for p in start.rglob("*") if p.is_file()]

    for fp in paths:
        if any(should_skip_dir(Path(part)) for part in fp.parts):
            continue
        if any(part in DEFAULT_IGNORE_DIRS for part in fp.parts):
            continue
        try:
            if fp.stat().st_size > 1_000_000:
                continue
            text = fp.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = fp.relative_to(root).as_posix()
        for i, line in enumerate(text.splitlines(), start=1):
            if regex.search(line):
                snippet = line.rstrip()
                if len(snippet) > LINE_MAX:
                    snippet = snippet[:LINE_MAX] + "…"
                matches.append(f"{rel}:{i}:{snippet}")
                if len(matches) >= GREP_MAX:
                    return "\n".join(matches) + "\n[truncated]"
    return "\n".join(matches) if matches else f"No matches for: {pattern}"


def grep_code(workspace: Path, args: dict[str, Any]) -> str:
    pattern = args.get("pattern")
    if not pattern:
        return "ERROR: pattern is required"
    path = args.get("path")
    glob = args.get("glob")
    case_insensitive = bool(args.get("case_insensitive", False))

    if _rg_available():
        return truncate(
            _grep_rg(
                workspace,
                pattern,
                path=path,
                glob=glob,
                case_insensitive=case_insensitive,
            )
        )
    return truncate(
        _grep_python(
            workspace,
            pattern,
            path=path,
            glob=glob,
            case_insensitive=case_insensitive,
        )
    )


def grep_tools() -> list[ToolSpec]:
    return [
        ToolSpec(
            name="grep",
            description=(
                "Search file contents with regex. Prefer when symbol tools are unavailable "
                "or the query is a natural-language concept keyword."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "pattern": {"type": "string"},
                    "path": {"type": "string", "description": "Subpath to search under"},
                    "glob": {"type": "string", "description": "File glob filter, e.g. '*.py'"},
                    "case_insensitive": {"type": "boolean"},
                },
                "required": ["pattern"],
            },
            handler=grep_code,
        )
    ]
