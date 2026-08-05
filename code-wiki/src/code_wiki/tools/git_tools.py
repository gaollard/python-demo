from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

from code_wiki.safety import PathEscapeError, resolve_under_root, truncate
from code_wiki.tools.base import ToolSpec

PATCH_MAX = 20_000
BLAME_MAX_LINES = 200


def _git_env() -> dict[str, str]:
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["GIT_OPTIONAL_LOCKS"] = "0"
    return env


def _find_git_root(workspace: Path) -> Path | str:
    if not shutil.which("git"):
        return "ERROR: git executable not found on PATH"
    workspace = workspace.resolve()
    try:
        proc = subprocess.run(
            ["git", "-C", str(workspace), "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            timeout=10,
            env=_git_env(),
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as e:
        return f"ERROR: {e}"
    if proc.returncode != 0:
        return "ERROR: not a git repository"
    git_root = Path(proc.stdout.strip()).resolve()
    try:
        git_root.relative_to(workspace)
    except ValueError:
        # workspace is inside repo but git root is parent — allow if workspace is under git_root
        try:
            workspace.relative_to(git_root)
        except ValueError:
            return "ERROR: git root outside workspace sandbox"
    return git_root


def _run_git(git_root: Path, args: list[str], timeout: float = 30) -> str:
    cmd = [
        "git",
        "-C",
        str(git_root),
        "-c",
        "safe.directory=*",
        *args,
    ]
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=_git_env(),
            check=False,
        )
    except subprocess.TimeoutExpired:
        return "ERROR: git timed out"
    except OSError as e:
        return f"ERROR: {e}"
    out = (proc.stdout or "") + (("\n" + proc.stderr) if proc.stderr else "")
    if proc.returncode != 0 and not proc.stdout:
        return f"ERROR: git {' '.join(args[:2])} failed: {(proc.stderr or '').strip()}"
    return truncate(out.strip(), PATCH_MAX)


def _safe_rel_path(workspace: Path, path: str) -> str | Path:
    try:
        resolved = resolve_under_root(workspace, path)
    except PathEscapeError as e:
        return f"ERROR: {e}"
    return resolved


def git_status(workspace: Path, args: dict[str, Any]) -> str:
    root = _find_git_root(workspace)
    if isinstance(root, str):
        return root
    porcelain = bool(args.get("porcelain", False))
    if porcelain:
        return _run_git(root, ["status", "--porcelain=v1", "-b"])
    return _run_git(root, ["status", "-sb"])


def git_log(workspace: Path, args: dict[str, Any], *, max_default: int = 10, max_cap: int = 30) -> str:
    root = _find_git_root(workspace)
    if isinstance(root, str):
        return root
    n = int(args.get("max_count") or max_default)
    n = max(1, min(n, max_cap))
    cmd = [
        "log",
        f"-n{n}",
        "--format=%h%x09%an%x09%ad%x09%s",
        "--date=short",
    ]
    if args.get("since"):
        cmd.append(f"--since={args['since']}")
    if args.get("until"):
        cmd.append(f"--until={args['until']}")
    if args.get("grep"):
        cmd.append(f"--grep={args['grep']}")
        cmd.append("--regexp-ignore-case")
    path = args.get("path")
    if path:
        resolved = _safe_rel_path(workspace, path)
        if isinstance(resolved, str):
            return resolved
        rel = resolved.relative_to(root).as_posix() if resolved.is_relative_to(root) else path
        cmd.extend(["--", rel])
    return _run_git(root, cmd)


def git_blame(workspace: Path, args: dict[str, Any]) -> str:
    root = _find_git_root(workspace)
    if isinstance(root, str):
        return root
    path = args.get("path")
    if not path:
        return "ERROR: path is required"
    resolved = _safe_rel_path(workspace, path)
    if isinstance(resolved, str):
        return resolved
    if not resolved.is_file():
        return f"ERROR: file not found: {path}"
    rel = resolved.relative_to(root).as_posix() if resolved.is_relative_to(root) else path

    start = args.get("start_line")
    end = args.get("end_line")
    cmd = ["blame", "--line-porcelain"]
    if start is not None or end is not None:
        s = int(start or 1)
        e = int(end or s)
        if e - s + 1 > BLAME_MAX_LINES:
            e = s + BLAME_MAX_LINES - 1
        cmd.append(f"-L{s},{e}")
    cmd.extend(["--", rel])

    raw = _run_git(root, cmd)
    if raw.startswith("ERROR:"):
        # fallback simpler blame
        cmd2 = ["blame", "-e"]
        if start is not None or end is not None:
            s = int(start or 1)
            e = int(end or s)
            cmd2.append(f"-L{s},{e}")
        cmd2.extend(["--", rel])
        return _run_git(root, cmd2)

    # Compact porcelain → readable lines
    return truncate(_format_blame_porcelain(raw), PATCH_MAX)


def _format_blame_porcelain(raw: str) -> str:
    lines_out: list[str] = []
    hash_ = author = date = ""
    content_line = None
    line_no = 0
    for line in raw.splitlines():
        if len(line) >= 40 and line[0:40].isalnum() and " " in line:
            parts = line.split()
            hash_ = parts[0][:8]
            if len(parts) >= 3:
                try:
                    line_no = int(parts[2])
                except ValueError:
                    pass
        elif line.startswith("author "):
            author = line[7:]
        elif line.startswith("author-time "):
            # keep unix; show as-is short
            date = line[12:]
        elif line.startswith("\t"):
            content_line = line[1:]
            lines_out.append(f"{line_no}| {hash_} | {author} | {content_line}")
            if len(lines_out) >= BLAME_MAX_LINES:
                lines_out.append("[truncated]")
                break
    return "\n".join(lines_out) if lines_out else raw


def git_show(workspace: Path, args: dict[str, Any]) -> str:
    root = _find_git_root(workspace)
    if isinstance(root, str):
        return root
    rev = args.get("revision")
    if not rev:
        return "ERROR: revision is required"
    # prevent option injection
    if rev.startswith("-"):
        return "ERROR: invalid revision"
    path = args.get("path")
    cmd = ["show", "--stat", "--format=fuller", rev]
    if path:
        resolved = _safe_rel_path(workspace, path)
        if isinstance(resolved, str):
            return resolved
        rel = resolved.relative_to(root).as_posix() if resolved.is_relative_to(root) else path
        cmd.extend(["--", rel])
    return _run_git(root, cmd)


def git_diff(workspace: Path, args: dict[str, Any]) -> str:
    root = _find_git_root(workspace)
    if isinstance(root, str):
        return root
    base = args.get("base")
    head = args.get("head") or "HEAD"
    for rev in (base, head):
        if rev and str(rev).startswith("-"):
            return "ERROR: invalid revision"
    cmd = ["diff"]
    if base:
        cmd.append(f"{base}...{head}")
    else:
        cmd.append(head)
        # working tree vs head if only head? actually git diff HEAD shows unstaged+staged vs HEAD
        # For clean API: no base → git diff (working tree)
        if head == "HEAD" and not base:
            cmd = ["diff"]
    path = args.get("path")
    if path:
        resolved = _safe_rel_path(workspace, path)
        if isinstance(resolved, str):
            return resolved
        rel = resolved.relative_to(root).as_posix() if resolved.is_relative_to(root) else path
        cmd.extend(["--", rel])
    return _run_git(root, cmd)


def git_tools(*, log_max: int = 30) -> list[ToolSpec]:
    def log_handler(workspace: Path, args: dict[str, Any]) -> str:
        return git_log(workspace, args, max_default=min(10, log_max), max_cap=log_max)

    return [
        ToolSpec(
            name="git_status",
            description="Show current branch and short git status (read-only).",
            parameters={
                "type": "object",
                "properties": {
                    "porcelain": {"type": "boolean"},
                },
            },
            handler=git_status,
        ),
        ToolSpec(
            name="git_log",
            description="Show recent commits (read-only). Optional path filter.",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "max_count": {"type": "integer"},
                    "since": {"type": "string"},
                    "until": {"type": "string"},
                    "grep": {"type": "string", "description": "Filter by commit message"},
                },
            },
            handler=log_handler,
        ),
        ToolSpec(
            name="git_blame",
            description="Blame lines of a file (read-only). Who last changed each line.",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "start_line": {"type": "integer"},
                    "end_line": {"type": "integer"},
                },
                "required": ["path"],
            },
            handler=git_blame,
        ),
        ToolSpec(
            name="git_show",
            description="Show a commit metadata and patch (read-only).",
            parameters={
                "type": "object",
                "properties": {
                    "revision": {"type": "string"},
                    "path": {"type": "string"},
                },
                "required": ["revision"],
            },
            handler=git_show,
        ),
        ToolSpec(
            name="git_diff",
            description="Show read-only diff. Optional base...head and path.",
            parameters={
                "type": "object",
                "properties": {
                    "base": {"type": "string"},
                    "head": {"type": "string"},
                    "path": {"type": "string"},
                },
            },
            handler=git_diff,
        ),
    ]
